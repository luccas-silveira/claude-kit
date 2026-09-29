# Fontes

Cada contradição entre as fontes (ou dentro de uma delas), com as duas versões citadas, a decisão
e o nível do desempate que decidiu. `X` é `~/Code/ux-lab/vendor`, a cópia travada das fontes.
Desempate, nesta ordem: tipo de tela, depois a regra mais verificável, depois hallmark. Decisão
que libera o que o detector acusa vira exceção em `ferramentas/impeccable/excecoes.json`.

## Tipografia

### Inter
- A: hallmark põe Inter entre os padrões proibidos, `X/hallmark/references/typography.md:40`, `X/hallmark/references/typography.md:236`
- B: taste só desencoraja e aceita em pedido neutro ou de setor público, `X/taste-skill/skills/taste-skill/SKILL.md:169-170`; brutalist recomenda Inter Extra Bold, `X/taste-skill/skills/brutalist-skill/SKILL.md:28`
- Decisão: fora como escolha do agente em todo tipo de tela; entra se o usuário pede ou o projeto já usa (TIP-02). Sem exceção no detector.
- Desempate: hallmark, que também cede ao pedido explícito do usuário (`typography.md:44`).

### Geist
- A: hallmark faz de Geist o corpo padrão, `X/hallmark/references/typography.md:89`; taste recomenda, `X/taste-skill/skills/taste-skill/SKILL.md:169`
- B: o detector acusa Geist como fonte batida, `X/impeccable/crates/live/assets/antipatterns.json:15`
- Decisão: permitida no corpo em Persuadir, Operar e Ler e nos títulos de painel; exceção configurada no detector (TIP-06).
- Desempate: tipo de tela (decisão 5 da spec).

### Fraunces
- A: hallmark usa Fraunces como display e no token de exemplo, `X/hallmark/references/typography.md:58`, `X/hallmark/references/typography.md:21`
- B: taste proíbe como padrão, `X/taste-skill/skills/taste-skill/SKILL.md:180`; impeccable chama de padrão de quem parou de procurar, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:67`
- Decisão: permitida no display de Persuadir e Experiência de tom editorial ou de luxo e no título de artigo em Ler, sempre romana; fora de Operar; exceção no detector (TIP-03).
- Desempate: tipo de tela (decisão 5 da spec).

### Serif padrão no display
- A: o gênero padrão do hallmark é editorial, com display serif, `X/hallmark/SKILL.md:230`, `X/hallmark/references/typography.md:117`
- B: taste diz que serif é muito desencorajada como padrão e não serve a painel, `X/taste-skill/skills/taste-skill/SKILL.md:173-178`, `X/taste-skill/skills/taste-skill/SKILL.md:609`
- Decisão: sans é o ponto de partida; serif no display só com tom editorial, luxo ou leitura longa; nunca em Operar (TIP-03).
- Desempate: tipo de tela.

### Número de famílias
- A: hallmark exige par (mínimo 2, teto 3) e proíbe página de uma fonte, `X/hallmark/references/typography.md:15`, `X/hallmark/references/typography.md:238`
- B: impeccable pede uma família bem ajustada para Operar e Ler, `X/impeccable/.claude/skills/impeccable/reference/typeset.md:8`, e uma família em distill, `X/impeccable/.claude/skills/impeccable/reference/distill.md:52`
- Decisão: teto de três em todo tipo (TIP-04); Operar e Ler podem usar uma família; Persuadir e Experiência usam par.
- Desempate: tipo de tela.

### Escala de tamanhos
- A: hallmark usa razão 1.25 e no máximo 5 tamanhos, `X/hallmark/references/typography.md:9`, `X/hallmark/references/typography.md:205`
- B: uupm usa escala aditiva 12/14/16/18/24/32 (16→18 é 1.125×), `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:119`
- Decisão: título e corpo separados por ≥ 1.25×, no máximo 5 tamanhos; degraus menores só entre rótulos densos de Operar (TIP-08).
- Desempate: verificável — o detector mede o degrau (`flat-type-hierarchy`).

### Peso de título
- A: hallmark exige ≥ 300 unidades entre título e corpo, 500 e 600 fora, `X/hallmark/references/typography.md:210`
- B: uupm põe título em 600–700 e rótulo em 500, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:122`
- Decisão: contraste ≥ 300 em Persuadir, Ler e Experiência; em Operar, 600–700 no título de painel e 500 no rótulo (TIP-09).
- Desempate: tipo de tela.

### Itálico no título
- A: hallmark proíbe título itálico e palavra itálica de ênfase no título, `X/hallmark/SKILL.md:56`
- B: taste manda enfatizar no título com itálico ou negrito da mesma família, `X/taste-skill/skills/taste-skill/SKILL.md:179`
- Decisão: título sempre romano; ênfase por peso, cor ou sublinhado desenhado; itálico só no corpo (TIP-18).
- Desempate: verificável — `font-style` do título é checável e o detector acusa `italic-serif-display`.

### Itálico dentro do hallmark (interna)
- A: a regra de tipografia proíbe itálico no título, `X/hallmark/SKILL.md:56`
- B: o conserto do título em gradiente sugere "peso ou itálico", `X/hallmark/references/anti-patterns.md:39`
- Decisão: vale a proibição; o conserto usa peso ou face de display.
- Desempate: verificável — a proibição é regra explícita, a outra é sugestão de passagem.

