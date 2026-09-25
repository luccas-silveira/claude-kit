import json
import os

from base import STUB
from test_instalar_arquivos import InstalarCaso

URL1 = 'https://github.com/zoi/r1.git'
URL2 = 'https://github.com/zoi/r2.git'
# git que, no clone bem-sucedido, cria a pasta de destino (como o git de verdade)
GIT = STUB.replace('exit 0\n', '[ "$1" = clone ] && mkdir -p "$3"\nexit 0\n')


class RestoCaso(InstalarCaso):
    def setUp(self):
        super().setUp()
        for n in ('brew', 'npm', 'uv', 'curl', 'sh', 'go', 'docker', 'jq', 'gh'):
            self.stub(n)
        with open(os.path.join(self.stubs, 'git'), 'w') as f:
            f.write(GIT)
        os.chmod(os.path.join(self.stubs, 'git'), 0o755)
        self.resposta('jq', '--version', 'jq-1.6')           # instalado, versão diferente
        self.resposta('gh', '--version', 'gh 2.0')           # instalado, mesma versão
        # `sumido` não tem stub: `sumido --version` falha -> ausente
        self.fontes({'programas': [
            {'nome': 'jq', 'versao': 'jq --version', 'instalar': 'brew install jq'},
            {'nome': 'gh', 'versao': 'gh --version', 'instalar': 'brew install gh'},
            {'nome': 'sumido', 'versao': 'sumido --version', 'instalar': 'brew install sumido'},
        ]})
        os.makedirs(self.arq('Code/presente'))
        self.manifesto({})

    def manifesto(self, extra):
        m = {
            'plugins': [], 'marketplaces': [],
            'programas': [
                {'nome': 'jq', 'versao': 'jq-1.7.1', 'instalar': 'brew install jq'},
                {'nome': 'gh', 'versao': 'gh 2.0', 'instalar': 'brew install gh'},
                {'nome': 'sumido', 'versao': 'sumido 9', 'instalar': 'brew install sumido'},
            ],
            'repositorios': [
                {'caminho': '__HOME__/Code/r1', 'remote': URL1, 'depois': 'touch depois.ok'},
                {'caminho': '__HOME__/Code/presente', 'remote': URL2,
                 'depois': 'touch depois.ok'},
            ],
            'credenciais': ['~/.config/deja/token', '__HOME__/.ssh/id_falta'],
        }
        m.update(extra)
        self.escreve('manifesto.json', json.dumps(m), raiz=self.kit)



class TestRepositorios(RestoCaso):
    def test_clona_repo_ausente_no_home_local(self):
        self.instala()
        self.assertIn('git clone %s %s' % (URL1, self.arq('Code/r1')), self.chamadas())

    def test_depois_roda_dentro_do_repo_clonado(self):
        self.instala()
        self.assertTrue(os.path.exists(self.arq('Code/r1/depois.ok')))
        self.assertFalse(os.path.exists(self.arq('depois.ok')))

    def test_repo_presente_nao_clona_nem_roda_depois(self):
        self.instala()
        self.assertIn('git clone %s %s' % (URL1, self.arq('Code/r1')), self.chamadas())
        self.assertFalse([c for c in self.chamadas() if URL2 in c], self.chamadas())
        self.assertFalse(os.path.exists(self.arq('Code/presente/depois.ok')))


class TestProgramas(RestoCaso):
    def test_ausente_roda_instalar(self):
        self.instala()
        self.assertIn('brew install sumido', self.chamadas())

    def test_versao_diferente_nao_reinstala(self):
        self.instala()
        c = self.chamadas()
        self.assertIn('jq --version', c)
        self.assertNotIn('brew install jq', c)
        self.assertNotIn('brew install gh', c)

    def test_versao_diferente_no_relatorio(self):
        saida = self.instala()
        self.assertRegex(saida, r'(?im)vers[ãa]o diferente.*$')
        self.assertRegex(saida, r'jq.*jq-1\.6.*→.*jq-1\.7\.1')
        self.assertNotRegex(saida, r'gh.*gh 2\.0.*→')


class TestFalhas(RestoCaso):
    def setUp(self):
        super().setUp()
        self.resposta('brew', 'install sumido', 'erro', codigo=1)
        self.resposta('git', 'clone %s %s' % (URL1, self.arq('Code/r1')), 'erro', codigo=1)
        os.rmdir(self.arq('Code/presente'))
        self.resposta('git', 'clone %s %s' % (URL2, self.arq('Code/presente')))

    def test_falhas_nao_param_e_saida_zero(self):
        codigo, saida = self.roda('instalar', '--kit', self.kit)
        self.assertEqual(codigo, 0, saida)
        self.assertIn('git clone %s %s' % (URL2, self.arq('Code/presente')), self.chamadas())
        self.assertTrue(os.path.exists(self.arq('Code/presente/depois.ok')))
        final = saida[saida.lower().rfind('falha em'):]
        self.assertIn('sumido', final, saida)
        self.assertIn('Code/r1', final, saida)

    def test_clone_que_falha_nao_roda_depois(self):
        self.instala()
        self.assertIn('git clone %s %s' % (URL1, self.arq('Code/r1')), self.chamadas())
        self.assertFalse(os.path.exists(self.arq('Code/r1/depois.ok')))


class TestRelatorio(RestoCaso):
    def test_credencial_ausente_so_o_caminho(self):
        saida = self.instala()
        self.assertIn('.ssh/id_falta', saida)
        self.assertNotIn('.config/deja/token', saida)
        self.assertNotIn('SEGREDO', saida)

    def test_lembretes_fixos(self):
        saida = self.instala()
        self.assertRegex(saida, r'(?i)whatsapp')
        self.assertRegex(saida, r'(?i)\bQR\b')
        self.assertRegex(saida, r'(?i)ponte')
        self.assertRegex(saida, r'(?i)abrir o claude code')

    def test_ordem_do_relatorio(self):
        self.resposta('brew', 'install sumido', 'erro', codigo=1)
        saida = self.instala()
        low = saida.lower()
        pos = [low.rfind('falha em'), low.rfind('diferente'), low.rfind('.ssh/id_falta'),
               low.rfind('whatsapp'), low.rfind('abrir o claude code'), low.rfind('snapshot:')]
        self.assertTrue(all(p >= 0 for p in pos), (pos, saida))
        self.assertEqual(pos, sorted(pos), saida)
        self.assertTrue(saida.rstrip().splitlines()[-1].startswith('snapshot: '), saida)
