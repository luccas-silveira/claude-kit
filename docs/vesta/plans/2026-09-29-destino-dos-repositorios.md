# Plano — destino dos repositórios

Objetivo: o `sync` publica o kit com cada repositório de apoio no destino `~/Code/<nome>`, em todos os arquivos que escreve, sem tocar na máquina de origem nem no instalador.

Spec: `docs/vesta/specs/2026-09-29-destino-dos-repositorios-design.md`

Comando de teste (da raiz do kit): `python3 -m unittest discover -s test -v`

Pastas de tela: nenhuma.

Mockup: nenhum: sem tela.

## Convenções que valem para todas as etapas

- Código em `espelho.py`, testes em `test/test_sync.py` (classe `KitCaso`, com HOME falso: helpers `fontes({...})`, `repo(rel, remote)`, `escreve`, `sync()`, `manifesto()`, `no_kit`, `le`) e `test/test_espelho_real.py` (lê o kit real). Modelo: `unittest`, como os testes que já existem.
- O mapa é uma lista de pares `(origem, destino)` com caminhos absolutos sob o home real, do mais longo para o mais curto. A troca casa caminho inteiro: depois da origem não pode vir letra, número, `_`, `.` ou `-` (assim `~/Code/vesta` não altera `~/Code/vesta-interface`). Padrão de casamento por caminho inteiro já existente: `espelho.py:96`.
- A troca roda ANTES da troca de home por `__HOME__`, sempre sobre texto que ainda tem o home real.
- Sem `destino` no `fontes.json`, ou `destino` igual a `caminho`: nenhum par no mapa, saída idêntica à de hoje (`test_sync_duas_vezes_nao_muda_kit`, `test/test_sync.py:268`, guarda isso).
- `git -C <origem>` (para descobrir o remote) continua usando o caminho de origem.

## Etapa 1 — Mapa de destino nos arquivos e links do espelho

- Tela: não.
- Arquivos: `espelho.py`, `test/test_sync.py`.
- O que prova a etapa:
  1. Repositório com `destino` (`~/Code/origem-r` → `~/Code/destino-r`) e um arquivo gerenciado (`.claude/settings.json`) que cita `<home>/Code/origem-r`: no espelho, o arquivo cita `__HOME__/Code/destino-r` e não sobra `origem-r`.
  2. Mesmo arquivo com a barra escapada do JSON (`<home>\/Code\/origem-r`): sai `__HOME__\/Code\/destino-r`.
  3. Link simbólico em `.claude/skills/s` apontando para `<home>/Code/origem-r/skills/s`: no espelho o link aponta para `__HOME__/Code/destino-r/skills/s` e continua sendo link.
  4. Prefixo: dois repositórios, `~/Code/vesta` (com `destino` `~/Code/vesta-novo`) e `~/Code/vesta-interface` (sem destino). Um arquivo que cita os dois: `vesta` vira `vesta-novo`, `vesta-interface` fica intacto.
  5. Sem `destino`: o teste existente de link para repositório (`test_link_para_repositorio_fica_link_com_marcador`) continua passando sem mudança.
- Como fazer: em `sync` (`espelho.py:121-129`), ao montar `repos`, expanda também `destino` com o mesmo `expandir` do `caminho` (`:125`), com padrão igual ao `caminho`; construa `ctx['mapa']` com os pares `(r['caminho'], r['destino'])` onde diferem, do mais longo para o mais curto. Crie a função `trocar(texto, mapa)` que aplica cada par com `re.sub(re.escape(origem) + r'(?![\w.-])', destino, texto)` (a função de troca recebe o destino como texto literal, escapando barra invertida). Em `espelhar`: no ramo de texto (`:109-114`) chame `trocar` no texto, e também sobre a variante com barra escapada de cada par (`origem.replace('/', '\\/')` → `destino.replace('/', '\\/')`), antes das trocas de home já existentes; no ramo de link (`:94-98`) aplique `trocar(real, ctx['mapa'])` antes de `real.replace(ctx['home'], MARCA)`. No modo instalar `ctx` não tem `mapa`: use `ctx.get('mapa', [])`.

## Etapa 2 — Mapa nos JSON escritos e manifesto com o destino