### Tracking e entrelinha do display
- A: hallmark usa entrelinha 1.05–1.2 e piso 1.0 em caixa-alta, `X/hallmark/references/typography.md:10`, `X/hallmark/references/typography.md:224`; impeccable põe piso de tracking em −0.04em, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:12`
- B: taste usa `tracking-tighter leading-none`, `X/taste-skill/skills/taste-skill/SKILL.md:166`; brutalist vai a entrelinha 0.85–0.95 e tracking −0.06em, `X/taste-skill/skills/brutalist-skill/SKILL.md:31-32`
- Decisão: tracking ≥ −0.04em, entrelinha 1.05–1.2, caixa-alta ≥ 1.0, itálico com descendente ≥ 1.1 (TIP-17).
- Desempate: verificável — os pisos têm número e o detector acusa `extreme-negative-tracking`.

### Tamanho máximo do display
- A: hallmark ≤ 5.5rem com teto 6rem, `X/hallmark/references/typography.md:190`; impeccable 6rem, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:12`
- B: brutalist `clamp(4rem, 10vw, 15rem)`, `X/taste-skill/skills/brutalist-skill/SKILL.md:30`
- Decisão: ≤ 5.5rem, teto 6rem; palavra única de ≤ 12ch até 7rem (TIP-11).
- Desempate: verificável.

### Tamanho mínimo de texto
- A: hallmark corpo ≥ 16px, nada abaixo de 10px, `X/hallmark/references/typography.md:223`, `X/hallmark/references/typography.md:240`; o detector acusa texto funcional abaixo de 11px, `X/impeccable/crates/live/assets/antipatterns.json:279`
- B: brutalist põe navegação e metadado em 10–14px, `X/taste-skill/skills/brutalist-skill/SKILL.md:39`; taste dá eyebrow de 11px como exemplo, `X/taste-skill/skills/taste-skill/SKILL.md:253`
- Decisão: corpo ≥ 16px; todo texto funcional ≥ 12px, o mesmo piso das direções do catálogo (TIP-13).
- Desempate: verificável.

### Texto claro no escuro
- A: hallmark reduz o peso do corpo em 50 unidades, `X/hallmark/references/color.md:68`
- B: impeccable dá um degrau a mais de peso, mais entrelinha e mais tracking, `X/impeccable/.claude/skills/impeccable/reference/typeset.md:48`
- Decisão: mais entrelinha e tracking (as duas concordam); peso −50 em face variável, nunca abaixo de 300 (TIP-15).
- Desempate: hallmark.

### Space Grotesk, Plus Jakarta e Outfit
- A: hallmark usa Space Grotesk (Cobalt) e Plus Jakarta Sans (Hum), `X/hallmark/SKILL.md:277`; taste recomenda Outfit, `X/taste-skill/skills/taste-skill/SKILL.md:169`; soft recomenda Plus Jakarta Sans, `X/taste-skill/skills/soft-skill/SKILL.md:15`
- B: impeccable lista as três como padrão de treino, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:67`; hallmark proíbe Outfit como padrão, `X/hallmark/references/typography.md:75`
- Decisão: Space Grotesk permitida no display técnico ou brutalista de Experiência e Persuadir; Plus Jakarta Sans no corpo de tom suave; Outfit só escolhida de propósito; exceções no detector para as duas primeiras.
- Desempate: tipo de tela (decisão 5 da spec).

### Pilha do sistema
- A: hallmark proíbe a pilha do sistema como única, `X/hallmark/references/typography.md:236`
- B: impeccable diz que Operar e Ler se servem bem de pilha do sistema, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:67`
- Decisão: pilha do sistema como fonte única permitida em Operar e Ler; em Persuadir e Experiência o display tem face própria (TIP-05).
- Desempate: tipo de tela.

### system-ui no tom Austere (interna do hallmark)
- A: hallmark lista `system-ui` entre os padrões proibidos, `X/hallmark/references/typography.md:40`
- B: o tom Austere do próprio hallmark usa `system-ui` no display e no corpo, `X/hallmark/references/typography.md:129`
- Decisão: o tom austero corresponde a Operar e Ler, onde a pilha do sistema é permitida.
- Desempate: tipo de tela.

## Pontuação, emoji e glifo

### Travessão
- A: hallmark prescreve travessão para interrupção e meia-risca para intervalo, `X/hallmark/references/copy.md:59`, `X/hallmark/references/typography.md:219`
- B: taste proíbe travessão e meia-risca em qualquer lugar, `X/taste-skill/skills/taste-skill/SKILL.md:687`, `X/taste-skill/skills/taste-skill/SKILL.md:693`
- Decisão: permitido com moderação no corpo, evitado em título, botão e rótulo; o detector acusa só a saturação (`em-dash-overuse`) (SLOP-47).
- Desempate: verificável — o limite do detector mede o excesso (decisão 2 da spec).

### Ponto médio
- A: hallmark usa `·` como separador de rodapé, `X/hallmark/references/component-cookbook.md:127`
- B: taste raciona a um por linha, `X/taste-skill/skills/taste-skill/SKILL.md:645`
- Decisão: no máximo um por linha em faixa de metadado; lista longa separa por quebra, fio ou coluna (SLOP-48).
- Desempate: verificável.

### Glifo como ícone
- A: a demonstração de estados do hallmark usa ⌛ ⚠ ✓, `X/hallmark/SKILL.md:111-113`
- B: impeccable proíbe glifo Unicode ou emoji no lugar de ícone, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:40`
- Decisão: ícone de estado ou função vem da biblioteca; seta tipográfica em link de texto vale (SLOP-38).
- Desempate: verificável — presença de glifo no lugar de ícone é checável; o exemplo do hallmark é esquema, não regra.

### Emoji no texto
- A: hallmark e uupm proíbem emoji só como ícone, `X/hallmark/references/assets.md:61`, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:81`
- B: taste desencoraja emoji em qualquer lugar, `X/taste-skill/skills/taste-skill/SKILL.md:148`; minimalist proíbe até em texto alternativo, `X/taste-skill/skills/minimalist-skill/SKILL.md:20`
- Decisão: nunca como ícone; no texto fora por padrão, salvo Experiência de tom lúdico ou social com pedido (SLOP-37, SLOP-39).
- Desempate: tipo de tela.

