# Modo componente

Um elemento só, fora do fluxo de página: botão, campo, card, modal, menu, dica, seletor, aba,
chip, selo, aviso, controle deslizante, seletor de data, avatar. Destilado de
`X/hallmark/SKILL.md:60-141`.

## Quando entra

Dois destes sinais disparam o modo; só sinais de página (várias seções, "faz a landing") ficam no
fluxo do [`SKILL.md`](../SKILL.md):

- o pedido nomeia um elemento só;
- o pedido é curto (até 30 palavras) e fala de um elemento;
- o alvo é um arquivo de componente (`Button.tsx`, `components/Input.css`);
- o usuário diz "só o X", "apenas este".

Ambíguo ("desenha a seção de preços": um card ou a página?), pergunte uma vez; sem resposta,
componente.

## Passos que roda

- **Passo 1:** varredura do projeto igual (tokens, fontes, framework, ícones). O componente herda
  o `docs/design/sistema.md` e o tipo de tela da tela onde vai morar; sem sistema, pergunte se há
  um a seguir ou se é para escolher. Sem questionário de página, sem busca de estilo.
- **Passo 3:** só os tokens que o componente usa, pelo sistema. Sem macroestrutura, menu, rodapé
  nem rotação: componente não gira e não entra em `docs/design/rotacao.json`.
- **Passo 4:** em React, o shadcn pelo CLI travado (COMP-06 em
  [`componentes.md`](../referencias/componentes.md)); sem React, HTML e CSS autocontidos com o
  visual do shadcn. O componente usa tokens por nome (`var(--primary)`), nunca valor cru.
- **Passo 5:** a rodada de [`verificacao.md`](../referencias/verificacao.md) sobre a prévia, só com
  as regras que valem para um elemento (cor, contraste, tipo, estados, acessibilidade, movimento);
  as de estrutura de página ficam de fora.

## O que entrega

Dois arquivos lado a lado:

1. O componente, no formato do projeto (`Button.tsx`, `Button.vue`, `button.css` + `button.html`).
2. A prévia de estados, `<Nome>.preview.html` (ou `.preview.tsx` na rota de mockup do app): uma
   página que mostra o componente nos oito estados de UX-01 ao mesmo tempo, empilhados e com
   rótulo: padrão, hover, foco, pressionado, desabilitado, carregando, erro, sucesso. Cada linha
   força o estado por classe, que o CSS atende junto da pseudo-classe real:

   ```css
   .btn:hover, .btn.is-hover { background: var(--accent); }
   .btn:focus-visible, .btn.is-focus { outline: 2px solid var(--ring); }
   .btn:active, .btn.is-active { transform: translateY(1px); }
   ```

   O usuário abre a prévia, vê o componente funcionando e apaga; ela não é código de produção. É
   nela que o passo 5 tira os prints e confere os estados.

Todo estado da lista tem estilo de verdade no arquivo; estado que não se aplica (um selo não
carrega) fica anotado na prévia com o motivo.
