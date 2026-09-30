#!/bin/bash
# Statusline em duas linhas, no laranja do painel da Vesta (#ff4d00):
#   1: cápsulas — modelo · esforço, projeto e branch, Vesta (link pro painel), graft;
#      e o nome da sessão
#   2: contexto, limites de 5h e da semana, linhas +/−, duração, mensagens
# Ícones da Symbols Nerd Font, que o Supacode (Ghostty) já traz. O bash do macOS é
# 3.2, sem $'\u…': os glifos estão literais no arquivo.

input=$(cat)
export LC_ALL=en_US.UTF-8   # ${#var} e ${var:0:n} contam caracteres, não bytes

# Um jq só pros campos do payload. Lido linha a linha porque campos vazios
# (effort ausente, por ex.) são linhas em branco — IFS=$'\n' as engoliria.
parsed=$(jq -r '
    (.model.display_name // "-"), (.effort.level // ""), (.session_name // ""),
    (.workspace.current_dir // .cwd // ""), (.workspace.project_dir // .cwd // ""),
    (.workspace.repo.name // ""),
    (.context_window.used_percentage // -1 | floor | tostring),
    (.rate_limits.five_hour.used_percentage // -1 | floor | tostring),
    (.rate_limits.five_hour.resets_at // 0 | tostring),
    (.rate_limits.seven_day.used_percentage // -1 | floor | tostring),
    (.rate_limits.seven_day.resets_at // 0 | tostring),
    (.cost.total_lines_added // 0 | tostring), (.cost.total_lines_removed // 0 | tostring),
    (.cost.total_duration_ms // 0 | tostring), (.transcript_path // "")
  ' <<< "$input" 2>/dev/null)

{
  IFS= read -r model;   IFS= read -r effort;  IFS= read -r sname
  IFS= read -r cwd;     IFS= read -r proj;    IFS= read -r repo
  IFS= read -r ctx_pct
  IFS= read -r h5_pct;  IFS= read -r h5_at;   IFS= read -r d7_pct; IFS= read -r d7_at
  IFS= read -r l_add;   IFS= read -r l_rm;    IFS= read -r dur_ms; IFS= read -r tx
} <<< "$parsed"
model="${model:--}"

# Cores do painel: um laranja, os cinzas e o âmbar de aviso. Terminal sem
# truecolor cai pros vizinhos na paleta de 256.
case "${COLORTERM:-}" in
  truecolor|24bit)
    OR='\033[38;2;255;77;0m';   OR_BG='\033[48;2;255;77;0m'
    AMB='\033[38;2;242;181;60m'; AMB_BG='\033[48;2;242;181;60m'
    INK='\033[38;2;15;15;15m';  T1='\033[38;2;232;232;232m'
    T3='\033[38;2;116;116;116m'; LINE='\033[38;2;51;51;51m' ;;
  *)
    OR='\033[38;5;202m'; OR_BG='\033[48;5;202m'; AMB='\033[38;5;214m'; AMB_BG='\033[48;5;214m'
    INK='\033[38;5;233m'; T1='\033[38;5;254m'; T3='\033[38;5;243m'; LINE='\033[38;5;236m' ;;
esac
OFF='\033[0m'; B1='\033[1m'; B0='\033[22m'; ITAL='\033[3m'

I_MODEL='󰚩' I_REPO='' I_BRANCH='' I_FIRE='󰈸' I_GRAFT=''
I_CHAT='' I_CTX='' I_5H='' I_WEEK='' I_CLOCK='' I_MSGS=''
CAP_L='' CAP_R=''

# Cápsula: $1 cor da borda (como frente), $2 fundo, $3 texto. Anexa em $L1.
L1=""
pill() {
  L1="${L1:+${L1} }${1}${CAP_L}${2}${INK}${3}${OFF}${1}${CAP_R}${OFF}"
}

# ── linha 1 ────────────────────────────────────────────────────────────────

pill "$OR" "$OR_BG" "${I_MODEL} ${B1}${model}${B0}${effort:+ · ${effort}}"

root=""
[ -n "$cwd" ] && [ -d "$cwd" ] && root=$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null)
base="${root:-$proj}"

# Projeto e branch; o ponto marca alteração não commitada.
if [ -n "$root" ]; then
  t="${I_REPO} ${repo:-$(basename "$root")}"
  branch=$(git -C "$root" --no-optional-locks symbolic-ref --short HEAD 2>/dev/null \
        || git -C "$root" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
  [ -n "$branch" ] && t="${t}  ${I_BRANCH} ${branch}"
  [ -n "$(git -C "$root" --no-optional-locks status --porcelain 2>/dev/null | head -1)" ] && t="${t} ${B1}●${B0}"
  pill "$OR" "$OR_BG" "$t"
elif [ -n "$proj" ]; then
  pill "$OR" "$OR_BG" "${I_REPO} $(basename "$proj")"
fi

# Vesta: aparece em projeto que tem Vesta, e a cápsula é link pro painel.
if [ -n "$base" ] && { [ -d "$base/docs/vesta" ] || [ -d "$base/.claude/vesta" ]; }; then
  vk=""; vt=""
  est="$base/.claude/vesta/estado.json"
  if [ -f "$est" ]; then
    v=$(jq -r '
      (.etapas | length) as $k | [.etapas[].status] as $s
      | ($s | index("pendente")) as $p | ($s | index("travada")) as $t
      | if .espera == "plano" then "plano|‖ plano p/ aprovar"
        elif .espera == "interrompida" then "pausa|‖ pausada \((($p // ($k - 1)) + 1))/\($k)"
        elif $t != null then "trava|⚠ travada \($t + 1)/\($k)"
        elif $p == null then "fim|✓ concluída"
        else "etapa|etapa \($p + 1)/\($k)" end' "$est" 2>/dev/null)
    [ -n "$v" ] && { vk=${v%%|*}; vt=${v#*|}; }
  fi
  # Sem execução em curso, a fase vem da sessão: o último arquivo de fase que ela
  # leu depois de invocar a Vesta.
  # ponytail: grep no transcript, não o parser do painel; menção solta ao caminho
  # num comando também conta. Trocar pelo painel se isso enganar.
  if { [ -z "$vk" ] || [ "$vk" = fim ]; } && [ -f "$tx" ] \
     && grep -q '"input":{"skill":"vesta"' "$tx" 2>/dev/null; then
    ph=$(grep -oE '"(file_path|command)":"[^"]*(skills/vesta|vesta/skill)/(spec|research|grill|mockup|plano|execucao)\.md' "$tx" \
        | tail -1 | grep -oE '(spec|research|grill|mockup|plano|execucao)\.md$')
    case "$ph" in
      spec.md) vt=spec ;; research.md) vt=pesquisa ;; grill.md) vt=grill ;;
      mockup.md) vt=mockup ;; plano.md) vt=plano ;; execucao.md) vt=execução ;; *) vt=ativação ;;
    esac
  fi
  url="http://localhost:${VESTA_PORTA:-4700}/?projeto=$(jq -rn --arg p "$base" '$p|@uri')"
  pill "$OR" "$OR_BG" "\033]8;;${url}\033\\\\${I_FIRE} ${B1}vesta${B0}${vt:+ ▸ ${vt}}\033]8;;\033\\\\"
fi

# Graft: estado do índice, lido do cache que os hooks dele mantêm. Âmbar quando
# há arquivo fora do índice.
gs="$base/graft/.cache/stats.json"
if [ -n "$base" ] && [ -f "$gs" ]; then
  g=$(jq -r 'if .syncing then "↻" elif .dirty then (if (.staleCount // 0) > 0 then "⚠ \(.staleCount)" else "⚠" end) else "✓" end' "$gs" 2>/dev/null)
  case "$g" in
    ✓) pill "$OR" "$OR_BG" "${I_GRAFT} graft ✓" ;;
    ?*) pill "$AMB" "$AMB_BG" "${I_GRAFT} graft ${g}" ;;
  esac
fi

if [ -n "$sname" ]; then
  [ "${#sname}" -gt 40 ] && sname="${sname:0:39}…"
  L1="${L1} ${T3}${ITAL}${I_CHAT} ${sname}${OFF}"
fi

# ── linha 2 ────────────────────────────────────────────────────────────────

# Medidor: ícone, rótulo, barra-cápsula de 6 células e o número, que acende em
# laranja a partir de 85%. Trunca (só 100% enche tudo), mas 1% já acende uma
# célula pra nunca parecer zerado quando não está.
meter() {
  local pct=$3 cells=6 fil i on off out="" num="$T1"
  fil=$(( pct * cells / 100 ))
  [ "$pct" -gt 0 ] && [ "$fil" -eq 0 ] && fil=1
  [ "$fil" -gt "$cells" ] && fil=$cells
  for ((i=0; i<cells; i++)); do
    if   [ "$i" -eq 0 ];             then on='' off=''
    elif [ "$i" -eq $((cells - 1)) ]; then on='' off=''
    else                                  on='' off=''; fi
    if [ "$i" -lt "$fil" ]; then out="${out}${OR}${on}"; else out="${out}${LINE}${off}"; fi
  done
  [ "$pct" -ge 85 ] && num="$OR"
  out="${T3}$1 $2${OFF} ${out}${OFF} ${num}${B1}${pct}${OFF}${T3}%${OFF}"
  [ -n "$4" ] && out="${out} ${T3}↻ $4${OFF}"
  printf '%s' "$out"
}

# Segundos até o reset em 2d14h / 3h12 / 45m.
until_reset() {
  local s=$(( $1 - $(date +%s) ))
  [ "$1" -gt 0 ] && [ "$s" -gt 0 ] || return
  if   [ "$s" -ge 86400 ]; then printf '%s' "$(( s / 86400 ))d$(( s % 86400 / 3600 ))h"
  elif [ "$s" -ge 3600 ];  then printf '%s' "$(( s / 3600 ))h$(printf %02d $(( s % 3600 / 60 )))"
  else                          printf '%s' "$(( s / 60 ))m"; fi
}

parts=()
[ "$ctx_pct" -ge 0 ] 2>/dev/null && parts+=("$(meter "$I_CTX" ctx "$ctx_pct")")
[ "$h5_pct" -ge 0 ] 2>/dev/null && parts+=("$(meter "$I_5H" 5h "$h5_pct" "$(until_reset "$h5_at")")")
[ "$d7_pct" -ge 0 ] 2>/dev/null && parts+=("$(meter "$I_WEEK" sem "$d7_pct" "$(until_reset "$d7_at")")")

if [ "${l_add:-0}" -gt 0 ] || [ "${l_rm:-0}" -gt 0 ]; then
  parts+=("${T1}${B1}+${l_add}${OFF} ${T3}−${l_rm}${OFF}")
fi

# ms → 1h05m / 12m05s / 45s.
if [ "${dur_ms:-0}" -gt 0 ] 2>/dev/null; then
  parts+=("${T3}${I_CLOCK}${OFF} ${T1}${B1}$(awk -v ms="$dur_ms" 'BEGIN{s=int(ms/1000); h=int(s/3600); m=int((s%3600)/60)
    if(h>0) printf "%dh%02dm",h,m; else if(m>0) printf "%dm%02ds",m,s%60; else printf "%ds",s}')${OFF}")
fi

# Prompts que EU mandei: entradas user do transcript, fora tool_results, meta e
# comandos locais (/clear, /model...) que também entram como user. O grep na
# frente poupa o jq de parsear o transcript inteiro.
if [ -n "$tx" ] && [ -f "$tx" ]; then
  n=$(grep '"type":"user"' "$tx" 2>/dev/null | jq -r '
    select(.type=="user" and (.isMeta != true))
    | (if (.message.content|type)=="string" then .message.content
       elif ([.message.content[]?.type] | index("tool_result")) then empty
       else (.message.content[0].text // "") end)
    | select(startswith("<command-") or startswith("<local-command") | not)
    | 1' 2>/dev/null | wc -l | tr -d ' ')
  [ "${n:-0}" -gt 0 ] && parts+=("${T3}${I_MSGS}${OFF} ${T1}${B1}${n}${OFF}")
fi

L2=""
for p in "${parts[@]}"; do L2="${L2:+${L2}  ${LINE}│${OFF}  }${p}"; done

printf '%b' "$L1"
[ -n "$L2" ] && printf '\n%b' "$L2"
