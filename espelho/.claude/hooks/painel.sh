#!/bin/bash
# Sobe o painel do wayfinder para o projeto da sessão. Sai calado em projeto que
# não usa wayfinder, que é a maioria.
#
# Três coisas o hook não faz, de propósito:
#   - não toca no core.hooksPath do projeto alvo, que desligaria os hooks de git dele;
#   - não copia nada por cima de um panel/ versionado, que é dono de si mesmo;
#   - não instala dependência: a cópia leva o node_modules junto, então instalar é copiar.
set -u

FONTE="$HOME/Code/claude-tooling/panel"
ESTADO="$HOME/.claude/painel"

entrada=$(cat)
projeto=$(jq -r '.cwd // ""' <<< "$entrada")
origem=$(jq -r '.source // ""' <<< "$entrada")

[ -n "$projeto" ] || exit 0
[ -d "$FONTE" ] || exit 0

# Sem tracker, o hook escreve um: o painel passa a valer em qualquer projeto, e o
# contrato de formato chega junto com ele. O como-construir vem junto porque o
# TRACKER é só o formato — sozinho ele deixa o agente montar mapa torto sem errar
# uma vírgula da sintaxe.
if [ ! -f "$projeto/docs/wayfinder/TRACKER.md" ]; then
  mkdir -p "$projeto/docs/wayfinder" || exit 0
  cp "$FONTE/../docs/wayfinder/TRACKER.md" "$projeto/docs/wayfinder/TRACKER.md" || exit 0
fi
[ -f "$projeto/docs/wayfinder/como-construir-um-mapa.md" ] ||
  cp "$FONTE/../docs/wayfinder/como-construir-um-mapa.md" "$projeto/docs/wayfinder/" 2>/dev/null

mkdir -p "$ESTADO"
slug=$(echo "$projeto" | shasum | cut -c1-12)
marca="$ESTADO/$slug.json"

# Porta estável por projeto: mesmo caminho, mesma porta, endereço que não muda
# entre sessões. A varredura resolve colisão entre dois projetos.
base=$((4700 + 0x$(echo "$projeto" | shasum | cut -c1-4) % 100))
porta=""
for tentativa in $(seq 0 99); do
  p=$(( (base - 4700 + tentativa) % 100 + 4700 ))
  if ! nc -z 127.0.0.1 "$p" 2>/dev/null; then porta=$p; break; fi
done

# panel/ versionado é dono de si: sobe e nunca é copiado por cima.
versionado=false
git -C "$projeto" ls-files --error-unmatch panel >/dev/null 2>&1 && versionado=true

# Guarda de posse: o .versao é a assinatura do hook. Um panel/ sem ela é de
# terceiro — projeto que não é repositório git, pasta ignorada, painel próprio de
# outra pessoa. O hook não apaga nem sobe o que não criou: sai calado.
if [ "$versionado" = false ] && [ -e "$projeto/panel" ] && [ ! -f "$projeto/panel/.versao" ]; then
  exit 0
fi

# A versão da fonte decide antes de tudo. A ordem importa: checar "já está de pé"
# primeiro faria a ressincronização nunca acontecer, porque o servidor não morre.
defasado=false
fonte_versao=$(git -C "$FONTE/.." rev-parse HEAD 2>/dev/null)
# Sem versão da fonte não há como comparar: copiar viraria ciclo de apagar e
# recopiar a cada sessão. Melhor não fazer nada.
[ -n "$fonte_versao" ] || exit 0
if [ "$versionado" = false ]; then
  copia_versao=$(cat "$projeto/panel/.versao" 2>/dev/null)
  [ "$fonte_versao" != "$copia_versao" ] && defasado=true
fi

vivo=false
pid_antigo=0
porta_antiga=0
if [ -f "$marca" ]; then
  pid_antigo=$(jq -r '.pid // 0' < "$marca")
  porta_antiga=$(jq -r '.porta // 0' < "$marca")
  # O pid sozinho não basta: pid é reciclado, e matar às cegas derrubaria um
  # processo alheio do usuário. Só é o nosso se ainda for um vite.
  # O caminho do binário, não a palavra solta: "vite" em qualquer lugar da linha
  # de comando casaria por acaso e mataria processo alheio.
  ps -o command= -p "$pid_antigo" 2>/dev/null | grep -qF 'node_modules/.bin/vite' && vivo=true