## Cor

### Espaço de cor
- A: hallmark exige OKLCH em toda cor, `X/hallmark/references/color.md:7`, `X/hallmark/SKILL.md:451`
- B: impeccable manda usar o espaço que o projeto já tem e OKLCH só na paleta nova, `X/impeccable/.claude/skills/impeccable/reference/colorize.md:38`; uupm usa tokens com hex, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:123`
- Decisão: paleta nova em OKLCH; projeto existente mantém o espaço de cor dele (COR-01).
- Desempate: verificável — a regra do impeccable é a mais específica, separa paleta nova de existente.

### Espaço de cor no exemplo do hallmark (interna)
- A: hallmark diz OKLCH só, `X/hallmark/references/color.md:7`
- B: os dois exemplos de paleta do hallmark trazem o acento em hex, `X/hallmark/references/color.md:31`, `X/hallmark/references/color.md:46`
- Decisão: o acento também vai em OKLCH na paleta nova; o hex do exemplo é descuido.
- Desempate: hallmark — vale a regra explícita, não o exemplo.

### Dose de acento
- A: hallmark quer um acento em ≤ 3% da viewport e nunca como grande preenchimento, `X/hallmark/references/color.md:8`, `X/hallmark/references/color.md:79`; taste, um acento, `X/taste-skill/skills/taste-skill/SKILL.md:186`
- B: impeccable admite cor comprometida (30–60% da superfície) e superfície inteira na cor, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:65`, e nega percentual fixo, `X/impeccable/.claude/skills/impeccable/reference/colorize.md:27`
- Decisão: Operar e Ler seguem ≤ 5% (COR-09); Persuadir e Experiência podem usar a estratégia forte quando a direção declara no `sistema.md`.
- Desempate: tipo de tela.

### Neutros
- A: hallmark exige neutro com matiz e proíbe croma zero, `X/hallmark/references/color.md:10`, `X/hallmark/references/color.md:77`
- B: impeccable aceita cinza neutro quando serve ao mundo da peça, `X/impeccable/.claude/skills/impeccable/reference/colorize.md:44`
- Decisão: neutro com croma ≥ 0.005 por padrão; cinza puro só em direção monocromática declarada (COR-05).
- Desempate: hallmark, que já traz a exceção monocromática na nota do gate 22.

### Branco puro
- A: hallmark proíbe `#fff` como superfície base, `X/hallmark/references/color.md:76`; taste proíbe `#000` e `#fff` puros, `X/taste-skill/skills/taste-skill/SKILL.md:585`
- B: minimalist usa canvas `#FFFFFF`, `X/taste-skill/skills/minimalist-skill/SKILL.md:33`
- Decisão: sem `#fff` como base e sem `#000` em lugar nenhum; papel branco só na direção modern-minimal declarada (COR-06).
- Desempate: hallmark.

### Branco puro no modern-minimal (interna do hallmark)
- A: a lista de proibições de cor veta `#fff` como base, `X/hallmark/references/color.md:76`
- B: o gate 7 e a auditoria aceitam papel `#fff` no gênero modern-minimal, `X/hallmark/references/slop-test.md:36`, `X/hallmark/references/verbs/audit.md:16`
- Decisão: vale a exceção de gênero: papel branco só com direção modern-minimal declarada no `sistema.md`.
- Desempate: hallmark — a nota de gênero é a versão mais específica dentro dele.

### Creme
- A: a paleta de exemplo do hallmark é papel de aveia quente, `X/hallmark/references/color.md:25`; soft usa creme `#FDFBF7`, `X/taste-skill/skills/soft-skill/SKILL.md:26`
- B: taste proíbe a família bege como padrão, `X/taste-skill/skills/taste-skill/SKILL.md:192-197`; impeccable chama creme com serif de trilho de IA, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:69-71`; o detector tem `cream-palette`, `X/impeccable/crates/live/assets/antipatterns.json:39`
- Decisão: creme e bege fora como padrão; entram quando a marca pede ou a direção justifica, registrado no `sistema.md` (COR-07).
- Desempate: verificável — o detector acusa a paleta.

### Gradientes
- A: hallmark aceita gradiente de duas paradas e veta os pares de IA, `X/hallmark/references/color.md:83`, `X/hallmark/references/color.md:78`
- B: taste pede gradiente de marca em células de bento, `X/taste-skill/skills/taste-skill/SKILL.md:259`; impeccable chama gradiente de lacuna vestida de cromo, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:128`
- Decisão: gradiente só com propósito, duas paradas, nunca em texto nem nos pares roxo→azul (COR-11, SLOP-02).
- Desempate: hallmark.

### Paradas de gradiente (interna do hallmark)
- A: a lista de proibições de cor aceita só duas paradas, `X/hallmark/references/color.md:83`
- B: o catálogo de recursos e o custom-craft aceitam até três, `X/hallmark/references/assets.md:319`, `X/hallmark/references/custom-craft.md:79`
- Decisão: duas paradas.
- Desempate: hallmark — vale a proibição da seção de cor, a tabela é catálogo.

### Gradientes no minimalist (interna do taste)
- A: minimalist proíbe gradientes, `X/taste-skill/skills/minimalist-skill/SKILL.md:18`
- B: o mesmo arquivo pede manchas de luz radiais e uma bolha que flutua, `X/taste-skill/skills/minimalist-skill/SKILL.md:67`, `X/taste-skill/skills/minimalist-skill/SKILL.md:74`
- Decisão: sem mancha radial decorativa, salvo a exceção atmosférica de Experiência (SLOP-05).
- Desempate: verificável — o detector acusa `radial-spotlight-glow`.

