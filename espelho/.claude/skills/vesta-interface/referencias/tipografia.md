# Tipografia

Regras de face, escala, peso e corpo de texto. Cada regra tem id estável; o que muda com o tipo
de tela está em `## Por tipo de tela`. As contradições entre as fontes, com as duas versões e a
decisão, estão em [`fontes.md`](fontes.md). Entre parênteses, as fontes que trazem a regra; três
ou mais fontes marcam regra de piso.

## Escolha de faces

- **TIP-01** Faces batidas ficam fora como padrão: Inter, Roboto, Open Sans, Lato, Poppins,
  Montserrat, DM Sans, Arial e Helvetica no corpo ou no display; Lora e Merriweather como serif de
  corpo. Entram só quando o usuário pede ou o projeto já usa. (hallmark, taste, impeccable)
- **TIP-02** Inter não é escolha do agente, nem no corpo nem no display; Inter Tight só como corpo
  de tom técnico, nunca como display. Se o projeto já usa Inter, mantém. (hallmark, taste)
- **TIP-03** Serif no display precisa de razão: tom editorial, luxo, publicação ou artigo longo.
  "Parece premium" não é razão. Fraunces e Instrument Serif não são padrão; entram escolhidas pelo
  tom (ver Por tipo de tela). (hallmark, taste, impeccable)
- **TIP-04** No máximo três famílias por página: display, corpo e uma face extra. A extra aparece
  em no máximo dois lugares (marca + número do hero, por exemplo). Mono conta como família; a mesma
  família em pesos diferentes conta como uma. (hallmark)
- **TIP-05** Pilha do sistema (`system-ui`) como fonte única só em Operar e Ler; em Persuadir e
  Experiência o display tem face própria, hospedada. (hallmark, impeccable)
- **TIP-06** Face acusada pelo detector (`overused-font`) e escolhida de propósito fica registrada
  no `docs/design/sistema.md`; a exceção já configurada está em
  `ferramentas/impeccable/excecoes.json`. Face nova fora dessa lista pede entrada em `fontes.md` e
  na lista de exceções. (decisão 5 da spec)
- **TIP-07** Fonte paga só com licença confirmada pelo usuário; sem ela, par gratuito (Google Fonts,
  Fontshare). (hallmark)

## Escala e peso

- **TIP-08** Escala por razão, não por incremento: título e corpo separados por ≥ 1.25× (o detector
  acusa `flat-type-hierarchy`). No máximo 5 tamanhos por página; mais hierarquia vem de peso e cor.
  (hallmark, impeccable)
- **TIP-09** Peso de título contrasta com o corpo em ≥ 300 unidades (corpo 400 → título 700 ou 200),
  exceto em Operar (ver Por tipo de tela). Corpo em um peso só; negrito só para ênfase. (hallmark)
- **TIP-10** Nunca sintetizar negrito nem itálico: carregue o arquivo do peso usado. (hallmark)
- **TIP-11** Display ≤ 5.5rem (88px), teto 6rem. Só uma palavra única de ≤ 12ch chega a 7rem.
  Emissão padrão: `clamp(2.75rem, 5vw + 1rem, 5.25rem)`. Título com mais de 50 caracteres desce um
  degrau. (hallmark, impeccable)

## Corpo de texto

- **TIP-12** Corpo ≥ 16px, entrelinha 1.5–1.65, medida 45–75 caracteres (`max-width: 65ch`).
  (hallmark, taste, impeccable, uupm)
- **TIP-13** Tamanho mínimo: texto funcional (link, botão, rótulo, célula, metadado) ≥ 12px em
  qualquer tipo de tela; o detector acusa abaixo de 11px (`undersized-ui-text`). (hallmark,
  impeccable)
- **TIP-14** Corpo nunca em caixa-alta, nunca justificado sem hifenização, tracking ≤ 0.05em.
  (hallmark, impeccable)
- **TIP-15** Texto claro sobre fundo escuro: entrelinha e tracking um pouco maiores e, em face
  variável, peso do corpo −50 (400 → 350), nunca abaixo de 300. (hallmark, impeccable)
- **TIP-16** Pontuação tipográfica: aspas curvas, reticências `…`, nunca `--` nem `...`. O uso do
  travessão segue SLOP-47. (hallmark)

## Display e títulos

- **TIP-17** Tracking do display entre −0.02em e −0.04em, nunca abaixo de −0.04em (o detector acusa
  `extreme-negative-tracking`). Entrelinha do display 1.05–1.2; em caixa-alta, ≥ 1.0 (1.02–1.08
  recomendado); com itálico e descendente, ≥ 1.1. (hallmark, taste, impeccable)
- **TIP-18** Título e display sempre romanos (`font-style: normal`). Ênfase no título vem de peso,
  cor do acento ou sublinhado desenhado; itálico só como ênfase dentro do corpo. (hallmark)
- **TIP-19** Rótulo curto em caixa-alta: tracking 0.08–0.14em, `all-small-caps` se a face tiver.
  (hallmark)
- **TIP-20** Níveis de título sem pular (`h1` → `h2` → `h3`); o estilo visual é livre, a ordem
  semântica não. (hallmark, uupm, impeccable)

## Recursos obrigatórios

- **TIP-21** Números tabulares em dado, preço, tabela e cronômetro
  (`font-variant-numeric: tabular-nums`). (hallmark, taste, impeccable, uupm)
- **TIP-22** `font-display: swap` em toda fonte web e fallback com métricas ajustadas
  (`size-adjust`, `ascent-override`, `descent-override`) para não deslocar a página; carregar só os
  pesos usados. (hallmark, taste, impeccable, uupm)
- **TIP-23** Toda `font-family` sai de token (`var(--font-display)`, `var(--font-body)`); declaração
  solta de fonte fora do `:root` falha (gate 48 em SLOP-09). (hallmark)

## Por tipo de tela

### Persuadir

- Par display + corpo, teto de três famílias (vale TIP-04); o display carrega a voz.
- Geist permitida no corpo; Plus Jakarta Sans permitida no corpo de tom suave (vale TIP-06).
- Fraunces permitida no display quando o tom é editorial ou de luxo, sempre romana (vale TIP-03 e
  TIP-18); fora desse tom, display sans.
- Peso de título com contraste ≥ 300 (vale TIP-09).

### Operar

- Uma família bem ajustada basta, mais mono para código e dado; pilha do sistema aceita (vale
  TIP-05).
- Geist permitida no corpo e nos títulos de painel, com Geist Mono nos números (vale TIP-06).
- Peso de título 600–700 aceito em títulos de painel e 500 em rótulos: a hierarquia densa pede
  degraus menores (exceção a TIP-09); escala fixa por papel, sem `clamp` no corpo.
- Sem serif no display de painel (vale TIP-03). Números tabulares em toda coluna de dado (vale
  TIP-21).

### Ler

- Uma família pode bastar; serif no corpo ou no display é permitida em artigo e documentação longa
  (vale TIP-03).
- Fraunces permitida no título de artigo, romana; Geist permitida no corpo de documentação.
- Medida 60–70ch e entrelinha 1.6 como ponto de partida (vale TIP-12); tamanhos previsíveis, sem
  display fluido no corpo.

### Experiência

- Display com face de ponto de vista; face extra permitida em até dois lugares (vale TIP-04).
- Space Grotesk permitida no display de tom técnico ou brutalista; Outfit só escolhida de
  propósito, nunca como padrão (vale TIP-06).
- Fraunces permitida no display de tom editorial, romana (vale TIP-18).
- Display até 6rem, palavra única até 7rem (vale TIP-11); tracking e entrelinha comprimidos só até
  o piso de TIP-17.