fi

# A abertura da aba é decidida aqui, antes de qualquer saída: decidida só no ramo
# que sobe servidor, um painel que nunca morre nunca mais abriria aba nenhuma.
abrir=""
hoje="$ESTADO/$slug.$(date +%Y-%m-%d).aberto"
[ "$origem" = "startup" ] && [ ! -f "$hoje" ] && abrir=1

# De pé e em dia: nada a fazer além de informar. É esta saída que impede um
# processo novo a cada /clear, compactação ou retomada. Marca sem porta não
# serve para informar nada: cai adiante e sobe de novo.
if [ "$vivo" = true ] && [ "$defasado" = false ] && [ "$porta_antiga" != 0 ]; then
  if [ -n "$abrir" ]; then
    open "http://localhost:$porta_antiga" >/dev/null 2>&1 && touch "$hoje"
  fi
  printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Painel deste projeto: http://localhost:%s"}}\n' "$porta_antiga"
  exit 0
fi

# De pé e defasado: derrubar antes de apagar a pasta, senão o servidor fica
# lendo código que não existe mais. Reaproveita a porta, que é estável.
if [ "$vivo" = true ]; then
  kill "$pid_antigo" 2>/dev/null
  [ "$porta_antiga" != 0 ] && porta=$porta_antiga
fi

[ -n "$porta" ] || exit 0

if [ "$defasado" = true ]; then
  rm -rf "$projeto/panel"
  # -P preserva os atalhos de node_modules/.bin; -R sozinho os segue e quebra.
  cp -RP "$FONTE" "$projeto/panel"
  echo "$fonte_versao" > "$projeto/panel/.versao"
fi

if [ "$versionado" = false ]; then
  # Só grava a exclusão quando o projeto é a raiz do repositório. Em monorepo, ou
  # projeto dentro de pasta pessoal versionada, o projeto é subdiretório de um
  # repositório maior: git -C resolve esse repositório pai, e gravar lá não exclui
  # nada (o padrão "/panel/" é ancorado na raiz e não casa um panel/ mais fundo) e
  # ainda suja um repositório que não é o alvo.
  # Comparação normalizada dos dois lados: -P resolve link simbólico (em macOS
  # /tmp é link para /private/tmp) e descarta a barra final, senão a raiz nunca
  # bate com o projeto e a exclusão simplesmente nunca é gravada.
  topo=$(git -C "$projeto" rev-parse --show-toplevel 2>/dev/null)
  if [ -n "$topo" ] && [ "$(cd -P "$topo" 2>/dev/null && pwd)" = "$(cd -P "$projeto" 2>/dev/null && pwd)" ]; then
    # Em worktree o .git é arquivo, e info/ pode não existir. Absoluto de
    # propósito: --git-path devolve caminho relativo ao repositório alvo, e o
    # cwd do hook aqui ainda é outro.
    info=$(git -C "$projeto" rev-parse --path-format=absolute --git-path info 2>/dev/null)
    if [ -n "$info" ]; then
      mkdir -p "$info" 2>/dev/null
      exclude=$(git -C "$projeto" rev-parse --path-format=absolute --git-path info/exclude)
      grep -qx "/panel/" "$exclude" 2>/dev/null || echo "/panel/" >> "$exclude"
    fi
  fi
fi

cd "$projeto/panel" || exit 0

# O vite direto, não `npm run dev`: com npm no meio, o pid guardado é o do npm,
# e derrubá-lo depois deixaria o servidor órfão.
PAINEL_RAIZ="$projeto" PAINEL_PORTA="$porta" PAINEL_ABRIR="$abrir" \
  nohup node_modules/.bin/vite > "$ESTADO/$slug.log" 2>&1 &
pid=$!
disown 2>/dev/null

# A marca do dia só depois de o processo existir: gravada antes, um servidor que
# falhasse ao subir consumiria a abertura de aba do dia.
[ -n "$abrir" ] && touch "$hoje"

# jq monta a marca: caminho com aspas ou barra invertida quebraria o JSON escrito
# à mão, e quem não relê a própria marca é o hook.
jq -n --arg projeto "$projeto" --argjson porta "$porta" --argjson pid "$pid" \
  '{projeto:$projeto,porta:$porta,pid:$pid}' > "$marca"
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Painel deste projeto: http://localhost:%s"}}\n' "$porta"
