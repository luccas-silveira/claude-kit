---
name: vesta-interface
description: Desenha e revisa interface (tela, página ou componente) num fluxo de cinco passos que junta hallmark, taste-skill, impeccable, ui-ux-pro-max, shadcn, inspo, Playwright e Chrome DevTools. Use ao criar ou redesenhar landing, painel, CRM, formulário, documentação, artigo, portfólio ou campanha; ao revisar ou auditar uma tela existente; ao estudar o visual de uma URL ou print de referência; ao desenhar um componente isolado com prévia de estados; ou num ajuste de tela pronta (bolder, quieter, distill, harden, onboard, optimize, polish, delight). Entrega código shadcn em projeto React e HTML autocontido nos outros, verificado no navegador antes de entregar. É a camada de interface da Vesta, chamada no passo de mockup. Dispara em "/vesta-interface", "desenha a tela", "faz a landing", "melhora o visual", "revisa essa interface", "estuda este site" ou em qualquer pedido de UI.
---

# vesta-interface

Pedido de interface vira tela verificada em cinco passos, nesta ordem. Cada passo manda abrir uma
referência antes de seguir: abra de fato, as regras moram lá. O que vale sempre está no
`## Piso`, logo abaixo.

Desempate entre regras, nesta ordem: o tipo de tela (a versão em `## Por tipo de tela` de cada
referência); a regra mais específica e verificável; o hallmark. As decisões já tomadas estão em
`referencias/fontes.md`.

## Piso

Vale em toda tela, de todo tipo, sem precisar abrir nada. O relatório do passo 5 confere cada
linha pelo id; o texto completo está na referência do prefixo.

- **SLOP-02** Nenhum texto em gradiente, nenhum gradiente roxo→azul ou brilho roxo.
- **SLOP-37** Uma família de ícones, traço constante (Lucide por padrão); emoji nunca como ícone.
- **SLOP-10** Nada de três cards iguais com ícone, título e texto como estrutura.
- **SLOP-11** Nenhum card dentro de card.
- **SLOP-22** Eyebrow acima do título fora por padrão; número de seção só se informa.
- **SLOP-21** Nenhum rótulo, número ou tag em coluna ao lado do título da seção.
- **SLOP-46** Nenhum número ou alegação inventada; sem dado, marcador rotulado.
- **SLOP-44** Vidro e desfoque só com função, com alternativa sólida.
- **SLOP-49** Sem jargão de marketing; verbo concreto.
- **TIP-01** Faces batidas (Inter, Roboto, Open Sans, Poppins…) fora por padrão.
- **TIP-12** Corpo ≥ 16px, entrelinha 1.5–1.65, medida 45–75 caracteres.
- **TIP-20** Níveis de título sem pular.
- **TIP-21** Números tabulares em dado, preço e tabela.
- **TIP-22** `font-display: swap` e fallback com métricas ajustadas.
- **COR-02** Tokens semânticos no `:root`; componente nunca usa valor cru.
- **COR-12** Contraste ≥ 4.5:1 no corpo, ≥ 3:1 em texto grande, ícone e borda de controle.
- **COR-13** Anel de foco visível, ≥ 3:1 contra o fundo vizinho.
- **COR-15** Nada de texto cinza sobre fundo colorido.
- **COR-16** Cor nunca é o único sinal.
- **COR-18** Modo escuro desenhado, não invertido.
- **LAY-03** Espaçamento em escala nomeada de base 4px; nenhum valor solto.
- **LAY-22** Nenhuma rolagem horizontal de 320 a 1440px.
- **LAY-26** Alvo de toque ≥ 44×44px, ≥ 8px entre alvos.
- **LAY-31** z-index em escala nomeada de tokens.
- **MOV-02** Todo movimento comunica algo; se ninguém notaria, corte.
- **MOV-03** Um momento autoral por página, em 1–2 elementos.
- **MOV-05** Transição de UI só em `transform` e `opacity`.
- **MOV-09** Saída com 60–75% da duração da entrada.
- **MOV-10** Curvas em tokens, entrada com `cubic-bezier(0.16, 1, 0.3, 1)`.
- **MOV-23** Toda animação tem caminho em `prefers-reduced-motion: reduce`.
- **UX-01** Oito estados em todo interativo (padrão, hover, foco, pressionado, desabilitado, carregando, erro, sucesso) e vazio onde há dado.
- **UX-08** Erro diz o que falhou, por quê e como sair, perto da origem.
- **UX-14** Rótulo visível acima do campo; placeholder nunca faz de rótulo.
- **UX-15** Ajuda e erro embaixo do campo, no mesmo lugar reservado.
- **UX-16** Validar ao sair do campo, não a cada tecla.
- **UX-26** Uma ação primária por tela; nenhum par de CTAs com a mesma intenção.
- **UX-11** Destrutiva reversível executa na hora, com desfazer, sem confirmação.
- **UX-12** Irreversível pede confirmação que nomeia ação e objeto.
- **UX-20** Tudo que funciona com mouse funciona com teclado.

