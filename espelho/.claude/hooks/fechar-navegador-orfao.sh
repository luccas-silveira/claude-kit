#!/bin/sh
# Fecha o Chrome sem janela do Playwright que ficou órfão (pai morreu, adotado pelo launchd).
# Não toca no Chrome pessoal nem no navegador-login, que roda com janela.
ps -axo pid=,ppid=,command= | awk '$2 == 1 && /claude-navegador/ && /--headless/ {print $1}' | xargs kill 2>/dev/null
exit 0
