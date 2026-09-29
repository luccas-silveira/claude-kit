# Componentes

De onde vem cada peça da tela: blocos de página do catálogo, ícones e, em projeto React,
componentes do shadcn pelo CLI travado. O que muda com o tipo de tela está em
`## Por tipo de tela`; as contradições resolvidas, em [`fontes.md`](fontes.md). Entre parênteses,
as fontes que trazem a regra; três ou mais fontes marcam regra de piso.

## Catálogo

- **COMP-01** Blocos de página vêm de `catalogo/components/`: 50 arquétipos de navegação, hero,
  cabeçalho de seção, recurso, CTA, prova e rodapé. O índice, com "use quando" e "não confunda
  com", está em `catalogo/component-cookbook.md`; abra só os arquivos escolhidos, 5–7 por tela.
  (hallmark)
- **COMP-02** Em Persuadir e Experiência, duas seções da mesma página nunca usam o mesmo
  arquétipo, e cada arquétipo tem 2–3 variações (proporção, alinhamento, divisor) que a tela
  seguinte do projeto não repete (R7 da spec). (hallmark, taste)
- **COMP-03** A linha `shadcn:` logo abaixo do título de um bloco do catálogo diz quais
  componentes do shadcn o montam; eles entram pelo fluxo de COMP-06. (catálogo)

## Ícones

- **COMP-04** Lucide é o ícone padrão em todo tipo de tela (decisão 1 da spec; o `init` do shadcn
  já o escolhe). Projeto com outra família mantém a dela; Phosphor, Tabler ou outra entram com
  pedido do usuário. (hallmark, uupm; taste diverge, ver fontes.md)
- **COMP-05** Uma família por projeto, traço uniforme (`strokeWidth` global, 1.5 ou 2); ícone
  nunca desenhado à mão: glifo que falta vira equivalente da mesma família ou texto. Ícone que é
  controle tem nome acessível; decorativo ao lado de texto leva `aria-hidden` (SLOP-36, SLOP-37).
  (hallmark, taste, impeccable, uupm)

## shadcn em projeto React

- **COMP-06** Em projeto React, o componente vem do shadcn pelo CLI travado na versão 4.21.0
  (R3 da spec), nesta ordem, na raiz do projeto:
  1. Sem `components.json` na raiz, rode `npx shadcn@4.21.0 init` antes de qualquer outro comando.
  2. Buscar: `npx shadcn@4.21.0 search @shadcn -q <termo>`.
  3. Ver o código e as dependências: `npx shadcn@4.21.0 view @shadcn/<nome>`.
  4. Ler API e exemplos: `npx shadcn@4.21.0 docs <nome>`.
  5. Prévia dos arquivos que mudam: `npx shadcn@4.21.0 add <nome> --dry-run`.
  6. Instalar: `npx shadcn@4.21.0 add <nome>`.
- **COMP-07** Nunca `@latest` e nunca o MCP do shadcn: a versão fica travada, e o MCP só devolve o
  comando de instalação, que na 4.21.0 sai quebrado (R3 da spec). (spec)
- **COMP-08** O componente nunca fica no estado padrão do shadcn: raio, cor, sombra, tipografia e
  espaço vêm dos tokens do `docs/design/sistema.md`, exportados como as variáveis CSS do shadcn
  (`--radius`, `--primary`, `--background`…), antes do primeiro `add`. (taste)
- **COMP-09** Um sistema por projeto: shadcn não se mistura com Material, Fluent ou Carbon; projeto
  que já está num design system oficial segue o dele. (taste)
- **COMP-10** Projeto sem React não usa o CLI: HTML autocontido com o visual do shadcn (os mesmos
  tokens como variáveis CSS, os mesmos raios e estados). (spec)

## Comportamento

- **COMP-11** Botão, link de navegação e aba numa linha de 320 a 1920px (`white-space: nowrap`);
  rótulo de CTA com até 3 palavras; não coube, encurte o rótulo antes de mexer no layout
  (SLOP-33). (hallmark, taste)
- **COMP-12** Elemento nativo primeiro: `<dialog>` para modal, Popover API para menu e dica,
  `<details>` para acordeão simples; controle do sistema só é trocado quando a marca exige.
  (hallmark, uupm)
- **COMP-13** Vidro só com função (SLOP-44): borda interna de 1px, brilho interno sutil e fundo
  sólido de reserva em `prefers-reduced-transparency`. (taste)

## Por tipo de tela

### Persuadir

- Blocos do catálogo girados entre seções e entre telas (vale COMP-02); em React, formulário e
  botão do shadcn com os tokens da direção (vale COMP-08).

### Operar

- shadcn é a base: tabela, formulário, diálogo, menu, comando (vale COMP-06); sem rotação de
  blocos, os mesmos componentes em toda tela.
- Ícone com rótulo na navegação do app; Lucide salvo família já adotada (vale COMP-04).

### Ler

- Poucos componentes: busca com ⌘K (N13), cabeçalho de seção fixo (S3), índice lateral; o texto
  manda (vale COMP-01).

### Experiência

- Componente pode ser desenhado para a peça, mas ícone segue COMP-04 e COMP-05, e o que vem do
  shadcn nunca fica no estado padrão (vale COMP-08).
