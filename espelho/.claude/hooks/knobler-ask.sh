#!/bin/bash
# Hook PreToolUse do Claude Code: intercepta AskUserQuestion e manda a
# pergunta pro card do Knobler. Respondida lá → devolve ao Claude via
# allow + updatedInput.answers (fluxo oficial: a tool completa sem prompt
# e sem renderizar "Error:" — deny+reason voltava como erro da tool).
# Knobler fechado, ✕ no card ou timeout → sai sem output e a pergunta
# aparece no terminal como sempre. Nunca falha a sessão: exit 0 em tudo.
set -uo pipefail
PORT="${KNOBLER_PORT:-4477}"
INPUT="$(cat)"
python3 "$HOME/.claude/skills/vesta/scripts/vesta.py" aberto "$(printf '%s' "$INPUT" | jq -r '.cwd // ""')" && exit 0
ID="ask-$$-$(date +%s)"

# source = pasta do projeto da sessão (basename do cwd) — identifica no card
# QUEM está perguntando quando há várias sessões abertas
PAYLOAD="$(printf '%s' "$INPUT" | jq -c --arg id "$ID" \
    '{id: $id, source: ((.cwd // "") | split("/") | last), questions: .tool_input.questions}')" || exit 0

# Knobler fora do ar → curl falha em ms → fluxo normal do terminal
curl -sf -m 1 -X POST "localhost:$PORT/ask" -d "$PAYLOAD" >/dev/null 2>&1 || exit 0

DEADLINE=$(( $(date +%s) + 570 ))  # < timeout de 600s do hook, folga pro cancel
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
    # long-poll: o app segura o GET até a resposta (teto 25 s, nunca além do
    # DEADLINE); app antigo ignora o header e responde na hora
    WAIT=$(( DEADLINE - $(date +%s) )); [ "$WAIT" -gt 25 ] && WAIT=25; [ "$WAIT" -ge 1 ] || WAIT=1
    STATE="$(curl -sf -m $((WAIT + 5)) -H "X-Knobler-Wait: $WAIT" "localhost:$PORT/ask/$ID" 2>/dev/null)"
    RC=$?
    if [ "$RC" -eq 28 ]; then
        # timeout do curl conta o tempo do Mac dormindo e o prazo do app não:
        # uma leitura sem espera separa "card ainda pendente" de "app travado"
        STATE="$(curl -sf -m 2 "localhost:$PORT/ask/$ID" 2>/dev/null)" || exit 0
    elif [ "$RC" -ne 0 ]; then
        exit 0
    fi
    if [ "$(printf '%s' "$STATE" | jq -r '.cancelled // false')" = "true" ]; then
        exit 0  # ✕ no card → pergunta vai pro terminal
    fi
    if [ "$(printf '%s' "$STATE" | jq -r '.answered // false')" = "true" ]; then
        # updatedInput substitui o input INTEIRO: ecoa questions original e
        # preenche answers {"<pergunta>": "<label(s)|texto>"} — texto vence
        QUESTIONS="$(printf '%s' "$INPUT" | jq -c '.tool_input.questions')" || exit 0
        printf '%s' "$STATE" | jq -c --argjson questions "$QUESTIONS" '{
            hookSpecificOutput: {
                hookEventName: "PreToolUse",
                permissionDecision: "allow",
                updatedInput: {
                    questions: $questions,
                    answers: (.answers | with_entries(.value = (
                        if (.value.text // "") != "" then .value.text
                        else ((.value.labels // []) | join(", "))
                        end
                    )))
                }
            }
        }'
        exit 0
    fi
    sleep 0.3
done
# timeout: remove o card órfão e devolve ao terminal
curl -sf -m 1 -X POST "localhost:$PORT/ask/$ID/cancel" >/dev/null 2>&1 || true
exit 0
