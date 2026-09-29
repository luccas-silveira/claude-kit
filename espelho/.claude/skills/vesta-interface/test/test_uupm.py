"""Etapa 1: busca do ui-ux-pro-max copiada para ferramentas/uupm, rodando só com a stdlib."""
import ast
import csv
import filecmp
import json
import os
import pathlib
import re
import subprocess
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UUPM = os.path.join(RAIZ, 'ferramentas', 'uupm')
SCRIPTS = os.path.join(UUPM, 'scripts')
DADOS = os.path.join(UUPM, 'data')
SEARCH = os.path.join(SCRIPTS, 'search.py')
COPIADOS = ('search.py', 'core.py', 'design_system.py', 'reasoning_contract.py')
PROPRIOS = {'core', 'design_system', 'reasoning_contract'}
ORIGEM = os.path.expanduser('~/Code/ux-lab/vendor/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max')
OPCIONAIS = {'phosphor-icons-upstream.json', 'google-font-licenses.json', 'data-provenance.json'}
HEX = re.compile(r'#[0-9A-Fa-f]{6}')


def rodar(*args, cwd='/tmp'):
    return subprocess.run([sys.executable, SEARCH, *args], capture_output=True, text=True,
                          encoding='utf-8', cwd=cwd, timeout=120)


def padroes_de_landing():
    """Nomes dos padrões de landing do banco (a coluna Pattern Name de data/landing.csv)."""
    with open(os.path.join(DADOS, 'landing.csv'), encoding='utf-8', newline='') as f:
        return [r['Pattern Name'] for r in csv.DictReader(f)]


def rodar_json(*args, cwd='/tmp'):
    r = rodar(*args, '--json', cwd=cwd)
    if r.returncode != 0:
        raise AssertionError(f'search.py saiu com {r.returncode}: {r.stderr}')
    return json.loads(r.stdout)


class TestDesignSystem(unittest.TestCase):
    def setUp(self):
        self.r = rodar('fintech banking dashboard', '--design-system', '--format', 'markdown')

    def test_sai_com_zero(self):
        self.assertEqual(self.r.returncode, 0, self.r.stderr)

    def test_tem_style_typography_e_cor(self):
        self.assertIn('### Style', self.r.stdout)
        self.assertIn('### Typography', self.r.stdout)
        self.assertRegex(self.r.stdout, HEX)

    def test_markdown_sem_ansi(self):
        self.assertEqual(self.r.returncode, 0, self.r.stderr)
        self.assertNotIn('\x1b[', self.r.stdout)

    def test_ascii_padrao_tem_ansi(self):
        # motivo de a skill sempre pedir --format markdown ou --json
        r = rodar('fintech banking dashboard', '--design-system')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('\x1b[', r.stdout)


class TestBuscaJson(unittest.TestCase):
    def test_dominio_ux_devolve_dois(self):
        d = rodar_json('form validation error', '--domain', 'ux', '-n', '2')
        self.assertIsInstance(d, dict)
        self.assertIn('count', d)
        self.assertIn('results', d)
        self.assertEqual(len(d['results']), 2)
        self.assertEqual(d['count'], 2)

    def test_stack_shadcn_devolve_um(self):
        d = rodar_json('dialog form', '--stack', 'shadcn', '-n', '1')
        self.assertEqual(len(d['results']), 1)


class TestIndependeDaPasta(unittest.TestCase):
    def test_mesma_saida_em_tmp_e_na_pasta_do_script(self):
        args = ('form validation error', '--domain', 'ux', '-n', '2')
        self.assertEqual(rodar_json(*args, cwd='/tmp'), rodar_json(*args, cwd=SCRIPTS))

    def test_design_system_igual_em_tmp_e_na_raiz(self):
        args = ('fintech banking dashboard', '--design-system', '--format', 'markdown')
        em_tmp, na_raiz = rodar(*args, cwd='/tmp'), rodar(*args, cwd=RAIZ)
        self.assertEqual(em_tmp.returncode, 0, em_tmp.stderr)
        self.assertEqual(em_tmp.stdout, na_raiz.stdout)


class TestSoStdlib(unittest.TestCase):
    def test_nenhum_import_fora_da_stdlib(self):
        permitidos = set(sys.stdlib_module_names) | PROPRIOS
        for nome in COPIADOS:
            with open(os.path.join(SCRIPTS, nome), encoding='utf-8') as f:
                arvore = ast.parse(f.read(), nome)
            for no in ast.walk(arvore):
                if isinstance(no, ast.Import):
                    modulos = [a.name for a in no.names]
                elif isinstance(no, ast.ImportFrom):
                    self.assertEqual(no.level, 0, f'{nome}: import relativo')
                    modulos = [no.module]
                else:
                    continue
                for m in modulos:
                    self.assertIn(m.split('.')[0], permitidos, f'{nome} importa {m}')


@unittest.skipUnless(os.path.isdir(ORIGEM), 'fonte congelada do ui-ux-pro-max ausente')
class TestCopiaFiel(unittest.TestCase):
    def test_scripts_sem_edicao(self):
        for nome in COPIADOS:
            self.assertTrue(filecmp.cmp(os.path.join(SCRIPTS, nome),
                                        os.path.join(ORIGEM, 'scripts', nome), shallow=False), nome)

    def test_data_completa(self):
        # só os três JSON opcionais podem faltar, e só se nenhum script copiado os citar
        fonte = os.path.join(ORIGEM, 'data')
        codigo = ''.join(pathlib.Path(SCRIPTS, n).read_text(encoding='utf-8') for n in COPIADOS)
        for pasta, _, arquivos in os.walk(fonte):
            for a in arquivos:
                if a == '.DS_Store':
                    continue
                rel = os.path.relpath(os.path.join(pasta, a), fonte)
                copia = os.path.join(DADOS, rel)
                if rel in OPCIONAIS and not os.path.exists(copia):
                    self.assertNotIn(rel, codigo, f'{rel} excluído mas um script o abre')
                    continue
                self.assertTrue(os.path.isfile(copia), rel)
                self.assertTrue(filecmp.cmp(copia, os.path.join(pasta, a), shallow=False), rel)


if __name__ == '__main__':
    unittest.main()
