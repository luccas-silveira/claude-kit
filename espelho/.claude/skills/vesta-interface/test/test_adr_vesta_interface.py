"""Etapa 12: ADR-0021 na Vesta registra a vesta-interface; claude-tooling aponta para ele."""
import os
import re
import subprocess
import unittest

VESTA = os.path.expanduser('~/Code/vesta')
TOOLING = os.path.expanduser('~/Code/claude-tooling')
ADR_0021 = os.path.join(VESTA, 'docs', 'decisoes', '0021-vesta-interface.md')
ADR_0018 = 'docs/decisoes/0018-mockup-e-frontend-na-vesta.md'
# último commit que tocou o ADR-0018 (etapa 5 da Vesta); ADR antigo nunca é reescrito
COMMIT_0018 = '354652e8b338097e84c529ded0a01897e5944b4a'
PONTEIRO = re.compile(r'~/Code/vesta/docs/decisoes/[\w.-]+\.md')


def git_vesta(*args):
    return subprocess.run(['git', '-C', VESTA, *args], capture_output=True, text=True, check=True).stdout


@unittest.skipUnless(os.path.isdir(VESTA), '~/Code/vesta ausente')
class TestAdrNaVesta(unittest.TestCase):
    def test_adr_0021_existe(self):
        self.assertTrue(os.path.isfile(ADR_0021), 'docs/decisoes/0021-vesta-interface.md não existe na Vesta')

    def test_adr_0021_cita_vesta_interface(self):
        with open(ADR_0021) as f:
            self.assertIn('vesta-interface', f.read())

    def test_adr_0018_sem_commit_novo(self):
        ultimo = git_vesta('log', '-1', '--format=%H', '--', ADR_0018).strip()
        self.assertEqual(ultimo, COMMIT_0018, 'o ADR-0018 foi alterado em commit')

    def test_adr_0018_sem_mudanca_pendente(self):
        self.assertEqual(git_vesta('status', '--porcelain', '--', ADR_0018), '', 'o ADR-0018 tem mudança não commitada')


@unittest.skipUnless(os.path.isdir(TOOLING), '~/Code/claude-tooling ausente')
class TestPonteiroNoClaudeTooling(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(TOOLING, 'docs', 'README.md')) as f:
            self.linhas = f.read().splitlines()

    def linha_seguinte_a_0020(self):
        i = next((n for n, l in enumerate(self.linhas) if l.startswith('- [ADR-0020')), None)
        self.assertIsNotNone(i, 'linha do ADR-0020 sumiu do docs/README.md')
        self.assertLess(i + 1, len(self.linhas))
        return self.linhas[i + 1]

    def test_linha_do_0021_logo_depois_da_do_0020(self):
        linha = self.linha_seguinte_a_0020()
        self.assertTrue(linha.startswith('- ') and 'ADR-0021' in linha, f'linha depois do ADR-0020: {linha!r}')

    def test_linha_do_0021_aponta_para_arquivo_que_existe(self):
        alvos = PONTEIRO.findall(self.linha_seguinte_a_0020())
        self.assertEqual(len(alvos), 1, 'a linha do ADR-0021 deve ter um caminho em ~/Code/vesta/docs/decisoes/')
        self.assertTrue(alvos[0].endswith('/0021-vesta-interface.md'), alvos[0])
        self.assertTrue(os.path.isfile(os.path.expanduser(alvos[0])), f'{alvos[0]} não existe')


if __name__ == '__main__':
    unittest.main()
