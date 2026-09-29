# Slop

O que denuncia tela feita no automático. Destila os gates de
`X/hallmark/references/slop-test.md` (a lista numerada vai de 1 a 57; o título diz 58, ver
`fontes.md`) e as proibições que se repetem nas outras fontes.

Marcadores nos itens com gate: `[detector]` quando o detector do impeccable acusa na página
renderizada (a regra dele vem entre crases; todo alarme é corrigido ou refutado com prova);
`[olho]` quando o detector não cobre e a conferência é no print, celular e desktop, ou no código.

Entre parênteses, as fontes que trazem a regra; três ou mais fontes marcam regra de piso.

## Tipo e cor

- **SLOP-01** gate 1 [detector] `overused-font`: display não é Inter, Roboto, Open Sans, Poppins nem
  Lato; em Persuadir e Experiência também não é a fonte do sistema. Faces com exceção decidida
  seguem TIP-06. (hallmark, taste, impeccable)
- **SLOP-02** gate 2 [detector] `gradient-text` `ai-color-palette`: nenhum texto em gradiente
  (`background-clip: text`) e nenhum gradiente roxo→azul, ciano→magenta ou brilho roxo. (hallmark,
  taste, impeccable)
- **SLOP-03** gate 7 [olho]: nenhum `#000` ou `#fff` puro como cor base (ver COR-06).
- **SLOP-04** gate 22, gate 23 [olho]: neutro com croma ≥ 0.005 (ver COR-05); acento cobre ≤ 5%
  de qualquer viewport, contando preenchimento, título no acento e fundo sangrado (ver COR-09).
- **SLOP-05** gate 29 [detector] `radial-halo` `radial-spotlight-glow`: fundo abstrato com um acento
  só, ≤ 5% da tela e sem malha de gradiente animada na página inteira (exceção de Experiência em
  Por tipo de tela).
- **SLOP-06** gate 37, gate 38 [olho]: no máximo três famílias; a face extra aparece em no máximo
  dois lugares (ver TIP-04).
- **SLOP-07** gate 55 [olho]: display em caixa-alta com entrelinha ≥ 1.0 (ver TIP-17).
- **SLOP-08** gate 40, gate 41 [detector] `low-contrast`: texto, ícone e anel de foco passam o
  limite contra o fundo calculado (ver COR-12); texto de botão nunca da mesma cor do preenchimento;
  seção escura troca a cor do texto na mesma regra que troca o fundo.
- **SLOP-09** gate 48 [olho]: toda cor e toda `font-family` vêm de token do `:root`; nenhum hex,
  `oklch()` ou fonte solta no meio do código.

## Estrutura

- **SLOP-10** gate 3 [detector] `icon-tile-stack`: nada de três cards iguais com ícone em cima,
  título e texto como estrutura da página. (hallmark, taste, impeccable)
- **SLOP-11** gate 4 [detector] `nested-cards`: nenhum card dentro de card. (hallmark, impeccable,
  taste)
- **SLOP-12** gate 5 [detector] `side-tab` `border-accent-on-rounded`: nenhuma borda lateral
  colorida grossa (> 1px) em card, item de lista ou alerta. (hallmark, impeccable)
- **SLOP-13** gate 6 [olho]: hero sem tudo centralizado; no máximo dois elementos no eixo central,
  o resto quebra o alinhamento.
- **SLOP-14** gate 8, gate 21, gate 32, gate 57 [olho]: em Persuadir e Experiência a estrutura gira:
  nem o molde Hero → 3 features → CTA → rodapé, nem a mesma macroestrutura (ou o mesmo arranjo de
  botões dentro dela) da tela anterior do projeto, nem a macroestrutura Specimen sem pedido
  editorial; se houve study, a tela usa o DNA estudado, não um tema do catálogo. Conferir em
  `docs/design/rotacao.json` (R7 da spec).
- **SLOP-15** gate 20 [olho]: a macroestrutura escolhida fica registrada em
  `docs/design/rotacao.json`, nunca em comentário no código entregue (A18 da spec).
- **SLOP-16** gate 9 [detector] `monotonous-spacing`: seções não se separam só por espaço igual;
  varie ritmo, use fio, ornamento ou mudança de fundo.
