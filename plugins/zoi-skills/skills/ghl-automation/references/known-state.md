# Known GHL State — BEAUTYFANS ACADEMY LLC

Snapshot of relevant state in the GHL account as discovered during build sessions. Update this file when you discover something new — it pays back the cost on every subsequent session.

> Location ID: `kMV30Up1fefbAFRwkOPT`
> Last full audit: 22/05/2026
> Last incremental update: 29/05/2026

## Custom field — `Status do Cliente`

**Type**: picklist (dropdown)
**Actual values in GHL**:
- `Prospecto`
- `Lead Quente`
- `Cliente`
- `Inativo`

**Spec values (Specs_M4_Pipeline.md)**: `Lead ativo · Cliente` (older draft)
**Arquitetura values (Arquitetura_Tags_e_Campos.md)**: `Ativo · Inativo · Qualificado · Desqualificado`

**Decision (26/05)**: use `Lead Quente` as the active-in-pipeline marker. Pending spec update.

## Custom field — `Etapa Follow-Up`

Used by M3. Type: number. Tracks day position in the follow-up sequence.

## Users

**User dropdown (full list, 27 users — discovered 26/05):**

Bruna Costa · Bruno Hinke · Caroline Baldovinotti · Christian Uzcategui · Claudia Camila Cesario Gonzeli · David Flores · Fabrizio Pirozzi · Fernanda Del Giudice · Guilherme de Melo · Joana Bortolozo · Joao Miranda · Jon Brito · **Joselyn Perez** · Karen Salim · Karina Gutierrez · Kevin Ferreira · Laura Santiago · Luccas Silveira · Mariellys Morillo · Mateus Brandão · Michael Higino Cezario de Oliveira · Neive Frota · Paola Marzola · Prospecta Clientes · Rodrigo Dias Souza · Suporte Geral · Yuri Brazil Nogueira

| User | Role | Channels |
|---|---|---|
| ~~Emerson~~ | ~~SDR~~ | ❌ **NOT in user list** as of 26/05 — fallback to Joselyn or Kevin |
| Joselyn Perez | SDR | WhatsApp (canonical spelling — "Jocelyn" in docs was wrong) |
| Kevin Ferreira | Manager | IG/FB inbound, GHL primary user |
| Michael Higino Cezario de Oliveira | Cliente PoC | All channels |
| Joana Bortolozo | (verify) | (verify) |

> **26/05 finding:** Emerson does NOT exist in the user dropdown. Specs reference Emerson 60% / Joselyn 40% but only Joselyn exists. Until Emerson is created (Settings → Staff), either:
> 1. Use Joselyn for both branches of the 60/40 split (effective 100% Joselyn)
> 2. Remove the random split entirely and direct-assign Joselyn (cleaner, single chain)
> 3. Create Emerson user in GHL before building workflows

> Canonical spelling: **Joselyn Perez** (matches GHL dropdown). Older specs use `Jocelyn` — that's wrong, treat as alias.

## Pipelines

| Pipeline | Stages (in order) | Notes |
|---|---|---|
| Inside Sales | 🆕 NOVO LEAD · 👋 PRIMEIRO CONTATO · 🚫 SEM CONTATO · 🌱 EM DESENVOLVIMENTO · 🔄 EM FOLLOW-UP · 🤝 EM NEGOCIAÇÃO · 🔮 OPORTUNIDADE FUTURA · **✅ CERRADO** | Stage names use **emoji prefixes** in real GHL. Pipeline canonical for M4. Pipeline id `UDo7GM3csHdbNeuyMiBL`. **`✅ CERRADO` stage added 29/05** (id `5689c5fd-24a6-4e42-b241-64f19913a695`, position 7, winProbability 100) — unblocked closing workflows W-M4-04/05/11–14. |
| Como ganar 5k mes | (verify) | Existing |
| Compradores do Evento | (verify) | Existing |
| Customer Success | (verify) | Existing |
| Mia - Estilista Milionário IA | (verify) | Existing (AI-related) |
| Renovação | (verify) | Existing |
| Social Selling - Facebook | (verify) | Created Feb/2026, undocumented |
| Social Selling - Instagran | (verify) | Note typo: "Instagran" not "Instagram" |
| Social Selling - Tiktok | (verify) | Existing |
| Suporte | (verify) | Existing |
| Webnário de Balayage Lunes | (verify) | Note: "Webnário" typo (should be Webinário) — keep as-is |

