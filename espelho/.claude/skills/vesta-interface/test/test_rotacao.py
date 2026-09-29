"""Etapa 9: ferramentas/rotacao.py registra macroestrutura, menu e rodapé e recusa repetição em Persuadir e Experiência."""
import ast
import json
import os
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROTACAO = os.path.join(RAIZ, 'ferramentas', 'rotacao.py')
LIMITE = 20


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.projeto = self._tmp.name  # sem docs/design/: o script cria
        self.arquivo = os.path.join(self.projeto, 'docs', 'design', 'rotacao.json')

    def tearDown(self):
        self._tmp.cleanup()

    def rodar(self, *args):
        return subprocess.run([sys.executable, ROTACAO, *args, '--projeto', self.projeto],
                              capture_output=True, text=True, encoding='utf-8', cwd=self.projeto, timeout=60)

    def registrar(self, tela, tipo, macro=None, menu=None, rodape=None):
        # ids próprios da tela por padrão, para só repetir o que o teste pede
        return self.rodar('registrar', '--tela', tela, '--tipo', tipo,
                          '--macro', macro or f'macro-{tela}', '--menu', menu or f'menu-{tela}',
                          '--rodape', rodape or f'rodape-{tela}')

    def ok(self, *args, **kw):
        r = self.registrar(*args, **kw)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r

    def entradas(self):
        with open(self.arquivo, encoding='utf-8') as f:
            return json.load(f)

    def telas(self):
        return [next(v for v in e.values() if isinstance(v, str) and v.startswith('tela-'))
                for e in self.entradas()]


class TestRegistrar(Base):
    def test_primeira_entrada_grava(self):
        self.ok('tela-inicio', 'Persuadir', macro='bento', menu='n5', rodape='ft2')
        dados = self.entradas()
        self.assertIsInstance(dados, list)
        self.assertEqual(len(dados), 1)
        valores = set(dados[0].values())
        self.assertLessEqual({'tela-inicio', 'Persuadir', 'bento', 'n5', 'ft2'}, valores)

    def test_pasta_sem_docs_design_e_criada(self):
        self.assertFalse(os.path.exists(os.path.join(self.projeto, 'docs')))
        self.ok('tela-inicio', 'Operar')
        self.assertTrue(os.path.isfile(self.arquivo))

    def test_mais_novo_primeiro(self):
        self.ok('tela-a', 'Operar')
        self.ok('tela-b', 'Persuadir')
        self.ok('tela-c', 'Ler')
        self.assertEqual(self.telas(), ['tela-c', 'tela-b', 'tela-a'])

    def test_nunca_passa_de_20(self):
        for i in range(LIMITE + 3):
            self.ok(f'tela-{i:02d}', 'Operar')
        telas = self.telas()
        self.assertEqual(len(telas), LIMITE)
        self.assertEqual(telas[0], f'tela-{LIMITE + 2:02d}')
        self.assertNotIn('tela-00', telas)  # sai a mais antiga

    def test_tipo_fora_dos_quatro_recusa_sem_gravar(self):
        self.ok('tela-a', 'Operar')
        r = self.registrar('tela-x', 'Landing')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.telas(), ['tela-a'])


