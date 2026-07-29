# GHL UI Cheatsheet — Workflow Editor

> All labels are in **Spanish** (BEAUTYFANS ACADEMY account). When the user asks in Portuguese ("trigger de tag"), translate mentally to the Spanish UI label before clicking.

## URL patterns

| Page | URL |
|---|---|
| Workflow list (root) | `/v2/location/{location_id}/automation/workflows?listTab=all` |
| Workflow list (folder) | `…/workflows?listTab=all&folder={folder_id}` |
| Workflow editor | `/location/{location_id}/workflow/{workflow_id}` |
| Dashboard | `/v2/location/{location_id}/dashboard` |

`location_id` for Gabriel Samra: `kMV30Up1fefbAFRwkOPT`.

## Folder structure (Gabriel Samra project)

```
Automatización / (root)
├── Luccas /
│   ├── Carrinhos abandonados/      ← M2 workflows
│   ├── Webnars/                    ← M3 workflows
│   ├── pipeline/                   ← older M4 work (duplicate — flag)
│   └── M4 — Pipeline Inside Sales/ ← canonical M4 folder (id 193d45c3-dae7-468e-bb04-9874b4f314ce)
├── Michael /
├── Joana - /
├── Importação e Distribuição - Kevin e Michael /
├── Templates Automações /
└── [SA] [...]                      ← Kevin-organized legacy
```

## Top-level navigation

1. Open workflow list (URL above)
2. Filter by smart list: **`Todos los flujos de trabajo`** · **`Requiere revisión`** · **`Eliminado`** · **`Trgr - Webhook`**
3. Search box: top-right, accepts partial text match
4. **Three create options**:
   - `Crear carpeta` — new folder
   - `Cree usando IA` — AI generator (avoid for ZOI work)
   - `Crear flujo de trabajo` — opens template picker → choose **`Empezar desde cero`**

## Workflow editor anatomy

| Region | What lives here |
|---|---|
| Top-left | `← Lista de flujos de trabajo` (back) |
| Top-center | Workflow name (click pencil icon to edit inline) |
| Top-right | `Cambios Recientes` · `Deshacer` · `Rehacer` · **`Guardar`** (saves workflow) · `Borrador / Publicar` toggle |
| Canvas left rail | View toolbar (mini-map, zoom, fit-screen) |
| Canvas center | Vue Flow tree with trigger node + action nodes |
| Bottom of canvas | `Añadir` button (add via UI) |
| Right side panel (when configuring a step) | Config form + footer with `Cancelar` / `Guardar acción` (or `Guardar trigger`) |

## Trigger setup

**Open**: click `Añadir disparador` on the trigger placeholder.

The picker shows categories: **Contacto** · **Eventos** · **Citas** · **Oportunidades** · **Afiliado** · **Cursos** · **Pagos** · **Tiendas de comercio electrónico** · **IVR** · **Eventos de Facebook/Instagram** + English-named newer categories (Contact / Events / Appointments / Affiliate / Payments / Communities / Certificates / Google Ads / Ecommerce Stores / Communication).

Common triggers we use:

| Need | Click |
|---|---|
| Tag added to contact | Category **Contacto** → `Etiqueta de contacto` → in config, add filter `Etiqueta añadida` → select tag from typeahead |
| Customer replied WA | Category **Eventos** → `El Cliente Respondió` → filter by channel = WhatsApp |
| Pipeline stage changed | Category **Oportunidades** → `Cambio en la etapa del pipeline` → select pipeline + stage |
| Form submitted | Category **Eventos** → `Formulario enviado` |
| Hotmart webhook | Category **Eventos** → `Webhook entrante` → paste URL after creating |

**Save trigger**: bottom of panel → **`Guardar trigger`**. Don't close the panel before clicking save — closing prompts an "unsaved changes" modal.

## Action picker

**Open**: click any `Añadir acción` (+) button between nodes or at the end.

Top-level categories: **Contacto** · **Objetos personalizados** · **Comunicación** · **Enviar Datos** · **Interno** · **AI de flujo de trabajo** · **Modelos externos de IA** · **Eliza** · **Citas** · **Oportunidad** · **Pagos** · **Marketing** · **Afiliado** · **Suscripción** · **IVR** · plus English newer ones.

The actions you'll reach for most often, by category:

### **Interno** (control flow)
- `If / Else` — branching by contact/opportunity fields
- `Esperar` — wait N time
- `Dividir` — random split (use for 60/40 routing)
- `Goteo` — drip schedule
- `Evento objetivo` — wait-until-event
- `Actualizar valor personalizado` — set workflow variable
- `Ir a` — jump to another step
- `Operación matemática` — arithmetic
- `Código personalizado` — custom JS
- `Añadir / Eliminar del flujo de trabajo` — enroll/un-enroll

### **Oportunidad**
- ~~`Crear/actualizar oportunidad`~~ — **DEPRECATED**. GHL is sunsetting the combined action. Use the dedicated successors below.
- **`Create opportunity` (BETA)** — canonical for creating a new opportunity. Use this in entry-into-pipeline workflows.
- **`Update opportunity`** — canonical for editing an existing opportunity. Use this in closing/stage-change workflows.
- `Eliminar oportunidad`
- **`Find Opportunity`** — **canonical duplicate guard.** Returns `Opportunity Found` / `Opportunity Not Found` branches. Use this instead of If/Else on `status_cliente`.
- `Add owner to opportunity` · `Remove owner from opportunity`
- `Add follower(s) to opportunity` · `Remove follower(s) from opportunity`

### **Contacto**
- `Añadir / Eliminar etiqueta` (add/remove tag)
- `Actualizar campo del contacto`
- `Asignar a usuario`

