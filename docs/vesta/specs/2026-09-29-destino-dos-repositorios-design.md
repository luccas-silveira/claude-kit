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
4. `README.md`: a frase "clonados no mesmo caminho da origem" passa a dizer que cada
   repositório vai para `~/Code/<nome>`.
5. `~/.claude/skills/ghl-api-docs/SKILL.md`: o texto deixa de citar `~/Documents/ghl-docs` e
   aponta para a pasta `docs` ao lado da skill (o próximo sync leva a mudança para o kit).

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
5. Consistência: o caminho do marketplace `zoi` no `settings.json` do espelho é o mesmo do
   `caminho` do repositório `automaster` no manifesto.

## Decisões do grill

- **A6** — exigido o teste que compara o caminho do marketplace no `settings.json` com o do
  manifesto. Motivo: sem ele, uma troca aplicada só num dos dois lugares deixa o plugin
  apontando para pasta que o instalador não clonou, e `desligar_sem_fonte` não pega
  (`espelho.py:346-360`).
- **A4** — README entra no escopo. Motivo: `README.md:99-110` fica falso para `automaster` e
  `ghl-docs`.
- **A3** — texto da skill `ghl-api-docs` entra no escopo. Motivo: cita
  `~/Documents/ghl-docs`, caminho que não existe na origem nem no destino
  (`SKILL.md:9`, `:13`).
- **A5** — descartado. Motivo: as duas origens são pastas reais, não links simbólicos; o
  caminho lógico é igual ao real.
- **A8** — mantido como está. Motivo: `mcp.json` continua entre os arquivos trocados por
  robustez, mesmo sem ocorrência hoje.
- **A1, A2, A7** — confirmam a spec, sem mudança.
