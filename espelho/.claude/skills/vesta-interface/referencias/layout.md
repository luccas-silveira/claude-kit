# Layout

Regras de grade, espaçamento, hero, navegação, responsivo e camadas. O que muda com o tipo de tela
está em `## Por tipo de tela`; as contradições resolvidas, em [`fontes.md`](fontes.md). Entre
parênteses, as fontes que trazem a regra; três ou mais fontes marcam regra de piso.

## Botões

Três botões de 1 a 10 regulam layout e movimento. São os três dials do taste
(`X/taste-skill/skills/taste-skill/SKILL.md:45-78`), com estes nomes: VARIACAO (`DESIGN_VARIANCE`,
1 simetria perfeita, 10 caos artístico), MOVIMENTO (`MOTION_INTENSITY`, 1 parado, 10
cinematográfico) e DENSIDADE (`VISUAL_DENSITY`, 1 galeria arejada, 10 cockpit de dados). Fora
desta seção, só esses três nomes, sem apelido (`:78`).

O passo 1 fixa os valores pelo tipo de tela com a tabela abaixo e grava em
`docs/design/sistema.md`; o usuário pode mudá-los no questionário (R2 da spec). Redesenho que
preserva parte dos valores lidos no site existente, com MOVIMENTO +1 (`:61`).

| Tipo de tela | VARIACAO | MOVIMENTO | DENSIDADE |
|---|---|---|---|
| Persuadir | 7 | 5 | 4 |
| Operar | 3 | 3 | 7 |
| Ler | 4 | 2 | 3 |
| Experiência | 8 | 7 | 3 |

De onde vêm: Persuadir é o landing do taste (7/6/4, `:67`) com MOVIMENTO 5 pelo momento único de
MOV-03; Experiência é o portfólio de estúdio (8/7/3, `:70`); Ler parte do editorial (6/4/3, `:72`)
e desce para estrutura previsível e página parada
(`X/impeccable/.claude/skills/impeccable/reference/layout.md:8`,
`X/hallmark/references/microinteractions.md:22`); Operar não tem preset no taste: VARIACAO e
MOVIMENTO do serviço público (`:73`), DENSIDADE na faixa de app (`:567`). As faixas de MOVIMENTO
estão em MOV-01, em [`movimento.md`](movimento.md).

- **LAY-01** VARIACAO por faixa. 1–3: grade simétrica de colunas iguais, alinhamento central
  permitido. 4–7: deslocamento, com sobreposição, proporções de imagem variadas, título à
  esquerda sobre dado centralizado. 8–10: assimetria, colunas fracionárias (`2fr 1fr 1fr`),
  zonas vazias grandes, mosaico. Liga LAY-08 (hero fora do centro) a partir de 5, LAY-09 e LAY-23
  a partir de 4, LAY-14 a partir de 7. (taste)
- **LAY-02** DENSIDADE por faixa, no espaço entre seções. 1–3: `--space-3xl`–`--space-4xl`
  (96–144px). 4–7: `--space-2xl`–`--space-3xl` (64–96px). 8–10: `--space-lg`–`--space-xl`
  (24–40px), sem card como contêiner genérico, fio de 1px separando dado, números tabulares
  (TIP-21). (taste, uupm)

## Espaçamento

- **LAY-03** Espaçamento em escala nomeada de base 4px, declarada no `:root`: `--space-3xs` 2,
  `--space-2xs` 4, `--space-xs` 8, `--space-sm` 12, `--space-md` 16, `--space-lg` 24,
  `--space-xl` 40, `--space-2xl` 64, `--space-3xl` 96, `--space-4xl` 144px. Todo padding, gap e
  margin sai dela; valor solto é falha (gate 24 em SLOP-17). (hallmark, impeccable, uupm; taste
  pela escala do Tailwind)
- **LAY-04** Ritmo por contraste: grupo apertado, separação generosa, mais espaço acima do título
  que abaixo (o detector acusa `heading-rhythm`). Padding do card, da seção e da página nunca
  iguais (SLOP-16). (hallmark, impeccable, uupm)
- **LAY-05** `gap` entre irmãos; `margin` só para ajuste ótico ou para sair do fluxo, nunca para
  espaçar uma lista. (hallmark, impeccable)
- **LAY-06** Agrupar por proximidade antes de pôr contêiner: card só quando a elevação comunica
  hierarquia real; senão fio ou espaço. Com DENSIDADE ≥ 8, nenhum card genérico. Nunca card dentro
  de card (SLOP-11). (hallmark, taste, impeccable)

