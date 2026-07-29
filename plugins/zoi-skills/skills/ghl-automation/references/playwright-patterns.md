# Playwright Patterns for GHL

The GHL workflow editor lives inside a cross-origin iframe (`iframe[name="workflow-builder"]`, served from `marketplace.gohighlevel.com` while the parent is `app.gohighlevel.com`). This breaks a lot of intuition — JS `evaluate` calls into the iframe fail with `SecurityError`, and DOM tree depth is unpredictable.

These patterns work. Use them instead of guessing.

## Iframe locator basics

When using `browser_click`, `browser_type`, `browser_snapshot` — passing the iframe ref as the parent target (e.g., `target: e154`) lets Playwright auto-resolve into the contentFrame. The MCP tooling tracks this for you via the `aria-ref=fNNeNN` namespacing (`f` = frame).

```
# Snapshot the iframe content
browser_snapshot(target: e154, depth: 5)

# Click inside the iframe — ref starts with f<frameNum>e<elNum>
browser_click(target: f27e2305, element: "trigger node")
```

## Cross-origin: when JS evaluate breaks

`browser_evaluate` runs in the parent context. Reading `iframe.contentDocument` returns null (cross-origin). You cannot:

- Walk the iframe DOM directly via JS
- Query elements inside via the parent's `document.querySelectorAll`
- Read `el.value` of inputs inside the iframe via parent

**You can** still pass a `target` ref to `browser_evaluate` with `(el) => {...}` — Playwright forwards the function into the frame for that one element. Use this for `.focus()`, `.select()`, `.click()`, `.value=''`, dispatching synthetic events.

```
# Force-clear and re-focus an input
browser_evaluate(
  function: "async (el) => { el.value=''; el.dispatchEvent(new Event('input',{bubbles:true})); el.focus(); el.click(); return 'ok'; }",
  target: f27e4725
)
```

## Snapshots: limits and tactics

`browser_snapshot` truncates by depth. Default depth (1-3) is too shallow for the workflow editor — most useful content lives 6-10 levels deep. But going too deep blows context.

**Strategy by goal:**

| Goal | Approach |
|---|---|
| Find a specific button you can see in the screenshot | `take_screenshot --fullPage true`, find rough region, then `snapshot --depth 5 --target <approximate ref>` to drill in |
| Inspect a config panel | `snapshot --depth 8 --target <panel-ref>` |
| List action picker categories | `snapshot --depth 5 --target <picker-ref>` is usually enough; expand individual category with `depth 8` |
| Find which "Guardar" button to click | Snapshot at depth 2 from root, then drill into the right `generic` |

**When refs go stale** (after click, navigation, panel close): re-snapshot from a stable ancestor (the iframe ref `e154` survives most navigations) and capture new refs. Don't try to reuse refs from before a state change.

## Popovers rendered outside parent

This is the single biggest gotcha. Many dropdowns (tag search, custom field selector, picklist value) use Vue's `<Teleport>` pattern — the listbox is appended as a sibling to the entire frame body, not inside the trigger element.

**Symptom**: you click a dropdown trigger, then snapshot the trigger ref, and see nothing — but the screenshot shows the popover is visibly open.

**Find it**: snapshot the iframe at depth 2-3. Look for a *new* top-level `generic` ref that didn't exist before the click (usually a higher ref number than everything else). Drill into that one.

```
# Before clicking a dropdown
browser_snapshot --depth 2
# → list of f27e* refs ends at f27e4720

# Click the dropdown
browser_click(target: f27e4632, ...)

# After: snapshot at same depth
browser_snapshot --depth 2
# → now there's a new f27e4727 sibling — that's the popover

browser_snapshot --depth 10 --target f27e4727
# → list items are inside this ref
```

## Click intercepts: "html intercepts pointer events"

GHL has invisible overlay layers (modal backdrops, loading overlays) that occasionally swallow clicks. Playwright will retry, but if the target is stale or hidden by an overlay you get:

```
TimeoutError: ...
- <html lang="en">…</html> intercepts pointer events
- element was detached from the DOM, retrying
```