### Modo escuro
- A: taste pede os dois modos e segue `prefers-color-scheme`, `X/taste-skill/skills/taste-skill/SKILL.md:531-535`, `X/taste-skill/skills/taste-skill/SKILL.md:574`; uupm desenha claro e escuro juntos, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:87`
- B: impeccable escolhe um modo pela cena de uso, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:42`; no hallmark o escuro é variante opcional, `X/hallmark/references/export-formats.md:316`
- Decisão: Operar ganha os dois; Persuadir, Ler e Experiência ficam com um, escolhido pelo contexto de uso (decisão 3 da spec).
- Desempate: tipo de tela.

### Acento no escuro
- A: hallmark reduz o croma do acento em 0.02–0.04, `X/hallmark/references/color.md:69`; uupm usa variantes dessaturadas, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:124`
- B: taste diz para não dessaturar a marca no escuro, `X/taste-skill/skills/taste-skill/SKILL.md:584`
- Decisão: mesmo matiz, croma −0.02 a −0.04 e luminosidade +5–10%; a marca continua reconhecível (COR-19).
- Desempate: verificável — a receita do hallmark tem números.

### Alvo de contraste do corpo
- A: hallmark, impeccable e uupm põem 4.5:1 como mínimo e 7:1 como alvo ou opção, `X/hallmark/references/color.md:57`, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:9`, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:125`
- B: taste pede AAA para o corpo, `X/taste-skill/skills/taste-skill/SKILL.md:534`
- Decisão: 4.5:1 é piso em todo tipo; 7:1 é alvo em Ler (COR-14).
- Desempate: tipo de tela.

## Slop

### Número de gates do slop-test (interna do hallmark)
- A: o título e a autocrítica falam em 58 gates, `X/hallmark/references/slop-test.md:1`, `X/hallmark/references/slop-test.md:11`
- B: a lista numerada termina no gate 57, `X/hallmark/references/slop-test.md:186`
- Decisão: vale a lista, 57 gates; `slop.md` cita de 1 a 57.
- Desempate: verificável.

## Layout

### Centralização do hero
- A: hallmark reprova hero com tudo centralizado, no máximo dois elementos no eixo, `X/hallmark/references/slop-test.md:35`, `X/hallmark/references/layout-and-space.md:74`
- B: taste aceita centralizar com variação ≤ 4 ou em manifesto, `X/taste-skill/skills/taste-skill/SKILL.md:210-211`; no uupm variação baixa é centralizada, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md:121`
- Decisão: com VARIACAO ≥ 5 (Persuadir, Experiência) vale o gate 6; com VARIACAO ≤ 4 (Operar, Ler) a coluna centralizada é permitida (LAY-08, SLOP-13).
- Desempate: tipo de tela.

### Eyebrow
- A: impeccable proíbe sem exceção, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:27`; hallmark desliga por padrão, `X/hallmark/references/anti-patterns.md:149`, `X/hallmark/references/anti-patterns.md:151`
- B: taste aceita um a cada três seções, um no hero, `X/taste-skill/skills/taste-skill/SKILL.md:240`, `X/taste-skill/skills/taste-skill/SKILL.md:254-255`; soft exige pílula acima de todo título, `X/taste-skill/skills/soft-skill/SKILL.md:52`
- Decisão: desligado por padrão em todo tipo de tela; o detector acusa `kicker-above-heading` e `hero-eyebrow-chip` (SLOP-22).
- Desempate: verificável.

### Números de seção
- A: hallmark aceita em Long Document, Manifesto ou Catálogo com conteúdo ordinal, `X/hallmark/SKILL.md:450`; impeccable, quando a sequência carrega informação, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:28`
- B: taste proíbe número de seção e rótulo de etapa genérico, `X/taste-skill/skills/taste-skill/SKILL.md:639`, `X/taste-skill/skills/taste-skill/SKILL.md:664`
- Decisão: número de seção só quando a ordem informa o leitor (passo a passo, capítulo, documentação em Ler); nunca ao lado do título na mesma linha (SLOP-21, SLOP-22).
- Desempate: tipo de tela.

### Card aninhado
- A: hallmark e impeccable proíbem card dentro de card, `X/hallmark/references/layout-and-space.md:76`, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:25`
- B: soft exige a moldura dupla (casca e núcleo) em todo card grande, `X/taste-skill/skills/soft-skill/SKILL.md:41-44`, `X/taste-skill/skills/soft-skill/SKILL.md:90`
- Decisão: nenhum card dentro de card (SLOP-11); o efeito de moldura dupla sai de borda e fundo num contêiner só.
- Desempate: verificável — o detector acusa `nested-cards`.

### Raio
- A: taste quer um sistema de raio por página, `X/taste-skill/skills/taste-skill/SKILL.md:217`; hallmark usa tokens por papel, `X/hallmark/references/export-formats.md:40`
- B: soft exige `rounded-[2rem]` e botão pílula, `X/taste-skill/skills/soft-skill/SKILL.md:47`, `X/taste-skill/skills/soft-skill/SKILL.md:82`; minimalist veta pílula e fica em ≤ 12px, `X/taste-skill/skills/minimalist-skill/SKILL.md:19`, `X/taste-skill/skills/minimalist-skill/SKILL.md:46`; brutalist zera o raio, `X/taste-skill/skills/brutalist-skill/SKILL.md:71`
- Decisão: um sistema por página em tokens por papel, valor escolhido pela direção; mistura só com regra escrita no `sistema.md` (LAY-33).
- Desempate: verificável — o detector acusa `design-system-radius`.

### Escala de espaço
- A: hallmark usa 2/4/8/12/16/24/40/64/96/144, `X/hallmark/references/layout-and-space.md:15-29`
- B: uupm usa base 4/8 e degraus 16/24/32/48, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:101`, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/pro-rules.md:58`; taste muda o padding de seção pela densidade, `X/taste-skill/skills/taste-skill/SKILL.md:566-567`; soft dobra o padding, `X/taste-skill/skills/soft-skill/SKILL.md:51`
- Decisão: base 4px com a escala nomeada do hallmark (LAY-03); a faixa entre seções vem de DENSIDADE (LAY-02).
- Desempate: hallmark.

### Breakpoints
- A: hallmark quer breakpoint onde o conteúdo quebra, em rem, e proíbe px fixo, `X/hallmark/references/responsive.md:22`, `X/hallmark/references/responsive.md:35`, `X/hallmark/references/responsive.md:137`
- B: taste fixa 640/768/1024/1280/1536, `X/taste-skill/skills/taste-skill/SKILL.md:151`; uupm 375/768/1024/1440, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:97`; impeccable dá faixas fixas por aparelho, `X/impeccable/.claude/skills/impeccable/reference/adapt.md:133-135`, e no mesmo arquivo manda não usar breakpoint genérico, `X/impeccable/.claude/skills/impeccable/reference/adapt.md:176`
- Decisão: mobile-first, breakpoint em rem onde o conteúdo quebra (padrão 40/60/90rem); as larguras fixas viram só pontos de conferência: 320, 375, 414, 768, 1024, 1440 (LAY-21, LAY-22).
- Desempate: hallmark.

