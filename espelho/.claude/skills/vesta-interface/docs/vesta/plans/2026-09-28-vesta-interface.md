# Plano — vesta-interface

- **Objetivo:** criar a skill `vesta-interface`, que funde hallmark, taste-skill, impeccable,
  ui-ux-pro-max, shadcn, Chrome DevTools MCP, Playwright MCP e inspo num fluxo único, e
  acoplá-la à Vesta no lugar de hallmark + inspo.
- **Spec:** `docs/vesta/specs/2026-09-28-vesta-interface-design.md` (revisada pelo grill).
- **Comando de teste** (raiz de `~/Code/vesta-interface`):
  `python3 -m unittest discover -s test -v && cd ~/Code/vesta && python3 -m unittest discover -s test -v && python3 -m unittest discover -s skill/scripts -v`
- **Pastas de tela:** nenhuma.
- **Mockup:** nenhum: sem tela (a entrega é texto de skill, scripts e configuração).

Siglas de caminho usadas abaixo:
- **R** = `~/Code/vesta-interface` (este repositório).
- **V** = `~/Code/vesta`.
- **X** = `~/Code/ux-lab/vendor` (fontes congeladas, só leitura; fica dentro do repositório git
  `~/Code/ux-lab`, mas `vendor/` é ignorado ali).
- **H** = `~/.claude/skills/hallmark` (pasta real, não link; some na etapa 13). Tudo que for
  citado em arquivo do repositório aponta para `X/hallmark/`, nunca para `H`, para a citação
  sobreviver à remoção.
- **C** = `docs/vesta/research/2026-09-28-conflitos-entre-fontes.md` (saída completa do agente de
  conflitos, em inglês: ~64 contradições com `arquivo:linha` dos dois lados, capacidades que o
  fluxo deixa de fora, regras em 3+ fontes).

Todos os testes deste repositório são `unittest` da stdlib, em `R/test/test_*.py`, com uma
docstring de uma linha no topo dizendo a etapa, no padrão de `V/test/test_sem_wayfinder.py:1`.
Constante `RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`.

---

## Etapa 0 — Esqueleto testável e cópia de segurança do hallmark

- **Tela:** não.
- **Arquivos:** criar `R/test/test_esqueleto.py`, `R/README.md`, `R/.gitignore`; copiar `H/`
  inteiro para `X/hallmark/`.
- **O que prova a etapa:**
  - `R/README.md` existe e cita o caminho da spec.
  - `X/hallmark/SKILL.md` existe e `X/hallmark/` tem 107 arquivos (constante no teste, não
    comparação com `H` ao vivo: `H` some na etapa 13 e o teste precisa continuar passando).
    Enquanto `H` existir, `X/hallmark/SKILL.md` é igual byte a byte a `H/SKILL.md` (pula com
    motivo quando `H` não existe). Isso garante que a fonte do hallmark sobrevive à remoção.
  - `.gitignore` ignora `__pycache__/` e `.DS_Store`.
- **Como fazer:** `[ -e ~/Code/ux-lab/vendor/hallmark ] || cp -R ~/.claude/skills/hallmark ~/Code/ux-lab/vendor/hallmark`
  (rodar `cp -R` duas vezes criaria `X/hallmark/hallmark`). README curto: o que é a skill, uma
  linha; como instalar (`./install.sh`); onde está a spec. O teste compara com
  `filecmp.cmp(shallow=False)` e conta com `os.walk`.

## Etapa 1 — Busca do ui-ux-pro-max em `ferramentas/uupm/`

- **Tela:** não.
- **Arquivos:** copiar `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/scripts/{search.py,core.py,design_system.py,reasoning_contract.py}`
  para `R/ferramentas/uupm/scripts/` e a pasta `data/` inteira para `R/ferramentas/uupm/data/`,
  exceto `phosphor-icons-upstream.json`, `google-font-licenses.json` e `data-provenance.json`
  **se** nenhum dos quatro scripts copiados os abrir (conferir com `grep -n` antes; se abrir,
  copia). Criar `R/test/test_uupm.py`.
- **O que prova a etapa:**
  - `search.py "fintech banking dashboard" --design-system --format markdown` sai com código 0 e
    a saída contém `### Style`, `### Typography` e ao menos uma cor em hex (`#[0-9A-Fa-f]{6}`).
  - `search.py "form validation error" --domain ux -n 2 --json` devolve JSON válido, um objeto
    `{count, results}`, com `len(d["results"]) == 2`.
  - `search.py "dialog form" --stack shadcn -n 1 --json` devolve `len(d["results"]) == 1`.
  - Rodar de outra pasta (cwd = `/tmp`) funciona igual: caminhos são relativos ao script
    (`core.py:15`).
  - Nenhum script copiado importa módulo fora da stdlib: o teste lê cada `.py`, extrai os
    `import`/`from` de topo e confere contra `sys.stdlib_module_names` mais os próprios módulos
    (`core`, `design_system`, `reasoning_contract`).
  - A saída ASCII padrão contém códigos ANSI; por isso a skill sempre usa `--format markdown`
    ou `--json` (teste: a saída com `--format markdown` não contém `\x1b[`).
- **Como fazer:** `subprocess.run([sys.executable, caminho, ...], capture_output=True, text=True, encoding='utf-8', cwd='/tmp')`.
  Não editar os scripts. Os três JSON excluídos só são abertos por `validate_data.py`, que não é
  copiado.

## Etapa 2 — Detector do impeccable travado, com reserva WASM

- **Tela:** não.
- **Arquivos:** copiar `X/impeccable/.claude/skills/impeccable/scripts/impeccable` e
  `scripts/VERSION` (conteúdo `0.1.6`) para `R/ferramentas/impeccable/`; copiar
  `X/impeccable/crates/live/assets/detect-antipatterns-browser.js` para
  `R/ferramentas/impeccable/reserva/`; copiar 3 fixtures de
  `X/impeccable/tests/fixtures/antipatterns/` para `R/test/fixtures/detector/`, com o mapa
  explícito (tirado dos goldens `X/impeccable/tests/oracle/golden/detect-fixture-json-*.json`):
  `should-pass.html` → nenhum achado; `css-in-prose-should-flag.html` → `gradient-text` e
  `ai-color-palette`; `placeholder-contrast.html` → `low-contrast`. Criar
  `R/ferramentas/impeccable/detectar` (script shell) e `R/test/test_detector.py`.