- **SLOP-17** gate 24 [olho]: todo padding, gap e margin na escala nomeada, múltiplos de 4px;
  `padding: 17px` é sinal.
- **SLOP-18** gate 25 [detector] `line-length`: todo contêiner de prosa entre 45 e 75 caracteres
  (ver TIP-12).
- **SLOP-19** gate 42, gate 43 [olho]: navegação e rodapé fogem do molde (marca à esquerda + 4–5
  links + botão à direita com fio embaixo; rodapé de 4 colunas + ícones sociais + copyright), salvo
  quando o conteúdo justifica.
- **SLOP-20** gate 44 [olho]: hero com padding de baixo ≥ 1.3× o de cima e cabendo na primeira dobra
  do notebook.
- **SLOP-21** gate 54 [detector] `numbered-section-labels`: nenhum rótulo, número ou tag em coluna
  ao lado do título da seção na mesma linha.
- **SLOP-22** Eyebrow ou kicker acima do título fica fora por padrão (o detector acusa
  `kicker-above-heading` e `hero-eyebrow-chip`); número de seção (01 / 02) só quando a sequência
  carrega informação que o leitor precisa. (hallmark, taste, impeccable)

## Movimento e interação

- **SLOP-23** gate 10 [olho]: nenhum `transition: all` nem `transition-all`; declare as
  propriedades.
- **SLOP-24** gate 14 [detector] `layout-transition`: não animar `width`, `height`, `top`, `left`,
  `margin` nem `padding`.
- **SLOP-25** gate 11, gate 13 [olho]: nenhum `scale` de hover igual em elementos sem relação, e no
  máximo um efeito de hover por elemento.
- **SLOP-26** gate 12 [detector] `bounce-easing`: nenhuma curva com ultrapassagem ou elástica em
  mudança de estado de UI (botão, modal, tooltip).
- **SLOP-27** gate 15, gate 17 [olho]: anel de foco aparece na hora, sem fade; tooltip espera
  800–1000ms no hover e 0ms no foco.
- **SLOP-28** gate 16 [olho]: sem toast de comemoração quando o efeito da ação já está visível na
  tela; toast é para falha e efeito invisível.
- **SLOP-29** gate 18 [olho]: conteúdo que gira sozinho (carrossel, faixa, número) pausa no hover e
  no foco (WCAG 2.2.2); o detector acusa `marquee` à parte.
- **SLOP-30** gate 26, gate 39 [olho]: todo elemento interativo tem hover, `:focus-visible`,
  `:active` e `:disabled`; campo mantém a borda de 1px em todo estado, foco por `outline`, altura
  igual à do botão vizinho (piso 44px), espaço de ajuda reservado e desabilitado por três canais
  (opacidade, cursor e atributo).
- **SLOP-31** gate 27 [olho]: toda animação tem alternativa em
  `@media (prefers-reduced-motion: reduce)`.
- **SLOP-32** gate 28 [olho]: vídeo de demonstração sem autoplay com som, com `poster`, sem
  `loading="lazy"` quando é o maior elemento da dobra.
- **SLOP-33** gate 36, gate 49 [olho]: barras interativas centralizadas na vertical
  (`align-items: center`); nenhum texto clicável quebra em duas linhas entre 320 e 1920px.
- **SLOP-34** gate 34 [detector] `text-overflow`: nenhuma rolagem horizontal entre 320 e 1920px;
  `overflow-x: clip` em `html` e `body`.
- **SLOP-35** gate 50, gate 51, gate 52, gate 53, gate 56 [olho]: trilha de grade com imagem usa
  `minmax(0, 1fr)`; display com `overflow-wrap: anywhere; min-width: 0`; cabeçalho de seção em
  colunas colapsa no celular; abas por rádio não pulam a rolagem; nenhum segundo elemento `sticky`
  em `top: 0` sob a navegação fixa.
- **SLOP-36** gate 33 [olho]: todo SVG, `canvas` ou arte em CSS decorativo tem `aria-label` ou
  `aria-hidden="true"`.

## Ícone, imagem e ornamento

- **SLOP-37** gate 30 [olho]: uma família de ícones por projeto, com traço e peso constantes
  (Lucide por padrão, decisão 1 da spec); emoji nunca como ícone de card, passo, preço ou
  navegação. (hallmark, taste, impeccable, uupm)
