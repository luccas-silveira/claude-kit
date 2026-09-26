"""Falhas relatadas numa instalação real (26/09/2026)."""
import json
import os

from test_instalar_arquivos import InstalarCaso
from test_sync import KitCaso


class TestSyncFeedback(KitCaso):
    def test_modo_executavel_preservado(self):
        self.escreve('.claude/hooks/h.sh', '#!/bin/sh\n')
        os.chmod(os.path.join(self.home, '.claude/hooks/h.sh'), 0o755)
        self.roda('sync', '--kit', self.kit)
        self.assertTrue(os.access(os.path.join(self.esp, '.claude/hooks/h.sh'), os.X_OK))

    def test_hook_de_pasta_excluida_sai_do_settings(self):
        fica = {'hooks': [{'type': 'command', 'command': 'fica.sh'}]}
        sai = {'hooks': [{'type': 'command',
                          'command': self.home + '/.claude/plugins/local/pipeline-reuniao/s.sh'}]}
        self.escreve('.claude/settings.json', json.dumps({'hooks': {'Stop': [fica, sai]}}))
        self.roda('sync', '--kit', self.kit)
        with open(os.path.join(self.esp, '.claude/settings.json')) as f:
            self.assertEqual(json.load(f)['hooks'], {'Stop': [fica]})


class TestInstalarFeedback(InstalarCaso):
    def test_modo_executavel_no_home(self):
        self.escreve('.claude/hooks/h.sh', '#!/bin/sh\n', raiz=self.esp)
        os.chmod(os.path.join(self.esp, '.claude/hooks/h.sh'), 0o755)
        self.instala()
        self.assertTrue(os.access(self.arq('.claude/hooks/h.sh'), os.X_OK))

    def test_cria_pasta_de_metricas(self):
        self.instala()
        self.assertTrue(os.path.isdir(self.arq('.claude/metrics')))

    def test_desliga_plugin_de_marketplace_local_ausente(self):
        self.escreve('.claude/settings.json', json.dumps(
            {'enabledPlugins': {'automaster@zoi': True, 'outro@x': True}}), raiz=self.esp)
        self.escreve('manifesto.json', json.dumps({
            'plugins': [], 'programas': [], 'repositorios': [], 'credenciais': [],
            'marketplaces': [{'nome': 'zoi', 'fonte': {'source': 'directory',
                                                        'path': '__HOME__/nao/existe'}}],
        }), raiz=self.kit)
        self.instala()
        with open(self.arq('.claude/settings.json')) as f:
            self.assertEqual(json.load(f)['enabledPlugins'],
                             {'automaster@zoi': False, 'outro@x': True})