- **O que prova a etapa:**
  - `detectar --json <should-pass.html>` sai com 0 e JSON `[]`.
  - `detectar --json <fixture>` sai com 2 e o JSON tem achados com `antipattern` igual a cada
    regra do mapa acima.
  - Arquivo inexistente: sai com 1.
  - A versão travada vence: com `HOME` e `IMPECCABLE_HOME` temporários, um executável falso em
    `<IMPECCABLE_HOME>/bin/0.1.6/impeccable` que imprime `falso-0.1.6`, e outro falso em
    `<IMPECCABLE_HOME>/bin/impeccable` (sem versão) que imprime `errado`, `detectar --version`
    imprime `falso-0.1.6`.
  - A reserva existe e contém a string `impeccableDetect`.
  - Página renderizada: `detectar --json --viewport 375x812 file://<css-in-prose-should-flag.html>`
    e o mesmo com `1440x900` saem com 2 e acusam `gradient-text`; `file://<should-pass.html>` sai
    com 0. É o modo que a verificação usa (motor de navegador do binário, Chrome sem janela
    achado nos locais padrão ou em `CHROME_PATH`; `X/impeccable/crates/cli/src/main.rs:136-143`).
    Pula com motivo quando não há Chrome na máquina.
- **Como fazer:** o lançador copiado (`scripts/impeccable:41-197`) procura `$IMPECCABLE_BIN`,
  `bin/<os>-<arch>`, `~/.impeccable/bin/impeccable` (sem versão), PATH, depois o cache versionado
  `~/.impeccable/bin/<VERSION>/impeccable`, e só então baixa da release `engine-v<VERSION>` com
  sha256. A versão vem só do arquivo `VERSION` ao lado do lançador. Um binário sem versão em
  `~/.impeccable/bin` furaria a trava, por isso `detectar` (shell curto) faz: se
  `${IMPECCABLE_HOME:-~/.impeccable}/bin/$(cat VERSION)/impeccable` existe, exporta
  `IMPECCABLE_BIN` apontando para ele; senão chama o lançador, que baixa essa versão. Antes de
  escrever o teste, rode `ferramentas/impeccable/impeccable --version` uma vez para baixar o
  binário 0.1.6 (é a instalação real que o `install.sh` fará). Se o download falhar, pare e
  reporte: a reserva WASM é para uso da skill, não substitui a prova. Contrato do CLI:
  `X/impeccable/docs/CLI-CONTRACT.md:110-167` (0 limpo, 2 achados, 1 falha; `--json` no stdout).
  O clone em X está fora da tag `engine-v0.1.6`, mas os arquivos de detect, ignores e fontes são
  iguais aos da tag.

## Etapa 3 — Exceções do detector

- **Tela:** não.
- **Arquivos:** criar `R/ferramentas/impeccable/excecoes.json` e `R/test/fixtures/detector/geist.html`;
  ampliar `R/ferramentas/impeccable/detectar` para aplicar as exceções; ampliar
  `R/test/test_detector.py`.
- **O que prova a etapa:**
  - `geist.html` é `should-pass.html` com só a fonte do corpo trocada para `Geist`: sem
    exceções (`--no-config`), `detectar` acusa `overused-font`; com `excecoes.json` (padrão do
    `detectar`), sai com 0. Idem para `Geist Mono`.
  - Cada entrada de `excecoes.json` tem `regra`, `valor` e `motivo` não vazio.
  - As fontes permitidas pela decisão 5 da spec (Geist, Geist Sans, Geist Mono, Fraunces, Space
    Grotesk, Plus Jakarta Sans, Instrument Serif) estão todas em `excecoes.json`.
  - As fixtures da etapa 2 continuam acusando o mesmo: exceção não desliga regra inteira.
  - Rodar `detectar` de dentro de um projeto que tem `.impeccable/config.json` próprio não muda o
    resultado.
- **Como fazer:** o CLI 0.1.6 lê ignores só de `.impeccable/config.json` na pasta corrente
  (`crates/common/src/lib.rs:44`, `cli.rs:420-423`); não há flag nem variável para outro caminho.
  `detectar` cria uma pasta temporária, gera nela `.impeccable/config.json` a partir de
  `excecoes.json` (formato: o que `impeccable ignores add-value <regra> <valor> --reason "..."`
  grava, conferir rodando uma vez numa pasta temporária), converte os argumentos em caminhos
  absolutos e roda o binário com essa pasta como corrente. O código de saída do binário já sai
  certo. A lista real de fontes da regra está em `X/impeccable/crates/foundation/src/constants.rs:85-105`.

## Etapa 4 — Licenças e atribuição

- **Tela:** não.
- **Arquivos:** criar `R/LICENSE` (MIT, titular luccas-silveira, 2026), `R/THIRD_PARTY_NOTICES.md`,
  `R/licencas/` com o texto de licença de cada fonte, `R/licencas/impeccable-NOTICE.md` (cópia de
  `X/impeccable/NOTICE.md`); criar `R/test/test_licencas.py`.
- **O que prova a etapa:**
  - `THIRD_PARTY_NOTICES.md` tem uma seção para cada uma das 8 fontes: hallmark, taste-skill,
    impeccable, ui-ux-pro-max, shadcn/ui, chrome-devtools-mcp, playwright-mcp, inspo; cada
    seção tem licença, URL do repositório e commit.
  - Os commits citados batem com `git -C X/<repo> rev-parse --short HEAD` para os seis que são
    clones (impeccable `9d715cc`, ui-ux-pro-max-skill `09170ee`, taste-skill `ce26fc2`, ui
    `db2db46`, chrome-devtools-mcp `89eb3d5`, playwright-mcp `e87bb89`). O teste só confere se
    `X/<repo>` existir (skip com motivo quando a pasta sumiu). hallmark cita `Nutlope/hallmark`
    commit `13ac0ec` (não é clone; conferido por igualdade do `SKILL.md` remoto). inspo fica
    isento de repositório e commit.
  - Todo arquivo citado em `licencas/` existe e não está vazio.
  - O `NOTICE.md` do impeccable está copiado byte a byte.
- **Como fazer:** hallmark é `Nutlope/hallmark`, MIT; o texto vem de
  `gh api repos/Nutlope/hallmark/license --jq .content | base64 -d`. shadcn/ui usa `LICENSE.md`,
  não `LICENSE`. inspo é serviço sem código copiado: a seção diz isso e não precisa de arquivo
  de licença.

## Etapa 5 — Catálogo

- **Tela:** não.
- **Arquivos:** copiar de `X/hallmark/references/` para `R/catalogo/`, mantendo a mesma posição
  relativa: `components/` (50), `macrostructures/` (21), `macrostructures.md`, `themes/` (5),
  `genres/` (4), e os cinco arquivos de apoio que o catálogo linka (`component-cookbook.md`,
  `hero-enrichment.md`, `assets.md`, `custom-craft.md`, `floating-nav.md`), para os links
  internos continuarem valendo. Copiar
  `X/taste-skill/skills/{minimalist-skill,soft-skill,brutalist-skill}/SKILL.md` para
  `R/catalogo/direcoes/{minimalista,sofisticada,brutalista}.md`; criar `R/catalogo/README.md`
  e `R/test/test_catalogo.py`.