### Z-index
- A: hallmark usa escala nomeada 1/10/100/200/400/500/600, `X/hallmark/references/layout-and-space.md:58-69`
- B: uupm sugere 0/10/20/40/100/1000, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:104`; taste só pede escala documentada, `X/taste-skill/skills/taste-skill/SKILL.md:548`
- Decisão: tokens do hallmark, `--z-base` a `--z-tooltip`; nenhum número solto (LAY-31).
- Desempate: hallmark.

### Sombras
- A: hallmark tira profundidade do peso e aceita só a sombra sussurro ou o anel sem deslocamento, `X/hallmark/references/layout-and-space.md:53-57`
- B: impeccable exige deslocamento e desfoque e chama o halo sem deslocamento de decoração, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:10`; soft usa sombra ambiente muito difusa, `X/taste-skill/skills/soft-skill/SKILL.md:27`
- Decisão: peso e escala antes de sombra; sombra única com deslocamento e desfoque, tingida; anel de 1px vale como borda, nunca colorido como halo (LAY-32).
- Desempate: verificável.

### Janela falsa
- A: hallmark proíbe barra de navegador, celular e janela de código desenhados, `X/hallmark/SKILL.md:52`; taste proíbe screenshot falso feito de div, `X/taste-skill/skills/taste-skill/SKILL.md:290`, `X/taste-skill/skills/taste-skill/SKILL.md:655`
- B: minimalist manda envolver o software numa janela com três bolinhas cinza, `X/taste-skill/skills/minimalist-skill/SKILL.md:60-61`; o bloco H8 do próprio hallmark desenha as bolinhas, `X/hallmark/references/components/h8-mockup-split-browser-framed.md:13-22`
- Decisão: nenhuma moldura desenhada (SLOP-43); o H8 do catálogo usa as variantes fio fino ou sem moldura, com print real.
- Desempate: hallmark — vale a regra do `SKILL.md`, o bloco é exemplo.

### Texto do hero
- A: hallmark põe o título em ≤ 7 palavras e ≤ 50 caracteres e o hero na dobra, `X/hallmark/SKILL.md:449`, `X/hallmark/references/slop-test.md:136`
- B: taste mede o subtexto (≤ 20 palavras, 3–4 linhas) e o tamanho pelo número de palavras, `X/taste-skill/skills/taste-skill/SKILL.md:236-237`
- Decisão: título ≤ 7 palavras e ≤ 50 caracteres em até 2 linhas; lede ≤ 20 palavras em até 3 linhas; CTA sem rolar (LAY-15, LAY-17).
- Desempate: verificável.

### Cabeçalho dividido (interna do taste)
- A: taste proíbe título à esquerda com parágrafo pequeno à direita, `X/taste-skill/skills/taste-skill/SKILL.md:258`
- B: o mesmo arquivo oferece "cabeçalho limpo de duas colunas" como conserto, `X/taste-skill/skills/taste-skill/SKILL.md:674`
- Decisão: empilhado por padrão; duas colunas só quando a da direita traz visual ou controle (LAY-10).
- Desempate: verificável — a proibição dá a condição de exceção.

### Navegação
- A: hallmark proíbe a barra fixa padrão de largura total e gira o arquétipo, `X/hallmark/references/anti-patterns.md:77`, `X/hallmark/SKILL.md:294`; soft também veta a barra colada no topo, `X/taste-skill/skills/soft-skill/SKILL.md:18`
- B: uupm quer a navegação na mesma posição em todas as páginas, com ícone e rótulo, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:217`, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:204`
- Decisão: Persuadir e Experiência giram o arquétipo; Operar e Ler repetem a mesma navegação em toda tela, e em Operar o item leva ícone e rótulo (LAY-19).
- Desempate: tipo de tela.