**Discovery (26/05):** Inside Sales dropdown in `Create opportunity` action shows stages with emoji prefix. Spec workflows should match the emoji-prefixed labels exactly.

**Update (29/05): `✅ CERRADO` stage created via internal API.** Pipeline stage CRUD works:
- `GET /opportunities/pipelines?locationId={loc}` (header `version: 2021-07-28`) → list pipelines with `stages[]`
- `PUT /opportunities/pipelines/{pipelineId}` (header `version: 2021-07-28`) with body `{name, stages:[...existing + new], showInFunnel, showInPieChart}` → append a stage. New stage object: `{name, showInFunnel:true, showInPieChart:true, position:N, stageWinProbability:100}` (no id → server generates). Reversible (delete by PUT without it). Stage object shape: `{id, name, showInFunnel, showInPieChart, position, stageWinProbability}`.
- The closing `Update opportunity` action stores stage as UUID in `attributes.__customInputFields__[].value` where `filterField=="pipelineStageId"`. These UUIDs are constant across replicas (same pipeline/stage) so the replicate script does NOT need to remap them.

**Tag CRUD via API (29/05):** `POST /locations/{loc}/tags` (header `version: 2021-07-28`) body `{name}` → `{tag:{id,name,locationId}}`. `GET /locations/{loc}/tags?limit=N` lists. Created all `[<funil>] compra aprovada` tags for closing workflows.

Status options per opportunity: `Aberto(a)` · `Perdido(a)` · `Ganho(a)` · `Abandonar`

Motivos de perda (already populated):
- `MIGRACION SISTÉMICA`
- `CLIENTE POTENCIAL DESCALIFICADO`
- `Não possui Visto americano`
- `AUTOMAÇÃO ERRADA`
- `número errado`
- `Deixou de interagir`
- `Oportunidade Duplicada`

Mixed PT/ES casing — Michael said keep as-is for now (22/05). Don't normalize without his approval.

## Tags — confirmed existing (post-migration 17-18/03)

Tags follow `[produto] evento` in lowercase in the DB (display rendering may capitalize first letter of segments). When selecting in workflows, search lowercase.

**Balayage Perfecto**:
- `[balayage perfecto] follow-up enviado`
- `[balayage perfecto] follow-up encerrado`
- `[balayage perfecto] webinário assistido`
- `[balayage perfecto] replay assistido`
- `[balayage perfecto] inscrito no webinário`
- `[balayage perfecto] lead opt-in`
- `[balayage perfecto] lead quente`
- `[balayage perfecto] lead fervendo`
- `[balayage perfecto] carrinho abandonado`
- `[balayage perfecto] compra aprovada` **← duplicated (2 entries with same name)** — flag for dedup
- `[balayage perfecto] compra cancelada`
- `[balayage perfecto] webinário acessado` (+ variants `— segunda`, `— terça`)
- `[balayage perfecto] pitch assistido`
- `[balayage perfecto] estava no pitch — segunda` / `— terça`
- `[balayage perfecto] estava na oferta — segunda` / `— terça`
- `[balayage perfecto] oferta clicada` (+ `— segunda`, `— terça`)
- `[balayage perfecto] assistiu 60 min — segunda` / `— terça`
- `[balayage perfecto] assistiu 60 min — segunda (dup)` ← also duplicate

**Comunidad Academia Samra** (BP destination product):
- `[comunidad academia samra] compra aprovada`
- `[comunidad academia samra] compra aprovada — lead fervendo`
- `[comunidad academia samra] carrinho abandonado`
- `[comunidad academia samra] downsell abandonado` / `comprado` / `— trigger de recuperação`
- `[comunidad academia samra] em acompanhamento`

**Balayage Avanzado**:
- `[balayage avanzado] carrinho abandonado` / `cancelado`
- `[balayage avanzado] lead opt-in` / `lead fervendo` / `lead vip`

**Camp Samra**:
- `[camp samra] carrinho abandonado`
- `[camp samra] lead morno`