## Modos

Antes do passo 1, veja se o pedido é um destes; se for, abra o modo e siga por ele.

- Referência trazida pelo usuário (URL ou print) para extrair o visual: `modos/estudo.md`.
- Um elemento só (botão, campo, card, modal): `modos/componente.md`.
- Ajuste de tela pronta (bolder, quieter, distill, harden, onboard, optimize, polish, delight):
  `modos/ajustes.md`.
- Revisar ou auditar tela existente sem pedido de mudança: rode só os passos 3 e 5, com a crítica
  heurística de `referencias/ux.md` (`## Crítica heurística`) na rodada; entregue o relatório e
  as notas antes de corrigir qualquer coisa.

Dentro da Vesta, o passo de mockup chama este fluxo inteiro; fora dela, vale o mesmo.

## Passo 1 — Entender o pedido

Abra `referencias/layout.md` agora e leia a `## Botões`.

1. **Varra o projeto existente** antes de desenhar: fontes carregadas, paleta e tokens,
   espaçamento, raio, framework (há React? há `components.json`?), biblioteca de movimento,
   família de ícones e se já existe `docs/design/sistema.md` ou `docs/design/rotacao.json`. Anote
   cada achado com arquivo:linha. O que o projeto já decidiu vence a sugestão; o sistema existente
   é seguido, não reinventado.
2. **Classifique no tipo de tela**, um dos quatro: **Persuadir** (landing, página de venda),
   **Operar** (painel, CRM, formulário), **Ler** (documentação, artigo) ou **Experiência**
   (portfólio, campanha). O tipo de tela decide as regras de `## Por tipo de tela` em cada
   referência.
3. **Fixe os três botões pelo tipo de tela**, com a tabela da `## Botões`: VARIACAO, MOVIMENTO e
   DENSIDADE, de 1 a 10. Projeto com `sistema.md` já tem os seus; redesenho parte dos valores
   lidos no site existente.
4. **Escolha a bifurcação.** Padrão: tela nova, com questionário; tela existente mudando, direto.
   O usuário troca quando quiser.
   - **Com questionário:** faça as perguntas de design que a tela pede, sem lista fixa, cada uma
     com a ferramenta `AskUserQuestion`: uma pergunta por chamada, com opções, a recomendada em
     primeiro lugar e marcada "(Recomendado)", e aceite a resposta livre ("Outro") do usuário.
     No questionário o usuário pode mudar os três botões: mostre os valores de VARIACAO,
     MOVIMENTO e DENSIDADE e pergunte se ajusta. Em tela nova, a direção não é perguntada: o
     usuário a escolhe vendo os dois mockups do passo 3; as outras perguntas continuam.
   - **Direto:** deduza as respostas (tipo de tela, direção, botões, tom) e mostre as respostas
     deduzidas junto do resultado, para o usuário corrigir.
5. **Busque no banco do ui-ux-pro-max** estilo, paleta e fontes para o produto, com a busca do
   tipo de tela (sem `--persist`: o sistema do projeto mora só no `sistema.md`):
   - Em Persuadir e Experiência, o design system, que aceita `--variance`, `--motion` e
     `--density` com os valores dos três botões:
     `python3 ferramentas/uupm/scripts/search.py "<produto> <público> <tom>" --design-system --format markdown`
   - Em Operar e Ler, uma busca por domínio, sem botões (ali são ignorados) e sem
     `--domain product`: o design system e o produto sempre trazem um padrão de landing.
     ```
     for d in style color typography ux; do python3 ferramentas/uupm/scripts/search.py "<produto> <público> <tom>" --domain $d; done
     ```

   A busca sugere; as regras vetam. Antes de levar a sugestão ao desenho, corte o que o `## Piso`
   e as referências proíbem (vidro decorativo, acento roxo, face batida). Consultas de UX,
   formulário e `--stack shadcn` entram sem filtro.

