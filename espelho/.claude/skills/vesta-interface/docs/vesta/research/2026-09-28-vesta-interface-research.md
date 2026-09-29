# Pesquisa — vesta-interface

Spec: `docs/vesta/specs/2026-09-28-vesta-interface-design.md`

Legenda de caminhos: **V** = `~/Code/vesta`; **X** = `~/Code/ux-lab/vendor`;
**H** = `~/.claude/skills/hallmark`; **T** = `X/taste-skill/skills/taste-skill/SKILL.md`;
**I** = `X/impeccable/.claude/skills/impeccable`; **U** = `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max`.

## Achados

### A1 — O detector do impeccable não é Python nem stdlib: é um motor Rust que baixa um binário por plataforma
- Fonte: `I/scripts/impeccable:41-197` (lança `$IMPECCABLE_BIN`, `scripts/bin/<os>-<arch>`, `~/.impeccable/bin`, PATH, ou baixa do GitHub com sha256); `X/impeccable/Cargo.toml`, `crates/*`; nenhum binário existe na máquina; `cargo` 1.97.1 instalado.
- Alternativa comprovada: `X/impeccable/crates/live/assets/detect-antipatterns-browser.js` (2,2 MB, motor compilado em WASM) rodou via Playwright, acusou 13 problemas numa página genérica e zero no `tests/fixtures/antipatterns/should-pass.html`. Deixou passar `overused-font`, `nested-cards`, `em-dash-overuse`, `marketing-buzzword` (as duas últimas são regras de texto que só o CLI pega).
- 61 regras (32 de slop, 29 de qualidade): `crates/foundation/src/registry.rs:32+`. 87 fixtures prontas em `tests/fixtures/antipatterns/`.
- Contradiz a spec: sim (spec diz "ferramentas stdlib").
- Pergunta que levanta: o detector roda como programa compilado aqui (pega todas as regras, mas é um binário que precisa ser recompilado a cada atualização) ou como script dentro do navegador que o Playwright já abre (zero instalação, mas perde 4 regras de texto)?

### A2 — O fluxo de 5 passos da spec deixa de fora 17 capacidades das fontes
- Fonte: agente de conflitos, seção 3. As que mais pesam:
  1. Varredura do projeto existente antes de desenhar (fontes, paleta, espaçamento já usados): `H:147-201`, `I/reference/new-work.md` §1.
  2. Escolha de macroestrutura, nav e rodapé com rotação para não repetir: `H:264-331` — o diferencial central do hallmark.
  3. `study` de URL ou print que o usuário traz: `H:28,490-552`.
  4. Trabalho com imagem gerada (image-to-code, imagegen do taste; comp-led do impeccable).
  5. Modo live do impeccable (variações no navegador por HMR): `I/reference/live.md`.
  6. Crítica heurística de UX (Nielsen, carga cognitiva, personas): `I/reference/critique.md:43-58`.
  7. Modos de refino (bolder, quieter, distill, harden, onboard, optimize, delight…).
  8. Design system persistente (PRODUCT.md, DESIGN.md, export para variáveis CSS do shadcn): `H:464-466`, `H/references/export-formats.md`.
  9. Fluxo de componente isolado com preview de 8 estados: `H:60-141`.
  10. Suporte nativo iOS/Android: `I/reference/ios.md`, `android.md`.
  11. Gráficos (25 tipos) e 22 stacks do ui-ux-pro-max.
- Contradiz a spec: sim.
- Pergunta que levanta: quais dessas entram na primeira versão? Cada uma a mais é mais texto para destilar e mais coisa para testar; cada uma a menos é algo que você hoje tem (hallmark) e perde.

### A3 — O critério "empate vence o hallmark" não resolve a maior parte das contradições
- Fonte: agente de conflitos, seção 1 — cerca de 60 contradições. Várias só se resolvem pelo tipo de tela: fontes, dose de cor e movimento mudam entre página de venda, painel operacional, texto longo e experiência. O impeccable tem esse eixo pronto: modos Persuade / Operate / Read / Experience (`I/SKILL.md:31-40`). Há ainda contradições dentro do próprio hallmark (OKLCH só vs hex no exemplo, `H/references/color.md:7` vs `:31`; proíbe loop infinito e oferece marquee infinito, `motion.md:109` vs `microinteractions.md:31`) e do taste (proíbe número inventado e dá "47.2%" de exemplo, `T:327` vs `T:618`).
- Contradiz a spec: parcial.
- Pergunta que levanta: a regra de desempate passa a ser "primeiro o tipo de tela, depois o mais verificável, por último o hallmark"? Sem isso, um painel administrativo herda regras de landing page.

