# claude-kit

Espelho do meu Claude Code. `sync.sh` publica o estado da máquina de origem; `install.sh`
deixa qualquer Mac idêntico a ela, sem sobras e sem faltas.

## Instalar

```bash
git clone https://github.com/luccas-silveira/claude-kit && bash claude-kit/install.sh
```

Precisa do Claude Code já instalado. O instalador:

- guarda o estado anterior em `~/claude-espelho-<data>.tar.gz` (o caminho sai na última linha);
- copia skills, agents, commands, hooks, output styles, settings e MCP, apagando o que não está no espelho;
- remove plugins e marketplaces fora do manifesto (os do manifesto se instalam ao abrir o Claude Code);
- clona os repositórios locais no mesmo caminho e instala os programas que faltam;
- avisa versões diferentes da origem e lista as credenciais que faltam.

## Publicar (na máquina de origem)

```bash
bash sync.sh
```

Mostra o que mudou e só publica com `s`. Barra segredo e qualquer termo de
`~/.config/claude-kit/bloqueio.txt` (nomes de clientes, fora do kit).

## Fica fora

O `CLAUDE.md` global, toda a memória e as credenciais. Credenciais viajam à mão.

Continua manual: credenciais, login do Claude Code, QR do WhatsApp e iniciar a ponte,
`graft init` em cada repositório.

## Desfazer

```bash
tar -xzf ~/claude-espelho-<data>.tar.gz -C ~
```

## Testes

```bash
python3 -m unittest discover -s test -v
```
