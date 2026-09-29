#!/bin/bash
# Instalador da vesta-interface: liga a skill, registra os MCPs travados e baixa o detector.
set -eu
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
REPO="$(cd "$(dirname "$0")" && pwd -P)"

ligar() {
  destino=$1 alvo=$2
  if [ -L "$destino" ]; then
    [ "$(readlink "$destino")" = "$alvo" ] && return 0
    ln -sfn "$alvo" "$destino"
  elif [ -e "$destino" ]; then
    copia="$destino.antes-da-vesta-interface-$(date +%Y%m%d%H%M%S)"
    mv "$destino" "$copia"
    echo "guardado: $(basename "$copia")"
    ln -s "$alvo" "$destino"
  else
    ln -s "$alvo" "$destino"
  fi
}

mkdir -p "$CLAUDE_HOME/skills"
ligar "$CLAUDE_HOME/skills/vesta-interface" "$REPO"

# Instalados numa pasta fixa: pelo `npx -y`, com a máquina carregada, os MCPs passavam dos 30 s
# de conexão e a sessão abria sem eles.
MCP_HOME="${VESTA_MCP_HOME:-$HOME/.local/share/vesta-interface/mcp}"
mkdir -p "$MCP_HOME"
npm install --prefix "$MCP_HOME" --no-audit --no-fund --save-exact \
  @playwright/mcp@0.0.82 chrome-devtools-mcp@1.10.1
BIN="$MCP_HOME/node_modules/.bin"

# claude mcp não expande ~: caminhos absolutos
mcp() {
  nome=$1; shift
  claude mcp remove --scope user "$nome" >/dev/null 2>&1 || true
  claude mcp add --scope user "$nome" -- "$@"
}
mcp chrome-devtools "$BIN/chrome-devtools-mcp" --headless --isolated --no-usage-statistics \
  --no-performance-crux --categoryInput=false --categoryEmulation=false \
  --categoryNetwork=false --categoryMemory=false
mcp playwright "$BIN/playwright-mcp" --headless --snapshot-mode none \
  --user-data-dir "$HOME/.cache/claude-navegador"

"$REPO/ferramentas/impeccable/detectar" --version \
  || echo "aviso: download do detector impeccable falhou; ele tenta de novo no primeiro uso"

python3 - "$(dirname "$CLAUDE_HOME")/.claude.json" <<'PY' || true
import json, sys
try:
    cj = json.load(open(sys.argv[1]))
except (OSError, ValueError):
    cj = None
if not (isinstance(cj, dict) and 'inspo' in (cj.get('mcpServers') or {})):
    print('aviso: MCP inspo não encontrado em mcpServers do .claude.json')
PY

echo "Pronto. Os MCPs e a skill carregam em sessão nova."