## Passo 2 — Referências

Abra `catalogo/macrostructures.md` agora: é com os nomes dele que cada referência vira estrutura.

1. Busque sites reais no inspo: um `mcp__inspo__recommend` com o pedido (produto, público, tipo de
   tela, direção), um ou dois `mcp__inspo__search_screens`, e `mcp__inspo__get_screen` nas que
   ficarem. Guarde de 2 a 5.
2. De cada uma, diga em uma linha o que entra: a macroestrutura mais próxima, o arquétipo de menu
   e hero, o ritmo. Leve a composição, nunca a transgressão: o que a referência faz e o `## Piso`
   proíbe fica fora.
3. Referência que o usuário trouxe passa pelo `modos/estudo.md` antes.
4. Tela de Operar ou Ler num projeto com `sistema.md` segue o sistema: pule a busca e diga por quê.

## Passo 3 — Sistema visual

Abra `referencias/tipografia.md`, `referencias/cor.md`, `referencias/layout.md` e
`referencias/movimento.md` agora; de cada `## Por tipo de tela`, leia só o tipo desta tela.

1. **Direção.** Escolha uma em `catalogo/direcoes/` (minimalista, sofisticada, brutalista) ou um
   tema de `catalogo/themes/`, com o gênero de `catalogo/genres/`. Abra `catalogo/README.md` para
   ver o que existe. Dentro da direção, as regras dela vencem as de gosto, nunca as mensuráveis
   (contraste, tamanho mínimo de texto, acessibilidade).
2. **Tokens.** Cor, tipografia, espaçamento, raio, sombra, z-index, duração e curva, pelas quatro
   referências abertas e pelos três botões.
3. **Estrutura.** Macroestrutura em `catalogo/macrostructures.md`; menu e rodapé em
   `catalogo/component-cookbook.md`, abrindo só os arquétipos escolhidos em `catalogo/components/`.
   - Em Operar e Ler, menu e rodapé vêm do `docs/design/sistema.md`: telas de app repetem de
     propósito. Sem sistema ainda, escolha uma vez e grave.
   - Em Persuadir e Experiência, a estrutura gira entre telas, pela rotação gravada em
     `docs/design/rotacao.json`. Rode `ferramentas/rotacao.py ultimas --projeto .` antes de
     escolher; ele imprime as 3 últimas de Persuadir e Experiência.
   - Escreva no chat, antes de escolher o menu, a linha:
     "Últimas: <macro/menu/rodapé das 3 últimas>; esta: <macro>, <menu>, <rodapé>, porque <motivo>."
     Primeira tela do projeto: "Últimas: nenhuma; esta: …, porque …".
   - Registre antes de construir, com os ids do catálogo (ex.: `03-marquee-hero`, `n5`, `ft5`):
     `ferramentas/rotacao.py registrar --projeto . --tela <nome> --tipo <Persuadir|Experiência> --macro <id> --menu <id> --rodape <id>`
     Saiu 1, o script diz o que repetiu: troque essa peça e registre de novo. Nunca construa sem
     o registro.
4. **Mockup de direções.** Em tela nova, duas versões estáticas da vista principal, cada uma numa
   direção diferente: de `catalogo/direcoes/`, de `catalogo/themes/` ou de referências do inspo
   diferentes, nunca duas variações de cor da mesma direção. Cada uma em HTML autocontido, em
   `docs/design/mockups/<tela>-a.html` e `docs/design/mockups/<tela>-b.html`, servidas por HTTP
   local como diz a VER-19 de `referencias/verificacao.md`; mostre ao usuário os prints do
   Playwright em 375 e 1440 de largura, em `docs/design/mockups/<tela>-a-375.png`,
   `<tela>-a-1440.png`, `<tela>-b-375.png` e `<tela>-b-1440.png`,
   os quatro gravados antes da pergunta. O usuário escolhe com `AskUserQuestion`, uma pergunta, a
   direção recomendada em primeiro e marcada "(Recomendado)". Só depois da escolha grave o
   `sistema.md` na direção escolhida e siga para o passo 4. Nenhum código da tela final antes da
   escolha.
   - Tela que já existe: um mockup só, no estilo atual, mostrado com os prints para aprovação ou
     ajuste antes do passo 4.
