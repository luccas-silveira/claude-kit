# GHL Workflow Build — Anti-Patterns

These are mistakes we've made or almost made on this project. Each one cost time. The right alternative is given inline.

## 1. Using `status_cliente` (or any picklist) as duplicate-entry guard

**Wrong**:
```
If/Else  →  Status do Cliente == "Lead Quente"
  Yes  →  END  (assume already in pipeline)
  None →  proceed
```

**Why wrong**: `Status do Cliente` is a contact-level state, not a pipeline membership flag. Other workflows or manual edits can set it for unrelated reasons. False positives quietly drop legitimate leads.

**Right**: use the native `Find Opportunity` step. It checks actual pipeline + opportunity status. Two branches: `Opportunity Found` (END) / `Opportunity Not Found` (proceed).

## 2. Silently substituting picklist values

**Wrong**: Spec says `status_cliente = "Lead ativo"`. GHL picklist only has `Prospecto · Lead Quente · Cliente · Inativo`. Pick `Lead Quente` without telling anyone.

**Why wrong**: spec and reality diverge silently. Later workflows that filter on `Lead ativo` will fail mysteriously. The user can't trace the bug because the substitution is undocumented.

**Right**: stop and surface the mismatch. Offer 3 options:
- Add the missing option in GHL settings → Custom Fields
- Update the spec to use the existing value
- Pick the closest existing value WITH the user's explicit yes

## 3. Workflow name with ASCII arrow `->`

**Wrong**: `[Balayage Perfecto] Follow-up enviado -> Captura + roteamento`

**Why wrong**: ZOI convention is Unicode `→` (U+2192). The spec and audit greps all assume `→`. ASCII `->` will fail every "all workflows follow the pattern" check.

**Right**: use `→`. Type it directly via `browser_type` — Unicode passes through fine.

## 4. Using internal codes in workflow names

**Wrong**: `[fsa002] webinario tag → follow-up`

**Why wrong**: ZOI nomenclature explicitly bans `fsa002`, `ba05`, `mme01mia`, `sale02`, `sale03` from new workflow names. The codes mean nothing to humans reading the canvas. Translate to the friendly product name.

**Right**: `[Balayage Perfecto] Webinário assistido → Follow-up comercial`

| Internal code | Friendly name |
|---|---|
| `ba05` | `Balayage Avanzado` |
| `fsa002` | `Balayage Perfecto` |
| `fsa003` | `Los Siete Materiales` |
| `fsa003 colorcorreccion` | `Corrección Premium` |
| `sale02` | `Comunidad Academia Samra` |
| `sale03` | (verify with project) |
| `mme01mia` | `Estilista Milionário` |

## 5. Publishing before final batch

**Wrong**: flipping the `Borrador / Publicar` toggle to test, "just to see if it works".

**Why wrong**: published workflows fire on every matching event from that point on. A test in a live account is a real production event. We had Hotmart webhooks fire on test contacts and bill people for nothing.

**Right**: always Draft until project's final publish batch. To test, use the `Probar el flujo de trabajo` button which simulates without firing actions.

## 6. Missing End on a guard branch

**Wrong**:
```
Find Opportunity
  Found     → (no action)  ← workflow continues to next sibling step
  Not Found → ...
```

**Why wrong**: in GHL workflow trees, an empty branch falls through to the next step in the parent. So your guard didn't guard — the Found path also runs the Not Found actions.

**Right**: every guard branch needs an explicit terminal action (`End workflow` step) or the action chain that's intentional for that branch.

## 7. Random 50/50 instead of 60/40

**Wrong**: `Dividir` with equal weights when the spec says 60% Emerson / 40% Joselyn.

**Why wrong**: weights matter for the load split. Defaults bias one way that's not what was agreed.

**Right**: configure the percentages explicitly. Verify in the canvas label after saving — GHL shows the percentage on each branch.

## 8. Skipping the `Asignar a usuario` before `Crear oportunidad`

