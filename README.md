# claude-kit

Meu setup de Claude Code em um repo: skills próprias empacotadas como plugin, o fluxo de
trabalho (Vesta) e o jeito de falar (output style Seco), mais a lista de plugins e skills
de terceiros que eu de fato uso.

## Instalar numa máquina nova

```bash
git clone https://github.com/luccas-silveira/claude-kit && bash claude-kit/install.sh
```

Idempotente: rodar de novo atualiza sem duplicar nada. Hooks e `outputStyle` são fundidos
no `settings.json` existente, sem apagar o que já está lá.

Ou só as skills próprias, sem clonar:

```
/plugin marketplace add luccas-silveira/claude-kit
/plugin install zoi-skills@zoi-kit
```

## O que tem aqui

`plugins/zoi-skills/skills/` — skills próprias, instaladas como plugin:

| skill | pra quê |
|---|---|
| `ghl-api-docs` | referência da API GoHighLevel v3 + gotchas medidos ao vivo |
| `prompt-engineering` | escrever e auditar system prompts |
| `supacode-cli`, `supacode-deeplinks` | controlar o Supacode pelo terminal ou por URL |

`home/` — o que vai direto para `~/.claude`, porque depende de caminho fixo e de hook:

| peça | pra quê |
|---|---|
| `skills/vesta` + `commands/vesta-*` | fluxo de trabalho criativo: spec → pesquisa → grill → plano → execução travada por prova de teste |
| `output-styles/seco.md` | output style padrão: diz só o que deve ser dito |
| `hooks.json` | hooks da Vesta (início, adoção, parada) e o lembrete do Seco depois de cada edição |

## Terceiros (o `install.sh` puxa da fonte)

Plugins: `superpowers`, `playwright`, `security-guidance`, `ponytail`, `watch`,
`impeccable`, `caveman` (só subagentes e skills; a fala fica com o Seco), `headroom`,
`automaster` (MCP de auditoria e edição do GoHighLevel; repo privado da zoi-tech, só
instala com acesso a ele e precisa de Python 3.12+).

Skills avulsas: `archify` (tt-a1i/archify), `grill-me` e `wayfinder` (mattpocock/skills).

## Fora do escopo

`deja` e `graft` instalam as próprias skills e hooks junto com o CLI. `headroom` precisa do
CLI (`uv tool install headroom-ai`). MCP servers com binário ou credencial local, o
`CLAUDE.md` global e a memória ficam de fora: são pessoais por máquina.

## Manutenção

O kit é gerado a partir da máquina viva. Pra saber o que ainda vale manter, conte as
invocações reais nos transcripts:

```bash
grep -roh '"skill":"[^"]*"' --include='*.jsonl' ~/.claude/projects \
  | sed 's/.*"skill":"//;s/"//' | sort | uniq -c | sort -rn
```