- **O que prova a etapa:**
  - Contagens: 50 componentes, 21 macroestruturas, 5 temas, 4 gêneros, 3 direções.
  - Nenhum link Markdown aponta para `site/` (os 5 links dos temas carnival, cobalt, hum e lumen
    para `site/css/tokens.css` e `site/examples/` são removidos). `components/s3-sticky-pinned.md`
    cita `tokens.css` como arquivo de saída legítimo e fica.
  - Todo link Markdown relativo dentro de `catalogo/` aponta para arquivo que existe.
  - `catalogo/README.md` lista os 5 temas que existem e diz que os outros nomes de tema citados
    no catálogo (Studio, Bloom, Midnight…) não existem nesta cópia.
  - Cada direção começa com um bloco "Limites" dizendo que contraste ≥ 4.5:1, texto ≥ 12px e
    acessibilidade não cedem; nenhuma das três direções tem tamanho de texto abaixo de 12px (o
    teste procura `\b(10|11)(\.\d+)?px`, `text-\[(10|11)px\]` e `0\.[0-6]\d*rem`; hoje há
    `brutalista:39` com `10px`/`0.7rem` e `sofisticada:52` com `text-[10px]`).
  - As direções não têm frontmatter de skill (`name:`), para não serem carregadas como skills.
  - Todo nome citado numa linha `shadcn:` existe em `X/ui/apps/v4/registry/new-york-v4/ui/`
    (61 componentes). O teste não exige a linha em nenhum componente: a maioria dos blocos do
    hallmark (feature, hero, navegação editorial) não tem equivalente e não ganha linha.
- **Como fazer:** Nas direções, remover o frontmatter, trocar tamanhos abaixo de 12px por 12px
  (`0.75rem`), e escrever no topo "Limites". Não editar as menções a temas inexistentes (são
  muitas; o README avisa). Nota shadcn: uma linha `shadcn: <componente>[, <componente>]` logo
  abaixo do título, só quando o bloco é de fato montado com aquele componente (ex.: menu → 
  `navigation-menu`, `sheet`; formulário inline → `input`, `button`), com nomes da pasta do
  registro acima (ou `npx shadcn@4.21.0 list @shadcn`; sem o `@shadcn` o comando sai com erro).

## Etapa 6 — Referências: slop, tipografia, cor

- **Tela:** não.
- **Arquivos:** criar `R/referencias/{slop,tipografia,cor}.md` e `R/referencias/fontes.md`
  (começa aqui, cresce nas etapas 7 e 8); criar `R/test/test_referencias.py`.
- **O que prova a etapa:**
  - Cada arquivo tem uma seção `## Por tipo de tela` com as quatro subseções
    `### Persuadir`, `### Operar`, `### Ler`, `### Experiência`.
  - Toda regra é um item com id estável `SLOP-01`, `TIP-01`, `COR-01`… e nenhum id se repete
    entre arquivos.
  - As decisões fixadas da spec estão presentes: `tipografia.md` permite Geist/Fraunces/Space
    Grotesk por tipo de tela e remete a `ferramentas/impeccable/excecoes.json`; `slop.md` permite
    travessão com moderação; `cor.md` trata modo escuro por tipo de tela (Operar ganha os dois).
  - `fontes.md` tem uma entrada por contradição resolvida nesses três temas, cada uma com as
    duas versões citadas (`fonte:arquivo:linha`), a decisão e o nível da regra de desempate que
    decidiu (tipo de tela / verificável / hallmark). Mínimo: Inter, Geist, Fraunces, serif
    padrão, número de famílias, escala de tamanhos, peso de título, itálico, travessão,
    ponto médio, glifo como ícone, emoji, espaço de cor, dose de acento, neutros, branco puro,
    creme, gradientes, modo escuro, acento no escuro, Space Grotesk/Plus Jakarta/Outfit, pilha
    do sistema, tracking e entrelinha do display, tamanho máximo do display, tamanho mínimo de
    texto, texto claro no escuro, alvo de contraste do corpo — 27 entradas. As citações apontam
    para `X/hallmark/…`, nunca para `H`.
  - `slop.md` cita cada um dos 58 gates de `X/hallmark/references/slop-test.md` (`gate N`, de 1
    a 58, ao menos uma vez), cada item com gate marcado `[detector]` ou `[olho]`, e todo item
    `[detector]` nomeia uma regra que existe em `X/impeccable/crates/live/assets/antipatterns.json`
    (o teste lê o JSON; pula com motivo se X sumiu).
  - Cada arquivo tem no máximo 400 linhas (carrega sob demanda; limite de custo).
- **Como fazer:** a lista de contradições com `arquivo:linha` dos dois lados está no dossiê
  `docs/vesta/research/2026-09-28-vesta-interface-research.md` (A3, A4) e, completa, em **C**
  (seção 1, ~64 tópicos; as listas das etapas 6, 7 e 8 somam 64 e cobrem todos); as fontes são `X/hallmark/references/{typography,color,anti-patterns,slop-test,copy}.md`,
  `X/taste-skill/skills/taste-skill/SKILL.md`, `X/impeccable/.claude/skills/impeccable/reference/{craft-floor,new-work,typeset,colorize}.md`,
  `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/{quick-reference,pro-rules}.md`.
  Regra que aparece em 3+ fontes é escrita uma vez. Desempate: tipo de tela, depois mais
  verificável, depois hallmark. Contradição interna de uma fonte (ex.: hallmark OKLCH-only vs
  hex no exemplo) também vai para `fontes.md`. Escrever em português, regras curtas e
  verificáveis ("contraste ≥ 4.5:1"), sem copiar parágrafos inteiros. `slop.md` destila também
  os 58 gates de `X/hallmark/references/slop-test.md`, marcando com `[detector]` os que o
  detector cobre (lista de regras em `X/impeccable/crates/live/assets/antipatterns.json`) e com
  `[olho]` os que exigem julgamento no print.

## Etapa 7 — Referências: layout, movimento, componentes

- **Tela:** não.
- **Arquivos:** criar `R/referencias/{layout,movimento,componentes}.md`; ampliar
  `R/referencias/fontes.md`; ampliar `R/test/test_referencias.py`.
