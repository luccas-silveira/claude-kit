"""Infra dos testes do espelho: HOME falso, pasta de stubs no PATH e STUB_LOG."""
import os
import subprocess
import tempfile
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(KIT, 'espelho.py')
for _k in [k for k in os.environ if k.startswith('GIT_')]:
    del os.environ[_k]

STUB = '''#!/bin/sh
n="$(basename "$0")"
echo "$n $*" >> "$STUB_LOG"
k="$STUB_DIR/$n@$(printf '%s' "$*" | tr ' /' '_%')"
if [ -f "$k.out" ]; then cat "$k.out"; elif [ -f "$STUB_DIR/$n.out" ]; then cat "$STUB_DIR/$n.out"; fi
[ -f "$k.rc" ] && exit "$(cat "$k.rc")"
exit 0
'''


def chave(args):
    """Nome do arquivo de resposta por argumentos: espaço vira _, / vira %."""
    return args.replace(' ', '_').replace('/', '%')


class Caso(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        raiz = os.path.realpath(self.tmp.name)
        self.home = os.path.join(raiz, 'home')
        self.stubs = os.path.join(raiz, 'stubs')
        self.log = os.path.join(raiz, 'stub.log')
        os.makedirs(self.home)
        os.makedirs(self.stubs)
        self.env = {k: v for k, v in os.environ.items() if k != 'CLAUDE_PROJECT_DIR'}
        self.env.update(HOME=self.home, PATH=self.stubs + ':/usr/bin:/bin',
                        STUB_LOG=self.log, STUB_DIR=self.stubs)

    def tearDown(self):
        self.tmp.cleanup()

    def stub(self, nome, saida=''):
        caminho = os.path.join(self.stubs, nome)
        with open(caminho, 'w') as f:
            f.write(STUB)
        os.chmod(caminho, 0o755)
        if saida:
            with open(caminho + '.out', 'w') as f:
                f.write(saida)

    def resposta(self, nome, args, saida='', codigo=0):
        """Resposta do stub só para `nome args` exatos; codigo != 0 faz o stub sair com ele."""
        base = os.path.join(self.stubs, nome + '@' + chave(args))
        with open(base + '.out', 'w') as f:
            f.write(saida)
        if codigo:
            with open(base + '.rc', 'w') as f:
                f.write(str(codigo))

    def _run(self, cmd, entrada=None):
        r = subprocess.run(cmd, cwd=self.home, env=self.env, capture_output=True, text=True,
                           input=entrada)
        return r.returncode, r.stdout + r.stderr

    def roda(self, *args, entrada=None):
        return self._run(['/usr/bin/python3', SCRIPT, *args], entrada)

    def roda_sh(self, nome, *args):
        return self._run(['/bin/bash', os.path.join(KIT, nome), *args])

    def chamadas(self):
        if not os.path.exists(self.log):
            return []
        with open(self.log) as f:
            return f.read().splitlines()
