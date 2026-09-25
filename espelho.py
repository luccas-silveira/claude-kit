"""Espelho do setup de Claude Code: `sync` copia do home para o kit, `instalar` faz o inverso."""
import argparse
import datetime
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

GERENCIADOS = [
    '.claude/settings.json', '.claude/settings.local.json', '.claude/keybindings.json',
    '.claude/statusline.sh', '.claude/skill-stats.py', '.claude/skills', '.claude/skills-disabled',
    '.claude/agents', '.claude/commands', '.claude/output-styles', '.claude/hooks',
    '.claude/helpers', '.claude/plugins/local', '.claude/plugins/config.json',
    '.claude/plugins/blocklist.json', '.mcp.json', '.config/deja', '.config/caveman',
    '.config/yt-dlp',
]
EXCLUIR_NOME = {'__pycache__', '.DS_Store', 'node_modules', '.git'}
EXCLUIR_REL = {'.claude/CLAUDE.md', '.claude/memory', '.claude/skills/synced'}
MARCA = '__HOME__'
SEGREDO = re.compile(
    r'\bghp_[A-Za-z0-9]{36}|\bsk-[A-Za-z0-9]{40}|eyJ[\w-]+\.eyJ[\w-]+\.[\w-]+'
    r'|-----BEGIN [A-Z ]*PRIVATE KEY-----'
    r'|(api[_-]?key|secret|token|password)["\']?\s*[:=]\s*["\'][A-Za-z0-9_/+-]{16,}')
BLOQUEIO = '.config/claude-kit/bloqueio.txt'


def barreiras(raiz, termos):
    """Devolve 'caminho:linha: motivo' para cada segredo ou termo bloqueado sob raiz."""
    achados = []
    for d, subs, arqs in os.walk(raiz):
        subs.sort()
        for n in sorted(arqs):
            p = os.path.join(d, n)
            if os.path.islink(p):
                continue
            try:
                with open(p, encoding='utf-8') as f:
                    linhas = f.read().splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            for i, linha in enumerate(linhas, 1):
                baixa = linha.lower()
                motivo = ('possível segredo' if SEGREDO.search(linha) else
                          next(('termo bloqueado: ' + t for t in termos if t in baixa), None))
                if motivo:
                    achados.append('%s:%d: %s' % (os.path.relpath(p, raiz), i, motivo))
    return achados


