# vesta-interface — design

Data: 2026-09-28. Classificação: estrutural.

## Objetivo

Uma skill única de frontend design que funde as capacidades de oito fontes e substitui
hallmark + inspo como camada de interface da Vesta (ADR-0018 da Vesta).

Fontes (código congelado em `~/Code/ux-lab/vendor`, hallmark em `~/.claude/skills/hallmark`):

| Fonte | Licença | Entra como |
|---|---|---|
| hallmark | MIT (arquivo ausente na cópia local) | regras destiladas |
| taste-skill | MIT | regras destiladas |
| impeccable | Apache-2.0 | regras destiladas + detector em `ferramentas/` |
| ui-ux-pro-max | MIT | regras UX destiladas + busca/banco em `ferramentas/` |
| shadcn/ui | MIT | CLI travado + mapa de componentes |
| Chrome DevTools MCP | Apache-2.0 | MCP global, usado na verificação |
| Playwright MCP | Apache-2.0 | MCP global (já existe), usado na verificação |
| inspo | serviço | MCP global (já existe), usado nas referências |

## Critério de sucesso (do usuário)

1. Visual menos genérico que o atual.
2. Regras de UX aplicadas e checadas: estados, formulários, acessibilidade.
3. Verificação no navegador antes de entregar: prints, CSS computado, console, desempenho.
4. Código pronto em shadcn quando o projeto é React.

## Abordagem

Destilar num fluxo único (escolhida sobre roteador fino e reescrita do zero). Uma voz, pouco
texto carregado por vez.

## Estrutura

Repositório `~/Code/vesta-interface`, link em `~/.claude/skills/vesta-interface`.

- `SKILL.md` — curto: o fluxo e qual referência abrir em cada passo.
- `referencias/` — nove arquivos, cada regra em um só:
  `slop.md`, `tipografia.md`, `cor.md`, `layout.md` (inclui espaçamento e responsivo),
  `movimento.md`, `componentes.md` (padrões + mapa para shadcn), `ux.md` (estados,
  formulários, acessibilidade), `verificacao.md`, `fontes.md` (origem de cada regra e
  contradições decididas).
- `catalogo/` — cópia quase integral dos catálogos do hallmark: 50 componentes, 21
  macroestruturas, 5 temas. Ajustes: remover a referência aos 21 temas que apontam para um
  `tokens.css` inexistente; cada peça ganha nota com o equivalente shadcn quando houver.
  Só as regras são destiladas; o catálogo é consulta sob demanda.
  Inclui `catalogo/direcoes/`: minimalista, sofisticada e brutalista do taste, como direções
  prontas ao lado dos 5 temas. Dentro da direção escolhida, as regras dela vencem as de
  gosto, nunca as mensuráveis (contraste, tamanho mínimo de texto, acessibilidade).
- `ferramentas/` — busca do ui-ux-pro-max (Python + CSV, só stdlib) e o lançador do detector
  do impeccable. O detector é o binário oficial (motor Rust, 61 regras), travado na versão
  congelada em `vendor`, baixado uma vez com conferência sha256 pelo `install.sh` para
  `~/.impeccable/bin`. Falhou o download: cai para o bundle WASM rodando no navegador do
  Playwright (perde 4 regras de texto).
  Fora: instaladores e integrações com outros editores.
- `install.sh` — cria o link da skill; registra MCPs globais com versão travada:
  `chrome-devtools-mcp@1.10.1 --headless --isolated --no-usage-statistics
  --no-performance-crux` só com os grupos de navegação, depuração e desempenho, e troca o
  Playwright de `@latest` para `@playwright/mcp@0.0.82 --snapshot-mode none` mantendo
  `--headless` e o perfil fixo. O shadcn não vira MCP: a skill usa `npx shadcn@4.21.0`. Baixa o
  detector do impeccable e aplica as exceções dele.

## Fluxo (dentro e fora da Vesta)

1. Entender o pedido: tipo de produto, público, o que é visível. Busca no banco do
   ui-ux-pro-max sugere estilo, paleta e fontes; as regras fundidas vetam o que for proibido
   (ex.: glassmorphism, acento roxo) antes da sugestão chegar ao desenho. Consultas de UX,
   formulário e stack shadcn do banco entram sem filtro.
2. Referências: 2 a 5 sites reais pelo inspo.
3. Sistema visual: cor, tipografia, espaçamento, movimento, pelas referências destiladas.
4. Construção: projeto React usa componentes shadcn pelo CLI travado; outros projetos, HTML
   com o visual do shadcn.
