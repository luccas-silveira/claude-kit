#!/bin/bash
# Statusline: modelo · effort   barra de contexto   tempo   prompts
# Números em destaque, rótulos e unidades apagados. Barra em braille com
# gradiente truecolor (verde → amarelo → vermelho) por posição na escala.

input=$(cat)

# Um jq só pros campos do payload. Lido linha a linha porque campos vazios
# (effort ausente, por ex.) sao linhas em branco — IFS=$'\n' as engoliria.
parsed=$(jq -r '
    (.model.display_name // "-"),
    (.effort.level // ""),
    (.context_window.used_percentage // -1 | floor | tostring),
    (.cost.total_duration_ms // 0 | tostring),
    (.transcript_path // "")
  ' <<< "$input" 2>/dev/null)

{
  IFS= read -r model
  IFS= read -r effort
  IFS= read -r ctx_pct
  IFS= read -r dur_ms
  IFS= read -r tx
} <<< "$parsed"

model="${model:--}"

DIM='\033[38;2;110;110;110m'   # rótulos, unidades, separadores
FG='\033[97m'                  # números e nome do modelo
OFF='\033[0m'

# Terminal sem truecolor cai pras 3 cores ANSI de sempre.
TRUECOLOR=0
case "${COLORTERM:-}" in truecolor|24bit) TRUECOLOR=1 ;; esac
[ "$TRUECOLOR" = 0 ] && { DIM='\033[90m'; FG='\033[1m'; }

# Cor do gradiente num ponto 0-100: verde -> amarelo na primeira metade,
# amarelo -> vermelho na segunda. Grava em $GRAD. Aritmetica inteira e sem
# subshell — a barra chama isso 10x por render.
GRAD=''
grad() {
  local p=$1 r g b u
  if [ "$p" -lt 50 ]; then
    r=$(( 46  + (241 - 46)  * p / 50 ))
    g=$(( 204 + (196 - 204) * p / 50 ))
    b=$(( 113 + (15  - 113) * p / 50 ))
  else
    u=$(( p - 50 ))
    r=$(( 241 + (231 - 241) * u / 50 ))
    g=$(( 196 + (76  - 196) * u / 50 ))
    b=$(( 15  + (60  - 15)  * u / 50 ))
  fi
  GRAD="\\033[38;2;${r};${g};${b}m"
}

EMPTY='\033[38;2;58;58;58m'
[ "$TRUECOLOR" = 0 ] && EMPTY='\033[90m'

# Barra braille de 10 posicoes. Trunca (so 100% enche tudo), mas 1% ja
# acende um ponto pra nunca parecer sessao zerada quando nao esta.
ctx=""
if [ "${ctx_pct:--1}" -ge 0 ] 2>/dev/null; then
  filled=$(( ctx_pct / 10 ))
  [ "$ctx_pct" -gt 0 ] && [ "$filled" -eq 0 ] && filled=1
  [ "$filled" -gt 10 ] && filled=10

  bar=""
  for ((i=0; i<10; i++)); do
    if [ "$i" -lt "$filled" ]; then
      if [ "$TRUECOLOR" = 1 ]; then grad $(( i * 10 + 5 )); bar="${bar}${GRAD}⣿"
      else bar="${bar}⣿"; fi
    else
      bar="${bar}${EMPTY}⣀"
    fi
  done

  if [ "$TRUECOLOR" = 1 ]; then grad "$ctx_pct"; pct_color="$GRAD"
  elif [ "$ctx_pct" -ge 85 ]; then pct_color='\033[31m'
  elif [ "$ctx_pct" -ge 60 ]; then pct_color='\033[33m'
  else pct_color='\033[32m'; fi

  [ "$TRUECOLOR" = 0 ] && bar="${pct_color}${bar}"
  ctx="${bar}${OFF} ${pct_color}${ctx_pct}${OFF}${DIM}%${OFF}"
fi

# ms -> 1h05m / 12m5s / 45s, com a unidade apagada e o numero em destaque.
dur=""
if [ "${dur_ms:-0}" -gt 0 ] 2>/dev/null; then
  dur=$(awk -v ms="$dur_ms" -v f="$FG" -v d="$DIM" -v o="$OFF" 'BEGIN{
    s=int(ms/1000); if(s<=0) exit
    h=int(s/3600); m=int((s%3600)/60); sec=s%60
    if(h>0)      printf "%s%d%s%sh%s %s%02d%s%sm%s", f,h,o,d,o, f,m,o,d,o
    else if(m>0) printf "%s%d%s%sm%s %s%d%s%ss%s", f,m,o,d,o, f,sec,o,d,o
    else         printf "%s%d%s%ss%s", f,sec,o,d,o
  }')
fi

# Prompts que EU mandei: entradas user do transcript, fora tool_results,
# meta e comandos locais (/clear, /model...) que também entram como user.
prompts=""
if [ -n "$tx" ] && [ -f "$tx" ]; then
  n=$(jq -r '
    select(.type=="user" and (.isMeta != true))
    | (if (.message.content|type)=="string" then .message.content
       elif ([.message.content[]?.type] | index("tool_result")) then empty
       else (.message.content[0].text // "") end)
    | select(startswith("<command-") or startswith("<local-command") | not)
    | 1' "$tx" 2>/dev/null | wc -l | tr -d ' ')
  [ "${n:-0}" -gt 0 ] && prompts="${FG}${n}${OFF}${DIM} msgs${OFF}"
fi

# Requests da sessao. Acima de 50 cada um rele o historico inteiro e o custo
# por request dispara — cortar a sessao ai vale ate 39% do relido (ticket 006).
reqs=""
if [ -n "$tx" ] && [ -f "$tx" ]; then
  r=$(jq -r 'select(.type=="assistant" and (.isSidechain != true)) | .requestId // empty' "$tx" 2>/dev/null | sort -u | wc -l | tr -d ' ')
  if [ "${r:-0}" -gt 0 ]; then
    if [ "$r" -gt 50 ]; then rc='\033[38;2;231;76;60m'; [ "$TRUECOLOR" = 0 ] && rc='\033[31m'
    else rc="$FG"; fi
    reqs="${rc}${r}${OFF}${DIM} reqs${OFF}"
  fi
fi

# Monta so o que tem valor. Espaco duplo separa, sem barra vertical.
out="${FG}${model}${OFF}"
[ -n "$effort" ] && out="${out} ${DIM}ᐧ${OFF} ${DIM}${effort}${OFF}"
for part in "$ctx" "$dur" "$prompts" "$reqs"; do
  [ -n "$part" ] && out="${out}   ${part}"
done

printf '%b' "$out"