### A4 — Contradições com efeito direto no que você vai ver
- Fonte: agente de conflitos, seção 1.
  - Ícones: shadcn usa Lucide por padrão; hallmark aceita Lucide (`H/references/assets.md:49`); taste desencoraja e prefere Phosphor (`T:141-142`).
  - Travessão: hallmark prescreve (`H/references/copy.md:59`); taste proíbe em todo lugar (`T:649`).
  - Modo escuro: taste e ui-ux-pro-max mandam fazer os dois sempre (`T:531-535`, `U/references/quick-reference.md:87`); impeccable diz escolher um pelo contexto de uso (`I/reference/craft-floor.md:42`).
  - Ação destrutiva: hallmark quer desfazer em vez de confirmação (`H/references/microinteractions.md:215`); ui-ux-pro-max quer confirmação (`quick-reference.md:170`).
  - Perguntas antes de desenhar: hallmark sempre 3 (`H:211-228`); taste infere e pergunta no máximo 1 (`T:33-36`).
  - Fontes proibidas: o detector do impeccable acusa Geist, Fraunces e Space Grotesk, que o hallmark usa como padrão (`H/references/typography.md:89`, `H:277`).
- Contradiz a spec: parcial.
- Pergunta que levanta: essas seis você quer decidir agora, ou deixo a regra de desempate decidir e você revisa o `fontes.md` depois?

### A5 — O detector do impeccable vai acusar escolhas que o hallmark faz de propósito
- Fonte: regra `overused-font` em `X/impeccable/crates/live/assets/antipatterns.json` acusa Geist, Fraunces, Space Grotesk, Plus Jakarta Sans; hallmark usa as quatro em temas (`H:277`, `typography.md:89`).
- Contradiz a spec: sim (spec põe o detector como juiz no passo 5).
- Pergunta que levanta: quando detector e regra fundida discordam, quem vence? O detector aceita exceções configuradas (`impeccable ignores add-value overused-font …`).

### A6 — Verificação sem limite de rodadas
- Fonte: spec passo 5 ("corrige e verifica de novo"); `I/SKILL.md:15` e `new-work.md:138` limitam a 2 rodadas; `H:474` e `T:979` não limitam.
- Contradiz a spec: parcial.
- Pergunta que levanta: ciclo sem teto pode rodar muito tempo corrigindo detalhe; limitar a 2 rodadas e reportar o que sobrou?

### A7 — O tamanho: 185 mil palavras de fonte para uma skill que a Anthropic recomenda com menos de 500 linhas no arquivo principal
- Fonte: https://code.claude.com/docs/en/skills (SKILL.md < 500 linhas, referências carregam sob demanda, descrição cortada em 1.536 caracteres). Hallmark 101,8 mil palavras (107 arquivos, catálogo de 50 componentes, 21 macroestruturas, 5 temas); impeccable 60,9 mil; taste 12,9 mil (principal); ui-ux-pro-max 7,3 mil + 5 MB de dados.
- Cerca de 40 regras aparecem em 3 ou mais fontes (um terço das regras distintas); o resto é de fonte única.
- Contradiz a spec: parcial (nove arquivos de regras não comportam os catálogos do hallmark).
- Pergunta que levanta: os catálogos (componentes, macroestruturas, temas) viram uma pasta `catalogo/` copiada quase inteira, ou são destilados junto com as regras?

### A8 — O banco do ui-ux-pro-max sugere o que as regras anti-slop proíbem
- Fonte: execução real de `U/scripts/search.py "saas analytics" --design-system` recomendou Glassmorphism; `"fintech banking dashboard"` recomendou acento roxo `#8B5CF6` e na mesma saída disse evitar roxo. Scripts são só stdlib, caminhos relativos ao próprio arquivo (`U/scripts/core.py:15`), rodam em 0,08 s.
- Contradiz a spec: parcial.
- Pergunta que levanta: o banco só sugere e as regras vetam (sugestão filtrada), ou o banco sai do passo 1 e fica só para consulta de UX e stack?

### A9 — As variações de estilo do taste (minimalista, soft, brutalista) contradizem o taste principal
- Fonte: `X/taste-skill/skills/soft-skill/SKILL.md:41-44` exige card dentro de card; `minimalist-skill/SKILL.md:60-61` exige janela falsa de sistema; `brutalist-skill` usa texto de 10px. Tudo proibido nas regras centrais.
- Contradiz a spec: parcial (a spec trata o taste como fonte de regras).
- Pergunta que levanta: essas variações viram "direções" prontas que a Vesta oferece no mockup (onde a regra da direção vence a geral), ou ficam de fora?