## Grade e seção

- **LAY-07** Grid para a página, flex para o interior do componente; nada de porcentagem em flex
  (`calc(33% - 1rem)`). Trilha com imagem usa `minmax(0, 1fr)` (SLOP-35). (hallmark, taste)
- **LAY-08** A página tem um eixo primário (esquerda, direita, topo ou base). Com VARIACAO ≥ 5, o
  hero não centraliza: no máximo dois elementos no eixo central (SLOP-13), o resto em divisão,
  texto à esquerda com visual à direita ou espaço assimétrico. VARIACAO ≤ 4 permite coluna
  centralizada. (hallmark, taste, uupm)
- **LAY-09** Com VARIACAO ≥ 4, cada seção usa uma família de layout diferente: duas seções nunca
  com o mesmo arquétipo, no máximo dois zigue-zagues de texto e imagem seguidos, página de 8
  seções com ≥ 4 famílias. (hallmark, taste)
- **LAY-10** Cabeçalho de seção empilhado: título em cima, texto até 65ch embaixo. Duas colunas só
  quando a da direita traz visual ou controle, nunca parágrafo solto no canto; colapsa numa coluna
  no celular (gate 52 em SLOP-35). (taste, hallmark)
- **LAY-11** Alinhamento do cabeçalho coerente com o corpo: à esquerda sobre corpo à esquerda,
  centralizado sobre corpo simétrico, ou quebra declarada. (hallmark)
- **LAY-12** Bento com tantas células quanto conteúdos (nenhuma vazia), tamanhos variados e 2–3
  células com variação visual real (imagem, textura, fundo tingido). (taste, hallmark)
- **LAY-13** Contêiner com uma largura máxima só (em torno de 1400px) e margem lateral fluida,
  `padding-inline: clamp(1rem, 4vw, 4rem)`. (hallmark, taste, uupm)
- **LAY-14** Seção presa ao scroll (pilha fixa, pan horizontal) só com MOVIMENTO ≥ 8 e
  VARIACAO ≥ 7, fixando no topo da tela; abaixo disso a seção rola normal. Nunca um segundo
  `sticky` em `top: 0` sob a navegação fixa (SLOP-35). (taste, hallmark)

## Hero

- **LAY-15** O hero cabe na primeira dobra do notebook: título em até 2 linhas no desktop, lede
  até 20 palavras em até 3 linhas, CTA visível sem rolar. Padding de cima ≤ 6rem, padding de baixo
  ≥ 1.3× o de cima (SLOP-20). (hallmark, taste)
- **LAY-16** No máximo 4 elementos de texto no hero: rótulo opcional (SLOP-22), título, lede e CTAs
  (um primário e no máximo um secundário). Faixa de logos, preço, lista de recursos e fila de
  avatares vão para a seção seguinte. (taste)
- **LAY-17** Título do hero escrito pelo agente: ≤ 7 palavras e ≤ 50 caracteres; mais longo, o
  tamanho desce um degrau (TIP-11). (hallmark, taste)

## Navegação

- **LAY-18** Navegação numa linha no desktop, altura 64–72px, teto 80px. Não coube: encurte os
  rótulos, esconda o item secundário, depois recolha em menu. Link e CTA nunca quebram (SLOP-33).
  (taste, hallmark)
- **LAY-19** Persuadir e Experiência giram o arquétipo de navegação e rodapé do catálogo
  (SLOP-19); Operar e Ler repetem a mesma navegação, na mesma posição, em todas as telas, com o
  item atual destacado. (hallmark, uupm)

## Responsivo

- **LAY-20** Responsivo mobile-first: o estilo base é o da tela menor e `min-width` acrescenta;
  `max-width` nunca é a direção principal. (hallmark, impeccable, uupm)
- **LAY-21** Breakpoints onde o conteúdo quebra, em rem (padrão 40, 60 e 90rem), três ou quatro
  no máximo; `clamp()` para tamanho que muda contínuo, media query para layout que muda em
  degrau. (hallmark, impeccable)
- **LAY-22** Conferir em 320, 375, 414, 768, 1024 e 1440px: nenhuma rolagem horizontal
  (`overflow-x: clip` em `html` e `body`, nunca `hidden`), nenhum texto clicável quebrando,
  nenhuma trilha de imagem estourando (SLOP-34, SLOP-35). (hallmark, taste, impeccable, uupm)