- **O que prova a etapa:**
  - Mesmas regras estruturais da etapa 6 (seções por tipo de tela, ids únicos `LAY-`, `MOV-`,
    `COMP-`, ≤ 400 linhas).
  - `layout.md` e `movimento.md` abrem com a seção `## Botões`: os três botões do taste
    (`VARIACAO`, `MOVIMENTO`, `DENSIDADE`, de 1 a 10; origem `X/taste-skill/skills/taste-skill/SKILL.md:45-78`),
    uma tabela de padrão por tipo de tela (Persuadir, Operar, Ler, Experiência) e as regras que
    cada faixa liga ou desliga. Toda regra de layout ou movimento que depende de faixa cita o
    botão pelo nome exato (o teste procura os três nomes nos dois arquivos).
  - `layout.md` inclui espaçamento, responsivo e z-index; `componentes.md` remete ao catálogo
    (`catalogo/components/`) e fixa Lucide como ícone padrão.
  - `componentes.md` diz que em projeto React o componente vem do shadcn pelo CLI travado
    (`npx shadcn@4.21.0 search @shadcn <termo>`, `view`, `docs`, `add --dry-run` e depois `add`;
    nunca `shadcn@latest`, nunca MCP) e nunca fica no estado padrão do shadcn (taste `T:627`), e
    que projeto sem `components.json` roda `npx shadcn@4.21.0 init` antes. O teste confere que
    toda chamada `shadcn` citada no repositório tem `@4.21.0`.
  - `fontes.md` ganha as contradições de layout e movimento: centralização, eyebrow, números de
    seção, card aninhado, raio, escala de espaço, breakpoints, z-index, sombras, janela falsa,
    texto do hero, navegação, imagem, conteúdo inventado, propriedades animadas, durações,
    easing, reveal no scroll, stagger, movimento reduzido, parallax, marquee, mudança
    instantânea, listener de scroll, Lucide (`T:623` só a pedido; spec decisão 1 fixa como
    padrão), SVG desenhado à mão — 26 entradas a mais (53 no total).
- **Como fazer:** fontes em `X/hallmark/references/{layout-and-space,responsive,motion,microinteractions,structure,component-cookbook}.md`,
  taste `T`, impeccable `reference/{layout,animate,adapt}.md`, ui-ux-pro-max
  `references/quick-reference.md`. Mesmo método da etapa 6.

## Etapa 8 — Referências: UX, verificação e crítica

- **Tela:** não.
- **Arquivos:** criar `R/referencias/{ux,verificacao}.md`; ampliar `fontes.md` e
  `test_referencias.py`.
