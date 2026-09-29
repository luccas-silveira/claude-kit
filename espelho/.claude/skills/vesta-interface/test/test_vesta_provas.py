"""Etapa 20: contrato com a Vesta; ela recusa tela sem as provas da verificação com os nomes daqui."""
import json
import os
import re
import subprocess
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VESTA = os.path.expanduser('~/Code/vesta')
SCRIPT = os.path.join(VESTA, 'skill', 'scripts', 'vesta.py')
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_') and k != 'CLAUDE_PROJECT_DIR'}
TESTE = 'test -f ok || { echo "FAIL test_um"; exit 1; }'

PASTA = 'docs/vesta/mockups/2026-09-28-x'
MOCK = PASTA + '/index.html'
# os nomes que a etapa 19 fixou em referencias/verificacao.md e no passo 3 do SKILL.md
PROVAS = ('relatorio.md', 'r<N>-375.png', 'r<N>-1440.png', 'r<N>-detector-375.json',
          'r<N>-detector-1440.json')
DIRECOES = ('<tela>-a.html', '<tela>-b.html', '<tela>-a-375.png', '<tela>-a-1440.png',
            '<tela>-b-375.png', '<tela>-b-1440.png')


def ler(base, rel):
    with open(os.path.join(base, rel)) as f:
        return f.read()


def paragrafos(texto):
    return [p for p in re.split(r'\n\s*\n', texto) if p.strip()]


def provas(pasta):
    return {f'{pasta}/relatorio.md': 'rodada 1', f'{pasta}/r1-375.png': 'png',
            f'{pasta}/r1-1440.png': 'png', f'{pasta}/r1-detector-375.json': '[]',
            f'{pasta}/r1-detector-1440.json': '[]'}


def direcoes():
    return {f'docs/design/mockups/painel-{n}': 'x' for n in
            ('a.html', 'b.html', 'a-375.png', 'a-1440.png', 'b-375.png', 'b-1440.png')}


@unittest.skipUnless(os.path.isdir(VESTA), '~/Code/vesta ausente')
class TestVestaRecusaSemProvas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = os.path.realpath(self.tmp.name)
        for args in (['init', '-q'], ['config', 'user.email', 't@t'], ['config', 'user.name', 't'],
                     ['commit', '-q', '--allow-empty', '-m', 'raiz']):
            self.git(*args)

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        subprocess.run(['git', *args], cwd=self.r, env=ENV, check=True, capture_output=True)

    def vesta(self, *args, entrada=None):
        return subprocess.run(['python3', SCRIPT, *args], cwd=self.r, env=ENV, input=entrada,
                              capture_output=True, text=True)

    def commitar(self, arquivos):
        for rel, conteudo in arquivos.items():
            caminho = os.path.join(self.r, rel)
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            with open(caminho, 'w') as f:
                f.write(conteudo)
        self.git('add', '-A')
        self.git('commit', '-q', '-m', 'arquivos')

    def criar(self):
        d = {'plano': 'plano.md', 'teste': TESTE, 'tela': [], 'mockup': MOCK,
             'etapas': [{'id': '1', 'titulo': 'tela', 'tela': True}]}
        p = self.vesta('criar', entrada=json.dumps(d))
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_iniciar_recusa_mockup_sem_relatorio(self):
        arquivos = {MOCK: '<p>', **provas(PASTA), **direcoes()}
        del arquivos[PASTA + '/relatorio.md']
        self.commitar(arquivos)
        self.criar()
        p = self.vesta('iniciar')
        self.assertEqual(p.returncode, 1, p.stdout)
        self.assertIn('relatorio.md', p.stderr)

    def test_concluir_recusa_etapa_de_tela_sem_as_provas_dela(self):
        self.commitar({MOCK: '<p>', **provas(PASTA), **direcoes()})
        self.criar()
        self.assertEqual(self.vesta('iniciar').returncode, 0)
        self.commitar({'test_um': ''})
        self.assertEqual(self.vesta('prova', 'vermelho', '1').returncode, 0)
        self.commitar({'ok': ''})
        self.assertEqual(self.vesta('prova', 'teste', '1').returncode, 0)
        p = self.vesta('concluir', '1')
        self.assertEqual(p.returncode, 1, p.stdout)
        self.assertIn('etapa-1', p.stderr)
        self.commitar(provas(PASTA + '/etapa-1'))
        self.assertEqual(self.vesta('prova', 'teste', '1').returncode, 0)
        p = self.vesta('concluir', '1')
        self.assertEqual(p.returncode, 0, p.stderr)


@unittest.skipUnless(os.path.isdir(VESTA), '~/Code/vesta ausente')
class TestTextoDaVesta(unittest.TestCase):
    def test_nomes_existem_aqui(self):
        # se a vesta-interface renomear uma prova, este contrato quebra antes da Vesta
        aqui = ler(RAIZ, 'referencias/verificacao.md') + ler(RAIZ, 'SKILL.md')
        faltam = [n for n in PROVAS + DIRECOES if n not in aqui]
        self.assertEqual(faltam, [], 'a vesta-interface não usa mais estes nomes')

    def test_mockup_md_usa_os_mesmos_nomes(self):
        mockup = ler(VESTA, 'skill/mockup.md')
        faltam = [n for n in PROVAS + DIRECOES if n not in mockup]
        self.assertEqual(faltam, [], 'skill/mockup.md da Vesta não usa estes nomes da vesta-interface')

    def test_mockup_md_diz_que_iniciar_recusa(self):
        ps = [p for p in paragrafos(ler(VESTA, 'skill/mockup.md'))
              if 'iniciar' in p and re.search(r'recus', p) and 'relatorio.md' in p]
        self.assertTrue(ps, 'skill/mockup.md não diz que iniciar recusa sem as provas')

    def test_plano_md_mostra_tela_existente_no_criar(self):
        blocos = re.findall(r'```bash\n(.*?)```', ler(VESTA, 'skill/plano.md'), re.S)
        self.assertTrue(any('vesta.py criar' in b and '"tela_existente"' in b for b in blocos),
                        'skill/plano.md não mostra tela_existente no criar')

    def test_execucao_md_roda_o_passo_5_antes_de_concluir(self):
        ordem = [r'verde', r'passo 5', r'vesta-interface', r'servid', r'etapa-<(id|n)>/',
                 r'commit', r'prova teste', r'concluir']
        ps = [p.lower() for p in paragrafos(ler(VESTA, 'skill/execucao.md'))]
        ok = []
        for p in ps:
            if not re.search(r'etapa-<(id|n)>/', p) or 'tela' not in p:
                continue
            pos, seguiu = 0, True
            for t in ordem:
                m = re.compile(t).search(p, pos)
                if not m:
                    seguiu = False
                    break
                pos = m.end()
            ok.append(seguiu)
        self.assertTrue(any(ok), 'skill/execucao.md não diz, em ordem: depois do verde de etapa com '
                                 'tela, passo 5 da vesta-interface na tela servida, provas em '
                                 'etapa-<id>/, commit, prova teste de novo, concluir')


if __name__ == '__main__':
    unittest.main()