5. Verificação: Playwright tira prints celular + desktop; Chrome DevTools confere CSS
   computado, console e desempenho; detector procura sinais de slop; lista de `ux.md`
   confere acessibilidade e estados. Falhou, corrige e verifica de novo, até 3 rodadas.
   Sobrou algo: entrega com lista curta do que falhou e por quê. Exceção: falha de
   acessibilidade ou contraste não pode sobrar; sem corrigir, não entrega.

Os comandos do impeccable (audit, polish, critique…) viram modos: revisar tela existente
roda só os passos 3 e 5.

## Escopo da v1

Entram:

1. Varredura do projeto existente antes de desenhar (fontes, paleta, espaçamento, framework).
2. Escolha de macroestrutura, nav e rodapé com rotação entre páginas de Persuadir e
   Experiência (hallmark); telas de Operar e Ler herdam nav e rodapé do design system.
3. `study`: extrair o DNA visual de URL ou print trazido pelo usuário.
4. Crítica heurística de UX (impeccable `critique`).
5. Modos de ajuste: bolder, quieter, distill, harden, onboard, optimize, polish, delight.
6. Design system persistente no projeto, com export para variáveis CSS do shadcn.
   Mora em `docs/design/sistema.md` (cor, tipografia, espaçamento, tipo de tela, direção; um
   formato só, substitui `design.md`/`DESIGN.md`/`PRODUCT.md` das fontes). A rotação do item
   2 registra em `docs/design/rotacao.json`. Ambos commitados; nada de metadado no código.
7. Fluxo de componente isolado com prévia de estados.

Ficam para depois: geração de imagem (API paga), modo live do impeccable, nativo iOS/Android,
regras de gráfico e das 22 stacks (os dados seguem consultáveis pela busca do ui-ux-pro-max).

## Regra de contradição

Três níveis, nesta ordem:

1. Tipo de tela (modos do impeccable): **Persuadir** (landing, página de venda), **Operar**
   (painel, CRM, formulário), **Ler** (documentação, artigo), **Experiência** (portfólio,
   campanha). Regra que depende do tipo é escrita nas quatro versões.
2. A mais específica e verificável ("contraste ≥ 4.5:1" vence "cores sutis").
3. Empate: hallmark.

Toda decisão registrada em `fontes.md` com as duas versões. O passo 1 do fluxo classifica a
tela num dos quatro tipos.

Detector contra regra fundida: vence a regra. Cada exceção decidida em `fontes.md` vira
exceção configurada no detector, com motivo, versionada no repositório e aplicada pelo
`install.sh`. Qualquer outro alarme do detector é corrigido.

## Decisões de conteúdo fixadas

1. Ícones: Lucide por padrão (vem com shadcn); projeto com outra família usa a dele.
2. Travessão: permitido com moderação; o detector acusa excesso.
3. Modo escuro: pelo tipo de tela e contexto de uso. Operar ganha os dois; Persuadir e Ler
   ficam com um, escolhido pelo contexto.
4. Ação destrutiva: reversível, desfazer sem confirmação; irreversível (apagar para sempre,
   pagamento), confirmação.
5. Fontes acusadas pelo detector (Geist, Fraunces, Space Grotesk…): permitidas quando servem
   ao tipo de tela; a escolha fica em `fontes.md` e vira exceção do detector.

## Perguntas de design (bifurcação)

Spec e grill da Vesta perguntam sobre funcionamento; ninguém pergunta sobre aparência. Ao
entrar no mockup, a Vesta oferece: **com questionário** ou **direto**.

- Padrão: tela nova, com questionário; tela existente mudando, direto. O usuário troca.
- Com questionário: o agente faz no chat, uma por vez, as perguntas de design que julgar
  necessárias para aquela tela (sem lista fixa), cada uma com opções e recomendação.
- Direto: o agente deduz as respostas e as mostra junto com o mockup para correção.
- Fora da Vesta, a vesta-interface usa a mesma bifurcação.

## Acoplamento à Vesta

`skill/mockup.md` (e demais arquivos da Vesta que citam hallmark/inspo: `SKILL.md`,
`research.md`, `execucao.md`, `scripts/painel.html`) passam a chamar a vesta-interface.
Formato do mockup depende do projeto: projeto React, página shadcn no próprio projeto;
outros, HTML autocontido como hoje. O mockup React vive numa rota própria de mockup
dentro do app; `docs/vesta/mockups/<data>-<feature>/index.html` vira página curta com os prints
celular + desktop da verificação e o link para a rota. O painel e a trava da Vesta seguem sem
mudança de código, e o aprovado fica registrado mesmo depois que o app mudar. Registrar em ADR novo na Vesta, revertendo em parte o
ADR-0018.

## O que sai

Com a master pronta, `~/.claude/skills/hallmark` sai do global (fonte preservada em
`~/Code/ux-lab/vendor`). Inspo segue como MCP. `~/Code/ux-lab` fica como está.

