# ghl-process-tool

Ferramenta reusável para **estudar e documentar o processo de atendimento/vendas** de
qualquer conta GoHighLevel a partir das conversas reais. Multi-cliente, config-driven,
zero dependências (Python stdlib). Passos determinísticos via CLI + passos com IA via
o skill Claude Code `processo-atendimento`.

## Pipeline
```
extract → clean → metrics → graph → judge → docs
(CLI)      (CLI)   (CLI)      IA      IA       IA
```

## Estrutura
```
ghl-process-tool/
  ghli.py                 CLI (subcomandos)
  ghltool/                pacote: config, extract, clean, metrics, graph, judge
  clients/
    _template.json        modelo de config
    instaltech.json       exemplo (cliente de referência)
  prompts/                templates dos subagents (grafo, judge, manual)
  SKILL.md                skill Claude Code que orquestra o pipeline inteiro
  README.md
```

## Uso rápido (determinístico)
```bash
cd ghl-process-tool
export GHL_TOKEN=pit-xxxxxxxx                       # token PIT do cliente (não vai no config)
python3 ghli.py init meucliente                     # cria clients/meucliente.json
$EDITOR clients/meucliente.json                     # location_id, vocabulary, domain_context, output_dir
python3 ghli.py all --config clients/meucliente.json   # extract + clean + metrics
```

## Pipeline completo (com IA)
No Claude Code, invoque o skill **processo-atendimento** apontando o config do cliente.
Ele roda os passos determinísticos e orquestra grafo + judge + documentação (subagents),
com auto-retry de chunks e geração dos manuais/dashboard.

## Config por cliente (`clients/<nome>.json`)
| Campo | O quê |
|---|---|
| `ghl.location_id` | Location ID da subconta |
| `ghl.token_env` | nome da env var com o token (default `GHL_TOKEN`) |
| `ghl.months_back` | janela de tempo |
| `ghl.workers` | threads p/ buscar mensagens |
| `objective` | `process` \| `leads` \| `quality` |
| `cleaning.*` | `min_turns`, `ratio_max`, `group_min`, `sample_n`, `channel_noise`, `extra_scrub_patterns` |
| `vocabulary.*` | ids canônicos do vertical (products/stages/objections/payment/intents) |
| `domain_context` | descrição da empresa p/ os subagents |
| `output_dir` | onde escrever os dados/saídas |

## Comandos do CLI
```
init <nome>                    cria config a partir do template
extract  --config C            puxa conversas (paralelo + cache incremental)
clean    --config C            limpa/qualifica
metrics  --config C            métricas determinísticas (SLA, quem larga, silêncio)
graph-prep / graph-status / graph-prompt --chunk N / graph-merge
judge-prep / judge-prompt --chunk N / judge-aggregate
all      --config C            extract + clean + metrics
```

## Otimizações embutidas
- **Extração paralela** (ThreadPool) + **cache incremental** (por `conversationId`+`dateUpdated`):
  re-runs só puxam o que mudou.
- **User-Agent de browser** (Cloudflare bane o urllib) + **retry** (429/5xx/timeout).
- **Métricas determinísticas** — % última-msg-nossa, SLA de 1ª resposta, latência, silêncio,
  exatas em 100% do corpus (não estimativa amostral).
- **Auto-retry de chunks** do grafo (`graph-status` lista os que faltam).
- **LLM-judge em lote** — desfecho + categoria de vazamento de TODAS as conversas, agregado.

## Instalar o skill globalmente (opcional)
Para usar em qualquer projeto/cliente do Claude Code:
```bash
cp -R ghl-process-tool ~/.claude/skills/processo-atendimento
```
(O `SKILL.md` já está na raiz da ferramenta.)