**Fix**: re-snapshot first to get a fresh ref, then click. The element ref often changes after a DOM update even when the visible thing stays the same.

If that doesn't work: dismiss whatever modal is in the way. Common culprits:
- "Cambios no guardados" — click `Cancelar` to keep the panel
- Loading spinner from save — wait 1-2s with `browser_wait_for --time 2`
- Tooltip stuck on a button — click elsewhere first

## Workflow editor — common click sequences

### Open editor for an existing workflow
```
browser_navigate(url: ".../workflows?listTab=all&folder={folder_id}")
browser_wait_for(time: 2)
browser_snapshot(depth: 6, target: e154)  # find the workflow row link
browser_click(target: <row-link-ref>)
```

### Create new workflow in a folder
```
browser_navigate(url: ".../workflows?listTab=all&folder={folder_id}")
browser_click(target: <Crear flujo de trabajo button>)
# modal opens with 5 options — pick "Empezar desde cero"
browser_click(target: <Empezar desde cero option>)
# editor opens at /location/{loc}/workflow/{new_id}
```

### Rename workflow
```
browser_click(target: <"Nombre del flujo de trabajo" pencil button>)
# turns into an inline textbox
browser_evaluate(function: "(el) => {el.focus(); el.select();}", target: <textbox>)
browser_type(target: <textbox>, text: "[Produto] Gatilho → Ação")
# do NOT press Enter — it triggers an unsaved-changes modal
# instead click elsewhere on the title bar to commit
```

### Add a trigger
```
browser_click(target: <Añadir disparador button>)
browser_snapshot(depth: 8, target: <config-panel>)
# pick category → trigger type, e.g. Contacto → Etiqueta de contacto
browser_click(target: <"Etiqueta de contacto" button>)
# back in config panel: rename trigger, add filter, pick tag
browser_click(target: <Guardar trigger button>)
```

### Add an action between two nodes
```
# Find the small `+` button on the edge where you want to insert
browser_click(target: <Añadir acción ref>)
# action picker opens — drill into category → action type
browser_click(target: <action button>)
# config panel appears — fill fields → Guardar acción
```

## Save flow

```
# Per-step (commits step to canvas):
browser_click(target: <Guardar trigger / Guardar acción button>)

# Per-workflow (persists to GHL):
browser_click(target: <top-bar Guardar button>)
browser_wait_for(text: "Guardado!")
```

If the top-bar button label is "Guardado" (no exclamation), it's disabled — no changes to save. Don't try to click it.

## Verification

```
browser_take_screenshot(fullPage: true, filename: "wf-built.png")
# read the screenshot, eyeball the canvas tree
# match nodes against spec one by one
```

The accessibility snapshot tree can hide collapsed branches, missing edges, and misplaced steps. The screenshot is the only reliable visual ground truth.

## Naive UI dropdown — the canonical interaction sequence

Almost every config field in the workflow editor uses a Naive UI select. The trigger element is a `<div class="n-base-selection">` wrapper containing a label span. The popover (listbox) renders elsewhere via Vue Teleport.

The reliable pattern:

```
# 1. Click the wrapper, not the label
browser_click(target: <wrapper-generic-ref>, element: "select wrapper")

# 2. Wait for popover to render — Vue is async
browser_wait_for(time: 1)

# 3. Save snapshot to file (popover deeply nested, can be huge)
browser_snapshot(depth: 20, target: e158, filename: "deep-snap.yml")

# 4. Grep the file for the option label
# Bash: grep -B1 -A2 "Usuario asignado" /path/deep-snap.yml

# 5. Click the option by ref
browser_click(target: <option-ref>)

# 6. Wait again — dependent fields may render
browser_wait_for(time: 1)
```

**Why save snapshot to file**: deep snapshots can be 50KB+. Loading into context burns budget. `--filename` writes to disk, then you grep for what you need (~200 bytes).

## Identifying the right `+` (Añadir acción) button — coord-mapping trick

If/Else creates multiple `+` buttons (one per branch + sequential ones between nodes). Snapshot order is DOM order, NOT visual layout. The clean way to know which ref maps to which visual position:

