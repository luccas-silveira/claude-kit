# Pesquisa — destino dos repositórios

Spec: `docs/vesta/specs/2026-09-29-destino-dos-repositorios-design.md`

Frente externa pulada: sem ferramenta externa nova e sem incerteza técnica na spec.

## Achados

### A1 — Hoje não existe nenhuma troca de caminho de repositório; só home por `__HOME__`
- Fonte: `espelho.py:80-84` (`escrever_json`), `:109-114` e `:94-98` (`espelhar`)
- Contradiz a spec: não
- `escrever_json` só recebe `home`, então o mapa origem→destino precisa entrar por parâmetro ou por `ctx`.

### A2 — O padrão de casar por caminho inteiro já existe
- Fonte: `espelho.py:96` (`real == r or real.startswith(r + os.sep)`)
- Contradiz a spec: não
- Serve de modelo para a regra de prefixo (`~/Code/vesta` não pode estragar `~/Code/vesta-interface`).

### A3 — O texto da skill `ghl-api-docs` cita `~/Documents/ghl-docs`, caminho que nem a origem usa
- Fonte: `espelho/.claude/skills/ghl-api-docs/SKILL.md:9`, `:13`
- Contradiz a spec: parcial
- O critério da spec (nenhum caminho `ZOI` sobra) passa mesmo assim. Depois da troca, o link da skill aponta para `~/Code/ghl-docs` e o texto continua dizendo outro lugar.
- Pergunta que levanta: a skill instalada manda o usuário procurar a documentação num lugar onde ela não estará. Corrigimos o texto da skill como parte deste trabalho?

### A4 — O README afirma que os repositórios são clonados no mesmo caminho da origem
- Fonte: `README.md:99-110`
- Contradiz a spec: sim
- A frase passa a ser falsa para `automaster` e `ghl-docs`.
- Pergunta que levanta: o README também entra no escopo, ou a divergência fica até alguém notar?

### A5 — O link simbólico do `ghl-api-docs` só é reescrito pelo caminho de link do `espelhar`, e usa o caminho real
- Fonte: `espelho/.claude/skills/ghl-api-docs/docs` (link para `__HOME__/Documents/2. ZOI/ghl-docs`), `espelho.py:95-97`, `:129` (`realpath`)
- Contradiz a spec: parcial
- Se uma origem for ela mesma um link, o texto dos arquivos usa o caminho lógico e o link usa o real. O mapa precisa cobrir os dois.
- Pergunta que levanta: aceitamos cobrir só o caminho lógico e o real igual a ele, ou o mapa trata origem que é link?

### A6 — Nenhum teste cobre `extraKnownMarketplaces` no `settings.json`, nem que manifesto e `settings.json` levem o mesmo destino
- Fonte: `test/test_sync.py:27-89`, `:239-249`, `test/test_espelho_real.py:62-68`, `espelho.py:346-360`
- Contradiz a spec: parcial
- Se o manifesto trocar e o `settings.json` não (ou o inverso), o plugin `automaster@zoi` aponta para pasta que o instalador não clonou, e `desligar_sem_fonte` não pega a divergência.
- Pergunta que levanta: o teste que compara os dois entra na spec como exigência?

### A7 — O instalador não muda: só clona no `caminho` do manifesto e depende do path do `settings.json`
- Fonte: `espelho.py:297-305`, `:330-343`; `known_marketplaces.json` não entra no espelho (`:16-23`)
- Contradiz a spec: não
- Confirma a abordagem escolhida. O Claude Code recria o registro dos marketplaces ao abrir.

### A8 — `espelho/mcp.json` não contém os caminhos em escopo
- Fonte: `espelho/mcp.json` (só `Code/whatsapp-mcp`, `Desktop/AgentStudio`, `Desktop/Projetos/ghraphnizer`)
- Contradiz a spec: parcial
- A spec lista `mcp.json` entre os arquivos trocados. Continua certo por robustez, mas hoje não há o que trocar lá, e o teste 1 da spec não o exercita com dado real.

## Fila do grill

1. A6 — Manifesto e `settings.json` precisam levar o mesmo destino: exigimos teste que compare os dois?
2. A4 — README entra no escopo?
3. A3 — Texto da skill `ghl-api-docs` entra no escopo?
4. A5 — Origem que é link simbólico: cobrimos?