### A10 — Mockup em React passa na trava da Vesta, mas some do painel
- Fonte: `V/skill/scripts/vesta.py:146-153` só confere que o caminho está no git; `V/skill/scripts/painel.py:56` só acha pastas datadas em `docs/vesta/mockups/`; `V/skill/scripts/painel.html:324` sempre abre `<pasta>/index.html`.
- Contradiz a spec: parcial.
- Pergunta que levanta: em projeto React, o mockup vive dentro do app (e o painel ganha um link para a rota) ou em `docs/vesta/mockups/` com um `index.html` que só redireciona para a rota?

### A11 — Trocar hallmark/inspo na Vesta quebra testes existentes
- Fonte: `V/test/test_mockup.py:34-75` confere palavras do `mockup.md` (inspo, playwright, celular, desktop); `V/test/test_install.py:27-29,113-136` exige aviso quando hallmark/inspo faltam; `V/test/test_docs.py:153` exige que `dependencias.md` cite hallmark e inspo. Referências também em `V/skill/SKILL.md:41`, `research.md:38-42`, `execucao.md:80-82`, `install.sh:28-30,47-48`, `README.md:66,78-80,174`, `docs/dependencias.md:4`. Padrão de teste "não cita mais X": `V/test/test_sem_wayfinder.py`.
- Contradiz a spec: não (a spec prevê o teste de integração), mas amplia o escopo.
- Pergunta que levanta: nenhuma; entra no plano.

### A12 — Próximo ADR é 0021 e vive na Vesta
- Fonte: `~/Code/claude-tooling/docs/decisions/` já tem 0019 e 0020; `V/docs/decisoes/0018-mockup-e-frontend-na-vesta.md`. Todo `.md` em `V/docs/decisoes/` começa com a linha de aviso histórico (`V/test/test_docs.py:212-217`) e `HISTORIA` precisa ganhar a entrada (`:170-177`, `:231-235`). ADR antigo nunca é reescrito.
- Contradiz a spec: não.
- Pergunta que levanta: nenhuma.

