# UX

Estados, formulários, acessibilidade, ação destrutiva e a crítica heurística. O que muda com o
tipo de tela está em `## Por tipo de tela`; as contradições resolvidas, em
[`fontes.md`](fontes.md). Entre parênteses, as fontes que trazem a regra; três ou mais fontes
marcam regra de piso. O CSS de cada estado (hover, `:focus-visible`, `:active`, `:disabled`,
campo sem salto) já está em SLOP-30; aqui fica o comportamento.

## Estados

- **UX-01** Todo elemento interativo tem os oito estados: padrão, hover (só em
  `@media (hover: hover)`), foco, pressionado, desabilitado, carregando, erro e sucesso; toda
  área que mostra dado tem também vazio. Faltou um, o elemento não está pronto.
  (hallmark, taste, impeccable, uupm)
- **UX-02** Foco visível em todo elemento interativo, por `:focus-visible`, na hora (COR-13,
  SLOP-27); nunca `outline: none` sem substituto; barra fixa, banner e toast nunca cobrem o
  controle focado (`scroll-padding` do tamanho da barra). (hallmark, impeccable, uupm)
- **UX-03** Pressionado: `:active` com `scale(0.98)` ou `translateY(1px)` em `--dur-micro`,
  volta ao soltar; nunca cresce ao pressionar. (hallmark, taste; uupm diverge, ver fontes.md)
- **UX-04** Desabilitado diz por quê (dica ou texto perto). O botão de envio só fica desabilitado
  com o formulário sabidamente inválido ou enviando, nunca parado à espera. (hallmark, uupm)
- **UX-05** Carregando: esqueleto com a forma final onde a forma é previsível (lista, card,
  tabela); spinner só dentro do botão ou do campo, no lugar do ícone, com o rótulo virando a ação
  em curso ("Salvando…") e a largura do botão fixa. O texto diz o que carrega; operação quase
  instantânea não pisca indicador; progresso determinado quando existe, nunca inventado.
  (hallmark, taste, impeccable, uupm)
- **UX-06** Enviando, o botão ignora o segundo clique e o campo continua editável.
  (hallmark, impeccable, uupm)
- **UX-07** Vazio explica o que vai aparecer ali e oferece uma ação para preencher; separa
  primeiro uso, busca ou filtro sem resultado (com "limpar filtros"), sem permissão e falha de
  carga. Nunca "Nenhum resultado" solto. (hallmark, taste, impeccable, uupm)
- **UX-08** Erro diz o que falhou, por quê (quando se sabe) e como sair, em linguagem simples,
  sem código como mensagem principal, perto da origem e com ação (tentar de novo, editar). O erro
  de um bloco não derruba a tela, e o que o usuário digitou fica. (hallmark, impeccable, uupm)
- **UX-09** Sucesso visível na tela dispensa aviso (SLOP-28); efeito invisível ganha sinal curto
  no próprio controle ("Copiado" com ✓ por 2.5s) ou toast. Nunca comemoração.
  (hallmark, impeccable; uupm diverge, ver fontes.md)
- **UX-10** Toast empilha num canto sem mover o conteúdo; informativo some em 5s, com desfazer
  fica 8s, e nenhum some com ponteiro ou foco nele; erro com ação fica até ser dispensado. Toast
  nunca rouba o foco e é anunciado por `aria-live="polite"`. (hallmark, uupm)

## Ação destrutiva

- **UX-11** Ação destrutiva reversível (arquivar, remover da lista, mover para a lixeira) executa
  na hora e oferece desfazer num toast (UX-10), sem confirmação. (hallmark, impeccable, uupm)
- **UX-12** Ação irreversível (apagar para sempre, pagamento, excluir conta) pede confirmação
  num `<dialog>` que nomeia ação e objeto no título e no botão ("Excluir 3 faturas"), nunca "OK"
  ou "Sim"; excluir conta ou base inteira exige digitar o nome. (hallmark, impeccable, uupm)
- **UX-13** Botão destrutivo na cor de erro, afastado da ação primária e fora da navegação comum.
  (uupm, impeccable)

## Formulários

- **UX-14** Rótulo visível acima do campo, ligado por `for` e `id`; placeholder mostra formato
  (`01 jan 2026`), nunca faz de rótulo. (hallmark, taste, impeccable, uupm)
- **UX-15** Ajuda embaixo do campo, com altura reservada (`min-height: 1lh`); o erro substitui a
  ajuda no mesmo lugar, ligado por `aria-describedby`, com `aria-invalid="true"` no campo.
  (hallmark, taste, uupm)
- **UX-16** Validar ao sair do campo, não a cada tecla; depois do primeiro blur, revalida a cada
  mudança. Envio falhou: foco no resumo de erros no topo (cada item leva ao campo) ou, sem
  resumo, no primeiro campo inválido. (hallmark, impeccable, uupm)
- **UX-17** Obrigatório marcado com texto ou asterisco e `aria-required`, nunca só com cor;
  formato e requisito ditos antes do envio. (hallmark, impeccable, uupm)
- **UX-18** Tipo certo de campo (`type="email"`, `tel`, `inputmode="numeric"`) e `autocomplete`
  em nome, email, endereço e senha; colar e gerenciador de senha nunca bloqueados; senha com
  mostrar e ocultar. (impeccable, uupm)
- **UX-19** Formulário longo salva rascunho; fechar diálogo com alteração não salva pede
  confirmação. (impeccable, uupm)

## Acessibilidade

- **UX-20** Tudo que funciona com mouse funciona com teclado: ordem do Tab igual à ordem visual,
  Enter e Espaço ativam, Esc fecha, nenhuma armadilha de foco; arrastar tem alternativa por
  teclado e clique. (hallmark, impeccable, uupm)