### Imagem
- A: no hallmark o padrão é só tipografia, com arte em CSS e SVG antes de imagem gerada, `X/hallmark/SKILL.md:397`, `X/hallmark/SKILL.md:401`
- B: taste manda gerar imagem primeiro e chama página só de texto de incompleta, `X/taste-skill/skills/taste-skill/SKILL.md:267`, `X/taste-skill/skills/taste-skill/SKILL.md:274`; impeccable faz de todo desenho maior que ícone uma placa gerada, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:110`
- Decisão: Persuadir de produto físico, comida, pessoa ou moda usa imagem real ou gerada; Operar e Ler, sem imagem decorativa; Experiência, pela direção. Sem imagem à mão, espaço rotulado e pedido ao usuário, nunca div imitando print.
- Desempate: tipo de tela.

### Conteúdo inventado
- A: hallmark proíbe métrica e logo inventados, `X/hallmark/SKILL.md:48`; impeccable exige afirmação verdadeira, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:59`; taste marca número falso-preciso, `X/taste-skill/skills/taste-skill/SKILL.md:327-330`
- B: o mesmo taste manda inventar marca em SVG para marca inventada, `X/taste-skill/skills/taste-skill/SKILL.md:279`, e usar dado "orgânico" como 47.2%, `X/taste-skill/skills/taste-skill/SKILL.md:618`
- Decisão: nenhum número, logo ou depoimento inventado; dado de demonstração rotulado como fictício; marca fictícia vai em texto, sem logo desenhado (SLOP-46).
- Desempate: hallmark, que o taste confirma na regra de `:327`.

## Movimento

### Propriedades animadas
- A: hallmark, taste e uupm animam só `transform` e `opacity`, `X/hallmark/references/motion.md:9`, `X/taste-skill/skills/taste-skill/SKILL.md:522`, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:137`
- B: impeccable manda ir além (blur, `clip-path`, máscara, sombra), `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:13`, `X/impeccable/.claude/skills/impeccable/reference/animate.md:38-43`; o próprio hallmark anima a largura do sublinhado da aba, `X/hallmark/references/microinteractions.md:144`
- Decisão: transição de UI só `transform` e `opacity` (a aba usa `scaleX`); blur, máscara e sombra só no momento autoral de Persuadir e Experiência (MOV-05).
- Desempate: tipo de tela.

### Duração
- A: hallmark usa 120/220/420ms, tudo entre 100 e 500ms, `X/hallmark/references/motion.md:10`, `X/hallmark/references/motion.md:31-36`
- B: impeccable aceita 500–800ms na entrada autoral, `X/impeccable/.claude/skills/impeccable/reference/animate.md:59`; taste revela em 600ms, `X/taste-skill/skills/taste-skill/SKILL.md:494`; soft usa 700–800ms, `X/taste-skill/skills/soft-skill/SKILL.md:55`, `X/taste-skill/skills/soft-skill/SKILL.md:69`
- Decisão: UI nos tokens de 120/220/420ms; só a entrada autoral de Persuadir e Experiência vai até 800ms (MOV-08).
- Desempate: tipo de tela.

### Easing
- A: hallmark fixa três curvas em token, sem ultrapassagem, `X/hallmark/references/motion.md:15-27`, `X/hallmark/references/motion.md:103`; impeccable usa desaceleração exponencial, `X/impeccable/.claude/skills/impeccable/reference/animate.md:61`
- B: uupm prefere mola a cubic-bezier, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:145`; taste usa mola no movimento perpétuo, `X/taste-skill/skills/taste-skill/SKILL.md:358`; soft proíbe `ease-in-out`, `X/taste-skill/skills/soft-skill/SKILL.md:19`, que o hallmark mantém como token, `X/hallmark/references/motion.md:23`
- Decisão: as três curvas do hallmark em token; mola só em interação física, sem passar de ~110% (MOV-10, MOV-11).
- Desempate: hallmark.

### Reveal no scroll
- A: hallmark faz uma entrada e nenhuma animação de scroll depois, `X/hallmark/references/microinteractions.md:196`; impeccable quer um momento autoral e conteúdo visível por padrão, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:13`, `X/impeccable/.claude/skills/impeccable/reference/animate.md:71`
- B: taste exige reveal nas seções-chave acima de movimento 4, `X/taste-skill/skills/taste-skill/SKILL.md:359`; minimalist anima todo bloco, `X/taste-skill/skills/minimalist-skill/SKILL.md:83`; soft não deixa nada aparecer parado, `X/taste-skill/skills/soft-skill/SKILL.md:69`
- Decisão: dispara uma vez, nunca no corpo de texto, nunca igual em toda seção; MOVIMENTO 1–3 nenhum, 4–7 até duas seções-chave, 8–10 coreografia declarada (MOV-15).
- Desempate: tipo de tela.

### Stagger
- A: uupm usa 30–50ms por item, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:147`; hallmark 60ms com teto de ~500ms, `X/hallmark/references/motion.md:61`, `X/hallmark/references/motion.md:68`
- B: o próprio hallmark usa 100ms, `X/hallmark/references/microinteractions.md:32`; taste 100ms, `X/taste-skill/skills/taste-skill/SKILL.md:515`; minimalist 80ms, `X/taste-skill/skills/minimalist-skill/SKILL.md:73`
- Decisão: 40–60ms por item (60 padrão), total ≤ 500ms (MOV-14).
- Desempate: verificável — o teto total se mede.

### Movimento reduzido
- A: hallmark reduz a crossfade ≤ 150ms, `X/hallmark/references/motion.md:13`; impeccable reduz sem apagar o feedback, `X/impeccable/.claude/skills/impeccable/reference/animate.md:77`
- B: taste faz tudo virar estático ou instantâneo, `X/taste-skill/skills/taste-skill/SKILL.md:529`
- Decisão: movimento espacial vira crossfade ≤ 150ms ou nada; loop, parallax e física param; feedback de estado fica (MOV-23).
- Desempate: hallmark.

