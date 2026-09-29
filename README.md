# claude-kit

O ClaudeKit é o conjunto de ferramentas que uso no Claude Code: skills, MCPs, hooks, estilos e
programas, documentado e instalável por qualquer pessoa. Leva as ferramentas, nunca as
informações: sem memória, sem dados de cliente, sem credenciais.

O Claude Code de uma máquina, empacotado para ser reproduzido em outra. Skills, plugins,
servidores MCP, hooks, output styles, programas e repositórios de apoio: tudo o que está
aqui é o que roda na máquina de origem, na mesma configuração.

`install.sh` deixa um Mac igual à origem. `sync.sh` roda na origem e publica o estado atual.

Agente de IA instalando o kit: siga o [INSTALAR.md](INSTALAR.md) antes de qualquer comando.

## Antes de instalar

Este é o setup de uma pessoa, não um framework configurável. O instalador **espelha**: o que
não está no kit sai da sua máquina.

- Skills, agents, commands, hooks, output styles e servidores MCP que você tenha e não estejam
  aqui são apagados. Plugins e marketplaces fora da lista são desinstalados.
- Antes de mexer em qualquer coisa, ele guarda o estado anterior em
  `~/claude-espelho-<data>.tar.gz`. Dá para desfazer (veja abaixo).
- Seu `CLAUDE.md`, sua memória, seus projetos e suas credenciais não são tocados.
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
| `prompt-engineering` | Escreve e audita system prompts de agentes. |
| `supacode-cli`, `supacode-deeplinks` | Controla o Supacode pelo terminal ou por URL. |
| `vesta-interface` | Desenha e revisa telas, páginas e componentes; camada de interface da Vesta. Link para o clone em `~/Code/vesta-interface` (repositório abaixo). |

### Plugins

Ligados: `superpowers` (skills de processo: TDD, debugging, revisão), `security-guidance`,
`caveman` (subagentes com saída comprimida), `ponytail` (a solução mais simples que
funciona), `watch` (assistir vídeo), `headroom` (compressão de contexto), `automaster`
(auditoria e edição de GoHighLevel).

Instalados e desligados: `code-review`, `pyright-lsp`, `typescript-lsp`, `swift-lsp`, `stripe`,
`playwright` (substituído pelo MCP `playwright` travado, abaixo).

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
| `playwright` | Navegador sem janela, com perfil fixo em `~/.cache/claude-navegador`. Travado em `@playwright/mcp@0.0.82`, com `--snapshot-mode none`. |
| `chrome-devtools` | DevTools do Chrome sem janela (console, desempenho). Travado em `chrome-devtools-mcp@1.10.1`, com as categorias input, emulation, network e memory desligadas. |

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
`supacode`, `knobler`. Via npm: `graft` e os pacotes dos MCPs `playwright` e `chrome-devtools`. Via uv: `headroom-ai`, `scrapling`. Script oficial:
`deja` e o próprio Claude Code.

O instalador só instala o que falta, na versão mais nova. Se a versão de lá for diferente da
origem, ele avisa e não reinstala.

### Repositórios de apoio

Clonados no mesmo caminho da origem:

| Repositório | Pra quê |
|---|---|
| `zoi-tech/automaster` | Servidor do plugin `automaster`. |
| `luccas-silveira/vesta` | A skill `vesta` e seus comandos, ligados por link ao clone. A cada parada, a Vesta confere se há versão nova aqui e se atualiza. |
| `luccas-silveira/vesta-interface` | A skill `vesta-interface`, ligada por link ao clone, com o detector de interface e os catálogos. Se atualiza junto com a Vesta, a cada parada. |
| `luccas-silveira/whatsapp-mcp` | Ponte do WhatsApp usada pelo MCP `whatsapp`; o `servico.sh` compila e liga como serviço do macOS, que sobe no login e volta sozinho quando cai. |
| `luccas-silveira/ghl-docs` | Espelho da documentação do GoHighLevel. |
| `ColeMurray/claude-code-otel` | Métricas do Claude Code em Grafana; sobe com `docker compose`. |

## Instalar

Se quem instala é um agente, o roteiro dele é o [INSTALAR.md](INSTALAR.md).

```bash
git clone https://github.com/luccas-silveira/claude-kit && bash claude-kit/install.sh
```

No fim, o instalador mostra, nesta ordem: o que falhou, programas com versão diferente,
credenciais que faltam, o que ainda é manual e o caminho do snapshot.

## O que fica fora e continua manual

Fora do kit: o `CLAUDE.md` global, toda a memória e as credenciais. O instalador lista quais
credenciais faltam, só pelo caminho.

Manual depois de instalar: copiar as credenciais, fazer login no Claude Code, ler o QR do
WhatsApp (`tail -f ~/Library/Logs/whatsapp-bridge.log`), rodar `graft init` em cada repositório.

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