## Testes (por script)

1. Estrutura: todo arquivo citado no `SKILL.md` existe; as nove referências existem.
2. Ferramentas: a busca devolve sugestão para um tipo de produto exemplo; o detector acusa
   um HTML genérico de exemplo e deixa passar um bom.
3. Integração: arquivos da Vesta citam vesta-interface e não citam hallmark nem inspo como
   skill; testes existentes da Vesta passam.
4. Prova real (manual, critério de pronto): a skill gera uma tela a partir de um pedido
   exemplo e a tela passa pela própria verificação.

## Decisões do grill

- **A2** — v1 com 7 capacidades (varredura, rotação de macroestrutura, study, crítica
  heurística, modos de ajuste, design system persistente, componente isolado); ficam fora
  imagem, live, nativo, gráficos/stacks. Motivo: o que o hallmark já dá não se perde; o resto
  depende de API paga ou duplica o mockup.
- **A3** — desempate em três níveis: tipo de tela, mais verificável, hallmark. Motivo: ~60
  contradições, muitas só se resolvem pelo tipo de tela.
- **A7** — catálogos do hallmark copiados, só regras destiladas. Motivo: catálogo é consulta
  sob demanda; resumir tira o que faz a peça funcionar.
- **A1** — detector binário oficial travado em 0.1.6, WASM no navegador como reserva. Motivo:
  61 regras, roda sem navegador, saída legível por teste.
- **A5** — regra fundida vence o detector; exceções versionadas. Motivo: detector acusa
  fontes que o hallmark usa de propósito.
- **A4** — cinco decisões de conteúdo fixadas; perguntas antes do desenho viraram bifurcação
  com/sem questionário, perguntas livres no chat. Motivo: pedido do usuário — a Vesta pergunta
  sobre funcionamento, faltava rodada de design.
- **A8** — banco do ui-ux-pro-max sugere, regras vetam. Motivo: testado, sugeriu glassmorphism e
  roxo.
- **A9** — variações do taste viram direções no catálogo, sem passar por cima do mensurável.
- **A10** — mockup React em rota do app, registro com prints em `docs/vesta/mockups/`. Motivo:
  painel só acha pastas ali; evita mexer no painel.
- **A6** — verificação até 3 rodadas; acessibilidade e contraste não podem sobrar.
- **A17/A18** — `docs/design/sistema.md` e `docs/design/rotacao.json`. Motivo: nomes das fontes
  colidem no macOS; impeccable proíbe metadado no código.
- **A13/A14** — Playwright travado em 0.0.82; Chrome DevTools sem janela, perfil temporário, sem
  telemetria, sem envio de URL ao CrUX, sem ferramentas de memória.
- **A16** — hallmark é MIT; `THIRD_PARTY_NOTICES.md` com licença e commit de cada fonte, e o
  `NOTICE.md` do impeccable.
- **A11, A12, A21** — entram no plano: testes da Vesta que citam hallmark/inspo, ADR-0021 em
  `~/Code/vesta/docs/decisoes/`, inventários do claude-tooling, claude-kit e settings.
- **A15, A19, A20, A22** — registro; não mudam a spec.

## Decisões da revisão do plano

Revisão com pesquisa da opinião da comunidade sobre as oito fontes, cada conclusão conferida no
código travado em `~/Code/ux-lab/vendor`.

- **R1** — `SKILL.md` ganha um piso com as regras de 3 ou mais fontes, e cada passo manda abrir
  a referência. Motivo: relatos de que o agente raramente abre referências de skill.
- **R2** — os três botões do taste (variação, movimento, densidade) entram, com padrão por tipo
  de tela, guardados no `sistema.md`. Motivo: é o que o taste tem de próprio, e combate telas
  que convergem para a mesma estrutura.
- **R3** — shadcn só como CLI travado, sem MCP. Motivo: o MCP só devolve o comando de instalação,
  e na 4.21.0 o imprime quebrado (`mcp/utils.ts:49`); o CLI faz busca, visão e prévia.
- **R4** — Chrome DevTools só com navegação, depuração e desempenho; sem regra de fechar.
  Motivo: a última aba não fecha, e as ferramentas de clique e tamanho duplicam o Playwright.
- **R5** — o detector examina a página renderizada, e todo alarme é corrigido ou refutado com
  prova. Motivo: os falsos positivos relatados vinham de ler o código-fonte.
- **R6** — Playwright MCP com `--snapshot-mode none`. Motivo: a árvore da página depois de cada
  ação é o maior custo relatado; o CLI mudaria o navegador geral.
- **R7** — rotação só em Persuadir e Experiência, garantida por `ferramentas/rotacao.py`.
  Motivo: é a regra mais violada do hallmark, e num app o menu deve se repetir.