### Parallax
- A: hallmark proíbe, `X/hallmark/references/motion.md:106`, `X/hallmark/references/microinteractions.md:211`
- B: uupm aceita com parcimônia, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:144`; taste libera com movimento 8–10, `X/taste-skill/skills/taste-skill/SKILL.md:563`
- Decisão: fora em Persuadir, Operar e Ler; em Experiência só com MOVIMENTO ≥ 8 e parado em movimento reduzido (MOV-17).
- Desempate: tipo de tela.

### Marquee
- A: o detector acusa faixa que rola sozinha, `X/impeccable/crates/live/assets/antipatterns.json:111`; hallmark proíbe loop infinito, `X/hallmark/references/motion.md:109`
- B: taste aceita um por página, `X/taste-skill/skills/taste-skill/SKILL.md:361`; o próprio hallmark tem marquee infinito de 40–60s, `X/hallmark/references/microinteractions.md:31`
- Decisão: fora por padrão; com pedido do usuário, um por página com pausa e parada em movimento reduzido, e o alarme se refuta citando o pedido (MOV-20). Sem exceção no detector.
- Desempate: verificável.

### Mudança instantânea
- A: hallmark diz que 0ms é muitas vezes a resposta certa e que o foco nunca anima, `X/hallmark/references/microinteractions.md:65`, `X/hallmark/references/microinteractions.md:218`
- B: uupm lista mudança instantânea como antipadrão e quer estado animado, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md:23`, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:142`
- Decisão: foco, teclado, erro e paleta de comandos em 0ms; hover, pressionar, abrir e fechar com os tokens (MOV-12).
- Desempate: verificável.

### Listener de scroll
- A: hallmark e taste proíbem ouvir o evento de scroll, `X/hallmark/references/motion.md:72`, `X/taste-skill/skills/taste-skill/SKILL.md:511`
- B: uupm e impeccable aceitam com debounce ou throttle, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:73`, `X/impeccable/.claude/skills/impeccable/reference/optimize.md:137`
- Decisão: animação lê o scroll por IntersectionObserver, `animation-timeline` ou biblioteca; listener com throttle só para lógica que não anima (MOV-16).
- Desempate: verificável.

## Ícones

### Lucide
- A: hallmark faz de Lucide o padrão, `X/hallmark/references/anti-patterns.md:199`, `X/hallmark/references/assets.md:394`; uupm o cita, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:81`; o `init` do shadcn o escolhe, `X/ui/packages/shadcn/src/commands/init.ts:975`
- B: taste aceita Lucide só a pedido e põe Phosphor primeiro, `X/taste-skill/skills/taste-skill/SKILL.md:141-142`, `X/taste-skill/skills/taste-skill/SKILL.md:623`; minimalist e soft o proíbem, `X/taste-skill/skills/minimalist-skill/SKILL.md:15`, `X/taste-skill/skills/soft-skill/SKILL.md:16`
- Decisão: Lucide é o ícone padrão em todo tipo de tela; projeto com outra família mantém a dela (COMP-04).
- Desempate: hallmark (decisão 1 da spec).

### SVG desenhado à mão
- A: hallmark aceita marca em SVG próprio e põe SVG feito à mão antes de imagem gerada, `X/hallmark/references/anti-patterns.md:223`, `X/hallmark/SKILL.md:401`; impeccable aceita ícone em SVG autoral, `X/impeccable/.claude/skills/impeccable/reference/craft-floor.md:40`
- B: taste proíbe desenhar ícone e desencoraja SVG decorativo, `X/taste-skill/skills/taste-skill/SKILL.md:143`, `X/taste-skill/skills/taste-skill/SKILL.md:285`; impeccable faz de SVG maior que ícone uma placa, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:110`
- Decisão: ícone vem da biblioteca, nunca desenhado (COMP-05); SVG próprio só para forma simples (marca geométrica, ornamento, divisor), antes de Lottie (SLOP-40); cena montada de formas primitivas fora (o detector acusa `shape-assembled-illustration`).
- Desempate: verificável.

## UX

### Ação destrutiva
- A: hallmark troca a confirmação por atualização otimista com desfazer, `X/hallmark/references/microinteractions.md:215`, `X/hallmark/SKILL.md:459`; impeccable prefere desfazer quando recuperar é seguro, `X/impeccable/.claude/skills/impeccable/reference/clarify.md:37`
- B: uupm confirma antes de toda ação destrutiva, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:170`; a heurística 5 do impeccable pede o mesmo, `X/impeccable/.claude/skills/impeccable/reference/critique.md:481`
- Decisão: reversível executa na hora e oferece desfazer, sem confirmação (UX-11); irreversível (apagar para sempre, pagamento) pede confirmação que nomeia ação e objeto, e excluir conta exige digitar o nome (UX-12).
- Desempate: hallmark, que separa os dois casos em `X/hallmark/references/interaction-and-states.md:147-148` (decisão 4 da spec).

### Feedback de sucesso
- A: hallmark quer sucesso silencioso, sem toast de "Pronto!", `X/hallmark/references/microinteractions.md:10`, `X/hallmark/references/microinteractions.md:214`
- B: uupm confirma toda ação concluída com check, toast ou lampejo de cor, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:179`
- Decisão: efeito visível na tela dispensa aviso; efeito invisível ganha sinal curto no próprio controle ou toast; nunca comemoração (UX-09, SLOP-28).
- Desempate: hallmark.

### Sucesso dentro do hallmark (interna)
- A: a tabela de estados dá ao sucesso check verde, confirmação e sumiço automático, `X/hallmark/references/interaction-and-states.md:16`
- B: as microinterações dizem que ação bem-sucedida não merece confirmação, `X/hallmark/references/microinteractions.md:10`
- Decisão: o check vale no próprio controle ou campo (estado de sucesso do elemento); confirmação à parte só para efeito invisível (UX-09).
- Desempate: verificável — o efeito está ou não está na tela.

