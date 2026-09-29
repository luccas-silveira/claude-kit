# Movimento

Regras de propósito, propriedades, tempo, curva, entrada, scroll, loop e movimento reduzido. O que
muda com o tipo de tela está em `## Por tipo de tela`; as contradições resolvidas, em
[`fontes.md`](fontes.md). Entre parênteses, as fontes que trazem a regra; três ou mais fontes
marcam regra de piso.

## Botões

Os mesmos três botões de [`layout.md`](layout.md), dials do taste
(`X/taste-skill/skills/taste-skill/SKILL.md:45-78`): VARIACAO (`DESIGN_VARIANCE`), MOVIMENTO
(`MOTION_INTENSITY`) e DENSIDADE (`VISUAL_DENSITY`), de 1 a 10. O passo 1 fixa os valores pelo tipo
de tela e grava em `docs/design/sistema.md`; o usuário pode mudá-los no questionário. As faixas de
VARIACAO e DENSIDADE estão em LAY-01 e LAY-02.

| Tipo de tela | VARIACAO | MOVIMENTO | DENSIDADE |
|---|---|---|---|
| Persuadir | 7 | 5 | 4 |
| Operar | 3 | 3 | 7 |
| Ler | 4 | 2 | 3 |
| Experiência | 8 | 7 | 3 |

- **MOV-01** MOVIMENTO por faixa. 1–3: nada automático; só transição de estado (hover,
  pressionar, abrir) e feedback funcional. 4–7: uma entrada orquestrada na carga, reveal único em
  até duas seções-chave (MOV-15), marquee se pedido (MOV-20), movimento perpétuo com função a
  partir de 6 (MOV-19). 8–10: coreografia por seção, animação ligada ao scroll, seção presa
  (LAY-14), parallax em Experiência (MOV-17). Tela com MOVIMENTO ≥ 4 se move de fato; sem escopo
  para fazer direito, desça para 3 e entregue parada. (taste)

## Propósito

- **MOV-02** Todo movimento comunica algo: feedback de ação, mudança de estado, continuidade
  espacial, hierarquia ou o momento autoral da peça. Se ninguém notaria a versão instantânea,
  corte a animação. (hallmark, taste, impeccable, uupm)
- **MOV-03** Um momento autoral por página, em 1–2 elementos por vista; nunca a mesma entrada em
  toda seção nem efeito espalhado. No máximo três primitivas de animação distintas por página.
  (hallmark, impeccable, uupm)
- **MOV-04** Conteúdo visível no repouso: a animação parte de um estado já visível e script que
  falha não esconde a página (o detector acusa `content-hidden-at-rest`). (impeccable)

## Propriedades

- **MOV-05** Transição de UI anima só `transform` e `opacity`; nunca propriedade de layout
  (SLOP-24). Acordeão por `grid-template-rows: 0fr → 1fr`, sublinhado de aba por
  `transform: scaleX`. Blur, `clip-path`, máscara, filtro e sombra só no momento autoral de
  Persuadir e Experiência, em região isolada e fluida no aparelho-alvo. (hallmark, taste, uupm;
  impeccable amplia, ver fontes.md)
- **MOV-06** `will-change` só no elemento e só enquanto anima, nunca numa classe inteira.
  (hallmark, taste, impeccable)
- **MOV-07** Nunca `transition: all` nem `transition-all` (SLOP-23): declare cada propriedade.
  (hallmark)

## Tempo e curva

- **MOV-08** Durações em tokens: `--dur-micro` 120ms (pressionar, marcar), `--dur-short` 220ms
  (hover, tooltip, menu), `--dur-long` 420ms (modal, gaveta, acordeão, entrada). UI fica entre 100
  e 500ms; só a entrada autoral de Persuadir e Experiência vai até 800ms; nada passa de 2s fora de
  loop contínuo. (hallmark, impeccable, uupm)
- **MOV-09** Saída mais curta que a entrada, 60–75% dela (300ms entra, 200ms sai). (hallmark,
  impeccable, uupm)
- **MOV-10** Curvas em tokens: `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)` para entrar,
  `--ease-in: cubic-bezier(0.7, 0, 0.84, 0)` para sair,
  `--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1)` para alternar estado. `ease` padrão do navegador fora; `linear`
  só em barra de progresso e carregador contínuo. (hallmark, taste, impeccable, uupm)
- **MOV-11** Mola só em interação física (soltar arrasto, gesto, roda de seleção), sem passar de
  ~110%; mudança de estado de UI nunca quica (SLOP-26). (hallmark, taste, uupm)