class TestRecusa(Base):
    def test_repetir_menu_da_penultima_persuadir_recusa(self):
        self.ok('tela-a', 'Persuadir', menu='n5')
        self.ok('tela-b', 'Persuadir', menu='n11')
        r = self.registrar('tela-c', 'Persuadir', menu='n5')
        self.assertEqual(r.returncode, 1)
        saida = (r.stdout + r.stderr).lower()
        self.assertIn('menu', saida)
        self.assertIn('n5', saida)
        self.assertEqual(self.telas(), ['tela-b', 'tela-a'])  # recusa não grava

    def test_repetir_macro_recusa(self):
        self.ok('tela-a', 'Persuadir', macro='bento')
        r = self.registrar('tela-b', 'Persuadir', macro='bento')
        self.assertEqual(r.returncode, 1)
        self.assertIn('bento', r.stdout + r.stderr)

    def test_repetir_rodape_recusa(self):
        self.ok('tela-a', 'Persuadir', rodape='ft5')
        r = self.registrar('tela-b', 'Persuadir', rodape='ft5')
        self.assertEqual(r.returncode, 1)
        self.assertIn('ft5', r.stdout + r.stderr)

    def test_experiencia_e_persuadir_contam_juntas(self):
        self.ok('tela-a', 'Experiência', menu='n5')
        self.assertEqual(self.registrar('tela-b', 'Persuadir', menu='n5').returncode, 1)
        self.ok('tela-c', 'Persuadir', rodape='ft7')
        self.assertEqual(self.registrar('tela-d', 'Experiência', rodape='ft7').returncode, 1)

    def test_a_quarta_mais_antiga_nao_conta(self):
        for tela, menu in [('tela-a', 'n1'), ('tela-b', 'n2'), ('tela-c', 'n3'), ('tela-d', 'n4')]:
            self.ok(tela, 'Persuadir', menu=menu)
        self.assertEqual(self.registrar('tela-e', 'Persuadir', menu='n2').returncode, 1)  # terceira conta
        self.ok('tela-f', 'Persuadir', menu='n1')

    def test_telas_de_app_nao_empurram_a_janela(self):
        # as 3 últimas são de Persuadir/Experiência, não as 3 últimas do arquivo
        self.ok('tela-a', 'Persuadir', menu='n5')
        for tela in ('tela-o1', 'tela-o2', 'tela-o3'):
            self.ok(tela, 'Operar')
        self.assertEqual(self.registrar('tela-b', 'Persuadir', menu='n5').returncode, 1)


class TestApp(Base):
    def test_repetir_numa_tela_de_operar_grava(self):
        self.ok('tela-a', 'Persuadir', macro='workbench', menu='n3', rodape='ft2')
        self.ok('tela-b', 'Operar', macro='workbench', menu='n3', rodape='ft2')
        self.ok('tela-c', 'Operar', macro='workbench', menu='n3', rodape='ft2')
        self.assertEqual(self.telas(), ['tela-c', 'tela-b', 'tela-a'])

    def test_repetir_numa_tela_de_ler_grava(self):
        self.ok('tela-a', 'Experiência', menu='n6')
        self.ok('tela-b', 'Ler', menu='n6')

    def test_menu_de_app_nao_bloqueia_pagina_de_persuadir(self):
        self.ok('tela-a', 'Operar', menu='n3')
        self.ok('tela-b', 'Persuadir', menu='n3')


class TestUltimas(Base):
    def test_sem_arquivo_nao_falha(self):
        r = self.rodar('ultimas')
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_imprime_as_3_ultimas_de_persuadir_e_experiencia(self):
        self.ok('tela-velha', 'Persuadir')
        self.ok('tela-exp', 'Experiência')
        self.ok('tela-painel', 'Operar')
        self.ok('tela-meio', 'Persuadir')
        self.ok('tela-doc', 'Ler')
        self.ok('tela-nova', 'Persuadir')
        r = self.rodar('ultimas')
        self.assertEqual(r.returncode, 0, r.stderr)
        saida = r.stdout
        for tela in ('tela-nova', 'tela-meio', 'tela-exp'):
            self.assertIn(tela, saida)
            for campo in ('macro', 'menu', 'rodape'):
                self.assertIn(f'{campo}-{tela}', saida)
        for tela in ('tela-velha', 'tela-painel', 'tela-doc'):
            self.assertNotIn(tela, saida)
        pos = [saida.index(t) for t in ('tela-nova', 'tela-meio', 'tela-exp')]
        self.assertEqual(pos, sorted(pos))  # mais nova primeiro


class TestStdlib(unittest.TestCase):
    def test_nenhum_import_fora_da_stdlib(self):
        with open(ROTACAO, encoding='utf-8') as f:
            arvore = ast.parse(f.read(), ROTACAO)
        for no in ast.walk(arvore):
            nomes = [a.name for a in no.names] if isinstance(no, ast.Import) else \
                [no.module or ''] if isinstance(no, ast.ImportFrom) else []
            for nome in nomes:
                self.assertIn(nome.split('.')[0], sys.stdlib_module_names, nome)


if __name__ == '__main__':
    unittest.main()
