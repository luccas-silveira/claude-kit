# claude-kit

O Claude Code de uma máquina, empacotado para ser reproduzido em outra. Skills, plugins,
servidores MCP, hooks, output styles, programas e repositórios de apoio: tudo o que está
aqui é o que roda na máquina de origem, na mesma configuração.

`install.sh` deixa um Mac igual à origem. `sync.sh` roda na origem e publica o estado atual.

## Antes de instalar

Este é o setup de uma pessoa, não um framework configurável. O instalador **espelha**: o que
não está no kit sai da sua máquina.

- Skills, agents, commands, hooks, output styles e servidores MCP que você tenha e não estejam
  aqui são apagados. Plugins e marketplaces fora da lista são desinstalados.
- Antes de mexer em qualquer coisa, ele guarda o estado anterior em
  `~/claude-espelho-<data>.tar.gz`. Dá para desfazer (veja abaixo).
- Seu `CLAUDE.md`, sua memória, seus projetos e suas credenciais não são tocados.
- Dois repositórios de apoio são privados (`whatsapp-mcp`, `ghl-docs`). Sem
  acesso, o clone falha, entra na lista de falhas e o resto da instalação segue.
- Feito para macOS com Homebrew. Precisa do Claude Code já instalado.

Se você quer só uma peça, pegue a pasta dela em `espelho/.claude/` e copie à mão.

## O que vem incluso

### Fluxo de trabalho e fala

| Item | Pra quê |
|---|---|
| `vesta` (skill) + `/vesta-painel`, `/vesta-pausar`, `/vesta-retomar` | Fluxo para qualquer feature: spec, pesquisa, grill, plano e execução travada por prova de teste. Um hook não deixa o Claude parar com etapa sem prova. O painel mostra no navegador a etapa em que o projeto está. |
| `seco` (output style, padrão) | Diz só o que deve ser dito, com a complexidade mínima que a ideia exige. |
| `concise` (output style) | Respostas curtas, sem preâmbulo. |
| `linguagem-simples` (output style) | Português claro e direto, baseado na NBR ISO 24495-1. |

### Skills

| Skill | Pra quê |
|---|---|
| `archify` | Diagramas de arquitetura, fluxo e sequência em HTML com SVG. |
| `deja-history` + `/deja` | Busca em sessões passadas de agentes de código ("já não corrigimos isso?"). |
| `ghl-api-docs` | Referência offline da API do GoHighLevel v3, com correções medidas ao vivo. |
| `graft` | Usa o grafo de código do graft antes de grep e leitura de arquivo. |
| `grill-me` | Entrevista cerrada sobre um plano até cada decisão estar resolvida. |
| `hallmark` | Design de páginas sem cara de gerado por IA: criação, auditoria, redesign. |
| `prompt-engineering` | Escreve e audita system prompts de agentes. |
| `supacode-cli`, `supacode-deeplinks` | Controla o Supacode pelo terminal ou por URL. |

### Plugins

Ligados: `superpowers` (skills de processo: TDD, debugging, revisão), `playwright` (navegador
automatizado), `security-guidance`, `caveman` (subagentes com saída comprimida), `ponytail`
(a solução mais simples que funciona), `watch` (assistir vídeo), `headroom` (compressão de
contexto), `automaster` (auditoria e edição de GoHighLevel).

Instalados e desligados: `code-review`, `pyright-lsp`, `typescript-lsp`, `swift-lsp`, `stripe`.

Os plugins se instalam sozinhos na primeira vez que você abre o Claude Code depois do
instalador.

### Servidores MCP

| Servidor | Pra quê |
|---|---|
| `deja` | Índice das sessões passadas. |
| `graft` | Grafo de símbolos e chamadas do repositório. |
| `scrapling` | Scraping de páginas, inclusive as protegidas. |
| `whatsapp` | Ler e enviar mensagens pelo WhatsApp (ponte local do `whatsapp-mcp`). |
| `inspo` | Referências de design (`inspomcp.dev`). |
| `playwright` | Navegador sem janela, com perfil fixo em `~/.cache/claude-navegador`. |

### Hooks

| Hook | Quando | Pra quê |
|---|---|---|
| `pre-tool-memory` | antes da primeira ferramenta | Injeta a memória do projeto no contexto. |
| `session-length` | a cada mensagem | Avisa uma vez quando a sessão passa de 50 pedidos. |
| `fechar-navegador-orfao` | fim da sessão | Fecha o navegador sem janela do Playwright que ficou aberto sozinho. |
| `knobler-ask` | pergunta ao usuário | Manda a pergunta para o app Knobler e devolve a resposta. |

Mais a statusline (`statusline.sh`) e o agente `web-search-agent` para pesquisa na web.

### Programas

Via Homebrew: `node`, `python@3.13`, `uv`, `jq`, `gh`, `go`, `ffmpeg`, `yt-dlp`, `docker`,
`supacode`, `knobler`. Via npm: `graft`. Via uv: `headroom-ai`, `scrapling`. Script oficial:
`deja` e o próprio Claude Code.

O instalador só instala o que falta, na versão mais nova. Se a versão de lá for diferente da
origem, ele avisa e não reinstala.

### Repositórios de apoio

Clonados no mesmo caminho da origem:

| Repositório | Pra quê |
|---|---|
| `zoi-tech/automaster_v2` (privado) | Servidor do plugin `automaster`. |
| `luccas-silveira/whatsapp-mcp` (privado) | Ponte do WhatsApp usada pelo MCP `whatsapp`; compila com `go build`. |
| `luccas-silveira/ghl-docs` (privado) | Espelho da documentação do GoHighLevel. |
| `ColeMurray/claude-code-otel` | Métricas do Claude Code em Grafana; sobe com `docker compose`. |

## Instalar

```bash
git clone https://github.com/luccas-silveira/claude-kit && bash claude-kit/install.sh
```

No fim, o instalador mostra, nesta ordem: o que falhou, programas com versão diferente,
credenciais que faltam, o que ainda é manual e o caminho do snapshot.

## O que fica fora e continua manual

Fora do kit: o `CLAUDE.md` global, toda a memória e as credenciais. O instalador lista quais
credenciais faltam, só pelo caminho.

Manual depois de instalar: copiar as credenciais, fazer login no Claude Code, ler o QR do
WhatsApp e iniciar a ponte, rodar `graft init` em cada repositório.

## Desfazer

```bash
tar -xzf ~/claude-espelho-<data>.tar.gz -C ~
```

## Publicar (só na máquina de origem)

```bash
bash sync.sh
```

Copia o estado de `~/.claude` para `espelho/`, gera `manifesto.json`, mostra o que mudou e
só publica com `s`. Recusa se achar segredo ou qualquer termo de
`~/.config/claude-kit/bloqueio.txt`, a lista de nomes que não podem sair da máquina.

## Testes

```bash
python3 -m unittest discover -s test -v
```
