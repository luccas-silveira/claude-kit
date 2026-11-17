---
name: what-have-I-done
description: Lista tudo que foi feito num dia nas sessões do Claude Code, agrupado por projeto, só com as tarefas. Lê todas as sessões com interação na data (padrão hoje), resume em lotes com subagentes e junta por projeto. Também pelo comando `/whid`. Use quando pedirem "resumo do dia", "o que foi feito hoje", "lista do dia", "tudo que fiz hoje", "resumo de ontem" ou equivalente, e para a rotina diária.
---

# Resumo do dia

Entrega uma lista por projeto com as tarefas feitas na data, sem referência a sessão.
Não use o deja para isso: ele casa texto, não data, e deixa de fora sessões do dia.

Data padrão: hoje (fuso America/Sao_Paulo). Se o pedido trouxer outra data, use essa.

## Passos

1. Gere os digests. Rode no shell, substituindo a data:

   ```
   python3 ~/.claude/skills/what-have-I-done/scripts/digest.py YYYY-MM-DD /tmp/resumo-YYYY-MM-DD
   ```

   O script pega todo `.jsonl` de `~/.claude/projects` (fora as pastas `subagents`, que
   pertencem à sessão pai) com mensagem do dono na data, e escreve um `.txt` por sessão,
   `INDEX.tsv` (projeto, tamanho, contagens) e `batch_N.txt` com lotes de ~100 KB.

2. Leia `INDEX.tsv` para ter o número de sessões e os projetos. Não leia os digests aqui.

3. Resuma os lotes com subagentes `general-purpose`, um por lote, todos em paralelo numa
   só mensagem. Cada brief precisa conter:
   - o caminho de `batch_N.txt` e a instrução de ler cada arquivo listado com Read;
   - o formato das linhas: `[HH:MM] USER:` é pedido do dono, `ASST:` é resposta do
     assistente, `TOOL:` é comando que muda estado (commit, deploy, SQL, API);
   - a saída: agrupada por projeto (o nome vem do cabeçalho de cada digest), uma linha por
     tarefa distinta, com horário, o que foi pedido, o que foi feito de concreto (arquivo,
     commit, deploy, teste com contagem, workflow ou dado alterado, mensagem enviada a
     alguém, número) e o resultado (concluído, falhou, pendente);
   - a regra: não invente; "não consta" quando o digest não disser; apontar quando um
     digest está cortado no meio de uma resposta; sem id de sessão na saída; sem
     introdução nem conclusão.

   Lote com um só arquivo grande é normal. Não divida um arquivo em partes.

4. Junte os retornos por projeto. Une tarefas repetidas, mantém pendências, e põe no fim
   qualquer coisa que exija decisão ou atenção do dono: mensagem enviada a cliente sem
   aprovação visível, chave ou segredo colado no chat, risco de dado, prazo.

5. Entregue no chat e grave em `~/Desktop/Resumos/resumo-YYYY-MM-DD.md`.

## Formato da entrega

Lista por projeto, sem id de sessão. Cada projeto é um título curto seguido de tarefas em
bullet. Pendências entram como bullet próprio, com a palavra "Pendente:". Nada de
cabeçalho de seção além dos projetos, nada de tabela.

## Ressalvas que valem sempre

- Os digests cortam linhas em 350, 220 e 200 caracteres. Uma resposta cortada vira
  "resultado não consta", não palpite.
- Sessão que só tem pedido de revisão de segurança, sem resposta, entra como "revisão
  pedida, sem resposta registrada". Não conte como feita.
- Afirmação do assistente ("deu certo", "fechei") é relatada como afirmação, a menos que
  haja verificação no digest.
- Sessões com zero mensagens do dono no dia não aparecem. O script já as descarta.
- Se o script achar sessões que não estavam no índice de uma execução anterior, isso não
  é erro: o índice do deja não é a fonte. A fonte é o arquivo `.jsonl`.

## Rotina diária

A skill roda sob pedido. Para rodar sozinha todo dia, use a skill `schedule` e aponte para
este fluxo. Sem agendamento, rode quando pedirem.
