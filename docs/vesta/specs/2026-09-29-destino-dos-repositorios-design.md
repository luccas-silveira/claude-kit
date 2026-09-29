# Destino dos repositórios no kit

Data: 2026-09-29. Contexto: [ADR-0021](~/Code/claude-tooling/docs/decisions/0021-claudekit-e-o-produto.md).

## Resultado

Quem instala o kit recebe cada repositório de apoio em `~/Code/<nome>`, não nas pastas pessoais
da origem (`~/Desktop/ZOI/Projetos_ZOI/automaster_v2`, `~/Documents/2. ZOI/ghl-docs`). Na
máquina de origem nada se move. Sucesso: no kit publicado não sobra nenhum desses dois caminhos
antigos, e o plugin `automaster` instalado numa máquina limpa aponta para a pasta que o
instalador clonou.

## Abordagem (aprovada)

A troca acontece na publicação. O instalador não muda.

`fontes.json` ganha um campo opcional `destino` por repositório, no mesmo formato de
`caminho` (`~/Code/automaster`). Sem `destino`, vale `caminho`.

Ao montar o kit, o `sync` troca cada caminho de origem pelo destino, em tudo o que escreve:
arquivos do espelho (`settings.json` e demais), links simbólicos que apontam para o repositório,
`mcp.json` e `manifesto.json` (repositórios e marketplaces). A troca roda antes da troca de home
por `__HOME__`. O manifesto passa a listar o destino como `caminho`; o instalador já clona no
`caminho` do manifesto.

## Componentes

1. Leitura do `destino` em `sync` e montagem do mapa origem→destino (junto de `repos`).
2. Aplicação do mapa em `espelhar` (texto e link simbólico) e em `escrever_json`.
3. `fontes.json`: `destino` para `automaster` (`~/Code/automaster`) e `ghl-docs`
   (`~/Code/ghl-docs`).

## Erros e limites

Caminho de origem que é prefixo de outro (`~/Code/vesta` e `~/Code/vesta-interface`): a troca
casa por caminho inteiro, para não estragar o vizinho.

`destino` igual ao `caminho`, ou ausente: sem troca.

Os repositórios que já ficam em `~/Code` (`vesta`, `whatsapp-mcp`) e o `claude-code-otel`
(`~/claude-code-otel`) não ganham destino: fora de escopo.

Efeito aceito: o kit publicado deixa de refletir o caminho real da origem. Rodar `install` na
própria origem criaria clones novos em `~/Code`; a origem não roda `install`.

## Testes

1. Um caminho de origem com `destino` sai trocado no `settings.json`, no `mcp.json` e no
   manifesto, e não sobra o caminho antigo em lugar nenhum do kit.
2. Prefixo: `~/Code/vesta` com destino não altera `~/Code/vesta-interface`.
3. Sem `destino`: saída idêntica à de hoje.
4. Kit real: `test_espelho_real` passa a exigir que os caminhos `ZOI` antigos não apareçam.
