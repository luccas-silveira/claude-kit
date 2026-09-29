# Cor

Regras de espaço de cor, paleta, acento, contraste e modo escuro. O que muda com o tipo de tela
está em `## Por tipo de tela`; as contradições resolvidas, em [`fontes.md`](fontes.md). Entre
parênteses, as fontes que trazem a regra; três ou mais fontes marcam regra de piso.

## Espaço e tokens

- **COR-01** Paleta nova em OKLCH, inclusive o acento; projeto que já tem paleta mantém o espaço de
  cor dele. Ao derivar rampas, reduza o croma perto do branco e do preto. (hallmark, impeccable)
- **COR-02** Tokens semânticos (superfície, tinta, acento, foco, erro, sucesso…) declarados no
  `:root`; componente nunca usa valor cru. Troca de tema remapeia os papéis, não os componentes.
  (hallmark, taste, impeccable, uupm)
- **COR-03** Paleta em quatro camadas: papel (base), tinta (texto), 5–9 neutros entre os dois e um
  acento com croma 0.12–0.22. (hallmark)
- **COR-04** Token de cor é opaco; transparência só modifica sobreposição e sombra, nunca define
  uma cor da paleta. (hallmark, impeccable)

## Neutros e extremos

- **COR-05** Neutros puxados para o matiz âncora com croma 0.005–0.015; cinza quente e cinza frio
  nunca na mesma página. Cinza de croma zero só em direção monocromática declarada no
  `docs/design/sistema.md`. (hallmark, taste)
- **COR-06** Nenhum `#000` puro em lugar nenhum; nenhum `#fff` puro como superfície base (papel com
  leve matiz). Exceção: direção modern-minimal declarada, que pode usar papel branco. (hallmark,
  taste)
- **COR-07** Creme ou bege de papel não é padrão (o detector acusa `cream-palette`); entra quando a
  marca pede ou a direção justifica, registrado no `sistema.md`. (taste, impeccable)

## Acento

- **COR-08** Um acento, dois no máximo, travado na página inteira: o mesmo acento em todas as
  seções e componentes. (hallmark, taste)
- **COR-09** Acento cobre ≤ 5% de qualquer viewport (≤ 3% como meta), contando preenchimento, título
  no acento e fundo sangrado. Usos: item ativo, anel de foco, link, borda ou texto do CTA principal.
  Estratégias mais fortes só pelo tipo de tela. (hallmark, taste)
- **COR-10** Superfície no acento com texto em cima ganha um token de tinta própria
  (`--color-accent-ink`) com ≥ 4.5:1 contra o acento. (hallmark)

## Gradientes

- **COR-11** Gradiente só com propósito (fundo, tom de marca), nunca em texto, nunca roxo→azul,
  roxo→ciano ou laranja→rosa, e com duas paradas. Gradiente não preenche lacuna de conteúdo.
  (hallmark, taste, impeccable)

## Contraste

- **COR-12** Contraste medido contra o fundo calculado: corpo e placeholder ≥ 4.5:1; texto grande
  (≥ 24px, ou ≥ 18.66px em negrito) ≥ 3:1; ícone com significado e borda de controle ≥ 3:1.
  (hallmark, taste, impeccable, uupm)
- **COR-13** Anel de foco visível, ≥ 3:1 contra o fundo vizinho, feito com `outline` na cor de foco.
  (hallmark, taste, impeccable, uupm)
- **COR-14** Alvo de contraste do corpo: 4.5:1 é o piso em todo tipo de tela; 7:1 é o alvo em Ler.
  (hallmark, taste, uupm)
- **COR-15** Nada de texto cinza sobre fundo colorido: o texto secundário deriva do matiz da
  superfície ou da tinta (o detector acusa `gray-on-color`). (hallmark, impeccable, uupm)
- **COR-16** Cor nunca é o único sinal: erro, sucesso, estado e série de dado levam também ícone,
  texto, forma ou padrão; nunca vermelho contra verde sozinhos. (hallmark, impeccable, uupm)
- **COR-17** Antes de entregar, simular deficiência de visão de cor no navegador e conferir os
  estados (hover, desabilitado, erro, texto sobre imagem). (hallmark, impeccable)

## Modo escuro

- **COR-18** Modo escuro é desenhado, não invertido: papel com luminosidade 12–18%, tinta 92–96%,
  superfície mais alta é mais clara (+~3% por nível), mesmo matiz âncora nos dois modos.
  (hallmark, impeccable, uupm)
- **COR-19** Acento no escuro mantém o matiz: croma −0.02 a −0.04 e luminosidade +5–10%; a marca
  continua reconhecível. (hallmark, uupm)
- **COR-20** Com dois modos, o contraste é conferido em cada um separadamente, e os estados
  (foco, pressionado, desabilitado) ficam igualmente distintos nos dois. (taste, impeccable, uupm)
- **COR-21** Com dois modos, o padrão segue `prefers-color-scheme`, há troca manual e uma só
  estratégia de tokens (variáveis CSS por `[data-theme]` ou media query). (taste, uupm)

## Por tipo de tela

### Persuadir

- Modo escuro: um modo só, claro ou escuro, escolhido pelo contexto de uso (quem, onde, sob que
  luz), nunca pela categoria do produto.
- Estratégia de cor pode ser comprometida (uma cor saturada em 30–60% da superfície) quando a
  direção declara no `sistema.md`; senão vale COR-09.

### Operar

- Modo escuro: os dois, claro e escuro, desenhados juntos desde o início (vale COR-18 a COR-21).
- Cor codifica ação, seleção, estado e caminho; acento restrito e raro (vale COR-09).
- Contraste conferido nos estados densos: tabela, desabilitado, erro, vazio (vale COR-12, COR-16).

### Ler

- Modo escuro: um modo só, escolhido pelo contexto de leitura (documentação técnica aberta ao lado
  do editor tende ao escuro; artigo longo, ao claro).
- Contraste do corpo com alvo 7:1 (vale COR-14); acento só em link e marcação de leitura.

### Experiência

- Modo escuro: um modo só, escolhido pela direção da peça.
- Estratégias fortes permitidas: cor comprometida ou a superfície inteira na cor, quando a
  direção declara (exceção a COR-09).
- Fundo atmosférico com manchas radiais segue a exceção de `slop.md` (vale SLOP-05).
