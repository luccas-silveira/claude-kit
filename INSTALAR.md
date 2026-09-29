# Instalação feita por agente

Instruções para o agente de IA que instala o claude-kit a pedido de alguém. Leia inteiro antes
do primeiro comando.

## A regra

A instalação só termina completa. Não existe "instalei, faltou X": cada item que falhar é
corrigido por você ou resolvido com o usuário, e depois vira issue neste repositório.

- Deu erro e você sabe a causa: corrija, rode de novo e abra a issue.
- Deu erro e você não tem certeza da causa ou da correção: pergunte ao usuário. Não chute, não
  pule, não encerre.
- O passo depende do usuário (acesso a repositório privado, credencial, QR do WhatsApp): peça,
  espere e confira depois que ele fizer.
- A instalação só está pronta quando a verificação do fim deste arquivo passa inteira.

Nunca declare a instalação pronta com item pendente, e nunca troque "corrigir" por "anotar para
depois".

## 1. Antes de rodar

O instalador espelha: o que o usuário tem e não está no kit é apagado (skills, agents,
commands, hooks, output styles, servidores MCP, plugins e marketplaces). Mostre isso ao usuário
com o que existe hoje e só siga com um sim explícito:

```bash
ls ~/.claude/skills ~/.claude/agents ~/.claude/commands ~/.claude/output-styles 2>/dev/null
claude plugin list
claude mcp list
```

Confira os pré-requisitos. Faltou algum, resolva antes de seguir:

```bash
sw_vers                 # macOS
brew --version          # Homebrew
claude --version        # Claude Code
gh auth status          # necessário para os repositórios privados e para abrir issues
```

Sem `gh` logado, peça ao usuário para rodar `! gh auth login`. Sem acesso aos repositórios
privados (`zoi-tech/automaster`, `luccas-silveira/whatsapp-mcp`, `luccas-silveira/ghl-docs`),
peça o acesso ao usuário antes de instalar: sem eles a instalação não fica completa.

## 2. Instalar

```bash
git clone https://github.com/luccas-silveira/claude-kit ~/claude-kit
bash ~/claude-kit/install.sh 2>&1 | tee ~/claude-kit-instalacao.log
```

O fim da saída tem, nesta ordem:

- `falha em:`: cada linha é um problema a corrigir.
- `versão diferente`: só aviso, não precisa igualar.
- `credenciais ausentes:`: arquivos que o usuário precisa trazer da máquina de origem.
- `snapshot:`: o backup do estado anterior. Guarde o caminho para o relatório final.

## 3. Corrigir o que falhou

Para cada linha de `falha em:` e para cada erro na saída:

1. Ache a causa no log (`~/claude-kit-instalacao.log`) ou rodando o comando isolado.
2. Corrija. Se não tiver certeza, pergunte ao usuário antes.
3. Rode `bash ~/claude-kit/install.sh` de novo. Ele pode rodar quantas vezes precisar: o que já
   está instalado ou clonado é pulado, e as credenciais não são apagadas.
4. Abra a issue (seção 5).

Repositório de apoio que falhou no clone ou no passo depois dele (`go build`,
`docker compose up -d`): rode o passo à mão na pasta do repositório. O Docker Desktop precisa
estar aberto para o `docker compose`.

## 4. Passos que dependem do usuário

Credenciais: para cada caminho em `credenciais ausentes:`, peça ao usuário para copiar da
máquina de origem para o mesmo caminho nesta. Confira com `ls` depois.

WhatsApp: peça ao usuário para rodar, num terminal separado, `cd ~/Code/whatsapp-mcp/whatsapp-bridge && ./whatsapp-bridge`
e ler o QR com o celular. Se a pasta `store` veio da origem, conecta sem QR. A ponte precisa
ficar rodando.

graft: pergunte em quais repositórios o usuário trabalha e rode `graft init` em cada um.

Plugins: eles se instalam sozinhos na próxima sessão do Claude Code. Se a verificação acusar
plugin ausente, instale com `claude plugin install <id>`.

## 5. Abrir issue

Todo problema encontrado vira issue em `luccas-silveira/claude-kit`, inclusive o que você já
corrigiu: a correção precisa voltar para o kit para o próximo não cair no mesmo buraco.

Procure antes se já existe:

```bash
gh issue list -R luccas-silveira/claude-kit --state all --search "<termo do erro>"
```

Se existir, comente nela com o seu caso. Se não, abra:

```bash
gh issue create -R luccas-silveira/claude-kit --label bug \
  --title "instalação: <o que falhou, em poucas palavras>" \
  --body "$(cat <<'EOF'
## O que falhou
<a linha exata do erro>

## Ambiente
- macOS: <sw_vers -productVersion>
- Claude Code: <claude --version>
- kit: <git -C ~/claude-kit rev-parse --short HEAD>

## Causa
<o que provocou, ou "não identificada">

## Correção aplicada
<o que você fez nesta máquina para resolver>

## O que mudar no kit
<a mudança que evita o problema na próxima instalação>
EOF
)"
```

Nunca coloque na issue credencial, token, conteúdo das pastas de credencial ou dado de cliente.
Troque o caminho do home por `~`.

## 6. Verificação

Rode os dois blocos. A instalação só está pronta quando o primeiro imprime `OK` e o segundo
mostra `Connected` para `chrome-devtools`, `deja`, `graft`, `inspo`, `playwright`, `scrapling`
e `whatsapp`.

```bash
cd ~/claude-kit && PATH="$PATH:$HOME/.local/bin:/opt/homebrew/bin" python3 - <<'PY'
import json, os, subprocess
home = os.path.expanduser('~')
m = json.load(open('manifesto.json'))
erros = []
saida = subprocess.run(['claude', 'plugin', 'list', '--json'], capture_output=True, text=True).stdout
ligados = {p['id']: p['enabled'] for p in json.loads(saida or '[]')}
for p in m['plugins']:
    if p['id'] not in ligados:
        erros.append('plugin não instalado: ' + p['id'])
    elif ligados[p['id']] != p['ligado']:
        erros.append('plugin %s: ligado=%s, esperado %s' % (p['id'], ligados[p['id']], p['ligado']))
for r in m['repositorios']:
    c = r['caminho'].replace('__HOME__', home)
    if not os.path.isdir(os.path.join(c, '.git')):
        erros.append('repositório não clonado: ' + c)
for c in m['credenciais']:
    c = c.replace('__HOME__', home)
    if not os.path.exists(c):
        erros.append('credencial ausente: ' + c)
for p in json.load(open('fontes.json'))['programas']:
    if subprocess.run(p['versao'], shell=True, capture_output=True).returncode:
        erros.append('programa ausente: ' + p['nome'])
print('\n'.join(erros) or 'OK')
PY
```

```bash
claude mcp list
```

Qualquer linha diferente disso volta para a seção 3.

## 7. Relatório ao usuário

Só depois da verificação passar: o caminho do snapshot, as issues abertas ou comentadas, e o
lembrete de abrir uma sessão nova do Claude Code, porque hooks e plugins só carregam nela.

Para desfazer tudo: `tar -xzf ~/claude-espelho-<data>.tar.gz -C ~`.