### A13 — Versões travadas e o Playwright hoje em `@latest`
- Fonte: `~/.claude.json:9206-9210` (playwright `@latest`, `--headless`, perfil fixo). Versões atuais: chrome-devtools-mcp 1.10.1, @playwright/mcp 0.0.82, shadcn 4.21.0. `@latest` consulta o registro a cada partida e já serviu pacote malicioso por 8 h em 2026-02-09 (https://archestra.ai/blog/pin-mcp-server-versions).
- Contradiz a spec: parcial (spec diz que o Playwright não muda).
- Pergunta que levanta: travar também o Playwright, já que é o mesmo risco?

### A14 — O Chrome DevTools MCP manda dados ao Google por padrão
- Fonte: `X/chrome-devtools-mcp/README.md:45-48` (estatísticas de uso ligadas; `--no-usage-statistics`); `--no-performance-crux` evita enviar URLs de trace à API CrUX. 46 ferramentas ligadas por padrão, 14 só de memória (`docs/configuration.md:47-50`). `--isolated` usa perfil temporário; `--headless` sem janela.
- Contradiz a spec: não, mas a spec não diz como configurar.
- Pergunta que levanta: registro com `--headless --isolated --no-usage-statistics --no-performance-crux --categoryMemory=false`? Sem janela e sem seus logins; login em site exigiria outro caminho, como já acontece com o Playwright.

### A15 — O shadcn MCP não funciona sem `components.json`
- Fonte: `X/ui/packages/shadcn/src/mcp/index.ts:205-215`; `registry/api.ts:227-247`. 7 ferramentas (`index.ts:59-183`). `mcp init` escreve `.mcp.json` do projeto com `latest` (`commands/mcp.ts:20-31`).
- Contradiz a spec: parcial (spec registra global; em projeto sem shadcn o MCP só devolve erro).
- Pergunta que levanta: nenhuma nova — a spec já diz que projeto não-React usa HTML. Consequência para o plano: o passo 4 em projeto React começa por `npx shadcn init` se o projeto ainda não tem `components.json`. Taste avisa: shadcn no estado padrão é slop (`T:627`).

### A16 — Hallmark tem licença MIT, e há obrigações de atribuição
- Fonte: GitHub API em 2026-09-28 (hallmark MIT, 29 mil estrelas) — a spec diz "sem arquivo de licença", a cópia local só não trouxe o arquivo. Apache-2.0 (impeccable, chrome-devtools, playwright) exige cópia da licença, aviso de modificação e levar o `NOTICE.md` do impeccable, que por sua vez credita trabalho MIT de ehmo.
- Contradiz a spec: sim (fato corrigido; não muda decisão).
- Pergunta que levanta: nenhuma; entra como `THIRD_PARTY_NOTICES.md` com licença e commit de cada fonte.

### A17 — Arquivos de design system com o mesmo nome e esquemas diferentes
- Fonte: hallmark lê `design.md` ou `DESIGN.md` (`H:153`); impeccable gera `DESIGN.md` e `PRODUCT.md` (`I/reference/document.md`); stitch-skill do taste gera outro `DESIGN.md`. No macOS os nomes colidem.
- Contradiz a spec: parcial (spec não prevê arquivo persistente).
- Pergunta que levanta: ligado a A2 item 8 — se entrar, a vesta-interface define um formato só.

### A18 — Hallmark carimba comentários no código; impeccable proíbe
- Fonte: `H:46,461` (comentário CSS com macroestrutura e notas de crítica, log `.hallmark/log.json`); `I/reference/new-work.md:77` (nada de metadado de direção no código).
- Contradiz a spec: parcial.
- Pergunta que levanta: a rotação de macroestrutura do hallmark depende desse log. Se a rotação entrar (A2 item 2), o log vai para uma pasta de estado fora do código-fonte?

### A19 — Evidência de efeito é fraca e há risco de estilo único
- Fonte: único teste controlado, https://www.justinwetch.com/blog/improvingclaudefrontend/ (50 prompts, 75% de vitórias, efeito maior no Haiku, menor no Opus); https://ruoqijin.com/blog/frontend-design-skills-ai-agents (proibição de fonte é "curativo"; ganho maior é o ciclo de print e correção). Nenhuma fonte fundiu as quatro; guias recomendam empilhar, não fundir (https://composio.dev/content/top-design-skills).
- Contradiz a spec: não.
- Pergunta que levanta: registro. Reforça A2 item 2 (variação escolhida por contexto) e o peso da verificação no navegador.

### A20 — Skills com descrição parecida disputam o mesmo pedido
- Fonte: https://code.claude.com/docs/en/skills; https://github.com/anthropics/claude-code/issues/20986. Globais hoje com papel parecido: `hallmark`, `design:*` do plugin design, `frontend-design` se instalado.
- Contradiz a spec: não (spec já tira o hallmark).
- Pergunta que levanta: registro; a descrição da vesta-interface precisa citar o caso principal nos primeiros 250 caracteres.

### A21 — Inventários fora da Vesta que mudam
- Fonte: `~/.claude/CLAUDE.md:136-141` (regra do Navegador, só Playwright); `~/.claude/settings.json:393-410` (permissões com nome antigo `mcp__plugin_playwright_playwright__*`); `~/Code/claude-tooling/docs/reference/estado-atual.md:44-47`; `~/Code/claude-kit/fontes.json:20-26` (não lista repos locais, então a skill é copiada), `README.md:45,65-70`.
- Contradiz a spec: não; amplia o escopo.
- Pergunta que levanta: nenhuma; entra no plano como etapa de inventário.

### A22 — Partes aproveitáveis e descartáveis das fontes
- Fonte: agente de anatomia.
  - ui-ux-pro-max: `design` exige APIs pagas (`GEMINI_API_KEY`, `ATLASCLOUD_API_KEY`); `slides` e `banner-design` são cópias idênticas de trechos do `design`; `brand` é marketing. Aproveitáveis: referências de tokens do `design-system` e de shadcn/Tailwind do `ui-styling`.
  - taste: `taste-skill-v1` e `gpt-tasteskill` são versões antigas; `output-skill` não é de design; `blocks/` está vazio (`T:835-841`).
  - hallmark: tokens de 21 temas apontam para `../../site/css/tokens.css`, que não existe na skill instalada (`H:282`); só 5 temas presentes.
  - impeccable: `live-browser*.js` (547 KB) e `font-index.json` (1,1 MB) só servem ao modo live.
- Contradiz a spec: não.
- Pergunta que levanta: registro.

## Fila do grill

Ordenada por dependência.

1. A2 — Quais capacidades entram na primeira versão? (trava A7, A17, A18, A9)
2. A3 — Regra de desempate começa pelo tipo de tela? (trava A4, A5, A9)
3. A7 — Catálogos do hallmark copiados ou destilados?
4. A1 — Detector compilado ou no navegador? (trava A5)
5. A5 — Detector ou regra fundida: quem vence?
6. A4 — As seis contradições visíveis: decidir agora ou pela regra?
7. A8 — Banco do ui-ux-pro-max sugere e as regras vetam?
8. A9 — Variações do taste viram direções prontas?
9. A10 — Onde mora o mockup React e como o painel acha?
10. A6 — Limite de rodadas na verificação?
11. A17 / A18 — Arquivo de design system e log de rotação (se A2 incluir).
12. A13 — Travar o Playwright também?
13. A14 — Flags do Chrome DevTools.

Registro, fora da fila: A11, A12, A15, A16, A19, A20, A21, A22.
