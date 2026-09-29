# Verificação

Roteiro do passo 5, para tela nova, mockup ou tela existente em revisão. Entradas: a URL da tela
(rota de mockup no projeto React, como `http://localhost:<porta>/<rota>`, ou, sem React, o HTML
autocontido servido como diz VER-19) e o tipo de tela gravado em `docs/design/sistema.md`. O que muda com o tipo de tela
está em `## Por tipo de tela`; as contradições resolvidas, em [`fontes.md`](fontes.md).

## Ferramentas

- **VER-01** Playwright (MCP 0.0.82, servidor com `--snapshot-mode none`) navega, clica,
  redimensiona e fotografa: `browser_navigate`, `browser_click`, `browser_type`,
  `browser_press_key`, `browser_resize`, `browser_emulate_media` e `browser_take_screenshot` com
  `filename`. As ações não devolvem a árvore da página. (spec R6)
- **VER-02** Para clicar, o `target` recebe um seletor CSS único; `browser_snapshot` só quando
  precisar do `ref` de um elemento que nenhum seletor alcança, com `depth` baixo. (spec R6)
- **VER-03** Chrome DevTools (MCP 1.10.1, `--headless --isolated`, só os grupos de navegação,
  depuração e desempenho) só lê: `take_snapshot` para achar o `uid`, `get_css_styles`,
  `list_console_messages`, `lighthouse_audit` e `performance_start_trace`. Roda num navegador
  próprio, então abre a mesma URL com `navigate_page`. Nunca age na página: `click`, `fill`,
  `hover`, `press_key`, `resize_page`, `emulate` e `take_screenshot` ficam com o Playwright.
  (spec R4)
- **VER-04** Terminada a última rodada, feche o Playwright com `browser_close`. O Chrome DevTools
  fica como está: a última aba não fecha (`X/chrome-devtools-mcp/docs/tool-reference.md:206`) e,
  com `--isolated`, o navegador dura o mesmo que a sessão; não há passo para ele. (spec R4)
- **VER-19** Servidor. Em projeto sem React, o HTML autocontido não abre por `file://`: o
  Playwright MCP recusa o protocolo. Sirva a pasta do HTML por HTTP local, em segundo plano,
  rodando nela `python3 -m http.server <porta> --bind 127.0.0.1`, e use a mesma URL
  `http://127.0.0.1:<porta>/<arquivo>.html` no Playwright, no Chrome DevTools e no detector.
  Terminada a última rodada, pare o servidor.

## Rodada

Uma rodada são os passos abaixo, nesta ordem, com a tela servida na URL.

- **VER-05** Prints. `browser_navigate` na URL; `browser_resize` para 375×812 e
  `browser_take_screenshot` com `filename` `r<N>-375.png` e `fullPage: true`; depois 1440×900 e
  `r<N>-1440.png`. Os arquivos ficam na pasta da entrega. Na Vesta, é a pasta do mockup,
  `docs/vesta/mockups/<data>-<feature>/`, na fase de mockup, e
  `docs/vesta/mockups/<data>-<feature>/etapa-<id>/` numa etapa de tela da execução. Nos dois,
  conferir rolagem horizontal, texto clicável quebrado e a dobra (LAY-15, LAY-22). Estado que só aparece com ação (erro de formulário, menu
  aberto, foco pelo Tab) se provoca com `browser_click`, `browser_type` ou `browser_press_key` e
  ganha print próprio; `browser_emulate_media` com `reducedMotion: "reduce"` e, com dois modos,
  `colorScheme: "dark"` também ganham print (MOV-23, COR-20).
- **VER-06** Elementos. No Chrome DevTools, `navigate_page` na mesma URL e `take_snapshot` para
  achar o `uid` do título principal, de um parágrafo do corpo e do botão principal. O `filePath`
  do `take_snapshot` fica dentro da pasta do projeto (em /tmp ou no scratchpad, o MCP recusa com
  `Access denied`), e o arquivo é apagado depois de achar os `uid`.
- **VER-07** CSS. `get_css_styles` em cada `uid` (título, corpo, botão principal) devolve as
  regras que casam, da maior para a menor precedência, com arquivo e linha; a declaração que vale
  vem sem marca e a vencida vem marcada `[overloaded]`. Conferir na que vale: família e tamanho
  por token (TIP-23, SLOP-09), corpo ≥ 16px com entrelinha 1.5–1.65 (TIP-12), cor e fundo por
  token semântico (COR-02), botão com altura ≥ 44px (LAY-26) e estados declarados (SLOP-30). O
  CSS lido vale na largura do navegador do Chrome DevTools; o que muda em outra largura se confere
  no print.
- **VER-08** Console. `list_console_messages` sem nenhum erro; recurso que falhou (fonte ou imagem
  404) conta como erro. Aviso vai ao relatório com a origem.
- **VER-09** Lighthouse e desempenho. Em Persuadir e Ler, `lighthouse_audit` com
  `mode: "navigation"`, uma vez com `device: "mobile"` e outra com `"desktop"`: toda auditoria de
  acessibilidade reprovada é corrigida; SEO e boas práticas reprovadas são corrigidas ou vão ao
  relatório com motivo. Depois, `performance_start_trace` com `reload` e `autoStop`: LCP < 2.5s,
  CLS < 0.1 e INP < 200ms (`X/taste-skill/skills/taste-skill/SKILL.md:976`). Operar e Experiência
  não rodam `lighthouse_audit`; Experiência com MOVIMENTO ≥ 7 roda o trace.
