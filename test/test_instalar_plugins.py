import json
import os

from test_instalar_arquivos import InstalarCaso

OFICIAL = 'claude-plugins-official'


class PluginsCaso(InstalarCaso):
    def setUp(self):
        super().setUp()
        self.escreve('manifesto.json', json.dumps({
            'plugins': [{'id': 'bom@zoi', 'versao': '1.0', 'ligado': True}],
            'marketplaces': [{'nome': 'zoi', 'fonte': 'github'},
                             {'nome': OFICIAL, 'fonte': 'github'}],
            'programas': [], 'repositorios': [], 'credenciais': [],
        }), raiz=self.kit)
        self.resposta('claude', 'plugin list --json', json.dumps([
            {'id': 'bom@zoi', 'version': '1.0', 'scope': 'user', 'enabled': True},
            {'id': 'velho@zoi', 'version': '0.1', 'scope': 'user', 'enabled': True},
            {'id': 'outro@caveman', 'version': '2', 'scope': 'user', 'enabled': False},
        ]))
        self.resposta('claude', 'plugin marketplace list --json', json.dumps([
            {'name': 'zoi', 'source': 'github'},
            {'name': OFICIAL, 'source': 'github'},
            {'name': 'caveman', 'source': 'github'},
        ]))

    def claude(self):
        return [c for c in self.chamadas() if c.startswith('claude ')]


class TestPlugins(PluginsCaso):
    def test_adiciona_marketplace_oficial(self):
        self.instala()
        self.assertIn('claude plugin marketplace add anthropics/claude-plugins-official',
                      self.claude())

    def test_desinstala_plugin_fora_do_manifesto(self):
        self.instala()
        c = self.claude()
        self.assertIn('claude plugin uninstall velho@zoi', c)
        self.assertIn('claude plugin uninstall outro@caveman', c)

    def test_nao_desinstala_plugin_do_manifesto(self):
        self.instala()
        self.assertFalse([c for c in self.claude() if 'uninstall' in c and 'bom@zoi' in c])

    def test_remove_marketplace_fora_do_manifesto(self):
        self.instala()
        c = self.claude()
        self.assertIn('claude plugin marketplace remove caveman', c)
        self.assertFalse([x for x in c if 'marketplace remove' in x and x.split()[-1] != 'caveman'],
                         c)

    def test_nao_remove_oficial_mesmo_fora_do_manifesto(self):
        self.escreve('manifesto.json', json.dumps({
            'plugins': [{'id': 'bom@zoi', 'versao': '1.0', 'ligado': True}],
            'marketplaces': [{'nome': 'zoi', 'fonte': 'github'}],
            'programas': [], 'repositorios': [], 'credenciais': [],
        }), raiz=self.kit)
        self.instala()
        c = self.claude()
        self.assertFalse([x for x in c if 'marketplace remove' in x and OFICIAL in x], c)
        self.assertIn('claude plugin marketplace remove caveman', c)

    def test_plugin_do_manifesto_nao_e_instalado(self):
        self.instala()
        self.assertFalse([c for c in self.claude()
                          if c.startswith('claude plugin install')
                          or c.startswith('claude plugin enable')
                          or ('marketplace add' in c and 'anthropics/' not in c)], self.claude())

    def test_relatorio_diz_que_plugins_instalam_ao_abrir(self):
        saida = self.instala()
        self.assertRegex(saida, r'(?i)abrir o claude code')

    def test_nao_copia_registros_de_plugin(self):
        self.escreve('.claude/plugins/installed_plugins.json', '{"x": 1}', raiz=self.esp)
        self.escreve('.claude/plugins/known_marketplaces.json', '{"y": 1}', raiz=self.esp)
        self.escreve('.claude/plugins/installed_plugins.json', 'LOCAL')
        self.instala()
        self.assertEqual(self.le(self.arq('.claude/plugins/installed_plugins.json')), 'LOCAL')
        self.assertFalse(os.path.exists(self.arq('.claude/plugins/known_marketplaces.json')))


class TestFalhas(PluginsCaso):
    def test_falha_nao_para_e_vai_para_lista(self):
        self.resposta('claude', 'plugin uninstall velho@zoi', 'erro', codigo=1)
        self.resposta('claude', 'plugin marketplace add anthropics/claude-plugins-official',
                      'erro', codigo=1)
        codigo, saida = self.roda('instalar', '--kit', self.kit)
        self.assertEqual(codigo, 0, saida)
        c = self.claude()
        self.assertIn('claude plugin uninstall outro@caveman', c)
        self.assertIn('claude plugin marketplace remove caveman', c)
        final = saida[saida.lower().find('falha'):]
        self.assertIn('velho@zoi', final, saida)
        self.assertIn('anthropics/claude-plugins-official', final, saida)
