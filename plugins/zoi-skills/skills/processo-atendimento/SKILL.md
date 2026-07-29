---
name: processo-atendimento
description: Estuda e documenta o processo de atendimento/vendas de uma conta GoHighLevel a partir das conversas reais. Puxa as conversas (GHL API), limpa/qualifica, calcula métricas determinísticas (SLA, quem larga, silêncio), mapeia o processo num grafo, classifica desfechos/vazamentos em lote (LLM-judge) e gera manuais operacionais + dashboard. Use quando o usuário pedir "estudar o atendimento de um cliente", "puxar conversas do GHL", "documentar o processo de vendas", "analisar o funil", "rodar o pipeline de atendimento" ou mencionar uma conta GHL + objetivo de processo. Multi-cliente via config JSON (clients/<nome>.json) + token por env (GHL_TOKEN).
---

# processo-atendimento — pipeline de estudo de atendimento (GHL)

Orquestra a ferramenta `ghl-process-tool` (CLI Python determinística + passos com IA).
Roda por cliente. **Antes de tudo**: identifique a pasta da ferramenta (`TOOL`) e o
config do cliente (`CONFIG = clients/<nome>.json`). Se o cliente não tem config,
rode `python3 ghli.py init <nome>` e ajude a preencher `location_id`, `vocabulary`,
`domain_context`. Exija `GHL_TOKEN` no ambiente (peça ao usuário: `export GHL_TOKEN=pit-...`).

Trabalhe a partir de `TOOL/`. `output_dir` do config aponta para onde os dados do
cliente serão escritos (ghl_export/, process_dataset/, graphify-out/, docs/).

## Passos

### 1–3. Determinísticos (CLI)
```bash
python3 ghli.py extract  --config CONFIG    # puxa conversas (paralelo + cache)
python3 ghli.py clean    --config CONFIG    # limpa/qualifica -> process_dataset/
python3 ghli.py metrics  --config CONFIG    # METRICAS.md (SLA, quem larga, silêncio)
```
Valide: nº de conversas, corte temporal, 0 lixo residual. Mostre os números das métricas.

### 4. Grafo do processo (subagents)
```bash
python3 ghli.py graph-prep --config CONFIG  # cria chunks
```
Para cada chunk `i` em `1..graph.chunks`: rode `python3 ghli.py graph-prompt --config CONFIG --chunk i`
e dispare um subagent **general-purpose** com esse texto como prompt (TODOS em paralelo, uma mensagem).
Depois faça o **auto-retry**:
```bash
python3 ghli.py graph-status --config CONFIG   # exit≠0 e lista chunks faltando
```
Re-dispare só os faltantes até `graph-status` zerar. Então:
```bash
python3 ghli.py graph-merge --config CONFIG    # -> .graphify_extract.json
```
Construa o grafo com graphify (`build_from_json` → `cluster` → rotular comunidades →
`export html`), como no skill `graphify`. Saída em `graphify-out/`.

### 5. Classificação em lote — LLM-judge (subagents)
```bash
python3 ghli.py judge-prep --config CONFIG
```
Para cada chunk: `python3 ghli.py judge-prompt --config CONFIG --chunk i` → subagent general-purpose
(todos em paralelo). Depois:
```bash
python3 ghli.py judge-aggregate --config CONFIG   # -> judge_out/JUDGE_AGG.md
```
Isto quantifica desfecho + categoria de vazamento em 100% das conversas (não amostra).

### 6. Análise + documentação
- Escreva `process_dataset/ANALISE_PROCESSO.md` cruzando: funil (do `graph.json`), métricas
  (`METRICAS.md`), e classificação (`judge_out/JUDGE_AGG.md`). Inclua playbook de fechamento
  e forense de evasão (leia uma amostra das conversas `fechou` e `sem_resposta`).
- Para cada linha de produto, dispare um subagent com `prompts/manual_brief.md`
  (substitua `{{PRODUCT_LINE}}`, `{{DOMAIN}}`, `{{ANALYSIS_PATH}}`, `{{CONVS_DIR}}`, `{{OUT_PATH}}`)
  → `docs/MANUAL_<LINHA>.md`.
- Gere `docs/README.md` (índice), `docs/CARTAO_REFERENCIA.md` (cola de bolso) e
  `docs/DASHBOARD_FUNIL.html` (self-contained) a partir dos números reais.

## Princípios (não pule)
- **Defina o objetivo antes de limpar** (process/leads/quality muda os filtros — está no config).
- **Confronte escolhas com evidência** (meça antes de cortar).
- **Vocabulário canônico** no grafo é o que faz o processo emergir — mantenha-o no config por vertical.
- **Honestidade nas métricas**: funil do grafo é frequência de atravessamento; o judge dá desfecho real.
- **Cache + auto-retry**: re-runs são baratos; nunca re-dispare chunks que já existem.

## Replicar em outro cliente
1. `python3 ghli.py init <novo>` → editar `location_id`, `vocabulary` (produtos/etapas/objeções
   do vertical), `domain_context`, `output_dir`.
2. `export GHL_TOKEN=pit-...` da conta do novo cliente.
3. Rodar os passos 1–6.
