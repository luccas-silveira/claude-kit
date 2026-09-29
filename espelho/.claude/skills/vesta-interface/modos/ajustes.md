# Modos de ajuste

Oito ajustes sobre uma tela que já existe. Cada um roda os passos 3 e 5 do
[`SKILL.md`](../SKILL.md): no passo 3, o ajuste mexe no sistema visual dentro do escopo pedido; no
passo 5, a rodada de `referencias/verificacao.md` confere o resultado. Passos 1, 2 e 4 não rodam:
o tipo de tela, a direção e os três botões vêm do `docs/design/sistema.md` do projeto (sem ele,
rode o passo 1 só para classificar a tela e gravar o sistema). Destilado dos arquivos de mesmo
nome em `X/impeccable/.claude/skills/impeccable/reference/`.

Vale para os oito: o escopo que o usuário nomeou é o limite. O resto da tela fica como está;
nenhuma cor, face, raio ou sombra nova entra sem pedido. Se o sistema não dá conta do ajuste,
pare e pergunte, dizendo o que entraria e para quê. O piso do `SKILL.md` vale sempre.

## bolder

Mais convicção num trecho que ficou apagado. Roda os passos 3 e 5.

- Descubra o que os vizinhos fazem e o trecho não: display com força total, o motivo gráfico da
  marca, a mudança de ritmo. Traga o trecho ao nível que o resto já tem, com o vocabulário do
  próprio sistema, nunca com efeito novo.
- Um gesto decidido, feito por inteiro, e o entorno mais quieto para ele aparecer. Tudo mais alto
  deixa tudo mais plano.
- Teste do esqueleto: sem o texto, a hierarquia ainda diz o que o trecho é? Se só funciona com as
  palavras, o ousado ficou no tamanho da letra.
- Conteúdo continua verdadeiro: número ou prova que falta se pede ao usuário (SLOP-46).

## quieter

Menos intensidade sem virar genérico. Roda os passos 3 e 5.

- Ache as fontes do barulho: saturação, pesos extremos, muitos acentos, efeitos, animação.
- Cor: croma menor, menos cores, neutro puxado para o matiz (`referencias/cor.md`); nada de texto
  cinza sobre fundo colorido (COR-15).
- Peso: títulos um degrau mais leves, hierarquia por tamanho e espaço antes de cor; fios mais
  finos ou fora.
- Movimento: distâncias menores, só o funcional, nunca curva elástica (`referencias/movimento.md`).
  Considere descer MOVIMENTO e VARIACAO no `sistema.md`.
- Quieto sem intenção cai no genérico: mantenha o traço que dá personalidade.

## distill

Tirar o que fica entre o usuário e o objetivo. Roda os passos 3 e 5.

- Diga a única coisa que a tela precisa fazer e o que é essencial para isso.
- Arquitetura: uma ação primária (UX-26), menos ações secundárias, divulgação progressiva no
  resto, nada dito duas vezes.
- Visual: 1–2 cores mais neutros, menos tamanhos e pesos, sem card em card (SLOP-11), card só
  quando a elevação comunica (LAY-06), uma escala de espaço.
- Interação: menos escolhas, padrão sensato, edição no lugar em vez de modal, um passo a menos.
- Texto: metade do tamanho, voz ativa, sem jargão (SLOP-49).

## harden

Aguentar dado real, erro, idioma e rede ruim. Roda os passos 3 e 5.

- Entrada extrema: texto muito longo, vazio, um caractere, emoji, número enorme, lista com
  milhares de itens. Quebra e reticências planejadas, nada de rolagem horizontal (LAY-22).
- Idioma: texto 30–40% mais longo, propriedades lógicas (LAY-30), direita para esquerda, data,
  número e moeda pelo `Intl`.
- Erro: cada chamada tem estado de erro com causa e saída (UX-08), repetir, rede caída, sessão
  expirada, permissão negada; nada se perde do que o usuário digitou.
- Limites: estados vazio, carregando, parcial e sem permissão (`referencias/ux.md`, `## Estados`);
  clique duplo em envio (UX-06).
- No passo 5, provoque esses casos no Playwright e fotografe cada um.

## onboard

Levar o usuário ao primeiro valor o quanto antes. Roda os passos 3 e 5.

- Defina o momento em que o produto prova que vale (o "aha") e o nível de quem chega.
- Mostre em vez de explicar; tutorial pulável; contexto na hora em vez de tour na entrada.
- Estado vazio que ensina: o que vai aparecer ali, por que importa, a ação que preenche (UX-07).
- Dica de recurso novo aparece uma vez, perto de onde se usa, e some quando dispensada.
- No passo 5, percorra o primeiro uso no Playwright do zero até o "aha".

## optimize

Desempenho: achar o gargalo desta tela, corrigir e medir. Roda os passos 3 e 5.

- Meça antes (VER-09 em `referencias/verificacao.md`): LCP < 2.5s, INP < 200ms, CLS < 0.1. Não
  otimize o que não está lento.
- Carga: imagem com tamanho declarado e `srcset` (LAY-28), fonte com `font-display: swap` e poucos
  pesos (TIP-22), código dividido por rota, nada de biblioteca pesada para pouco uso.
- Render: animação só em `transform` e `opacity` (MOV-05), `will-change` pontual (MOV-06), lista
  longa virtualizada.
- Meça depois com o mesmo trace e ponha os dois números na entrega.

## polish

Acabamento, nunca redesenho escondido. Roda os passos 3 e 5.

- Leia o `sistema.md`, os tokens e os componentes vizinhos. Classifique cada desvio: token que
  falta, peça avulsa que devia ser o componente comum, fluxo que difere das telas irmãs, defeito
  local.
- Ordem de correção: tarefa quebrada ou inacessível; estado que falta (carregando, vazio, erro,
  sucesso, desabilitado); fluxo, hierarquia e responsivo; detalhe visual e de movimento; limpeza
  de código.
- Se o conceito está errado, diga e recomende redesenho ou bolder em vez de trocar por baixo.
- Alarme do detector é indício, não atestado: o passo 5 olha a tela renderizada.

## delight

Um momento de prazer onde ele ajuda, sem atrapalhar. Roda os passos 3 e 5.

- Persuadir e Experiência: personalidade pode correr pela voz, composição, movimento e
  descoberta. Operar e Ler: só em momentos que importam (primeiro uso, tarefa concluída,
  recuperação de erro); no resto, confiabilidade.
- Uma tese só: qual momento, que sensação, por quê.
- Sucesso proporcional ao esforço (SLOP-28); espera com progresso verdadeiro, nunca trabalho
  fingido; erro com problema e saída antes de graça, nunca piada com dinheiro, dado ou perda.
- Repetido cem vezes ainda agrada; movimento reduzido tem caminho (MOV-23).