```
# For each candidate ref, get its viewport coordinates:
browser_evaluate(
  function: "(el) => { const r = el.getBoundingClientRect(); return {x: r.x, y: r.y}; }",
  target: f45e10741
)
# → {x: 998, y: 814}  → this is the RIGHT branch (high x)

browser_evaluate(
  function: "(el) => { const r = el.getBoundingClientRect(); return {x: r.x, y: r.y}; }",
  target: f45e12992
)
# → {x: 759, y: 814}  → this is the LEFT branch (low x, same y)
```

Reading: same `y` = same vertical level (branch row). Low `x` = LEFT branch (typically `Sim`/Yes). High `x` = RIGHT branch (typically `None`). Different `y` = different position in sequential chain (top→bottom).

Cost: 3 `browser_evaluate` calls (~negligible). Saves a wrong-click → delete confirmation modal → action re-creation cycle (~15 calls + potential validation issues from stranded actions).

## Action picker — three navigation strategies

The action picker has 25+ categories. Three ways to find what you want, by speed:

1. **Acciones Recientes section** (top) — last 4-5 actions you used. After ~3 actions in a session, your most-needed actions show up here. Just click. Fastest.

2. **Search box** — type partial Spanish or English (`Asignar al`, `Update opp`, `Find opp`). One-shot if you know the exact label. Note: filters to "Acciones" + "Más aplicaciones" — your target is always under "Acciones".

3. **Browse by category** — `Contacto` / `Comunicación` / `Interno` / `Oportunidad` etc. Categories collapse/expand. Useful for discovery.

## Action-level vs workflow-level save (critical distinction)

| Save type | Button | What it does |
|---|---|---|
| Per-step | `Guardar trigger` / `Guardar acción` (panel footer) | Commits config to canvas in-memory. Closes panel on success. NOT persisted to GHL. |
| Per-workflow | `Guardar` (top-right) | Persists entire canvas to GHL. Shows `Guardado!` toast. Button label changes from `Guardar` to `Guardado` (disabled) when no pending changes. |

If you skip the top-right `Guardar`, a refresh wipes ALL step-level changes. Lost ~15 min of work this way once.

## Detecting "Save action failed silently"

After `Guardar acción`, the panel SHOULD close. If it stays open:

1. Look for red toast at panel top: "Please check the fields for valid inputs"
2. Look for inline red text below any required field: "Esto no puede estar vacío"
3. Snapshot the panel and grep for `"Esto no puede"` or `"valid input"`

Common offenders:
- `Notificación Interna` → `Página de redirección` is mandatory but easy to overlook (renders below the message editor)
- `Create opportunity` → `Stage` is mandatory; defaults to the LAST pipeline stage which is almost always wrong
- `Find Opportunity` → at least one matching criterion is required

## Refs invalidate aggressively after each click

GHL's Vue tree re-renders on virtually every state change. Refs from snapshot N-1 are usually invalid after any click in N. Always snapshot after click before using a ref.

Symptom of stale ref: `TimeoutError: ... element was detached from the DOM`.

Fix: re-snapshot. Don't try to click the same stale ref.

## Don't trust panel state after `Guardar acción` — trust the canvas

After saving an action, sometimes the panel re-opens showing what appears to be empty fields. Doesn't mean the save failed. Means GHL re-opened the panel in "edit mode" for the just-saved node, and the rerender raced ahead of state hydration.

To verify save: close the panel, take a `fullPage` screenshot, look for the action label as a card on the canvas (e.g., "Notificar owner — Novo lead BP"). If card is there, save worked. If not, save failed.

## Anti-patterns

- ❌ Trying to read `iframe.contentDocument.querySelector(...)` from `browser_evaluate` without a `target` — fails cross-origin
- ❌ Pressing Enter inside the workflow name editable — triggers "Cambios no guardados" modal
- ❌ Reusing refs across navigations or modal toggles — refs change
- ❌ Snapshotting at `depth: 30` everywhere — context burn
- ❌ Clicking the Publicar toggle to "test" — that publishes the workflow to production
