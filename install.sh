#!/usr/bin/env bash
# Instala o setup de Claude Code do luccassilveira numa máquina nova.
# Uso:  ./install.sh          (ou)  bash <(curl -sL <raw-url-deste-arquivo>)
set -euo pipefail

REPO="${ZOI_KIT_REPO:-luccassilveira/claude-kit}"   # troque se o repo tiver outro nome

say() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }

command -v claude >/dev/null || { echo "Claude Code não encontrado no PATH."; exit 1; }

say "Adicionando marketplaces"
# ponytail: sempre reinvoca em toda resposta; claude-video: skill /watch; thedotmack: claude-mem
for m in "$REPO" DietrichGebert/ponytail bradautomates/claude-video thedotmack/claude-mem pbakaus/impeccable; do
  claude plugin marketplace add "$m" || echo "  (já existe ou falhou: $m)"
done

say "Instalando plugins de terceiros"
for p in \
  superpowers@claude-plugins-official \
  playwright@claude-plugins-official \
  code-review@claude-plugins-official \
  security-guidance@claude-plugins-official \
  pyright-lsp@claude-plugins-official \
  typescript-lsp@claude-plugins-official \
  ponytail@ponytail \
  claude-mem@thedotmack \
  watch@claude-video
do
  claude plugin install "$p" || echo "  (falhou: $p)"
done

say "Instalando as skills próprias"
claude plugin install zoi-skills@zoi-kit

say "MCP servers"
cat <<'EOF'
  Não instalados automaticamente (precisam de binário/credencial local):
    gitnexus   — indexação de repo em grafo
    ghraphnizer / codegraph — idem
  Configure em ~/.claude.json -> mcpServers, ou rode `claude mcp add`.
EOF

say "Pronto. Reinicie o Claude Code."
