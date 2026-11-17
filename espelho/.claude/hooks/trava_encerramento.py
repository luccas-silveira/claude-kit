#!/usr/bin/env python3
"""Trava de encerramento: hook de parada que não deixa o Claude encerrar com trabalho pela
metade. Só biblioteca padrão.

Lê o JSON do Stop pelo stdin e escreve a decisão no stdout. Qualquer erro vira saída 0 sem
nada no stdout (falha aberta): a trava nunca prende uma sessão por defeito próprio.
"""
import json
import os
import subprocess
import sys

LIMITE_PEDIDO = 2000
LIMITE_LINHA = 200
LIMITE_LINHAS = 60
EDITORES = ('Edit', 'Write', 'MultiEdit', 'NotebookEdit')
TEMPO_JUIZ = 25


def git(pasta, *args):
    try:
        p = subprocess.run(['git', '-C', pasta, *args], capture_output=True, text=True)
    except OSError:
        return None
    return p.stdout if p.returncode == 0 else None


def raiz(pasta):
    """Raiz do git de qualquer subpasta, ou None fora de repositório."""
    r = git(pasta, 'rev-parse', '--show-toplevel')
    return r.strip() if r else None


def texto_do_usuario(linha):
    """Texto que o usuário escreveu, ou None quando a linha não abre turno (tool_result,
    isMeta, linha que não é mensagem do usuário)."""
    if linha.get('type') != 'user' or linha.get('isMeta'):
        return None
    conteudo = (linha.get('message') or {}).get('content')
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        textos = [b.get('text', '') for b in conteudo
                  if isinstance(b, dict) and b.get('type') == 'text']
        if textos:
            return '\n'.join(textos)
    return None


def resumo(bloco):
    nome = bloco.get('name') or '?'
    entrada = bloco.get('input') or {}
    if nome == 'Bash' and entrada.get('command'):
        return f'{nome}: {entrada["command"]}'
    if nome in ('Edit', 'Write', 'Read') and entrada.get('file_path'):
        return f'{nome}: {entrada["file_path"]}'
    return nome


def turno(transcript_path):
    """(pedido, ferramentas, caminhos) do turno atual: o que vem depois da última mensagem de
    texto do usuário. Transcript ausente levanta OSError; o main trata."""
    linhas = []
    with open(transcript_path) as f:
        for bruta in f:
            try:
                linha = json.loads(bruta)
            except ValueError:
                continue
            if isinstance(linha, dict):
                linhas.append(linha)
    inicio, pedido = 0, ''
    for i in range(len(linhas) - 1, -1, -1):
        t = texto_do_usuario(linhas[i])
        if t is not None:
            inicio, pedido = i + 1, t
            break
    ferramentas, caminhos = [], []
    for linha in linhas[inicio:]:
        if linha.get('type') != 'assistant':
            continue
        conteudo = (linha.get('message') or {}).get('content')
        if not isinstance(conteudo, list):
            continue
        for b in conteudo:
            if not isinstance(b, dict) or b.get('type') != 'tool_use':
                continue
            if len(ferramentas) < LIMITE_LINHAS:
                ferramentas.append(resumo(b)[:LIMITE_LINHA])
            if b.get('name') in EDITORES:
                entrada = b.get('input') or {}
                c = entrada.get('file_path') or entrada.get('notebook_path')
                if isinstance(c, str) and os.path.isabs(c) and c not in caminhos:
                    caminhos.append(c)
    return pedido[:LIMITE_PEDIDO], ferramentas, caminhos


def pasta_existente(caminho):
    p = os.path.dirname(caminho)
    while p and not os.path.isdir(p):
        p = os.path.dirname(p) if os.path.dirname(p) != p else ''
    return p or None


