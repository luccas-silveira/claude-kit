"""Espelho do setup de Claude Code: `sync` copia do home para o kit, `instalar` faz o inverso."""
import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
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


def rodar(cmd):
    """Roda um comando externo pelo PATH; devolve a saída se deu certo, senão None."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    except (FileNotFoundError, PermissionError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


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
        dados = dados.decode('utf-8').replace(ctx['home'], MARCA).encode('utf-8')
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

    espelho = os.path.join(kit, 'espelho')
    shutil.rmtree(espelho, ignore_errors=True)
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
    escrever_json(os.path.join(kit, 'manifesto.json'), {
        'plugins': [{'id': i, 'versao': (v[0].get('version') if v else None),
                     'ligado': ligados.get(i) is True} for i, v in sorted(instalados.items())],
        'marketplaces': [{'nome': n, 'fonte': m.get('source')} for n, m in sorted(
            ler_json(os.path.join(plug, 'known_marketplaces.json'), {}).items())],
        'programas': [dict(p, versao=rodar(shlex.split(p['versao'])))
                      for p in fontes.get('programas', [])],
        'repositorios': repositorios,
        'credenciais': cred,
    }, home)
    return 0


def instalar(args):
    if not shutil.which('claude'):
        print('Claude Code não encontrado no PATH. Instale o Claude Code antes.', file=sys.stderr)
        return 1
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog='espelho.py')
    sub = p.add_subparsers(dest='cmd')
    ps = sub.add_parser('sync', help='copia o setup do home para o kit')
    ps.add_argument('--kit', help='pasta do kit (padrão: a do espelho.py)')
    ps.set_defaults(fn=sync)
    sub.add_parser('instalar', help='instala o setup do kit no home').set_defaults(fn=instalar)
    args = p.parse_args(argv)
    if not args.cmd:
        p.print_usage(sys.stderr)
        return 2
    return args.fn(args)


if __name__ == '__main__':
    sys.exit(main())