- **SLOP-38** Glifo Unicode (⌛ ⚠ ✓ ★) não substitui ícone de estado ou de função; o ícone vem da
  biblioteca. Seta tipográfica (→) em link de texto é pontuação, vale. (impeccable, hallmark)
- **SLOP-39** Emoji no texto fica fora por padrão; só entra em Experiência de tom lúdico ou social
  com pedido do usuário, e com parcimônia. (taste)
- **SLOP-40** gate 31 [olho]: ilustração não começa por Lottie; SVG feito à mão ou forma em CSS
  primeiro.
- **SLOP-41** gate 35 [olho]: todo efeito decorativo sobre texto (marca-texto, sublinhado, traço)
  conferido no print: a faixa fica atrás da altura-x, não na linha de base.
- **SLOP-42** gate 45 [olho]: nenhum elemento decorativo no hero sem âncora no conteúdo (cursor,
  scanline, mancha, forma, selo); o detector pega parte (`blinking-cursor`, `pulsing-dot`).
- **SLOP-43** gate 47 [olho]: nenhuma moldura falsa desenhada em HTML/CSS (barra de navegador com
  três bolinhas, celular, janela de código, terminal, IDE); print real num `<figure>` ou nada.
  (hallmark, taste)
- **SLOP-44** Vidro e desfoque só com função (fundo de modal, folha, barra sobre conteúdo), nunca
  como decoração; com alternativa sólida. (hallmark, taste, impeccable, uupm)

## Texto

- **SLOP-45** gate 19 [olho]: nenhum nome de exemplo (João da Silva, Jane Doe) nem marca clichê
  (Acme, Nexus); nomes do domínio e do lugar.
- **SLOP-46** gate 46 [olho]: nenhum número inventado ("10× mais rápido", "+47% de conversão",
  "50 mil equipes"); sem dado do usuário, use marcador rotulado ("métrica a confirmar") ou outra
  estrutura. Dado de demonstração é rotulado como fictício. (hallmark, impeccable, taste)
- **SLOP-47** Travessão (—) permitido com moderação: no corpo, bem abaixo da saturação que o
  detector acusa (`em-dash-overuse`: 8 ou mais, perto de um a cada 500 caracteres); evite em
  título, botão, rótulo, pílula e navegação. Intervalo numérico com meia-risca (`10–20`) ou hífen,
  um só padrão por projeto. (decisão 2 da spec; hallmark, taste, impeccable)
- **SLOP-48** Ponto médio (·) no máximo um por linha em faixa de metadado; lista longa se separa
  por quebra, fio ou coluna. (taste, hallmark)
- **SLOP-49** Sem jargão de marketing: "revolucionar", "potencializar", "sem esforço", "de ponta",
  "elevar", "streamline", "seamless" (o detector acusa `marketing-buzzword`); verbo concreto.
  (taste, impeccable)

## Por tipo de tela

### Persuadir

- Todos os gates valem; a rotação de estrutura é obrigatória (vale SLOP-14, SLOP-15).
- Navegação, rodapé e hero fora do molde (vale SLOP-13, SLOP-19, SLOP-20).
- Emoji fora do texto (vale SLOP-39); número sem fonte nunca (vale SLOP-46).

### Operar

- Sem rotação: menu, navegação e estrutura se repetem entre telas (R7 da spec); SLOP-13, SLOP-14,
  SLOP-19 e SLOP-20 não se aplicam.
- Estados completos e campos sem salto de layout pesam mais que tudo (vale SLOP-30, SLOP-33).
- Dado de demonstração rotulado como fictício (vale SLOP-46); emoji fora (vale SLOP-39).

### Ler

- Sem rotação (SLOP-14 não se aplica); medida da prosa é o gate central (vale SLOP-18).
- Artigo longo pode ter travessões, sempre abaixo do limite do detector (vale SLOP-47).
- Número de seção vale quando a sequência importa, como em passo a passo (vale SLOP-22).

### Experiência

- A rotação é obrigatória (vale SLOP-14); a direção pode quebrar o molde de hero e navegação.
- Fundo atmosférico: até duas manchas radiais de tom quente cobrindo ~20–30% da tela, fixas e sem
  animação (exceção a SLOP-05, nota do gênero atmospheric do hallmark).
- Emoji só com pedido de tom lúdico ou social (vale SLOP-39).
