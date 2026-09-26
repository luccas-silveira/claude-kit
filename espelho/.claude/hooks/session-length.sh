#!/bin/bash
# UserPromptSubmit: avisa uma vez por sessão quando ela passa de LIMITE requests.
# Acima disso cada request relê o histórico inteiro — cortar a sessão a cada 50
# vale até 39% do contexto relido do baseline (ticket 006).
# Silencioso custa 0 tokens; o aviso custa 49, medido.
LIMITE=50

input=$(cat)
sid=$(jq -r '.session_id // ""' <<< "$input" 2>/dev/null)
tx=$(jq -r '.transcript_path // ""' <<< "$input" 2>/dev/null)
[ -f "$tx" ] || exit 0   # sessão nova: o transcript só existe a partir do 2o prompt

marca="/tmp/claude-sessao-longa-${sid}"
[ -f "$marca" ] && exit 0

n=$(jq -r 'select(.type=="assistant" and (.isSidechain != true)) | .requestId // empty' "$tx" 2>/dev/null | sort -u | wc -l | tr -d ' ')
[ "${n:-0}" -le "$LIMITE" ] && exit 0

touch "$marca"
echo "Esta sessão passou de $n requests. Daqui pra frente cada chamada relê o histórico inteiro. Se a próxima tarefa não depende do que já foi feito, /clear antes."
