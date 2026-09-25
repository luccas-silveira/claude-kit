"""Etapa 7: conteúdo real do kit (espelho/ e manifesto.json), não o HOME."""
import glob
import json
import os
import pwd
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESPELHO = os.path.join(KIT, 'espelho')
MANIFESTO = os.path.join(KIT, 'manifesto.json')
HOME_REAL = pwd.getpwuid(os.getuid()).pw_dir
BLOQUEIO = os.path.join(HOME_REAL, '.config/claude-kit/bloqueio.txt')


def ler(rel):
    with open(os.path.join(ESPELHO, rel), encoding='utf-8') as f:
        return f.read()


def manifesto():
    with open(MANIFESTO, encoding='utf-8') as f:
        return json.load(f)


class TestEspelhoReal(unittest.TestCase):
    def test_existem(self):
        self.assertTrue(os.path.isdir(ESPELHO), 'espelho/ ausente')
        self.assertTrue(os.path.isfile(MANIFESTO), 'manifesto.json ausente')
        self.assertTrue(os.path.isfile(os.path.join(ESPELHO, '.claude/settings.json')))

    def test_lixo_removido(self):
        self.assertTrue(os.path.isdir(ESPELHO), 'espelho/ ausente')
        self.assertEqual(glob.glob(os.path.join(ESPELHO, '.claude/skills-disabled/gsd-*')), [])
        for rel in ['.claude/hooks/knobler-agent-notify.sh', '.claude/statusline-command.sh',
                    '.claude/statusline-test.sh', '.claude/hooks/context-mode-cache-heal.mjs',
                    '.claude/skills/wayfinder/SKILL.md.orig']:
            self.assertFalse(os.path.lexists(os.path.join(ESPELHO, rel)), rel)

    def test_settings_limpo(self):
        s = ler('.claude/settings.json')
        for termo in ['get contatos', 'context-mode-cache-heal', 'subagentStatusLine']:
            self.assertNotIn(termo, s)

    def test_settings_local_limpo(self):
        s = ler('.claude/settings.local.json')
        self.assertNotIn('ralph-loop', s)
        self.assertNotIn('vesta.py" silenciar', s.replace('\\"', '"'))

    def test_sem_home_real(self):
        self.assertTrue(os.path.isdir(ESPELHO), 'espelho/ ausente')
        achados = []
        for d, _, arqs in os.walk(ESPELHO):
            for n in arqs:
                p = os.path.join(d, n)
                if os.path.islink(p):
                    continue
                with open(p, 'rb') as f:
                    if HOME_REAL.encode() in f.read():
                        achados.append(os.path.relpath(p, ESPELHO))
        self.assertEqual(achados, [])

    def test_repositorios(self):
        repos = manifesto()['repositorios']
        caminhos = {r['caminho'].rstrip('/').rsplit('/', 1)[-1]: r['remote'] for r in repos}
        self.assertIn('luccas-silveira/', caminhos.get('whatsapp-mcp', ''))
        self.assertIn('luccas-silveira/ghl-docs', caminhos.get('ghl-docs', ''))
        self.assertNotIn('claude-tooling', json.dumps(repos))

    def test_manifesto_sem_termo_bloqueado(self):
        self.assertTrue(os.path.isfile(MANIFESTO), 'manifesto.json ausente')
        if not os.path.isfile(BLOQUEIO):
            self.skipTest('sem ' + BLOQUEIO)
        with open(BLOQUEIO, encoding='utf-8') as f:
            termos = [t.strip().lower() for t in f if t.strip()]
        with open(MANIFESTO, encoding='utf-8') as f:
            texto = f.read().lower()
        self.assertEqual([t for t in termos if t in texto], [])


if __name__ == '__main__':
    unittest.main()