- **MOV-12** Zero ms onde o movimento atrasa: anel de foco, navegação por teclado, aparição de
  erro, abertura da paleta de comandos, tooltip no foco (SLOP-27). Hover, pressionar, abrir e
  fechar animam com os tokens de MOV-08. (hallmark; uupm diverge, ver fontes.md)

## Entrada e scroll

- **MOV-13** Entrada da página numa sequência só, escalonada pelo índice do DOM (`--i`) em CSS:
  `translateY(8px)` e opacidade, `--dur-long`, `--ease-out`. (hallmark)
- **MOV-14** Stagger de 40–60ms por item (60 padrão) e total ≤ 500ms, só em lista que aparece como
  lista. (hallmark, impeccable, uupm)
- **MOV-15** Reveal no scroll dispara uma vez e nunca repete; nunca em corpo de texto; nunca a
  mesma entrada em toda seção; nada ligado ao scroll abaixo de 40rem. MOVIMENTO ≤ 3: nenhum.
  4–7: até duas seções-chave além da entrada. 8–10: coreografia por seção, declarada no
  `sistema.md`. (hallmark, taste, impeccable)
- **MOV-16** Scroll lido por IntersectionObserver, `animation-timeline: view()`, `useScroll` ou
  ScrollTrigger; nunca `addEventListener('scroll')` nem `window.scrollY` em estado para animar.
  (hallmark, taste)
- **MOV-17** Parallax fora; só Experiência com MOVIMENTO ≥ 8, e parado em movimento reduzido.
  (hallmark; ver fontes.md)
- **MOV-18** A entrada acompanha a composição: com VARIACAO ≤ 4 é só opacidade e deslocamento
  vertical curto; varredura horizontal e máscara que se abre (`clip-path`) pedem VARIACAO ≥ 7,
  onde a assimetria dá a direção do movimento. (hallmark)

## Loops e hover

- **MOV-19** Loop infinito só funcional (carregador, progresso, status real) ou marquee decidido
  (MOV-20); movimento perpétuo (pulso, flutuar, digitar) só com MOVIMENTO ≥ 6 e quando a seção
  ganha com ele. Loop para fora da tela e em aba escondida; nada pisca acima de 3 Hz. (hallmark,
  taste, impeccable, uupm)
- **MOV-20** Marquee fora por padrão (o detector acusa `marquee`). Com pedido do usuário e
  MOVIMENTO ≥ 4: um por página, 24–60s por volta, pausa no hover e no foco (SLOP-29), parado em
  movimento reduzido mostrando os primeiros itens. (hallmark, taste, impeccable)
- **MOV-21** Sem cursor personalizado, sem seguidor de cursor, sem gradiente de fundo animado no
  hover. (hallmark, taste)
- **MOV-22** Um efeito de hover por elemento (SLOP-25); imagem não escala nem gira no hover (o
  detector acusa `image-hover-transform`). (hallmark, impeccable)

## Movimento reduzido e controle

- **MOV-23** Toda animação tem caminho em `prefers-reduced-motion: reduce` (SLOP-31): movimento
  espacial vira crossfade ≤ 150ms ou nada; loop, parallax, seção presa e física param; feedback de
  estado e progresso continuam, mais lentos. (hallmark, taste, impeccable, uupm)
- **MOV-24** Animação nunca bloqueia a entrada: é interrompível, o clique cancela a anterior e o
  estado final é gravado sem depender do fim da animação. (impeccable, uupm)
- **MOV-25** Com DENSIDADE ≥ 8, nenhuma coreografia de carga: o dado já aparece no lugar; só
  transição de estado e número que atualiza, anunciado uma vez por `aria-live="polite"`.
  (impeccable, hallmark)

## Por tipo de tela

### Persuadir

- MOVIMENTO 5: uma entrada orquestrada na dobra e até duas seções-chave com reveal único (vale
  MOV-03, MOV-15); entrada autoral até 800ms (vale MOV-08).
- Marquee só com pedido (vale MOV-20); parallax fora (vale MOV-17).

### Operar

- MOVIMENTO 3: sem entrada coreografada; movimento só de feedback, estado e continuidade, rápido
  (vale MOV-12, MOV-25).
- Nenhum loop decorativo; carregador e progresso seguem MOV-19.

### Ler

- MOVIMENTO 2: página parada; nenhum reveal no corpo (vale MOV-15), transição só de estado.

### Experiência

- MOVIMENTO 7: o movimento pode carregar a voz; blur, máscara e `clip-path` no momento autoral
  (vale MOV-05).
- Parallax e seção presa só com MOVIMENTO 8 ou mais declarado no `sistema.md` (vale MOV-17,
  LAY-14).