- **UX-21** Semântica nativa: `<button>` para ação, `<a>` para ir a outro lugar, landmarks
  (`header`, `nav`, `main`, `footer`) e um `h1` (níveis em TIP-20); nunca `div` clicável.
  (hallmark, impeccable, uupm)
- **UX-22** Leitor de tela: todo controle tem nome acessível que bate com o rótulo visível (botão
  só com ícone leva `aria-label`, COMP-05); imagem com informação tem `alt` que a diz, decorativa
  `alt=""`; mudança assíncrona anunciada por `aria-live="polite"` (`assertive` só em risco),
  erro de formulário por `role="alert"`. (hallmark, impeccable, uupm)
- **UX-23** Modal em `<dialog>` com `showModal()` (COMP-12): foco no primeiro elemento
  interativo, fundo `inert`, fecha com Esc, clique no fundo e botão visível, e o foco volta ao
  gatilho ao fechar. (hallmark, impeccable, uupm)
- **UX-24** Link "Pular para o conteúdo" como primeiro foco quando há navegação antes do `main`;
  em troca de rota, o foco vai ao `main`. (impeccable, uupm)
- **UX-25** Zoom nunca bloqueado (`maximum-scale` e `user-scalable` fora do `viewport`); a tela
  funciona em 200% de zoom sem cortar rótulo. (impeccable, uupm)

## Clareza e navegação

- **UX-26** Uma ação primária por tela; nenhum par de CTAs com a mesma intenção ("Fale conosco" e
  "Entre em contato"); o secundário fica visualmente abaixo. (hallmark, taste, uupm)
- **UX-27** Rótulo diz o que acontece, com verbo e objeto ("Salvar rascunho"), e a mesma palavra
  para a mesma coisa na interface inteira. (impeccable, uupm)
- **UX-28** Lugar atual marcado na navegação (`aria-current="page"`); voltar restaura rolagem,
  filtro e campo preenchido. (impeccable, uupm)
- **UX-29** Fluxo de várias etapas mostra a etapa atual e o total e deixa voltar sem perder o
  preenchido. (impeccable, uupm)

## Crítica heurística

Roda no passo 5 ao revisar tela existente e no modo de crítica: cada heurística recebe nota de 0
a 4, com o problema que tirou ponto e sua prioridade (P0 impede a tarefa, P1 dificulta muito, P2
incomoda, P3 acabamento). Em Persuadir e Experiência, as heurísticas 7 e 10 podem ficar `n/a`
com motivo de uma linha, e o total se mede sobre as que valeram
(`X/impeccable/.claude/skills/impeccable/reference/critique.md:120`).

- **UX-30** heurística 1, visibilidade do estado do sistema. Olhar: toda ação responde em até
  100ms; carregando, salvo e erro aparecem (UX-05, UX-08); a navegação marca onde se está.
- **UX-31** heurística 2, correspondência com o mundo real. Olhar: termos do público, sem jargão
  interno nem código; a informação vem na ordem da tarefa; ícones reconhecíveis.
- **UX-32** heurística 3, controle e liberdade do usuário. Olhar: desfazer (UX-11), cancelar em
  formulário e modal, Esc fecha, limpar filtro e busca, sair de fluxo longo sem perder o feito.
- **UX-33** heurística 4, consistência e padrões. Olhar: a mesma palavra, a mesma cor e o mesmo
  componente para a mesma coisa; convenções da web (link distinto, marca leva ao início).
- **UX-34** heurística 5, prevenção de erros. Olhar: confirmação só no irreversível (UX-12);
  restrição que impede entrada inválida (seletor de data, máscara); padrão sensato; rascunho salvo.
- **UX-35** heurística 6, reconhecer em vez de lembrar. Olhar: opções à vista, não enterradas em
  menu; ícone com rótulo; recentes e sugestões; nada exige lembrar um valor de outra tela.
- **UX-36** heurística 7, flexibilidade e eficiência de uso. Olhar: atalho de teclado nas ações
  frequentes, ação em lote, paleta ⌘K em Operar, sem complicar o caminho do novato.
- **UX-37** heurística 8, estética e design minimalista. Olhar: só o necessário em cada passo; a
  hierarquia leva o olho à ação primária (UX-26); nenhum enfeite disputa com o conteúdo.
- **UX-38** heurística 9, ajudar a reconhecer, diagnosticar e recuperar erros. Olhar: mensagem
  simples com o problema exato e a saída, perto da origem, preservando o digitado (UX-08).
- **UX-39** heurística 10, ajuda e documentação. Olhar: dica contextual no campo difícil, ajuda
  achável sem sair da tarefa, estado vazio que ensina o próximo passo (UX-07).

## Por tipo de tela

### Persuadir

- Uma ação primária na dobra, repetida no fim com o mesmo rótulo (vale UX-26); formulário só com
  os campos que a conversão precisa (vale UX-14, UX-18).
- Na crítica, heurísticas 7 e 10 podem ficar `n/a` com motivo (vale UX-36, UX-39).

### Operar

- Estados com dado pesam mais que tudo: vazio por tipo, esqueleto na carga, erro por bloco (vale
  UX-05, UX-07, UX-08); desfazer em toda ação reversível de lista (vale UX-11).
- Atalhos, ação em lote e ⌘K (vale UX-36); navegação igual em toda tela (vale UX-28).

### Ler

- Teclado e leitor de tela primeiro: pular para o conteúdo, landmarks, níveis de título (vale
  UX-21, UX-24); posição atual no índice (vale UX-28).

### Experiência

- A peça autoral nunca tira teclado, foco nem leitor de tela (vale UX-20, UX-22); arte decorativa
  com `aria-hidden` (SLOP-36).
- Na crítica, heurísticas 7 e 10 podem ficar `n/a` com motivo (vale UX-36, UX-39).
