---
description: Busca referências visuais reais no inspo para um brief de design
---

Monte o brief a partir de `$ARGUMENTS`. Se vier vazio, pergunte o brief pelo `AskUserQuestion` antes de buscar.

1. Uma chamada de `mcp__inspo__recommend` com o brief. Use `device`, `mode` ou `pageType` só se o pedido disser.
2. Uma ou duas chamadas de `mcp__inspo__search_screens` com o brief, para cobrir o que o `recommend` deixou de fora. Não passe disso.
3. `mcp__inspo__get_screen` nas 2 a 5 referências que servirem, pelo slug.
4. Para cada uma, uma linha: a macroestrutura, o que entra nesta tela (estrutura, tipografia, ritmo, paleta) e a URL do site como fonte. Leve a composição, não a transgressão.
5. Se o projeto tem `## Piso` ou regras de design, corte da sugestão o que elas vetam antes de mostrar.

Termine com a lista. Quem chamou (a pesquisa ou o mockup da Vesta) grava o que precisar.
