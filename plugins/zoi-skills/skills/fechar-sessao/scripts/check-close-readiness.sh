#!/usr/bin/env bash
# Reporta o que falta pra fechar a sessão (AgentStudio). Read-only, não altera nada.
# Uso: bash .claude/skills/fechar-sessao/scripts/check-close-readiness.sh
set -uo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }

echo "== Fechamento de sessão — checklist =="

# 1. Gates — não dá pra saber se rodaram; lembrete.
echo "[1] Gates"
warn "rode: cd zoi-agent && make fmt && make lint && make typecheck && make test-unit"

# 2. Git: uncommitted (ignorando PII) + unpushed
echo "[2] Git"
dirty=$(git status --porcelain | grep -vE 'Nick Multimarcas\.svg|noxcar-estoque\.json|-estoque\.json|\.gitignore$' || true)
if [ -n "$dirty" ]; then warn "mudanças não commitadas:"; echo "$dirty" | sed 's/^/      /'
else ok "working tree limpo (PII/.gitignore ignorados)"; fi
branch=$(git branch --show-current)
unpushed=$(git log "origin/$branch..HEAD" --oneline 2>/dev/null || echo "?")
if [ -n "$unpushed" ] && [ "$unpushed" != "?" ]; then warn "commits não enviados em $branch:"; echo "$unpushed" | sed 's/^/      /'
elif [ "$unpushed" = "?" ]; then warn "branch $branch sem upstream — push -u origin $branch"
else ok "$branch sincronizado com origin"; fi
[ "$branch" = "master" ] && warn "você está em master — NÃO force-push"

# 3. Deploy: git HEAD != VPS (rsync). Só lembrete se zoi_agent mudou.
echo "[3] Deploy (prod = rsync, git HEAD != VPS)"
if git diff --name-only "origin/$branch..HEAD" 2>/dev/null | grep -q '^zoi-agent/zoi_agent/'; then
  warn "código de runtime mudou — deploy + health 200 + registrar no HANDOFF o que ficou deployado"
else ok "sem mudança em zoi_agent/ vs origin (provável sem deploy)"; fi

# 4. HANDOFF freshness: HEAD mais novo que o último commit que tocou HANDOFF.md?
echo "[4] HANDOFF.md"
head_ts=$(git log -1 --format=%ct HEAD)
hand_ts=$(git log -1 --format=%ct -- HANDOFF.md 2>/dev/null || echo 0)
if [ "$head_ts" -gt "$hand_ts" ]; then warn "HANDOFF.md desatualizado — prepend bloco '# 🏁 SESSÃO <data>'"
else ok "HANDOFF.md atualizado com o trabalho recente"; fi
sz=$(wc -c < HANDOFF.md 2>/dev/null || echo 0); sessions=$(grep -c '^# 🏁' HANDOFF.md 2>/dev/null || echo 0)
[ "$sz" -gt 153600 ] && warn "HANDOFF grande (${sz}B, ${sessions} sessões) — podar antigas p/ docs/claude/estado.md"

# 5/6. graphify freshness: grafo mais velho que o último commit de código?
echo "[5/6] ROADMAP + graphify-out"
warn "ROADMAP.md: reflita milestones/followups fechados ou abertos hoje"
if [ -f graphify-out/manifest.json ]; then
  graph_ts=$(stat -f %m graphify-out/manifest.json 2>/dev/null || stat -c %Y graphify-out/manifest.json 2>/dev/null || echo 0)
  code_ts=$(git log -1 --format=%ct -- zoi-agent/zoi_agent 2>/dev/null || echo 0)
  if [ "$code_ts" -gt "$graph_ts" ]; then warn "graphify-out mais velho que o último commit de código — regenere se a estrutura mudou (skill graphify)"
  else ok "graphify-out mais novo que o código"; fi
else warn "sem graphify-out/ — gere com a skill graphify se for útil"; fi

# 7. Memória
echo "[7] Memória"
warn "registre learnings: zoi-agent/MEMORY.md + ~/.claude/memory/ (tópicos relevantes)"

echo "== fim =="