def sujos(r):
    """Caminhos absolutos (resolvidos) que o git status do repositório r mostra."""
    saida = git(r, 'status', '--porcelain', '-uall', '-z') or ''
    campos = saida.split('\0')
    resultado, i = set(), 0
    while i < len(campos):
        item = campos[i]
        i += 1
        if len(item) < 4:
            continue
        resultado.add(os.path.realpath(os.path.join(r, item[3:])))
        if item[0] in 'RC':
            i += 1  # renomeado ou copiado: o campo seguinte é a origem
    return resultado


def sem_commit(caminhos):
    """Só os caminhos que aparecem no git status do próprio repositório. Fora de git não
    entra."""
    por_raiz, resultado = {}, []
    for c in caminhos:
        pasta = pasta_existente(c)
        r = raiz(pasta) if pasta else None
        if not r:
            continue
        if r not in por_raiz:
            por_raiz[r] = sujos(r)
        if os.path.realpath(c) in por_raiz[r]:
            resultado.append(c)
    return resultado


def vesta_ativa(entrada):
    """Execução da Vesta desta sessão em andamento: a trava da Vesta já cuida da parada."""
    r = raiz(entrada.get('cwd') or os.getcwd())
    if not r:
        return False
    try:
        with open(os.path.join(r, '.claude', 'vesta', 'estado.json')) as f:
            e = json.load(f)
    except (OSError, ValueError):
        return False
    sid = entrada.get('session_id')
    return (isinstance(e, dict) and bool(sid) and e.get('sessao') == sid
            and e.get('espera') is None
            and any(x.get('status') == 'pendente' for x in e.get('etapas') or []))


def deve_ignorar(entrada, env):
    """True quando a trava não se aplica a esta parada."""
    if env.get('CLAUDE_CODE_SESSION_ATTENDED') != '1':
        return True
    if entrada.get('agent_id'):
        return True
    if any(isinstance(t, dict) and t.get('status') == 'running'
           for t in entrada.get('background_tasks') or []):
        return True
    return vesta_ativa(entrada)


CRITERIOS = """O assistente tem shell, SSH nos servidores, git, navegador automatizado (Playwright) com as sessões do usuário já logadas (CRM, GHL, Meta e outros), WhatsApp e as ferramentas do CRM. O usuário quer que ele faça tudo o que consegue com isso e só deixe com o usuário o que de fato exige o usuário. A reclamação mais comum dele é o assistente parar e devolver trabalho que podia ter feito.

Barre quando a mensagem final:

1. pede licença para algo que o próprio assistente pode fazer agora, dentro do que foi pedido ("quer que eu…?", "posso…?", "corrijo…?", "se quiser, eu…");
2. diz que está pronto, feito ou corrigido sem que o turno tenha rodado teste ou verificação;
3. lista pendência que o próprio assistente resolve com as ferramentas que tem;
4. pede ao usuário que rode, teste, clique, abra uma tela ou confira algo que o assistente pode fazer pelo navegador, pelo shell ou pelas ferramentas, fora login;
5. teve trabalho e não deixa claro o que falta e o que depende do usuário.

Não barre quando o que falta depende de login que só o usuário faz, de um aparelho físico dele, de aprovação, de decisão de negócio do usuário (escolher entre opções, aprovar texto, plano ou contrato) ou de ação irreversível ou externa: mandar mensagem a cliente ou a terceiro, deploy em produção, apagar dado, gastar dinheiro. Mexer nos sistemas do próprio usuário para cumprir o pedido (código, automação, configuração) não é ação externa. Arquivo sem commit não barra sozinho: entra como fato para o item 5, porque commit só acontece quando o usuário pede.

Pergunta que só pede confirmação de algo que o assistente já devia fazer conta como licença (item 1), não como decisão.

Quando barrar, o motivo é uma instrução curta e direta ao assistente dizendo o que fazer, em português (ex.: "rode os testes antes de dizer que está pronto")."""

LIMITE_BARRADAS = 2