- **VER-10** Detector na página renderizada, nunca nos arquivos-fonte:
  `ferramentas/impeccable/detectar --json --viewport 375x812 <url>` e
  `ferramentas/impeccable/detectar --json --viewport 1440x900 <url>`, em que `<url>` é a rota de
  mockup no React ou, sem React, `http://127.0.0.1:<porta>/<arquivo>.html` do servidor HTTP local
  (VER-19). Sai 0 sem achado e 2 com achados; exceção
  decidida em `fontes.md` já vem de `ferramentas/impeccable/excecoes.json` e não alarma. Sem o
  binário ou sem Chrome na máquina, a reserva roda na página aberta no Playwright:
  `browser_run_code_unsafe` com `page.addScriptTag({ path })` no caminho absoluto de
  `ferramentas/impeccable/reserva/detect-antipatterns-browser.js`, depois
  `window.impeccableDetectAsync()`; ela perde 4 regras de texto, e o relatório diz isso. A
  reserva não lê `excecoes.json`: grave o JSON que ela devolve e passe por
  `ferramentas/impeccable/filtrar.py <arquivo>` (ou pelo stdin) antes de tratar os alarmes; ele
  imprime o resto no mesmo formato e sai 0 sem achado e 2 com achados, como o `detectar`.
  Grave a saída de cada `detectar --json` na pasta da entrega, em `r<N>-detector-375.json` e
  `r<N>-detector-1440.json`, com o mesmo N dos prints de VER-05. Na reserva, a saída do
  `filtrar.py` vai para os mesmos nomes.
- **VER-11** Alarme. Todo alarme do detector é corrigido ou refutado com prova: o CSS de
  `get_css_styles` (a declaração que vale, com arquivo e linha) ou o print que mostra o contrário.
  A refutação entra na entrega com a prova ao lado; alarme de gosto que o usuário pediu (marquee,
  eyebrow) se refuta citando o pedido. Motivo: os falsos positivos relatados (impeccable #633,
  #428, #837) vinham de ler o código-fonte e adivinhar o resultado.
- **VER-12** Contraste. Alarme de contraste (`low-contrast`) só se refuta com as cores efetivas do
  texto e do fundo lidas no Chrome DevTools (a declaração que vale de `color` no elemento e de
  `background-color` no ancestral que pinta o fundo, em `get_css_styles`) e a razão calculada
  com elas; nunca pelo print nem pelo código-fonte.
- **VER-13** Itens `[olho]` de `referencias/slop.md`: cada um contra os prints e o CSS lido;
  passou, ou vira correção.
- **VER-14** Lista de `referencias/ux.md`: estados (UX-01 a UX-10, provocados no Playwright ou
  vistos na prévia de estados; sem como provocar, entra no relatório como não conferido),
  formulário, teclado (Tab pela página com `browser_press_key`, foco visível no print), ação
  destrutiva e, em revisão de tela existente, a crítica heurística com as notas.
- **VER-15** Rotação. Em Persuadir e Experiência, a tela tem entrada em `docs/design/rotacao.json`,
  gravada por `ferramentas/rotacao.py registrar` no passo 3; sem entrada, a rodada falha e volta
  ao passo 3. Operar e Ler não passam por `rotacao.json`.
- **VER-16** Relatório. Cada rodada termina num relatório: número da rodada, caminhos dos prints,
  ids das regras conferidas (ao menos todos os do `## Piso` do `SKILL.md`, mais os que a rodada
  tocou), cada um com passou ou falhou, alarmes do detector com a correção ou a refutação e sua
  prova, console e, quando rodam, Lighthouse e trace. Grave o relatório em `relatorio.md` na pasta
  da entrega. A rodada nova reescreve o mesmo arquivo.

## Limite e entrega

- **VER-17** No máximo 3 rodadas: a primeira acha, as correções entram em lote, a seguinte
  confere. Depois da terceira, o que sobrou vai na entrega com o id da regra, o que falhou e por
  quê. Acessibilidade e contraste nunca sobram: sem corrigir, não entrega. (spec A6; o
  impeccable para antes, ver fontes.md)
- **VER-18** A entrega traz os prints 375 e 1440 da última rodada, o último relatório e cada
  refutação com a prova.
- **VER-20** Correção feita depois da 3ª rodada não sai só com a largura conferida: sobre a versão
  corrigida, prints nas duas larguras, detector nas duas larguras e console sem erro. O relatório
  marca a correção como pós-rodada.

## Por tipo de tela

### Persuadir

- `lighthouse_audit` e trace rodam (vale VER-09); rotação conferida em `rotacao.json` (vale
  VER-15); na crítica, heurísticas 7 e 10 podem ficar `n/a`.

### Operar

- Sem `lighthouse_audit` e sem conferência de `rotacao.json` (vale VER-09, VER-15); estados com
  dado (vazio, esqueleto, erro por bloco) provocados no Playwright pesam mais que tudo.

### Ler

- `lighthouse_audit` roda, com acessibilidade e SEO pesando mais (vale VER-09); `rotacao.json`
  não se confere (vale VER-15). Contraste do corpo conferido contra o alvo de 7:1 (COR-14).

### Experiência

- Rotação conferida (vale VER-15); sem `lighthouse_audit`, e o trace roda com MOVIMENTO ≥ 7 (vale
  VER-09). Print com `reducedMotion: "reduce"` obrigatório (vale VER-05, MOV-23).
