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
echo "$(basename "$0") $*" >> "$STUB_LOG"
[ -f "$STUB_DIR/$(basename "$0").out" ] && cat "$STUB_DIR/$(basename "$0").out"
exit 0
'''


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