- **O que prova a etapa:**
  - As nove referências da spec existem.
  - `ux.md` tem: estados (vazio, erro, carregando, sucesso, desabilitado, foco), formulários,
    acessibilidade, ação destrutiva (reversível → desfazer; irreversível → confirmação), e a
    crítica heurística (as 10 heurísticas de Nielsen com o que olhar em cada).
  - `verificacao.md` descreve as rodadas, na ordem: prints Playwright em 375 e 1440 de largura;
    Chrome DevTools `take_snapshot` para achar o `uid` e `get_css_styles` (devolve as regras
    que casam, com as vencidas marcadas `[overloaded]`) nos elementos de título, corpo e botão
    principal,
    `list_console_messages` sem erro, `lighthouse_audit` só em Persuadir e Ler; detector na
    página renderizada, não nos arquivos-fonte (`ferramentas/impeccable/detectar --json
    --viewport 375x812 <url>` e `1440x900`; a URL é a rota de mockup no React ou `file://` do
    HTML); itens `[olho]` do `slop.md`; lista de `ux.md`; em Persuadir e Experiência, a tela
    tem entrada em `docs/design/rotacao.json`.
  - `verificacao.md` diz que todo alarme do detector é corrigido ou refutado com prova (CSS de
    `get_css_styles` ou o print), e a refutação aparece na entrega com a prova. Alarme de
    contraste só se refuta com as cores efetivas lidas no Chrome DevTools. Motivo: os falsos
    positivos relatados (impeccable #633, #428, #837) vinham de ler o código-fonte e adivinhar o
    resultado.
    Limite de 3 rodadas; acessibilidade e contraste nunca sobram. O relatório de cada rodada
    lista os ids das regras conferidas (ao menos todos os do `## Piso` do `SKILL.md`).
  - `verificacao.md` divide as ferramentas sem sobreposição: Playwright navega, clica,
    redimensiona e tira os prints (`browser_take_screenshot` com `filename`; `browser_snapshot`
    só quando precisar do `ref` para clicar, porque o servidor roda com `--snapshot-mode none`);
    Chrome DevTools só lê (CSS, console, Lighthouse, trace de
    desempenho). Manda fechar o Playwright ao terminar (`browser_close`). O Chrome DevTools não
    tem como fechar o navegador (a última aba não fecha, `X/chrome-devtools-mcp/docs/tool-reference.md:206`);
    com `--isolated` ele vive enquanto durar a sessão, e `verificacao.md` não manda fechá-lo.
  - `fontes.md` ganha: ação destrutiva, feedback de sucesso, duração de toast, indicador de
    carregamento, alvo de toque, escala ao pressionar, perguntas antes de desenhar, rodadas de
    verificação, metadado no código, insistência do usuário, escolha de design system — 11 a
    mais (64 no total). O teste confere o mínimo de 64 entradas.
- **Como fazer:** fontes em `X/impeccable/.claude/skills/impeccable/reference/{critique,audit,harden,onboard,clarify}.md`,
  `X/hallmark/references/interaction-and-states.md`, `X/ui-ux-pro-max-skill/.../references/*.md`,
  e a lista de ferramentas do Chrome DevTools em `X/chrome-devtools-mcp/docs/tool-reference.md`.

## Etapa 9 — SKILL.md e script de rotação

- **Tela:** não.
- **Arquivos:** criar `R/SKILL.md` e `R/modos/{estudo,componente,ajustes}.md`; criar
  `R/ferramentas/rotacao.py` (só stdlib); criar `R/test/test_skill.py` e `R/test/test_rotacao.py`.
- **O que prova a etapa:**
  - Frontmatter com `name: vesta-interface` e `description` (mais `when_to_use`, se houver) de
    até 1536 caracteres somados, com o caso principal (desenhar ou revisar
    interface/tela/componente) na primeira frase.
  - `SKILL.md` tem menos de 500 linhas.
  - `SKILL.md` tem uma seção `## Piso` com as regras que aparecem em 3 ou mais fontes (**C**,
    seção 4; cerca de 40), uma linha cada, começando pelo id da regra (`SLOP-03 …`). Todo id do
    piso existe em algum `referencias/*.md`, e nenhum id do piso se repete. Motivo: a comunidade
    relata que o agente raramente abre referências (ktlesr; ui-ux-pro-max #484), então o que
    vale sempre fica no arquivo que ele com certeza lê.
  - Cada passo de `SKILL.md` diz, no imperativo, qual referência abrir antes de seguir ("Abra
    `referencias/cor.md` agora"), e o teste confere que os passos 3 e 5 citam ao menos uma
    referência cada.
  - Os cinco passos da spec aparecem como seções numeradas, na ordem: entender, referências,
    sistema visual, construção, verificação.
  - O passo 1 contém: varredura do projeto existente; classificação no tipo de tela; a
    bifurcação com/sem questionário (tela nova → com; tela existente → direto; perguntas livres
    no chat, uma por vez, com recomendação; direto mostra as respostas deduzidas junto do
    resultado); a busca `ferramentas/uupm/scripts/search.py --format markdown` com veto pelas
    regras.
  - O passo 1 fixa os três botões (`VARIACAO`, `MOVIMENTO`, `DENSIDADE`) pelo tipo de tela; no
    questionário, o usuário pode mudá-los.
  - `rotacao.py registrar --projeto <pasta> --tela <nome> --tipo <Persuadir|Operar|Ler|Experiência> --macro <id> --menu <id> --rodape <id>`
    grava em `<pasta>/docs/design/rotacao.json` (lista, mais novo primeiro, no máximo 20).
    Em Persuadir e Experiência, sai com 1 e diz o que repetiu quando a macroestrutura, o menu
    ou o rodapé é igual ao de alguma das 3 últimas entradas desses dois tipos; em Operar e Ler,
    grava sem conferir (telas de app repetem menu e rodapé de propósito, que vêm do
    `docs/design/sistema.md`). `rotacao.py ultimas --projeto <pasta>` imprime as 3 últimas de
    Persuadir/Experiência. Testes: primeira entrada grava; repetir o menu da penúltima página de
    Persuadir recusa; repetir numa tela de Operar grava; a quarta mais antiga não conta; o
    arquivo nunca passa de 20 entradas; pasta sem `docs/design/` é criada.
  - O passo 3, em Persuadir e Experiência, manda rodar `rotacao.py ultimas`, escrever a linha
    "Últimas: …; esta: …, porque …" (formato do hallmark, `X/hallmark/SKILL.md:317-323`) e
    registrar com `rotacao.py registrar` antes de construir; em Operar e Ler, menu e rodapé vêm
    do `sistema.md`. Motivo: a rotação é "a regra mais violada na prática" no próprio hallmark
    (`:294`), porque dependia do agente manter o log.
  - O passo 3 cita a rotação em `docs/design/rotacao.json` e o design system em
    `docs/design/sistema.md` (que guarda tipo de tela, direção e os três botões), com export para
    variáveis CSS do shadcn.
  - O passo 4 diferencia projeto React (CLI `shadcn@4.21.0`, rota de mockup dentro do app) de projeto sem
    React (HTML autocontido com o visual do shadcn).
  - Todo caminho relativo citado em `SKILL.md` e em `modos/*.md` existe no repositório.
  - Nenhum arquivo do repositório (fora de `catalogo/`, `licencas/`, `ferramentas/`,
    `THIRD_PARTY_NOTICES.md`, `docs/`) cita `~/.claude/skills/hallmark` nem chama comando
    `/impeccable` (regex `(^|[\s`(])/impeccable\b`, que não pega `ferramentas/impeccable/`).
  - `modos/ajustes.md` cobre os oito modos da spec (bolder, quieter, distill, harden, onboard,
    optimize, polish, delight), cada um dizendo quais passos roda (3 e 5).
- **Como fazer:** `SKILL.md` só tem o fluxo e aponta qual referência abrir em cada passo. Modo
  estudo destila `X/hallmark/references/study.md`; modo componente destila `H/SKILL.md:60-141`;
  ajustes destila os `reference/*.md` do impeccable de mesmo nome. Descrição no estilo das
  outras skills do usuário (português).

## Etapa 10 — install.sh

- **Tela:** não.
- **Arquivos:** criar `R/install.sh` e `R/test/test_install.py`.
- **O que prova a etapa** (com `CLAUDE_HOME` temporário e um `claude` falso no `PATH` que grava
  os argumentos recebidos num arquivo):
  - Cria o link `CLAUDE_HOME/skills/vesta-interface → R`; rodar duas vezes não muda nada; se
    havia pasta real no lugar, ela é guardada com sufixo `.antes-da-vesta-interface-<data>`.
  - Chama `claude mcp add --scope user` para `chrome-devtools` com
    `npx -y chrome-devtools-mcp@1.10.1 --headless --isolated --no-usage-statistics --no-performance-crux --categoryInput=false --categoryEmulation=false --categoryNetwork=false --categoryMemory=false`
    (ficam navegação, depuração e desempenho, cerca de 18 ferramentas em vez de 43;
    `X/chrome-devtools-mcp/docs/configuration.md:7-57`),
    e troca `playwright` para
    `npx -y @playwright/mcp@0.0.82 --headless --snapshot-mode none --user-data-dir ~/.cache/claude-navegador`
    (`--snapshot-mode none`: a árvore da página só vem quando o agente pede `browser_snapshot`,
    em vez de depois de toda ação; conferido no `--help` da 0.0.82)
    (remove antes de adicionar, para ser idempotente). Forma exata:
    `claude mcp remove --scope user <nome> || true` e
    `claude mcp add --scope user <nome> -- npx -y …`.
  - O `claude` falso sai com 1 quando recebe `mcp add` sem `--` antes de `npx`, e sai com 1 em
    `mcp remove` de nome que ainda não adicionou: o teste prova que o `install.sh` usa o
    separador e tolera a primeira remoção (com `set -eu`, sem `|| true`, a primeira instalação
    abortaria).
  - Nenhum argumento gravado registra o shadcn como MCP (o shadcn entra só como CLI travado;
    o MCP dele só devolve o comando de instalação, e na 4.21.0 a busca o imprime como
    `[object Promise]`, `X/ui/packages/shadcn/src/mcp/utils.ts:49`).
  - Nenhum argumento gravado contém `@latest`.
  - Não mexe no `CLAUDE_HOME/CLAUDE.md` (o `CLAUDE.md` falso do teste sai idêntico).
  - Chama `ferramentas/impeccable/detectar --version` (baixa o binário travado) e não falha a
    instalação se o download falhar: imprime `aviso:`.
  - Avisa (sem falhar) quando o MCP `inspo` não está em `mcpServers` do `.claude.json`.
- **Como fazer:** seguir `V/install.sh:1-26` (`set -eu`, `CLAUDE_HOME`, `REPO`, função `ligar`)
  e o teste `V/test/test_install.py:22-50` (fixture com `.claude.json` falso). O `claude`
  falso é um shell em diretório temporário que faz `echo "$@" >> $LOG`, guarda os nomes
  adicionados num arquivo e aplica as duas recusas acima.

## Etapa 11 — Acoplamento à Vesta

- **Tela:** não.
- **Arquivos (em V):** mudar `skill/mockup.md`, `skill/SKILL.md:41`, `skill/execucao.md:80-82`,
  `install.sh:28-30`, `README.md:78-80,174`, `docs/dependencias.md:4`,
  `skill/scripts/painel.html:2-5`; mudar `test/test_mockup.py`, `test/test_install.py:27-29,113-128`,
  `test/test_docs.py:153`; criar `test/test_sem_hallmark.py`. Ficam como estão, porque só citam o
  inspo, que continua: `skill/research.md:38-42`, `README.md:66`, `install.sh:47-48`,
  `test/test_install.py:129-136`. Ficam também `docs/exemplo/` e `docs/vesta/mockups/*/`, que
  citam hallmark como registro do que foi feito (histórico).
- **O que prova a etapa:**
  - `test_sem_hallmark.py`: nenhum arquivo rastreado em `skill/`, `commands/`, `README.md`,
    `install.sh` cita `hallmark` (`docs/` inteiro fica de fora: decisões, exemplo e mockups são
    histórico).
  - `mockup.md` manda ler `~/.claude/skills/vesta-interface/SKILL.md`; oferece a bifurcação
    com/sem questionário; mantém as duas direções para tela nova (uma pode vir de
    `catalogo/direcoes/`); descreve o mockup React em rota do app com página de registro em
    `docs/vesta/mockups/<data>-<feature>/index.html` contendo prints celular e desktop e o link
    da rota; autoverificação passa a ser a de `referencias/verificacao.md` da vesta-interface.
  - `test_mockup.py` reescrito para as novas palavras: vesta-interface, questionário, direções,
    rota, prints, celular, desktop, 3 rodadas.
  - `research.md` continua chamando o inspo na frente de referências visuais (o inspo segue como
    MCP) mas sem citar hallmark.
  - `execucao.md` manda o implementador de etapa com tela ler a vesta-interface.
  - `install.sh` da Vesta avisa quando `vesta-interface` falta, no lugar de hallmark;
    `test_install.py` confere esse aviso.
  - `dependencias.md` lista vesta-interface; `test_docs.py:153` atualizado.
  - Todos os testes existentes da Vesta passam.
- **Como fazer:** padrão de teste de "não cita mais X": `V/test/test_sem_wayfinder.py`. Não mexer
  em `vesta.py` nem em `painel.py`: a trava e o painel já funcionam com a página de registro
  (`vesta.py:146-153` só exige o caminho no git; `painel.py:56` acha pastas datadas).

## Etapa 12 — ADR-0021 na Vesta

- **Tela:** não.
- **Arquivos (em V):** criar `docs/decisoes/0021-vesta-interface.md`; mudar
  `docs/decisoes/README.md` e `test/test_docs.py` (`HISTORIA`, `:170-177`). Em
  `~/Code/claude-tooling`: acrescentar em `docs/README.md` uma linha nova (hoje a 42, depois do
  bloco 39-41) com o ponteiro para o ADR-0021.
- **O que prova a etapa:**
  - O ADR começa com a linha de aviso histórico exigida por `V/test/test_docs.py:213-218`.
  - Tem `# ADR-0021 — ...`, a linha `Data: 2026-09-28. Status: em vigor. Reverte em parte o ADR-0018.`,
    `## Contexto`, `## A decisão`, `## O que se perde`.
  - `HISTORIA` ganha a entrada nova no fim e `decisoes/README.md` lista os links na mesma ordem
    (`test_readme_das_decisoes_lista_em_ordem`, `:232-236`).
  - O ADR-0018 não é alterado (regra da casa: ADR antigo nunca é reescrito).
- **Como fazer:** formato em `V/docs/decisoes/0018-mockup-e-frontend-na-vesta.md`. "O que se
  perde": modo live, imagem gerada, nativo, gráficos/stacks. A tupla nova em `HISTORIA` usa como
  original um caminho que não existe no claude-tooling; `test_resto_igual_ao_original` faz
  `continue` quando não há original (passa sem comparar), que é o efeito desejado.

## Etapa 13 — Instalação real, saída do hallmark e inventários

- **Tela:** não.
- **Arquivos:** criar `R/test/test_instalacao_real.py`. Rodar `R/install.sh` de verdade. Remover
  `~/.claude/skills/hallmark` (a cópia está em `X/hallmark` desde a etapa 0). Mudar
  `~/Code/claude-tooling/docs/reference/estado-atual.md:44-47` (vesta-interface nas skills
  próprias) e criar ali uma seção de MCPs com os travados (não existe hoje);
  `~/.claude/settings.json`, dentro de `permissions.allow` (linhas 13-42; as do Playwright estão
  em 17 e 28-34): trocar as regras `mcp__plugin_playwright_playwright__*` por uma só
  `mcp__playwright` (servidor inteiro; trocar só o prefixo geraria `browser_run_code` e
  `browser_install`, que não existem na 0.0.82), acrescentar `mcp__chrome-devtools` e
  `Bash(~/.claude/skills/vesta-interface/ferramentas/*)` (sem isso o lançador do detector é
  recusado quando a sessão não está em modo livre; impeccable #744);
  `~/Code/claude-kit/README.md:45,51,65-70` (tira hallmark, acrescenta vesta-interface e os MCPs;
  a linha 51 diz que o plugin playwright está ligado, e ele está desligado).
- **O que prova a etapa** (lê o sistema real; pula com motivo quando rodando fora desta máquina,
  detectado pela ausência de `~/.claude.json`):
  - `~/.claude/skills/vesta-interface` é link para `R`.
  - `~/.claude/skills/hallmark` não existe; `X/hallmark/SKILL.md` existe.
  - `~/.claude.json` tem `chrome-devtools` e `playwright` em `mcpServers`, nenhum com
    `@latest`, nas versões 1.10.1 e 0.0.82, e não tem `shadcn`. O `playwright` tem
    `--snapshot-mode none`.
  - O `chrome-devtools` em `~/.claude.json` tem as quatro flags `--category…=false`.
  - O binário do detector está em `~/.impeccable/bin/0.1.6/impeccable` e
    `ferramentas/impeccable/detectar --version` imprime 0.1.6.
  - `estado-atual.md` do claude-tooling cita vesta-interface; `claude-kit/README.md` não cita
    hallmark.
- **Como fazer:** seguir `V/test/test_instalacao_real.py`. Remover o hallmark com `rm -rf` só
  depois de o teste da etapa 0 passar de novo. Não rodar o `backup/sync.sh` do claude-tooling nem
  o do claude-kit: o próximo sync pega a mudança.

## Etapa 14 — Verificação por HTTP, snapshot no projeto e correção depois da 3ª rodada

- **Tela:** não.
- **Origem:** teste de pronto de 2026-09-28 (sessão em `~/Desktop/teste-vesta`). O Playwright MCP
  0.0.82 recusa `file://` (`Access to "file:" protocol is blocked`); o `take_snapshot` do Chrome
  DevTools com `filePath` fora da pasta do projeto é recusado (`Access denied`); uma correção
  entrou depois da 3ª rodada e só teve a largura conferida.
- **Arquivos:** mudar `R/referencias/verificacao.md`, `R/SKILL.md` (passo 5 e onde citar
  `file://`), `V/skill/mockup.md` se citar `file://`; ampliar `R/test/test_referencias.py` e
  `R/test/test_skill.py`.
- **O que prova a etapa:**
  - `verificacao.md` manda, em projeto sem React, servir a pasta do HTML por HTTP local
    (`python3 -m http.server <porta> --bind 127.0.0.1`, em segundo plano) e usar
    `http://127.0.0.1:<porta>/<arquivo>.html` no Playwright, no Chrome DevTools e no detector; e
    manda parar o servidor ao terminar. Nenhuma instrução de `SKILL.md` ou `referencias/` manda
    abrir `file://` no Playwright ou no Chrome DevTools.
  - `verificacao.md` diz que o `filePath` do `take_snapshot` fica dentro da pasta do projeto e o
    arquivo é apagado depois de achar os `uid`.
  - `verificacao.md` diz o que fazer com correção feita depois da 3ª rodada: prints nas duas
    larguras, detector nas duas larguras e console sem erro sobre a versão corrigida, e o relatório
    marca a correção como pós-rodada.
  - Os testes existentes de `verificacao.md` que exigiam `file://` passam a exigir o servidor HTTP.

## Etapa 15 — Perguntas do questionário por menu

- **Tela:** não.
- **Origem:** no teste de pronto, as perguntas vieram por `AskUserQuestion` (menu, uma por vez,
  recomendação primeiro, "Outro" livre) e funcionaram; o `SKILL.md:93` pedia perguntas no chat.
  Decisão do usuário: o menu vira a forma padrão.
- **Arquivos:** mudar `R/SKILL.md` (passo 1), `V/skill/mockup.md` (bifurcação); ampliar
  `R/test/test_skill.py` e `V/test/test_mockup.py`.
- **O que prova a etapa:**
  - O passo 1 manda fazer cada pergunta com a ferramenta `AskUserQuestion`, uma pergunta por
    chamada, com a opção recomendada em primeiro lugar e marcada "(Recomendado)", e aceitar a
    resposta livre ("Outro") do usuário.
  - O passo 1 não diz mais "no chat" para as perguntas.
  - `V/skill/mockup.md` descreve o questionário do mesmo jeito.

## Etapa 16 — Exceções também na reserva do detector

- **Tela:** não.
- **Origem:** no teste de pronto, o detector de navegador (`reserva/detect-antipatterns-browser.js`),
  usado para examinar estados que só existem depois de clicar (painel aberto, formulário com
  erro), acusou `overused-font` em Geist, que está em `excecoes.json`; o alarme teve de ser
  refutado à mão.
- **Arquivos:** criar `R/ferramentas/impeccable/filtrar.py` (só stdlib) e uma fixture com a saída
  real da reserva; mudar `R/referencias/verificacao.md`; ampliar `R/test/test_detector.py`.
- **O que prova a etapa:**
  - `filtrar.py` lê do stdin (ou de arquivo) o JSON que a reserva devolve, tira os achados que
    casam com `excecoes.json` (mesma regra e mesmo valor que o `detectar` ignora) e imprime o
    resto no mesmo formato; sai 0 sem achado e 2 com achado, como o `detectar`.
  - Com a fixture de uma página em Geist, o achado `overused-font` some; com a fixture de uma
    página em Inter, fica. Achados de outras regras ficam.
  - `verificacao.md` manda passar a saída da reserva pelo `filtrar.py` antes de tratar os alarmes.
- **Como fazer:** gerar a fixture rodando a reserva de verdade numa página com Geist e noutra
  com Inter (Chrome sem janela: `page.addScriptTag` e `window.impeccableDetectAsync()`), e gravar
  o JSON devolvido em `R/test/fixtures/detector/`.

## Etapa 17 — Busca do ui-ux-pro-max por tipo de tela

- **Tela:** não.
- **Origem:** no teste de pronto, `search.py "CRM lead dashboard …" --design-system` devolveu o
  padrão de landing "Scroll-Triggered Storytelling" para um painel de Operar; a sessão vetou, mas
  a busca não ajudou.
- **Arquivos:** mudar `R/SKILL.md` (passo 1); ampliar `R/test/test_skill.py` e `R/test/test_uupm.py`.
- **O que prova a etapa:**
  - O passo 1 diz qual busca rodar por tipo de tela: em Persuadir e Experiência, a de design
    system; em Operar e Ler, buscas por domínio (`--domain` de estilo, cor, tipografia, ux e
    produto) mais os três botões (`--variance`, `--motion`, `--density`) se o script os aceitar,
    sem usar a seção de padrão de landing.
  - O comando que o `SKILL.md` prescreve para Operar, rodado com "CRM lead dashboard", sai com 0 e
    não traz nenhum padrão de landing (conferir contra a lista de padrões do `data/` da busca).
- **Como fazer:** ler `R/ferramentas/uupm/scripts/search.py --help` e `design_system.py` para
  saber o que `--variance/--motion/--density` e `--domain product` mudam. Não editar os scripts
  copiados.

## Etapa 18 — Mockup de duas direções antes de construir

- **Tela:** não.
- **Origem:** no teste de pronto, fora da Vesta, a skill foi das perguntas direto à tela final;
  o usuário não viu nenhum mockup antes da construção. Decisão do usuário: em tela nova, duas
  direções em mockup, com escolha antes de construir, como na fase de mockup da Vesta.
- **Arquivos:** mudar `R/SKILL.md` (passos 1, 3 e 4), `V/skill/mockup.md` (trecho das duas
  direções); ampliar `R/test/test_skill.py` e `V/test/test_mockup.py`.
- **O que prova a etapa:**
  - O passo 3 tem um item de mockup de direções: em tela nova, duas versões estáticas da vista
    principal, cada uma numa direção diferente (de `catalogo/direcoes/`, de `catalogo/themes/` ou
    de referências do inspo diferentes; não duas variações de cor da mesma direção), em HTML
    autocontido em `docs/design/mockups/<tela>-a.html` e `-b.html`, servidas por HTTP local,
    com prints em 375 e 1440 de largura mostrados ao usuário.
  - O usuário escolhe com `AskUserQuestion` (uma pergunta, a direção recomendada primeiro e
    marcada "(Recomendado)"); só depois a skill grava o `sistema.md` na direção escolhida e segue
    para o passo 4. Nenhum código da tela final é escrito antes da escolha.
  - Tela que já existe: um mockup só, no estilo atual, mostrado com os prints para aprovação ou
    ajuste antes do passo 4.
  - No questionário de tela nova, a direção não é perguntada: ela é escolhida vendo os dois
    mockups. As outras perguntas continuam.
  - `V/skill/mockup.md` diz que as duas direções e a escolha seguem o passo 3 da vesta-interface
    (sem descrever um segundo processo).

## Etapa 19 — Provas da verificação com nome fixo

- **Tela:** não.
- **Origem:** no segundo teste de pronto (sessão em `~/Desktop/teste-vesta-2`), a skill não rodou
  o detector nem o Chrome DevTools, não escreveu relatório e declarou contraste suficiente sem
  medir; faltou o print 375 da direção escolhida. As provas da verificação não têm nome fixo, e
  por isso nenhum script consegue conferir se a rodada aconteceu.
- **Arquivos:** mudar `R/referencias/verificacao.md` (VER-05, VER-10, VER-16) e `R/SKILL.md`
  (passo 3, item 4; passo 5); ampliar `R/test/test_referencias.py` e `R/test/test_skill.py`.
- **O que prova a etapa:**
  - VER-10 manda gravar a saída de cada `detectar --json` na pasta da entrega, em
    `r<N>-detector-375.json` e `r<N>-detector-1440.json`, do mesmo N dos prints; na reserva, a saída
    do `filtrar.py` vai para os mesmos nomes.
  - VER-16 manda gravar o relatório em `relatorio.md` na pasta da entrega, e a rodada nova
    reescreve o mesmo arquivo.
  - VER-05 diz a pasta da entrega na Vesta: a do mockup (`docs/vesta/mockups/<data>-<feature>/`)
    na fase de mockup, e `docs/vesta/mockups/<data>-<feature>/etapa-<id>/` numa etapa de tela da
    execução.
  - O passo 3, item 4, dá nome aos prints das direções: `docs/design/mockups/<tela>-a-375.png`,
    `<tela>-a-1440.png`, `<tela>-b-375.png` e `<tela>-b-1440.png`, os quatro gravados antes da
    pergunta.
  - O passo 5 diz que a verificação só vale com os arquivos gravados: prints, as duas saídas do
    detector e `relatorio.md`; contraste e rolagem lateral só se afirmam medidos na rodada.

## Etapa 20 — A Vesta recusa tela sem as provas da verificação

- **Tela:** não.
- **Origem:** a mesma sessão; na Vesta, a instrução sozinha não segurou a verificação. Decisão do
  usuário: a conferência vira script.
- **Arquivos:** mudar `V/skill/scripts/vesta.py`, `V/skill/mockup.md`, `V/skill/execucao.md`,
  `V/skill/plano.md`; ampliar `V/skill/scripts/test_vesta.py` e `V/test/test_mockup.py`; criar em
  R um teste de contrato (`R/test/test_vesta_provas.py`) commitado por último, que pula com motivo
  sem `~/Code/vesta`.
- **O que prova a etapa:**
  - `iniciar` e `adicionar` de plano com tela recusam, dizendo o arquivo que falta, quando a
    pasta do mockup não tem, rastreados no git, `relatorio.md` e, para algum N, `r<N>-375.png`,
    `r<N>-1440.png`, `r<N>-detector-375.json` e `r<N>-detector-1440.json`; um detector que não é
    JSON válido também recusa.
  - Os mesmos dois comandos recusam quando não há, rastreados, `docs/design/mockups/<tela>-a.html`,
    `<tela>-b.html` e os quatro prints das direções da etapa 19, para algum `<tela>`. Estado criado
    com `"tela_existente": true` dispensa as direções (tela que já existe tem um mockup só) e
    mantém as outras provas.
  - `concluir` de etapa com tela recusa sem o mesmo conjunto de provas, rastreado, em
    `<pasta do mockup>/etapa-<id>/`; etapa sem tela conclui como antes.
  - Os testes antigos de mockup continuam valendo com as provas acrescentadas.
  - `V/skill/mockup.md` usa os nomes da etapa 19 na autoverificação e diz que `iniciar` recusa
    sem eles; `V/skill/plano.md` mostra `tela_existente` no `criar`; `V/skill/execucao.md` diz que,
    depois do verde de uma etapa com tela, a sessão principal roda o passo 5 da vesta-interface na
    tela servida, grava as provas em `etapa-<id>/`, commita, roda `prova teste` de novo e só
    então `concluir`.

## Etapa 21 — MCPs de navegador instalados, sem npx

- **Tela:** não.
- **Origem:** no terceiro teste de pronto (projeto evolution), as duas sessões abriram sem o
  Playwright e o Chrome DevTools: `MCP server chrome-devtools connection timed out after 30000ms`,
  o mesmo para o playwright. Com a máquina carregada, o `npx -y` não sobe em 30 s, e a
  verificação caiu num Playwright em script, sem o Chrome DevTools.
- **Arquivos:** mudar `R/install.sh`, `R/test/test_install.py`, `R/test/test_instalacao_real.py`,
  `R/README.md` (se citar o npx dos MCPs); rodar o `install.sh` de verdade.
- **O que prova a etapa:**
  - O `install.sh` instala `@playwright/mcp@0.0.82` e `chrome-devtools-mcp@1.10.1`, versões
    exatas, com `npm install --prefix` numa pasta fixa (`$HOME/.local/share/vesta-interface/mcp`,
    trocável por `VESTA_MCP_HOME`); npm falhou, o instalador para com erro e não registra MCP.
  - Os dois MCPs são registrados pelo caminho absoluto do executável nessa pasta
    (`node_modules/.bin/playwright-mcp` e `node_modules/.bin/chrome-devtools-mcp`), com os mesmos
    argumentos de antes e sem `npx`.
  - Instalação real: `~/.claude.json` tem os dois sem `npx`, o executável registrado existe, e o
    `package.json` instalado de cada um tem a versão travada.

---

Critério de pronto (parada 2, manual): numa sessão nova, pedir à vesta-interface uma tela a
partir de um pedido exemplo (painel de leads da ZOI, tipo Operar) e conferir que ela pergunta
sobre design, gera, e passa pela própria verificação.
