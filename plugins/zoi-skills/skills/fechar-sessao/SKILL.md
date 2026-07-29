---
name: fechar-sessao
description: Rotina de fechamento de sessão do projeto AgentStudio — garante que a próxima sessão comece no melhor estado possível (gates, commit/push, deploy, HANDOFF, ROADMAP, graphify, memória). Use quando o usuário pedir para "fechar a sessão", "encerrar", "finalizar", "wrap up", "fazer o handoff", "vou parar por hoje", ou antes de terminar o trabalho.
---

# Fechar sessão (AgentStudio)

Checklist ordenado de fechamento. **Rode primeiro** `scripts/check-close-readiness.sh` (a partir da raiz do repo) para ver o que está pendente — ele reporta gates, commits não enviados, frescura do grafo e do HANDOFF. Depois execute os passos abaixo, pulando o que já estiver verde.

## Checklist

1. **Gates verdes** — `cd zoi-agent && make fmt && make lint && make typecheck && make test-unit`. Nunca feche com gate vermelho. (CLAUDE.md: "antes de declarar pronto".)

2. **Commit + push** — sem trabalho órfão local (risco recorrente no histórico do repo). Push para `origin`; **NUNCA force-push em `master`**. Deixe FORA os untracked com PII (`Nick Multimarcas.svg`, `noxcar-estoque.json`, qualquer `*-estoque.json` cru).

3. **Deploy + sanity** (só se mexeu em `zoi-agent/zoi_agent/`) — **prod roda por rsync, `git HEAD ≠ VPS`**. Use `zoi-agent/scripts/deploy/deploy-ghl-telegram-adapter.sh` (adapter :8200) e/ou `deploy-studio.sh` (:8300); confirme health 200 nos dois; **registre no HANDOFF o que ficou DEPLOYADO vs só commitado**. (Ruído de migration `034_routine_cutover.sql` "transaction aborted" é pré-existente e tolerado.)

4. **HANDOFF.md** ← passo mais importante. Prepend de um bloco `# 🏁 SESSÃO <data> — <título>` com: **O que foi feito** / **Validação** / **Pendências e followups**. É o primeiro doc que a próxima sessão lê (apontado pelo CLAUDE.md). Pode usar o skill `handoff` para compactar.

5. **ROADMAP.md** — atualize status de milestone e followups fechados/abertos.

6. **graphify-out/** — regenere (skill `graphify`) **só se a estrutura do código mudou materialmente** (novos módulos/funções, refactor). Tem custo (`cost.json`) e é consultado no início da sessão seguinte. Mudança trivial → pular.

7. **Memória** — registre learnings que valem persistir: `zoi-agent/MEMORY.md` (projeto) + `~/.claude/memory/` tópicos (`tools/dev-env.md`, etc.). O `claude-mem` captura observações sozinho; o índice estruturado é manual.

8. **Higiene do HANDOFF** — quando inchar (>~150 KB ou >20 sessões empilhadas), mova as sessões mais antigas para `docs/claude/estado.md`.

## Princípios (lições do projeto)

- **Não declare pronto sem evidência.** Gates verdes + (em fix de runtime do agente) **drive live + audit**. Fix por *directive* de LLM não é verificável por unit test — só o drive live + `audit_log` pega um fix inócuo.
- **Prod = rsync, não git.** Sempre diga o que está deployado, não só commitado.
- **Não commitar PII** (catálogos crus com telefone). O `catalog.yaml` tracked já é a versão limpa.
- Padrões a preservar (exemplos): `_picked_candidate` é a **fonte única de verdade** da escolha do lead; canais persistentes vivem em `PERSISTENT_UNDERSCORE_CHANNELS` (`state.py`).