### Duração de toast
- A: hallmark deixa o toast 4–6s, `X/hallmark/references/microinteractions.md:128`, e o de desfazer 5–10s, `X/hallmark/references/interaction-and-states.md:147`
- B: uupm fecha em 3–5s, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:169`
- Decisão: informativo 5s, com desfazer 8s, pausa com ponteiro ou foco, erro com ação fica até ser dispensado (UX-10).
- Desempate: verificável — 5s cabe nas duas faixas e se mede.

### Indicador de carregamento
- A: taste usa esqueleto e evita spinner genérico, `X/taste-skill/skills/taste-skill/SKILL.md:221`; hallmark prefere esqueleto quando a forma é previsível, `X/hallmark/references/interaction-and-states.md:152`
- B: uupm põe spinner no botão durante a operação, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:40`; hallmark manda o spinner trocar o rótulo, `X/hallmark/references/interaction-and-states.md:153`, e também manter o rótulo legível, `X/hallmark/references/interaction-and-states.md:14`
- Decisão: esqueleto para conteúdo de forma previsível; spinner só no botão ou campo, no lugar do ícone, com o rótulo virando a ação em curso e a largura fixa (UX-05).
- Desempate: hallmark.

### Alvo de toque
- A: hallmark pede 44×44 CSS px, `X/hallmark/references/interaction-and-states.md:42`; impeccable 44px na auditoria e 44pt na persona móvel, `X/impeccable/.claude/skills/impeccable/reference/audit.md:50`, `X/impeccable/.claude/skills/impeccable/reference/critique.md:762`
- B: uupm aceita 24×24 CSS px na web (WCAG 2.2) e deixa 44pt/48dp para o nativo, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:28`, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:37`
- Decisão: 44×44 CSS px em todo tipo de tela, com a área clicável maior que o desenho quando preciso (LAY-26); 24px é o mínimo da WCAG, não o alvo.
- Desempate: hallmark.

### Escala ao pressionar
- A: hallmark e taste usam `scale(0.98)`, `X/hallmark/references/microinteractions.md:106`, `X/taste-skill/skills/taste-skill/SKILL.md:224`
- B: uupm aceita 0.95–1.05, `X/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/references/quick-reference.md:152`
- Decisão: `scale(0.98)` ou `translateY(1px)` no `:active`, em `--dur-micro`; nunca cresce ao pressionar (UX-03).
- Desempate: hallmark.

## Processo

### Perguntas antes de desenhar
- A: hallmark sempre faz três perguntas, sem exceção, `X/hallmark/SKILL.md:211`, `X/hallmark/SKILL.md:228`; impeccable faz duas ou três, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:20`
- B: taste não pergunta quando dá para deduzir e, na dúvida, faz uma pergunta só, `X/taste-skill/skills/taste-skill/SKILL.md:33-36`
- Decisão: bifurcação da spec: tela nova vai com questionário (perguntas livres no chat, uma por vez, com opções e recomendação); tela existente vai direto, com as respostas deduzidas mostradas junto do resultado; o usuário troca.
- Desempate: hallmark, que sempre oferece a pergunta (decisão A4 da spec).

### Rodadas de verificação
- A: hallmark corrige até todo gate passar, `X/hallmark/SKILL.md:474`; taste não entrega com caixa desmarcada, `X/taste-skill/skills/taste-skill/SKILL.md:979`
- B: impeccable verifica em rodadas limitadas, no máximo duas, `X/impeccable/.claude/skills/impeccable/SKILL.md:15`, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:138`
- Decisão: até 3 rodadas; o que sobra vai na entrega com id e motivo; acessibilidade e contraste nunca sobram (VER-17).
- Desempate: verificável — o limite se conta, e o que não pode sobrar se mede.

### Metadado no código
- A: hallmark carimba no CSS as notas da autocrítica e a macroestrutura, `X/hallmark/SKILL.md:46`, `X/hallmark/SKILL.md:461`
- B: impeccable proíbe direção e contrato no código, até em comentário, `X/impeccable/.claude/skills/impeccable/reference/new-work.md:77`
- Decisão: nada de metadado no código; direção e sistema em `docs/design/sistema.md`, rotação em `docs/design/rotacao.json`.
- Desempate: verificável — o registro em `docs/design/` se confere por script (`ferramentas/rotacao.py`).

### Insistência do usuário
- A: impeccable diz que o pedido vence, `X/impeccable/.claude/skills/impeccable/SKILL.md:27`; hallmark faz o que o usuário insiste, `X/hallmark/references/typography.md:44`
- B: o mesmo hallmark diz que a proibição do eyebrow não cede a pedido de paridade, `X/hallmark/references/anti-patterns.md:155`
- Decisão: pedido explícito vence regra de gosto (face, eyebrow, marquee, emoji), fica em `docs/design/sistema.md` e o alarme do detector se refuta citando o pedido (VER-11); nunca vence regra que se mede (contraste, tamanho mínimo, alvo de toque, acessibilidade).
- Desempate: verificável.

### Escolha de design system
- A: taste usa o sistema oficial quando o pedido o implica (Fluent, Carbon, GOV.UK) e nunca mistura, `X/taste-skill/skills/taste-skill/SKILL.md:86-104`
- B: hallmark exporta os tokens para as variáveis do shadcn, `X/hallmark/SKILL.md:465`, e a spec põe shadcn em todo projeto React; taste aceita shadcn só fora do estado padrão, `X/taste-skill/skills/taste-skill/SKILL.md:627`
- Decisão: shadcn é o padrão em React (COMP-06), nunca no estado padrão (COMP-08); projeto já num sistema oficial, ou pedido que o exige, segue o dele, sem misturar (COMP-09).
- Desempate: verificável — `components.json` ou o pacote do sistema no `package.json` decide.