5. **Grave o sistema** em `docs/design/sistema.md`, formato único do projeto: tipo de tela,
   direção, os três botões (VARIACAO, MOVIMENTO, DENSIDADE), tokens de cor, tipografia,
   espaçamento, raio e movimento, menu e rodapé do app. Commitado com o código; nada de metadado
   de design no código. Projeto que já tem o arquivo: atualize, não duplique.
6. **Exporte** os tokens para as variáveis CSS do shadcn (`--background`, `--foreground`,
   `--primary`, `--primary-foreground`, `--muted`, `--accent`, `--destructive`, `--border`,
   `--ring`, `--radius`…), em `oklch()`, no CSS global do projeto; sem React, as mesmas variáveis
   no `<style>` do HTML.

## Passo 4 — Construção

Abra `referencias/componentes.md` e `referencias/ux.md` agora; com a página na frente, abra
`referencias/slop.md` para conferir o que construir.

1. **Blocos** do catálogo: os arquétipos escolhidos no passo 3, na direção escolhida no mockup, com a linha `shadcn:` de cada um
   dizendo o que os monta.
2. **Projeto React:** componentes do shadcn pelo CLI travado `npx shadcn@4.21.0`, na raiz do
   projeto e na ordem da COMP-06: sem `components.json`, `npx shadcn@4.21.0 init`; depois
   `npx shadcn@4.21.0 search @shadcn -q <termo>`, `view`, `docs`, `add <nome> --dry-run` e
   `add <nome>`. Nunca `@latest`, nunca o MCP do shadcn. Tokens do passo 3 entram antes do
   primeiro `add`; nenhum componente fica no estado padrão. No React, o mockup vive numa rota de
   mockup própria dentro do app (ex.: `app/mockup/<feature>/page.tsx`), servida pelo dev server.
3. **Projeto sem React:** nada de CLI; HTML autocontido com o visual do shadcn (as mesmas
   variáveis CSS, raios e estados), CSS e JS no próprio arquivo, fontes por `<link>`.
4. **Estados e formulário:** cada interativo com os oito estados, formulário com rótulo, ajuda e
   validação da `referencias/ux.md`; ícones Lucide salvo família já adotada.
5. **Na Vesta**, `docs/vesta/mockups/<data>-<feature>/index.html` é o mockup (sem React) ou uma
   página curta com os prints do passo 5 e o link para a rota (React).

## Passo 5 — Verificação

Abra `referencias/verificacao.md` agora e siga a `## Rodada` dela, na ordem, com a tela servida
numa URL: a rota de mockup no React ou, sem React, a pasta do HTML servida por HTTP local
(`python3 -m http.server <porta> --bind 127.0.0.1`); nunca `file://`, que o Playwright recusa.

A verificação só vale com os arquivos gravados na pasta da entrega: os prints,
as duas saídas do detector e o `relatorio.md`. Contraste e rolagem lateral só se afirmam medidos na rodada.

1. Cada rodada: prints 375 e 1440 no Playwright; CSS computado, console e desempenho no Chrome
   DevTools; detector na página renderizada (`ferramentas/impeccable/detectar`); itens `[olho]`
   de `referencias/slop.md`; lista de `referencias/ux.md`; rotação em Persuadir e Experiência.
2. Todo alarme do detector é corrigido ou refutado com prova (CSS lido ou print).
3. Relatório por rodada com os ids de cada linha do `## Piso`, mais os que a rodada tocou, cada um
   com passou ou falhou.
4. No máximo 3 rodadas: a primeira acha, as correções entram em lote, a seguinte confere. Sobrou
   algo, entregue com o id, o que falhou e por quê. Acessibilidade e contraste nunca sobram: sem
   corrigir, não entrega.
5. Entregue os prints da última rodada, o último relatório, as refutações com prova e, no modo
   direto, as respostas deduzidas do passo 1. Feche o Playwright com `browser_close`.