**Academia Samra** (legacy — verify migration completeness):
- `[academia samra] alunos`
- `[academia samra] caliente respondio pesquisa`
- `[academia samra] compradores` / `compradores sale03`
- `[academia samra] compra aprovadoa >< upsell para evento` ← typo "aprovadoa"
- `[academia samra] hirviendo - chat yt`
- `[academia samra] inscritos`
- `[academia samra] tarjeta rechazada`
- `[academia samra][ação externa][00]`

**Beauty Elite Club**:
- `[beauty elite club][caliente][lista de epsera]` ← typo "epsera"
- `[beauty elite club][tibio][lista de epsera]`

**Como Ganar 5k Como Estilista** (legacy product/event):
- `[como ganar 5k como estilista] assistiu 60 minutos` / `clicou na oferta` / `estava na oferta` / `estava no pitch` / `acessou` / `enviou`

## Tags — flagged anomalies (cleanup backlog)

| Anomaly | Tag | Action |
|---|---|---|
| Duplicate | `[balayage perfecto] compra aprovada` ×2 | Merge — verify which is referenced by which workflows first |
| Duplicate | `[balayage perfecto] assistiu 60 min — segunda` ×2 (one with `(dup)` suffix) | Delete the `(dup)` variant after verifying zero references |
| Typo | `[academia samra] compra aprovadoa >< upsell para evento` | Rename to `compra aprovada` |
| Typo | `[beauty elite club][...][lista de epsera]` (×2) | Rename to `espera` |

## Folder structure (Automatización)

```
(root)
├── Importação e Distribuição - Kevin e Michael/  ← legacy/admin
├── Joana -/                                       ← name has trailing dash
├── Luccas/                                        ← ZOI working folder (id a314aad8-d40b-429f-a019-f8b374c4b236)
│   ├── Carrinhos abandonados/                     ← M2 workflows
│   ├── Webnars/                                   ← M3 workflows
│   ├── pipeline/                                  ← M4 work-in-progress (CREATED BY USER, may be duplicate of M4 folder)
│   └── M4 — Pipeline Inside Sales/                ← canonical M4 (id 193d45c3-dae7-468e-bb04-9874b4f314ce)
├── Michael/
├── SA][MME01MIA][Organização Kevin]               ← Kevin-organized legacy
├── Templates Automações/                          ← (Oct 2025)
├── Webnário EUA/                                  ← new (May 2026)
├── [SALE03][Organização - Kevin]/
├── [SA][BEAUTYELTIECLUB][Organização Kevin]/
└── [SA][FSA002][Organização -Kevin]/
```

> Note: there are **two M4-adjacent folders** under `Luccas/` — `pipeline/` (May 25) and `M4 — Pipeline Inside Sales/` (May 26). User created one then the other. Confirm with user which is canonical before creating new workflows.

## Workflows — current state (Luccas folders, partial inventory)

In `Luccas / M4 — Pipeline Inside Sales/` — **14/14 workflows exist as of 29/05 (all DRAFT)**:

Captura + roteamento (6, Find Opp guard + Random Split 60/40 + assign + Create opp + field + notify):
- `[Balayage Perfecto] …` `48fa909c-af5a-45d7-ac02-02538e3c7191` (W-M4-01, UI original)
- `[Los Siete Materiales] …` `59ff38e9-834c-4d3e-83b4-71241074376a` (W-M4-02, UI dup)
- `[Balayage Avanzado] …` `0acb2c30-16dc-4efe-aa10-af47b57c1905` (W-M4-07, API)
- `[Estilista 360] …` `9b5d4b26-509f-46af-ae59-6e46e2073a1f` (W-M4-08, API)
- `[Camp Samra] …` `6a08aa19-b8c4-4fa6-8088-b0fa3bf87398` (W-M4-09, API)
- `[Balayage Business] …` `5368c3c4-3eaf-4910-a328-8c088bc5b725` (W-M4-10, API)