**Wrong**: create opportunity with `Use Contact's Owner` as assigned user, but the contact has no owner yet (M3 hasn't assigned).

**Why wrong**: the opportunity is created with no owner. Workflow 3 (alerta WA) later can't find an owner to notify.

**Right**: in the 60/40 branches, first `Asignar a usuario` (Emerson or Joselyn) on the contact, then create the opportunity with `Use Contact's Owner`. The contact-level assign cascades.

## 9. Notification to "Todos los usuarios"

**Wrong**: send internal notification to all staff.

**Why wrong**: floods Emerson/Joselyn/Kevin/Michael with notifications for leads they don't own. Notification fatigue → real alerts get ignored.

**Right**: target `Assigned User of Contact` (or `Owner`). Single recipient = the person responsible for that lead.

## 10. Closing config panel without saving

**Wrong**: filling out an action's fields, then clicking `Cerrar panel` (X) to go look at the canvas.

**Why wrong**: GHL prompts "Cambios no guardados — ¿Confirmar?" — and habit pushes "Confirmar" which discards everything you typed.

**Right**: click `Guardar trigger` / `Guardar acción` first, THEN close. If you accidentally hit `Cerrar`, choose `Cancelar` in the modal to stay in the panel.

## 10a. Clicking `Cancelar` in a newly-added action's config panel

**Wrong**: action is added to canvas via the action picker, config panel opens. You realize you want a different action, click `Cancelar` in the panel footer thinking it just closes without saving.

**Why wrong**: For freshly-added (not yet saved) actions, `Cancelar` **deletes the node entirely** from the canvas. Not just closes the panel — the action vanishes. You then have to re-add and reconfigure from scratch.

**Right**: if you want to abort a newly-added action, `Cancelar` is the correct action — but expect the node to disappear. If you want to keep the node but edit later, fill the minimum required fields and click `Guardar acción` first.

**Distinction**:
- New action + Cancelar = delete node ✘
- Existing action + edit + Cancelar = discard edits, keep node ✓

## 10b. Validation errors silently swallow Guardar acción clicks

**Wrong**: click `Guardar acción`, panel doesn't close, assume save worked, click `Guardar` workflow.

**Why wrong**: missing required field → save fails but no obvious feedback unless you look for the red "Please check the fields for valid inputs" toast at the top of the panel and the per-field "Esto no puede estar vacío" inline error.

**Right**: after clicking `Guardar acción`, **always re-snapshot and check** for the toast or inline errors. If present, locate the missing field, fill it, click `Guardar acción` again. Don't move on until the panel actually closes.

Common required fields you might miss:
- `Notificación Interna` → **`Página de redirección`** is mandatory (options: Contacto · Conversación · Oportunidad)
- `Notificación Interna` → **`Para el tipo de usuario`** is mandatory
- `Create opportunity` (BETA) → **`Stage`** is mandatory (defaults to last stage of pipeline 🔮 OPORTUNIDADE FUTURA, almost always wrong — change to actual entry stage)

## 11. Reusing Playwright refs after a state change

**Wrong**:
```
browser_click(target: f27e2031)  # opens dropdown
browser_wait_for(time: 1)
browser_click(target: f27e2031)  # try to close — ref is stale
```

**Why wrong**: GHL re-renders aggressively. Refs change after every click, modal toggle, navigation.

**Right**: re-snapshot before each click that depends on a fresh ref. Yes, this is more API calls. The alternative is timeouts.

## 12. Trying to add picklist options inline

**Wrong**: attempting to type a new value into the `Status do Cliente` picklist dropdown.

**Why wrong**: GHL picklists don't allow inline option creation in the workflow editor. You can only add options via Settings → Custom Fields.

**Right**: navigate to Settings → Custom Fields → edit the field → add option → return to workflow. Or change the strategy to use a different field that's freeform.

## 13. Workflows at root instead of in a project folder

**Wrong**: leaving `New Workflow : 1779800095013` at root after creation.

**Why wrong**: pollutes the root list, can't find later, breaks folder-based audits.

**Right**: when creating, ensure URL has `&folder={folder_id}` before clicking `Crear flujo de trabajo`. The new workflow inherits the active folder.

## 14. Using `Crear/actualizar oportunidad` (legacy combined action)

**Wrong**: pick the `Crear/actualizar oportunidad` action from the Oportunidad category.

**Why wrong**: GHL is deprecating it. The config panel itself shows: *"Aviso de interrupción de acción — Crear/Actualizar acción se interrumpirá próximamente. Los flujos de trabajo existentes no se verán afectados; sin embargo, las nuevas acciones Crear oportunidad y Actualizar oportunidad serán las acciones que se utilizarán en el futuro."*

**Right**: use the dedicated successors in the same Oportunidad category:

- **`Create opportunity`** (BETA) — for creating a new opportunity
- **`Update opportunity`** — for editing an existing opportunity

Both are listed below `Crear/actualizar oportunidad` in the action picker. When building new workflows in this project, always pick one of these, never the combined legacy one.

## 15. Naming inconsistency across BP and LSM variants

**Wrong**: `[Balayage Perfecto] Follow-up enviado → Captura + roteamento` paired with `[LSM] Follow-up enviado → captura`.

**Why wrong**: ZOI bans abbreviations in workflow names. `LSM` is a code, not a friendly name. Variants of the same workflow pattern must be byte-identical except for the product token.

**Right**: `[Los Siete Materiales] Follow-up enviado → Captura + roteamento`. Capitalization, spacing, arrows — all identical to the BP variant.

## 16. Snapshotting immediately after picking a dropdown option

**Wrong**: pick a select option, immediately re-snapshot to look at next state.

**Why wrong**: GHL uses Naive UI (Vue) with Teleport-rendered popovers. After picking an option, the panel often re-renders to add dependent fields (e.g., picking `Tipo de notificación = Notification` adds Título, Mensaje, Página de redirección, Para el tipo de usuario fields). The snapshot may capture the **old DOM** before Vue re-renders, leading to refs that don't exist or fields that look missing.

**Right**: after every select-option click, **`browser_wait_for --time 1` (or 2)** before the next snapshot. If the snapshot looks wrong, wait again and re-snapshot before clicking elsewhere.

## 17. Clicking the inner label span of a Naive UI select

**Wrong**: clicking the `<span>` text "Seleccionar tipo de Usuario" inside the dropdown trigger.

**Why wrong**: Naive UI listens to `mousedown` on the wrapper `<div class="n-base-selection">`, not the inner span. Click on the span doesn't fire the trigger event reliably.

**Right**: click the wrapper `<div>` (the parent of the label span). When you snapshot the field, there's typically an outer `generic` ref (the wrapper) and an inner `generic` ref (the label) — target the outer one. If you can't tell, try the parent ref before the label ref.

## 18. Pressing Enter in the workflow name inline editor

**Wrong**: edit workflow title via the pencil icon, type new name, press Enter to commit.

**Why wrong**: Enter triggers a navigation event that opens a "Cambios no guardados" confirmation modal — even when there ARE no unsaved changes. You then have to click Cancelar in the modal to dismiss it. Adds friction every rename.

**Right**: type the new name, then click elsewhere on the title bar (the icons row, the back button area) to commit via blur. No modal.

## 19. Trusting snapshot order of `+` (Añadir acción) buttons

**Wrong**: workflow has 8 `+` buttons. Snapshot lists them in some order. You click the 5th assuming it's the 5th visually top-to-bottom.

**Why wrong**: snapshot order = creation/DOM order, NOT visual position. Clicking the wrong `+` inserts an action **between** two existing nodes instead of after the chain, breaking the linear sequence (e.g., Notification ends up between Create Opportunity and Update Field).

**Right**: take a `browser_take_screenshot` first. Find the visual position of the `+` you want (badge appears "Por favor, seleccione la acción" at click position before picking action — confirms position). If wrong, click `Cancelar` in the action picker (this doesn't add a node since none was picked) and try a different `+`.

**Best (confirmed 26/05 W-M4-06)**: map ref → coord via `browser_evaluate` BEFORE clicking:
```
browser_evaluate(
  function: "(el) => { const r = el.getBoundingClientRect(); return {x: r.x, y: r.y}; }",
  target: <ref>
)
```
For branched If/Else: low `x` = LEFT branch (typically `Sim`/Yes), high `x` = RIGHT branch (typically `None`). Vertical `y` distinguishes between sequential `+` (between Trigger/Wait/If/Else nodes). 3 coord checks (~3 tool calls) costs less than a wrong-click delete cycle (~10+ calls + risk of breaking validation state).

Note: snapshot order for `Añadir acción` refs follows DOM creation order, so the LAST `+` you used gets recreated with a NEW ref while ORIGINAL `+`s keep their refs. So after deleting an action, the `+` slot where the deleted action lived gets a fresh ref number — that ref does NOT correspond to the visual `+` button position you previously clicked.

Alternative: hover each `+` to see GHL highlight what edge it sits on. Or open the source workflow node in the snapshot, find its `id` (UUID), then locate the `+` whose CSS id matches `<UUID>-plus-button` (that's the `+` immediately after that node).

## 20. Not updating the spec after a UI-driven decision

**Wrong**: discover that GHL picklist real values differ from spec, work around it in the UI, move on.

**Why wrong**: the spec is the contract. The next person to touch this workflow will read the spec and see the old values, then "fix" it back to the (wrong) spec version.

**Right**: every time you adapt to an unexpected UI state, update the corresponding `Specs_M*.md` file with the actual decision and a one-line note: `(decisão UI 22/05: real picklist usa Lead Quente, não Lead ativo — atualizado)`.
