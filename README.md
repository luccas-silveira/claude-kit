# claude-kit

Meu setup de Claude Code em um repo — skills próprias empacotadas como plugin, mais a
lista de plugins de terceiros que eu de fato uso (medida por contagem de invocações
nos transcripts, não por palpite).

## Instalar numa máquina nova

```bash
git clone https://github.com/luccas-silveira/claude-kit && bash claude-kit/install.sh
```

Ou só as skills próprias, sem clonar:

```
/plugin marketplace add luccas-silveira/claude-kit
/plugin install zoi-skills@zoi-kit
```

## O que tem aqui

`plugins/zoi-skills/skills/` — 9 skills próprias:

| skill | pra quê |
|---|---|
| `fechar-sessao` | rotina de encerramento (gates, commit, handoff, memória) |
| `ghl-api-docs` | referência offline da API GoHighLevel v3 |
| `impeccable`, `taste-skill` | frontend / design |
| `graphify` | knowledge graph de qualquer input |
| `prompt-engineering` | escrever e auditar system prompts |
| `root-cause` | achar e confirmar causa raiz antes de corrigir |
| `research` | pesquisa preliminar estruturada |
| `supacode-cli` | controlar Supacode pelo terminal |

## Plugins de terceiros (o `install.sh` puxa)

`superpowers` (brainstorming, writing-plans, subagent-driven-development — as mais usadas),
`playwright` (o MCP mais chamado de longe), `ponytail`, `claude-mem`, `watch`,
`code-review`, `security-guidance`, `pyright-lsp`, `typescript-lsp`.

## Fora do escopo

MCP servers com binário/credencial local (`gitnexus`, `ghraphnizer`, `codegraph`) e o
conteúdo de `~/.claude/memory/` — memória é pessoal por máquina, não entra no repo.

## Manutenção

Pra saber o que ainda vale manter, conte as invocações reais nos transcripts:

```bash
grep -roh '"skill":"[^"]*"' --include='*.jsonl' ~/.claude/projects \
  | sed 's/.*"skill":"//;s/"//' | sort | uniq -c | sort -rn
```
