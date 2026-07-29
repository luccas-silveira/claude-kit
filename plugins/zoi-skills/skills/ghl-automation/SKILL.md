---
name: ghl-automation
description: Build, edit, audit, or document automations and workflows in GoHighLevel (GHL) via Playwright browser automation. Covers the GHL workflow editor (triggers, actions, branches, filters, pipelines, opportunities), naming conventions used by ZOI, and the cross-origin iframe quirks of `app.gohighlevel.com`. Use whenever the user mentions creating/configuring a GHL workflow, automation, trigger, pipeline action, opportunity action, opportunity capture, branching logic, tag-based flow, or asks anything like "no GHL" / "monta esse workflow" / "cria automação no GHL" / "configurar trigger" / "Find Opportunity step". Also triggers on Spanish UI mentions (`Crear flujo de trabajo`, `Etiqueta de contacto`, `Añadir acción`, `Guardar acción`) since the BEAUTYFANS ACADEMY location is in Spanish. ZOI nomenclature `[Produto] Gatilho → Ação` should be enforced for every new workflow created in this account.
---

# GHL Automation — Build & Audit Workflows

This skill turns Claude into a competent operator of the GoHighLevel workflow editor via Playwright. It encodes:

- The shape of the UI (so you don't have to rediscover trigger names every session)
- ZOI naming conventions for workflows, tags, and fields
- Cross-origin iframe quirks of `app.gohighlevel.com`
- The standard "build a captura → roteamento → criar oportunidade" pattern used in the Gabriel Samra project

When you build a workflow, ground every step in `Specs_M*_Pipeline.md` / `Specs_M*_Webinario.md` of the relevant project. The skill is operational — the spec is the source of truth.

---

## Why this skill exists

GoHighLevel has no public API for visual workflow editing, so we drive the UI with Playwright. The UI is dense, the iframe is cross-origin (so direct DOM access from the parent fails), and labels are localized — in the BEAUTYFANS ACADEMY account they're in **Spanish**. Without a memory of where things live and what they're called, every session burns ~30+ tool calls just relearning the surface. This skill captures that surface so you can go straight to building.

The other reason this skill exists: ZOI has strict naming conventions (`[Produto] Gatilho → Ação`) and a workflow that looks correct in isolation can still violate the naming standard or duplicate an existing automation. The skill encodes those guardrails.

---

## How to use this skill

When the user asks to build or modify a GHL workflow:

1. **Confirm the spec.** Open the corresponding `Specs_M*.md` for the project and re-read the workflow's section. Don't trust memory — these specs evolve. If no spec exists yet, refuse to build until one is written; the GHL surface is too dense for ad-hoc decisions.
2. **Confirm pre-reqs in GHL.** Pipeline name, stages, custom fields, tags, and users must already exist. The workflow editor doesn't let you create most of these inline.
3. **Drive the UI step by step.** Use the patterns in `references/ghl-ui-cheatsheet.md` for trigger/action selection, save flow, and dropdown popovers.
4. **Save as Draft, never publish unless asked.** Project convention is to keep workflows in Draft until a final publication wave at the end of the project.
5. **Cross-check the canvas** against the spec before declaring done. Common misses: missing "End workflow" on a guard branch, picklist value mismatch (real values in GHL ≠ values written in spec), wrong stage name (`Cerrado` vs `Fechado`).

For audits (rather than builds), inspect an existing workflow's nodes against the spec and report deltas inline.

---

## Spec → workflow translation

The standard workflow pattern in this project — entrada no pipeline — has this skeleton:

```
[Trigger: Tag Added — [Produto] <evento>]
            ↓
[Find Opportunity (Inside Sales, contact = current)]
    ↓ Found                ↓ Not Found
   [End]            [Random Split 60/40 — Emerson/Joselyn]
                    ↓ 60%              ↓ 40%
              [Assign Emerson]   [Assign Joselyn]
                            ↓
                [Create Opportunity Inside Sales / Novo Lead]
                            ↓
                [Update Field Status do Cliente = Lead Quente]
                            ↓
                [Send Internal Notification]
```

**The duplicate-prevention guard is `Find Opportunity`, not an If/Else on a custom field.** Find Opportunity returns native `Opportunity Found` / `Opportunity Not Found` branches and respects the actual pipeline state. Using `Status do Cliente == Lead Quente` (or any picklist) as a proxy is a known anti-pattern — see `references/anti-patterns.md`.

For variants — fechamento workflow, timer-based mover, alerta de resposta — the trigger and the actions change but the pattern of `confirm spec → check pre-reqs → drive UI → save Draft` stays the same.

---

## ZOI conventions (mandatory)

Every workflow you create or rename must follow these conventions. They live in the project's `CLAUDE.md` but are reproduced here so you don't need to re-read it every session.

### Workflow name format
**`[Produto] Gatilho → Ação`**

- `→` is U+2192, not `->`
- Português brasileiro
- No internal codes (`fsa002`, `ba05`, `mme01mia`, `sale02`, `sale03`) — translate to the friendly product name

### Product vocabulary (canonical)
`Balayage Avanzado` · `Balayage Perfecto` · `Los Siete Materiales` · `Comunidad Academia Samra` · `Corrección Premium` · `Estilista Milionário` · `Estilista 360` · `Camp Samra` · `Balayage Business` · `Suporte` · `Social` · `Infraestrutura`

### Trigger vocabulary (a few common ones — full list in CLAUDE.md)
`Compra aprovada` · `Carrinho abandonado` · `Webinário assistido` · `Webinário — replay assistido` · `Follow-up enviado` · `Mensagem WA recebida` · `Tag adicionada: [nome]` · `Estágio alterado`

### Action vocabulary
`Boas-vindas` · `Recuperação (N dias)` · `Follow-up comercial` · `Roteamento` · `Captura + roteamento` · `Notificação interna` · `Sync Google Sheets` · `Atribuição` · `Cerrar pipeline` · `Mover + alertar`

### Tags
**`[Produto] Evento`** — same product vocabulary. Tag = event/behavior. Field = state/origin. See `Arquitetura_Tags_e_Campos.md`.

---

## Reference files

Read these on demand. They're split out so this SKILL.md stays focused on the *what* and *why*.

- `references/ghl-ui-cheatsheet.md` — UI labels in Spanish, common refs, click sequences for trigger setup, action selection, save flow.
- `references/playwright-patterns.md` — How to drive the cross-origin iframe, handle dropdown popovers that render outside their parent, recover from "html intercepts pointer events" errors, capture refs after re-snapshots.
- `references/anti-patterns.md` — Known wrong moves and the right alternative (e.g., status field proxy vs `Find Opportunity`, ASCII arrows in names, publishing too early, internal codes in labels, missing End branch on guards).
- `references/known-state.md` — Real picklist values, tag list quirks (duplicates, casing), existing users (Emerson/Joselyn), pipeline names. Updated as discoveries happen.

---

## Operating rules

1. **The spec wins.** If the GHL state contradicts the spec, document the contradiction and ask before changing either side. Don't silently adapt one to the other.
2. **Localized picklist values matter.** When the spec says `status_cliente = "Lead ativo"` but the GHL picklist only has `Lead Quente`, **don't substitute silently**. Surface the mismatch and offer to either (a) add the option in GHL settings, or (b) update the spec to match reality, or (c) pick the closest existing value with explicit user approval.
3. **Draft always.** Toggle stays on `Borrador`. Project publishes in a final batch.
4. **Folder structure is project state.** Use the folder hierarchy (`Luccas / M4 — Pipeline Inside Sales` etc.) — don't create workflows at root.
5. **The Spanish UI is canonical here.** Match labels exactly when telling the user about what you clicked. They use the Spanish UI too.
6. **Cross-check before claiming done.** Take a `browser_take_screenshot --fullPage true` after the workflow is built and visually verify the canvas matches the spec. Don't trust the snapshot tree alone — it can miss collapsed nodes.

---

## When NOT to use this skill

- The user wants to query GHL data, not build a workflow → use the GHL API or Make/Zapier (no Playwright)
- The user wants to edit a `Specs_M*.md` document → use file edit tools directly; this skill is for the UI side
- The user wants to render a diagram → use ASCII or Mermaid in markdown; this skill doesn't do that
