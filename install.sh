#!/usr/bin/env bash
# Instala o setup de Claude Code do luccassilveira numa máquina nova. Idempotente.
# Uso:  git clone https://github.com/luccas-silveira/claude-kit && bash claude-kit/install.sh
set -euo pipefail

REPO="${ZOI_KIT_REPO:-luccas-silveira/claude-kit}"   # troque se o repo tiver outro nome
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
C="$HOME/.claude"

say() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }

command -v claude >/dev/null || { echo "Claude Code não encontrado no PATH."; exit 1; }

say "Adicionando marketplaces"
for m in "$REPO" DietrichGebert/ponytail bradautomates/claude-video pbakaus/impeccable \
         JuliusBrussee/caveman headroomlabs-ai/headroom; do
  claude plugin marketplace add "$m" || echo "  (já existe ou falhou: $m)"
done

say "Instalando plugins"
for p in \
  superpowers@claude-plugins-official \
  playwright@claude-plugins-official \
  security-guidance@claude-plugins-official \
  ponytail@ponytail \
  watch@claude-video \
  impeccable@impeccable \
  caveman@caveman \
  headroom@headroom-marketplace \
  zoi-skills@zoi-kit
do
  claude plugin install "$p" || echo "  (falhou: $p)"
done

say "Skills de terceiros, direto da fonte"
if command -v npx >/dev/null; then
  npx -y skills add tt-a1i/archify -g -a claude-code -y || echo "  (falhou: archify)"
  npx -y skills add mattpocock/skills -s grill-me -s wayfinder -g -a claude-code -y || echo "  (falhou: mattpocock/skills)"
else
  echo "  npx ausente: archify, grill-me e wayfinder ficaram de fora."
fi

say "Vesta, output style Seco e hooks"
mkdir -p "$C/skills" "$C/commands" "$C/output-styles"
rm -rf "$C/skills/vesta" && cp -R "$KIT/home/skills/vesta" "$C/skills/vesta"
cp "$KIT"/home/commands/*.md "$C/commands/"
cp "$KIT"/home/output-styles/*.md "$C/output-styles/"
# funde os hooks do kit em settings.json sem duplicar e sem apagar o que já existe
python3 - "$C/settings.json" "$KIT/home/hooks.json" <<'PY'
import json, sys, pathlib
dest, novos = pathlib.Path(sys.argv[1]), json.loads(pathlib.Path(sys.argv[2]).read_text())
s = json.loads(dest.read_text()) if dest.exists() else {}
hooks = s.setdefault('hooks', {})
for evento, grupos in novos.items():
    atuais = hooks.setdefault(evento, [])
    existentes = {h.get('command') for g in atuais for h in g.get('hooks', [])}
    atuais += [g for g in grupos if g['hooks'][0]['command'] not in existentes]
s.setdefault('outputStyle', 'Seco')
dest.write_text(json.dumps(s, indent=2, ensure_ascii=False) + '\n')
PY
# o Seco governa a fala; o caveman fica só com subagentes e skills
mkdir -p "$HOME/.config/caveman"
[ -f "$HOME/.config/caveman/config.json" ] || echo '{ "defaultMode": "off" }' > "$HOME/.config/caveman/config.json"

say "Falta fazer à mão"
cat <<'EOF'
  headroom precisa do CLI:        uv tool install headroom-ai
  deja e graft instalam as próprias skills e hooks quando o CLI deles é instalado.
  MCP servers ficam fora (binário ou credencial local).
EOF

say "Pronto. Reinicie o Claude Code."