- Tela: não.
- Arquivos: `espelho.py`, `test/test_sync.py`.
- O que prova a etapa:
  1. `manifesto.json`: o repositório com `destino` sai com `caminho` `__HOME__/Code/destino-r` e o `remote` correto (lido do repositório de origem).
  2. `known_marketplaces.json` do HOME falso com um marketplace de fonte `directory` cujo `path` é `<home>/Code/origem-r`: em `manifesto.json`, `marketplaces[].fonte.path` sai `__HOME__/Code/destino-r`.
  3. `mcp.json`: um servidor MCP global cujo comando cita `<home>/Code/origem-r/bin/x`: em `espelho/mcp.json` sai `__HOME__/Code/destino-r/bin/x`.
  4. Consistência: com o mesmo marketplace em `extraKnownMarketplaces` do `.claude/settings.json` do HOME falso e em `known_marketplaces.json`, o `path` no `settings.json` do espelho é igual ao `path` do marketplace no manifesto, e igual ao `caminho` do repositório no manifesto.
  5. Sem `destino`: `manifesto.json` idêntico ao de hoje (o teste `test_manifesto_repositorios_e_credenciais`, `test/test_sync.py:239-249`, continua passando sem mudança).
- Como fazer: `escrever_json(caminho, dados, home)` (`espelho.py:80-84`) ganha o parâmetro opcional `mapa=()`; aplique `trocar(texto, mapa)` sobre o texto serializado antes de `texto.replace(home, MARCA)`. Passe `ctx['mapa']` nas duas chamadas de `montar` (`:188-192` para `mcp.json`, `:205-214` para o manifesto). Em `montar` (`:197-204`), os dicts de `repos` já trazem `destino` (etapa 1): o manifesto emite `'caminho': r['destino']`, mas o `git remote get-url` continua usando `r['caminho']`. Para o teste 2, o `known_marketplaces.json` é lido em `:208-209`; o HOME falso o cria em `.claude/plugins/known_marketplaces.json`.

## Etapa 3 — Destinos reais, textos e kit regenerado

- Tela: não.
- Arquivos: `fontes.json`, `README.md`, `~/.claude/skills/ghl-api-docs/SKILL.md` (fora do repositório do kit; o sync leva para `espelho/.claude/skills/ghl-api-docs/SKILL.md`), `test/test_espelho_real.py`, e o resultado do sync: `espelho/` e `manifesto.json`.
- O que prova a etapa:
  1. No kit real (`espelho/` e `manifesto.json`), nenhum arquivo contém `Projetos_ZOI` nem `2. ZOI`, e nenhum link simbólico do espelho aponta para caminho com `ZOI`.
  2. No manifesto real, os repositórios `automaster` e `ghl-docs` têm `caminho` `__HOME__/Code/automaster` e `__HOME__/Code/ghl-docs`, com os `remote` de hoje.
  3. Consistência real: o `path` do marketplace `zoi` em `espelho/.claude/settings.json` (`extraKnownMarketplaces.zoi.source.path`) é igual ao `caminho` do repositório `automaster` no manifesto.
  4. O link `espelho/.claude/skills/ghl-api-docs/docs` aponta para `__HOME__/Code/ghl-docs`, e o `SKILL.md` do espelho não cita `~/Documents/ghl-docs`.
  5. A suíte inteira passa, inclusive `test_sem_home_real` e `test_repositorios`.
- Como fazer:
  1. `fontes.json`: nos dois itens de `repositorios`, acrescente `"destino": "~/Code/automaster"` e `"destino": "~/Code/ghl-docs"` (formato igual ao `caminho`).
  2. `~/.claude/skills/ghl-api-docs/SKILL.md:9` e `:13`: troque a citação de `~/Documents/ghl-docs` por "a pasta `docs` ao lado desta skill", mantendo o resto do texto.
  3. `README.md:99-110`: a frase "Clonados no mesmo caminho da origem" passa a dizer que cada repositório é clonado em `~/Code/<nome>`.
  4. Regenere o kit: `python3 espelho.py sync --kit .` na raiz do kit, respondendo `N` quando perguntar "Publicar?". Isso atualiza `espelho/` e `manifesto.json` na árvore de trabalho sem commit nem push. Confira `git diff --stat` e `git status --short` e commite só os arquivos desta etapa mais `espelho/` e `manifesto.json`. Não faça push.
  5. `test/test_espelho_real.py`: acrescente os testes 1 a 4 acima, no estilo dos existentes (`ler(rel)`, `manifesto()`, `os.walk(ESPELHO)`, checando links com `os.path.islink` e `os.readlink`).