def rodar(cmd, mostrar_erro=False, cru=False, cwd=None):
    """Roda um comando externo pelo PATH; devolve a saída se deu certo, senão None.
    Texto (vindo de fontes.json/manifesto) roda com shell=True."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd,
                           shell=isinstance(cmd, str))
    except (FileNotFoundError, PermissionError):
        return None
    if r.returncode != 0 and mostrar_erro:
        print(r.stderr.strip(), file=sys.stderr)
    return (r.stdout.rstrip() if cru else r.stdout.strip()) if r.returncode == 0 else None


def ler_json(caminho, padrao):
    try:
        with open(caminho) as f:
            return json.load(f)
    except (OSError, ValueError):
        return padrao


def escrever_json(caminho, dados, home):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    texto = json.dumps(dados, indent=2, ensure_ascii=False, sort_keys=True) + '\n'
    with open(caminho, 'w') as f:
        f.write(texto.replace(home, MARCA))


def espelhar(origem, destino, rel, ctx):
    """Copia origem (caminho lógico sob o home) para destino, trocando o home por __HOME__."""
    if os.path.basename(origem) in EXCLUIR_NOME or rel in EXCLUIR_REL or origem in ctx['cred']:
        return
    if os.path.islink(origem) and ctx.get('inverso'):
        os.symlink(os.readlink(origem).replace(MARCA, ctx['para']), destino)
        return
    if os.path.islink(origem):
        real = os.path.realpath(origem)
        if any(real == r or real.startswith(r + os.sep) for r in ctx['repos']):
            os.symlink(real.replace(ctx['home'], MARCA), destino)
            return
        if not os.path.exists(real):
            return
    if os.path.isdir(origem):
        os.makedirs(destino, exist_ok=True)
        for nome in sorted(os.listdir(origem)):
            espelhar(os.path.join(origem, nome), os.path.join(destino, nome),
                     rel + '/' + nome, ctx)
        return
    with open(origem, 'rb') as f:
        dados = f.read()
    try:
        dados = dados.decode('utf-8').replace(ctx['home'], ctx.get('para', MARCA)).encode('utf-8')
    except UnicodeDecodeError:
        pass
    with open(destino, 'wb') as f:
        f.write(dados)


def sync(args):
    home = str(Path.home())
    kit = os.path.abspath(args.kit or os.path.dirname(os.path.abspath(__file__)))
    fontes = ler_json(os.path.join(kit, 'fontes.json'), {})
    expandir = lambda c: os.path.join(home, c[2:]) if c.startswith('~/') else c
    cred = [expandir(c) for c in fontes.get('credenciais', [])]
    repos = [dict(r, caminho=expandir(r['caminho'])) for r in fontes.get('repositorios', [])]
    ctx = {'home': home, 'cred': set(cred),
           'repos': [os.path.realpath(r['caminho']) for r in repos]}

    bloqueio = os.path.join(home, BLOQUEIO)
    try:
        with open(bloqueio) as f:
            termos = [t.strip().lower() for t in f if t.strip()]
    except OSError:
        print('recusado: crie %s com os termos de cliente, um por linha.' % bloqueio)
        return 1

    tmp = tempfile.mkdtemp(prefix='.sync-', dir=kit)
    try:
        codigo = montar(home, kit, tmp, fontes, cred, repos, ctx, termos)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return codigo or publicar(kit, args.sim)


def publicar(kit, sim):
    """Mostra o que mudou no kit e, confirmado, commita espelho e manifesto e empurra."""
    topo = rodar(['git', '-C', kit, 'rev-parse', '--show-toplevel'])
    if not topo or os.path.realpath(topo) != os.path.realpath(kit):
        return 0
    git = ['git', '-C', kit]
    alvo = ['--', 'espelho', 'manifesto.json']
    status = rodar(git + ['status', '--short'] + alvo, cru=True)
    if not status:
        print('nada mudou')
        return 0
    print(status)
    print(rodar(git + ['diff', '--stat'] + alvo) or '')
    if not sim:
        try:
            resp = input('Publicar? [s/N] ')
        except EOFError:
            resp = ''
        if resp.strip().lower() != 's':
            return 0
    data = datetime.datetime.now().isoformat(timespec='seconds')
    for cmd in (['add', '-A'] + alvo[1:], ['commit', '-q', '-m', 'espelho: ' + data] + alvo,
                ['push', '-q']):
        if rodar(git + cmd, mostrar_erro=True) is None:
            return 1
    return 0


def montar(home, kit, tmp, fontes, cred, repos, ctx, termos):
    espelho = os.path.join(tmp, 'espelho')
    os.makedirs(espelho)
    for rel in GERENCIADOS:
        origem = os.path.join(home, rel)
        if os.path.lexists(origem):
            destino = os.path.join(espelho, rel)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            espelhar(origem, destino, rel, ctx)

    cj = ler_json(os.path.join(home, '.claude.json'), {})
    escrever_json(os.path.join(espelho, 'mcp.json'), {
        'global': cj.get('mcpServers', {}),
        'porProjeto': {k: v['mcpServers'] for k, v in cj.get('projects', {}).items()
                       if v.get('mcpServers')},
    }, home)

    plug = os.path.join(home, '.claude/plugins')
    ligados = ler_json(os.path.join(home, '.claude/settings.json'), {}).get('enabledPlugins', {})
    instalados = ler_json(os.path.join(plug, 'installed_plugins.json'), {}).get('plugins', {})
    repositorios = []
    for r in repos:
        remote = rodar(['git', '-C', r['caminho'], 'remote', 'get-url', 'origin'])
        if remote:
            repositorios.append({'caminho': r['caminho'], 'remote': remote,
                                 'depois': r.get('depois', '')})
        else:
            print('aviso: repositório sem remote, fora do manifesto: ' + r['caminho'])
    escrever_json(os.path.join(tmp, 'manifesto.json'), {
        'plugins': [{'id': i, 'versao': (v[0].get('version') if v else None),
                     'ligado': ligados.get(i) is True} for i, v in sorted(instalados.items())],
        'marketplaces': [{'nome': n, 'fonte': m.get('source')} for n, m in sorted(
            ler_json(os.path.join(plug, 'known_marketplaces.json'), {}).items())],
        'programas': [dict(p, versao=rodar(shlex.split(p['versao'])))
                      for p in fontes.get('programas', [])],
        'repositorios': repositorios,
        'credenciais': cred,
    }, home)

    achados = barreiras(tmp, termos)
    if achados:
        print('\n'.join(achados))
        print('ABORTADO: nada foi escrito no kit.')
        return 1
    shutil.rmtree(os.path.join(kit, 'espelho'), ignore_errors=True)
    os.replace(espelho, os.path.join(kit, 'espelho'))
    os.replace(os.path.join(tmp, 'manifesto.json'), os.path.join(kit, 'manifesto.json'))
    return 0


def instalar(args):
    if not shutil.which('claude'):
        print('Claude Code não encontrado no PATH. Instale o Claude Code antes.', file=sys.stderr)
        return 1
    home = str(Path.home())
    kit = os.path.abspath(args.kit or os.path.dirname(os.path.abspath(__file__)))
    esp = os.path.join(kit, 'espelho')
    cred = {os.path.join(home, c[2:]) if c.startswith('~/') else c.replace(MARCA, home)
            for c in ler_json(os.path.join(kit, 'manifesto.json'), {}).get('credenciais', [])}

    snap = None
    while not snap or os.path.exists(snap):  # nome é por segundo; espera o próximo
        if snap:
            time.sleep(0.2)
        snap = os.path.join(home, 'claude-espelho-%s.tar.gz'
                            % datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    with tarfile.open(snap, 'w:gz') as tar:
        for rel in GERENCIADOS + ['.claude.json']:
            if os.path.lexists(os.path.join(home, rel)):
                tar.add(os.path.join(home, rel), arcname=rel)

    ctx = {'home': MARCA, 'para': home, 'cred': set(), 'repos': [], 'inverso': True}
    for rel in GERENCIADOS:
        origem = os.path.join(esp, rel)
        if not os.path.lexists(origem):
            continue
        destino = os.path.join(home, rel)
        limpar(destino, rel, cred)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        espelhar(origem, destino, rel, ctx)

    with open(os.path.join(esp, 'mcp.json')) as f:
        mcp = json.loads(f.read().replace(MARCA, home))
    caminho = os.path.join(home, '.claude.json')
    cj = ler_json(caminho, {})
    cj['mcpServers'] = mcp.get('global', {})
    projetos = cj.setdefault('projects', {})
    for p in projetos.values():
        p.pop('mcpServers', None)
    for p, servidores in mcp.get('porProjeto', {}).items():
        projetos.setdefault(p, {})['mcpServers'] = servidores
    with open(caminho, 'w') as f:
        f.write(json.dumps(cj, indent=2, ensure_ascii=False) + '\n')

    falhas, versoes = [], []
    manifesto = ler_json(os.path.join(kit, 'manifesto.json'), {})
    plugins(manifesto, falhas)
    for r in manifesto.get('repositorios', []):
        destino = r['caminho'].replace(MARCA, home)
        if os.path.exists(destino):
            continue
        if rodar(['git', 'clone', r['remote'], destino]) is None:
            falhas.append(destino)
        elif r.get('depois') and rodar(r['depois'], cwd=destino) is None:
            falhas.append(destino + ' (depois)')
    comandos = {p['nome']: p['versao']
                for p in ler_json(os.path.join(kit, 'fontes.json'), {}).get('programas', [])}
    for p in manifesto.get('programas', []):
        local = rodar(comandos[p['nome']]) if p['nome'] in comandos else None
        if local is None:
            if rodar(p['instalar']) is None:
                falhas.append(p['nome'])
        elif local != p['versao']:
            versoes.append('%s: %s → %s' % (p['nome'], local, p['versao']))
    if falhas:
        print('falha em:\n' + '\n'.join('  ' + f for f in falhas))
    if versoes:
        print('versão diferente (daqui → do manifesto):\n'
              + '\n'.join('  ' + v for v in versoes))
    ausentes = [c for c in sorted(cred) if not os.path.exists(c)]
    if ausentes:
        print('credenciais ausentes:\n' + '\n'.join('  ' + c for c in ausentes))
    print('WhatsApp: faça o login por QR e inicie a ponte.')
    print('Abrir o Claude Code para os plugins do manifesto se instalarem.')
    print('snapshot: ' + snap)
    return 0


def plugins(manifesto, falhas):
    """Marketplace oficial garantido; plugins e marketplaces fora do manifesto saem."""
    oficial = 'anthropics/claude-plugins-official'
    if rodar(['claude', 'plugin', 'marketplace', 'add', oficial]) is None:
        falhas.append(oficial)
    ids = {p['id'] for p in manifesto.get('plugins', [])}
    for p in json.loads(rodar(['claude', 'plugin', 'list', '--json']) or '[]'):
        if p['id'] not in ids and rodar(['claude', 'plugin', 'uninstall', p['id']]) is None:
            falhas.append(p['id'])
    nomes = {m['nome'] for m in manifesto.get('marketplaces', [])} | {'claude-plugins-official'}
    for m in json.loads(rodar(['claude', 'plugin', 'marketplace', 'list', '--json']) or '[]'):
        if m['name'] not in nomes and rodar(
                ['claude', 'plugin', 'marketplace', 'remove', m['name']]) is None:
            falhas.append(m['name'])


def limpar(destino, rel, cred):
    """Apaga destino, poupando EXCLUIR_REL e credenciais que estiverem dentro dele."""
    if rel in EXCLUIR_REL or destino in cred or not os.path.lexists(destino):
        return
    if os.path.isdir(destino) and not os.path.islink(destino):
        for nome in os.listdir(destino):
            limpar(os.path.join(destino, nome), rel + '/' + nome, cred)
        try:
            os.rmdir(destino)
        except OSError:
            pass
    else:
        os.remove(destino)


def main(argv=None):
    p = argparse.ArgumentParser(prog='espelho.py')
    sub = p.add_subparsers(dest='cmd')
    ps = sub.add_parser('sync', help='copia o setup do home para o kit')
    ps.add_argument('--kit', help='pasta do kit (padrão: a do espelho.py)')
    ps.add_argument('--sim', action='store_true', help='publica sem perguntar')
    ps.set_defaults(fn=sync)
    pi = sub.add_parser('instalar', help='instala o setup do kit no home')
    pi.add_argument('--kit', help='pasta do kit (padrão: a do espelho.py)')
    pi.set_defaults(fn=instalar)
    args = p.parse_args(argv)
    if not args.cmd:
        p.print_usage(sys.stderr)
        return 2
    return args.fn(args)


if __name__ == '__main__':
    sys.exit(main())