Closing / Cerrar pipeline (6, Update opp [Won + stage ✅ CERRADO] + field Cliente + Remove follow-up tag) — created 29/05:
- `[Comunidad Academia Samra] …` `45262d63-e53f-40a8-b8d0-9171a3a618c3` (W-M4-04, UI template)
- `[Corrección Premium] …` `8bdc6f93-8b3d-4759-92fc-0f7b5b04d919` (W-M4-05, API)
- `[Balayage Avanzado] …` `94a4f56f-66cf-4886-b0af-7f66852955ff` (W-M4-11, API)
- `[Estilista 360] …` `4b26f89a-b9bd-4fe1-a663-240d4ecbb66a` (W-M4-12, API)
- `[Camp Samra] …` `787a8851-9efc-492c-8b0f-f1c62c32a666` (W-M4-13, API)
- `[Balayage Business] …` `1aeecebd-5f38-448e-b16d-0c85c4785063` (W-M4-14, API)

Infra (2):
- `[Infraestrutura] Primeiro Contato → Sem Contato (24h sem resposta)` `66f5a2c8-b1a8-4ae4-be04-3f04b853e395` (W-M4-06, complete)
- `[Infraestrutura] Mensagem WA recebida → Mover + alertar` `c90bd575-7571-4445-8389-df9e20837a94` (W-M4-03, complete: WA-reply trigger → Find Opp guard → on `Opportunity Found` an If/Else `Estágio = Primeiro Contato?` → Sim: `Mover para Em Desenvolvimento` (Update opp stage=🌱 EM DESENVOLVIMENTO); None/Not Found → FINAL. Owner notifications per spec not added — auto-move is the core behavior; notify is optional polish.)

All 6 capture WFs assign 60/40 to Emerson/Joselyn but **Emerson user still does not exist** — Random Split branch fires to a missing user. Resolve when Emerson is created (Settings → Staff) or repoint to Joselyn.

M3 Webnars `21b1565c-…` (W5 BP Inscrito) and `4441f1d3-…` (W6 LSM opt-in) were cloned from M3-W1 and carry the **wrong** internal steps (4-SMS follow-up, not the spec's 2× WhatsApp "wait-until-specific-time" lembrete). Need manual rebuild with the correct WA copy + send windows — out of scope for structural replication.

In `Luccas / Carrinhos abandonados/`:
- `[Infraestrutura] Carrinho abandonado → Roteamento por produto` (PUBLISHED, 1845 enrolled, since Mar 12)
- 8 `[<produto>] Carrinho abandonado → Recuperação` (DRAFT)

In `Luccas / Webnars/`: M3 workflows (DRAFT)

In root (legacy publicados):
- Many `[comercial][fsa002][...]` workflows
- `Auto Welcome WhatsApp BR/EUA`
- `Fluxo de renovação` / `Fluxo de renovação 2`
- `ROTEAMENTO – WhatsApp Oficial (60% Emerson | 40% Jocelyn)` (couldn't find via search "ROTEAMENTO" — may be renamed or in subfolder; full text `"60"` returns unrelated workflows)

## Trigger schema discoveries

- `Etiqueta de contacto` trigger requires adding a filter (`Etiqueta añadida` or `Etiqueta eliminada`) — the trigger alone doesn't specify which tag. The filter picks the tag.
- Tag-added trigger only fires for tags added **after** the workflow is published. For retroactive enrollment use the bulk-enroll guide (link in the trigger config alert).

## Save flow confirmed

1. Configure step → click `Guardar trigger` or `Guardar acción` in panel footer
2. Repeat for all steps
3. Click top-right `Guardar` to persist workflow → toast `Guardado!`
4. Refresh-safe at this point

## Action picker observations

The action list shows mixed Spanish-translated and English-untranslated entries. Newer features (Agent Studio, Voice AI, Communities, Certificates, Google Ads, Ecommerce, Communication) are in English. The core internal/contact/opportunity/payments actions are translated.

When searching the action picker, both languages work — type "If" or "Si" and you'll find If/Else.

## ZOI Agentic OS notes (out of scope for this skill but related)

The project also runs a Python "Agentic OS" in `scripts/zoi/` with skills like `auditar-workflow-ghl`. That skill audits exported workflow JSON against ZOI standards. The export is via the GHL admin `automaster` feature.

This skill (`ghl-automation`) is for **building/editing** in the UI. The Python skill is for **auditing** exported JSON. Different surfaces, complementary.
