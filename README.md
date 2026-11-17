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
| `ghl-api-docs` | Referência offline da API do GoHighLevel v3, com correções medidas ao vivo. |
| `graft` | Usa o grafo de código do graft antes de grep e leitura de arquivo. |
| `grill-me` | Entrevista cerrada sobre um plano até cada decisão estar resolvida. |
| `hyperframes`, `hyperframes-cli`, `hyperframes-registry` | Vídeo a partir de HTML: as regras de render, a linha de comando e cerca de 450 blocos prontos. |
| `media-use` | Música, efeito sonoro, imagem, locução e transcrição para um vídeo HyperFrames. |
| `prompt-engineering` | Escreve e audita system prompts de agentes. |
| `reverse-any-video`, `style-sampling` | Reconstrói um vídeo existente como projeto editável; faz um episódio novo num estilo já provado. |
| `reverse-engineer-anything` | Engenharia reversa de binário, app Electron, firmware e alvo de navegador com o REA. |
| `supacode-cli`, `supacode-deeplinks` | Controla o Supacode pelo terminal ou por URL. |
| `terminal-browser` | Navegador de verdade dentro do terminal, lado a lado com a conversa. |
| `vesta-interface` | Desenha e revisa telas, páginas e componentes; camada de interface da Vesta. Link para o clone em `~/Code/vesta-interface` (repositório abaixo). |
| `video-use` | Edita vídeo por conversa: transcreve, corta, colore e legenda. Link para o clone em `~/Code/video-use` (repositório abaixo). |
| `what-have-I-done` + `/whid` | Lista por projeto tudo o que foi feito num dia nas sessões do Claude Code. |

### Plugins

Todos ligados: `automaster` (auditoria e edição de GoHighLevel), `calado` (troca a instrução de
narrar entre ferramentas por uma regra contra narração), `reflect-mod` (acha correções
reutilizáveis no que você digita e salva no `CLAUDE.md` com uma tecla), `terminal-browser`
(navegador dentro do Claude Code) e `watch` (assistir vídeo).

Os plugins se instalam sozinhos na primeira vez que você abre o Claude Code depois do
instalador.

### Servidores MCP

| Servidor | Pra quê |
|---|---|
| `deja` + `/deja` | Índice das sessões passadas ("já não corrigimos isso?"). |
| `graft` | Grafo de símbolos e chamadas do repositório. |
| `scrapling` | Scraping de páginas, inclusive as protegidas. |
| `whatsapp` | Ler e enviar mensagens pelo WhatsApp (ponte local do `whatsapp-mcp`). |
| `inspo` + `/inspo` | Referências de design (`inspomcp.dev`). |
| `playwright` | Navegador sem janela, com perfil fixo em `~/.cache/claude-navegador`. Travado em `@playwright/mcp@0.0.82`, com `--snapshot-mode none`. |

### Hooks

| Hook | Quando | Pra quê |
|---|---|---|
| `pre-tool-memory` | antes da primeira ferramenta | Injeta a memória do projeto no contexto. |
| `session-length` | a cada mensagem | Avisa uma vez quando a sessão passa de 50 pedidos. |
| `fechar-navegador-orfao` | fim da sessão | Fecha o navegador sem janela do Playwright que ficou aberto sozinho. |
| `knobler-ask` | pergunta ao usuário | Manda a pergunta para o app Knobler e devolve a resposta. |
| `trava_encerramento` | fim de cada resposta | Um juiz (Haiku, via `claude -p`) lê a última mensagem e não deixa o Claude parar com ponta solta que ele mesmo resolve. Barra no máximo duas vezes por pedido e, se falhar, libera. |

Mais a statusline (`statusline.sh`), o tema `destaque-branco` e o agente `web-search-agent` para
pesquisa na web.

### Programas

Via Homebrew: `node`, `python@3.13`, `uv`, `jq`, `gh`, `go`, `ffmpeg`, `yt-dlp`, `docker`,
`supacode`, `knobler`, `terminal-browser`. Via npm: `graft` e o pacote do MCP `playwright`. Via
uv: `scrapling`. Script oficial:
`deja` e o próprio Claude Code.

O instalador só instala o que falta, na versão mais nova. Se a versão de lá for diferente da
origem, ele avisa e não reinstala.

### Repositórios de apoio

Cada repositório é clonado em `~/Code/<nome>`:

| Repositório | Pra quê |
|---|---|
| `zoi-tech/automaster` | Servidor do plugin `automaster`. |
| `luccas-silveira/vesta` | A skill `vesta` e seus comandos, ligados por link ao clone. A cada parada, a Vesta confere se há versão nova aqui e se atualiza. |
| `luccas-silveira/vesta-interface` | A skill `vesta-interface`, ligada por link ao clone, com o detector de interface e os catálogos. Se atualiza junto com a Vesta, a cada parada. |
| `luccas-silveira/calado` | O plugin `calado`. |
| `luccas-silveira/reflect-mod` | O plugin `reflect-mod`. |
| `browser-use/video-use` | A skill `video-use`, ligada por link ao clone; o instalador roda `uv sync` nele. A transcrição pede uma chave da ElevenLabs em `.env`. |
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