- **LAY-23** Todo layout de várias colunas declara, no mesmo componente, como fica abaixo do
  primeiro breakpoint; com VARIACAO ≥ 4 a assimetria vira uma coluna no celular. (taste, hallmark)
- **LAY-24** Altura de tela em `dvh` ou `svh`, nunca `vh` nem `h-screen` no hero; largura em
  `100%`, nunca `100vw`. (hallmark, taste, uupm)
- **LAY-25** Capacidade de interação por `@media (hover: hover)` e `(pointer: coarse)`, não pela
  largura; nenhuma interação existe só no hover. (hallmark, impeccable, uupm)
- **LAY-26** Alvo de toque ≥ 44×44 CSS px (a área clicável pode passar do desenho, com padding ou
  `::before`) e ≥ 8px entre alvos. (hallmark, impeccable, uupm)
- **LAY-27** Área segura: `viewport-fit=cover` e padding com `env(safe-area-inset-*)`; barra fixa
  reserva espaço para o conteúdo que fica por baixo. (hallmark, impeccable, uupm)
- **LAY-28** Imagem com `width` e `height` (ou `aspect-ratio`) e `srcset`; `loading="lazy"` só
  abaixo da dobra. (hallmark, taste, uupm)
- **LAY-29** Tabela larga no celular é redesenhada (colunas prioritárias ou um cartão por linha);
  tabela de 10+ colunas nunca vai crua para 320px. (hallmark)
- **LAY-30** Propriedades lógicas (`margin-inline`, `padding-block`) e 30–40% de folga horizontal
  para texto traduzido. (hallmark)

## Camadas, sombra e raio

- **LAY-31** z-index em escala nomeada de tokens: `--z-base` 1, `--z-raised` 10,
  `--z-dropdown` 100, `--z-sticky` 200, `--z-modal` 400, `--z-toast` 500, `--z-tooltip` 600.
  Nenhum número solto (`z-50`, `9999`). (hallmark, taste, uupm)
- **LAY-32** Profundidade vem de peso, escala e tom antes de sombra. Sombra: uma por elemento, com
  deslocamento e desfoque, tingida do matiz do fundo
  (`0 1px 2px oklch(20% 0.01 <matiz> / 0.05)`), numa escala de elevação só. Anel de 1px sem
  deslocamento vale como borda, nunca colorido como halo. Sem sombra em card escuro, sem sombra
  larga com borda fina (o detector acusa `gpt-thin-border-wide-shadow`), sem sombra dura deslocada
  fora de direção neobrutalista. (hallmark, taste, impeccable, uupm)
- **LAY-33** Raio: um sistema por página, em tokens por papel (`--radius-card`, `--radius-input`,
  `--radius-pill`), com o valor da direção (0 no brutalista, ≤ 12px no minimalista). Mistura só
  com regra escrita no `sistema.md` e seguida em toda parte (o detector acusa
  `design-system-radius`). (hallmark, taste)

## Por tipo de tela

### Persuadir

- VARIACAO 7 e DENSIDADE 4 (tabela de Botões): hero fora do centro (vale LAY-08), família de
  layout diferente por seção (vale LAY-09), navegação e rodapé girados (vale LAY-19).
- Hero na dobra com até 4 elementos de texto (vale LAY-15, LAY-16, LAY-17).

### Operar

- VARIACAO 3 e DENSIDADE 7: grade previsível e densa; tela de dado sobe a DENSIDADE para 8 ou
  mais, sem card e com fio de 1px (vale LAY-02, LAY-06).
- Sem rotação: a mesma navegação em toda tela (vale LAY-19); LAY-08 e LAY-09 não se aplicam.
- Tabela redesenhada no celular e alvo de toque cheio (vale LAY-26, LAY-29).

### Ler

- VARIACAO 4: coluna de leitura centralizada permitida (exceção a LAY-08); estrutura linear,
  cabeçalho empilhado (vale LAY-10).
- DENSIDADE 3: espaço generoso entre seções; navegação e índice iguais em todas as páginas (vale
  LAY-19).

### Experiência

- VARIACAO 8: assimetria, colunas fracionárias e uma quebra de grade de propósito; seção presa ao
  scroll permitida com MOVIMENTO 8 ou mais declarado (vale LAY-14).
- Raio, sombra e densidade seguem a direção registrada no `sistema.md` (vale LAY-32, LAY-33).