def texto_ao_juiz(pedido, ferramentas, arquivos, mensagem):
    lista = lambda xs: '\n'.join(f'- {x}' for x in xs) or '(nenhum)'
    return (
        'Você revisa a última mensagem de um assistente de código antes de ela ir ao usuário.\n\n'
        f'## Pedido do usuário\n{pedido or "(vazio)"}\n\n'
        f'## Ferramentas usadas no turno\n{lista(ferramentas)}\n\n'
        f'## Arquivos editados ainda sem commit\n{lista(arquivos)}\n\n'
        f'## Mensagem final do assistente\n{mensagem or "(vazia)"}\n\n'
        f'## Critérios\n{CRITERIOS}\n\n'
        'Responda só com o JSON: {"barrar": true|false, "motivo": "..."}\n')


def ler_resposta(saida):
    """{"barrar": bool, "motivo": str} do primeiro { ao último }, ou None fora do formato."""
    i, j = saida.find('{'), saida.rfind('}')
    if i < 0 or j < i:
        return None
    try:
        r = json.loads(saida[i:j + 1])
    except ValueError:
        return None
    if not isinstance(r, dict) or not isinstance(r.get('barrar'), bool):
        return None
    return r


def julgar(pedido, ferramentas, caminhos, mensagem, env):
    """Resposta do juiz, ou None em erro, timeout ou formato inválido."""
    try:
        tempo = float(env.get('TRAVA_TIMEOUT') or TEMPO_JUIZ)
    except ValueError:
        tempo = TEMPO_JUIZ
    try:
        p = subprocess.run(
            ['claude', '-p', '--model', 'haiku', '--setting-sources', '', '--strict-mcp-config'],
            input=texto_ao_juiz(pedido, ferramentas, sem_commit(caminhos), mensagem),
            capture_output=True, text=True, timeout=tempo)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if p.returncode != 0:
        return None
    return ler_resposta(p.stdout)


def arquivo_contador(entrada, env):
    pasta = env.get('TRAVA_DIR') or os.path.expanduser('~/.claude/trava-encerramento')
    return os.path.join(pasta, f'{entrada.get("session_id") or "sem-sessao"}.json')


def barradas(arquivo, prompt_id):
    """Quantas vezes este prompt_id já foi barrado; prompt_id novo zera."""
    try:
        with open(arquivo) as f:
            c = json.load(f)
    except (OSError, ValueError):
        return 0
    if not isinstance(c, dict) or c.get('prompt_id') != prompt_id:
        return 0
    n = c.get('barradas')
    return n if isinstance(n, int) else 0


def gravar_barradas(arquivo, prompt_id, n):
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    tmp = arquivo + '.tmp'
    with open(tmp, 'w') as f:
        json.dump({'prompt_id': prompt_id, 'barradas': n}, f)
    os.replace(tmp, arquivo)


def bloqueio(motivo):
    motivo = str(motivo or 'a mensagem final deixa trabalho pela metade').strip().rstrip('.')
    return {'decision': 'block',
            'reason': f'Trava de encerramento: {motivo}. Resolva e só então encerre. '
                      'Se depende do usuário, diga o que e por quê.'}


def main():
    try:
        entrada = json.loads(sys.stdin.read())
        if not isinstance(entrada, dict) or deve_ignorar(entrada, os.environ):
            return 0
        pedido, ferramentas, caminhos = turno(entrada['transcript_path'])
        if not ferramentas:
            return 0
        arquivo, prompt_id = arquivo_contador(entrada, os.environ), entrada.get('prompt_id')
        n = barradas(arquivo, prompt_id)
        if n >= LIMITE_BARRADAS:
            return 0
        r = julgar(pedido, ferramentas, caminhos, entrada.get('last_assistant_message'),
                   os.environ)
        if r and r['barrar']:
            gravar_barradas(arquivo, prompt_id, n + 1)
            print(json.dumps(bloqueio(r.get('motivo'))))
    except Exception:
        pass
    return 0


if __name__ == '__main__':
    sys.exit(main())