### **Comunicación**
- `Enviar SMS` · `Enviar Email` · `Enviar mensaje de WhatsApp` · `Enviar Voz`

### **Interno → notification**
- For internal team notification: look under **Comunicación** for `Notificación interna` or `Send Internal Notification` (English label sometimes)

## Step config panel — save flow

Every step config panel has the same footer pattern:

```
[ Cancelar ] [ Guardar acción ]     ← for actions
[ Cancelar ] [ Guardar trigger ]    ← for triggers
```

- `Guardar acción` / `Guardar trigger` commits the step config to the canvas (does NOT save the workflow to GHL).
- Then click **top-right `Guardar`** to persist the workflow itself.
- Without that final `Guardar`, your steps are local-only and refresh wipes them.

If you close the panel via `Cerrar panel` or `Atrás` with unsaved field changes, GHL shows the modal:

> "Cambios no guardados — ¿Seguro que desea descartar los cambios?"
> [Cancelar] [Confirmar]

`Cancelar` keeps you in the panel. `Confirmar` discards.

## If/Else step (when you need it)

Layout:

| Field | Notes |
|---|---|
| `Nombre de la acción` | Defaults to "Condition" — overwrite with descriptive name |
| `Receta de escenario` | Templates; default `Build Your Own` |
| `Ramas` (Branches) | Each branch has a name + condition rows |
| Branch row: `Seleccionar` field | Typeahead — search for the contact/opportunity field |
| Branch row: operator | `Es` (=) · `No es` (≠) · `Está vacío` · `No está vacío` (more for typed fields) |
| Branch row: value | Dropdown of picklist options or free text |
| `Añadir segmento` | AND/OR within a branch |
| `Añadir rama` | New mutually-exclusive branch |
| `Ninguna sucursal` | The default "None" branch — fires when no other branch matches |

## Find Opportunity step

Searches the contact's opportunities by filter (pipeline, stage, status, name). Returns 2 branches:

- `Opportunity Found` — at least one match exists
- `Opportunity Not Found` — no match

Use this for duplicate guards on pipeline entry. Each branch needs its own action chain.

## Random Branch (Dividir)

Splits inscritos by weighted percentages. Each branch has a percentage and a label. Useful for 60/40 routing between sales reps. Branches converge back at next step or run independently.

## Dropdown popovers — important quirk

Many dropdowns (tag search, field selector, picklist value) render the listbox **outside the parent element** via Vue teleport. So a `browser_snapshot` targeting the parent ref won't show the listbox.

To find them:
1. Snapshot the whole iframe content at low depth
2. Look for the latest top-level `generic` ref (usually a fresh ref number, e.g. `f27e4727`)
3. Snapshot that ref at depth 10 to get the list items

Pattern in `references/playwright-patterns.md`.

## Save state indicators

- Top-right button label changes between **`Guardar`** (unsaved changes) and **`Guardado`** (no pending changes). The `Guardado` state is disabled.
- After a successful save: a toast at bottom-right shows **`Guardado! El flujo de trabajo ha sido guardado.`** with a close button.

## Draft vs Publish

Top-right toggle: **`Borrador`** (left) → **`Publicar`** (right). Click moves the slider.

**Project convention**: keep all workflows in `Borrador` until final batch publication. Don't toggle to `Publicar` unless explicitly asked.

## Action-specific field requirements (most common)

These are the fields you MUST set or `Guardar acción` silently fails:

### `Find Opportunity` (Oportunidad → Find Opportunity)
- Pipeline (required)
- Status (Open/Won/Lost/Abandoned — Open for duplicate-guard purposes)
- Returns 2 branches: `Opportunity Found` and `Opportunity Not Found`

### `Dividir` (Random Split / Interno → Dividir)
- Tipo de distribución: `Random Split` (default, leave)
- Rutas: at least 2 paths with name + percentage (must sum to 100)
- Use case: 60/40 SDR routing

### `Asignar al usuario` (Contacto → Asignar al usuario)
- Usuarios: at least 1 user from the dropdown
- Optional: `Aplicar solo a los contactos no asignados` toggle (recommended OFF for round-robin scenarios)

### `Create opportunity` BETA (Oportunidad → Create opportunity)
- Pipeline (required, pre-filled if previously set)
- Stage (required, **defaults to last stage `🔮 OPORTUNIDADE FUTURA` — change to actual entry stage**)
- Opportunity Name (recommended: `{{contact.full_name}} — [Funil]`)
- Optional: Source · Value · Status · Custom fields

### `Actualizar el campo de contacto` (Contacto → Actualizar el campo de contacto)
- Tipo de acción: `Actualizar datos de campo` (default)
- Fields: at least one row with `Seleccionar campo` + value
- For picklist fields: dropdown shows existing options only (cannot add inline)

### `Notificación Interna` (Comunicación → Enviar notificación interna)
- Tipo de notificación: Email / **Notification** / SMS / WhatsApp
- Título (required)
- Mensaje (required, rich text)
- **Página de redirección (required, but easy to overlook):** Contacto / Conversación / Oportunidad
- Para el tipo de usuario (required): Todos los usuarios / **Usuario asignado al contacto** (= owner) / Usuario específico

### `If / Else` (Interno → If / Else)
- Receta de escenario: `Build Your Own` (default)
- At least 1 branch with name + condition (field + operator + value)
- `Ninguna sucursal` (None branch) is the default fallthrough

### Trigger: `Etiqueta de contacto` (Contacto → Etiqueta de contacto)
- Filtro: `Etiqueta añadida` (or `Etiqueta eliminada`) + select specific tag from dropdown
- Only fires for tags added AFTER publish — bulk-enroll guide linked in trigger info alert
