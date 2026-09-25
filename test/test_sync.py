import json
import os
import subprocess

from base import Caso

GERENCIADOS = [
    '.claude/settings.json', '.claude/settings.local.json', '.claude/keybindings.json',
    '.claude/statusline.sh', '.claude/skill-stats.py',
    '.claude/skills/a/SKILL.md', '.claude/skills-disabled/b/SKILL.md',
    '.claude/agents/x.md', '.claude/commands/c.md', '.claude/output-styles/Seco.md',
    '.claude/hooks/h.sh', '.claude/helpers/u.py', '.claude/plugins/local/p/plugin.json',
    '.claude/plugins/config.json', '.claude/plugins/blocklist.json', '.mcp.json',
    '.config/deja/config.toml', '.config/caveman/c.json', '.config/yt-dlp/config',
]
FORA = [
    '.claude/CLAUDE.md', '.claude/memory/general.md', '.claude/skills/synced/s/SKILL.md',
    '.claude/skills/a/__pycache__/m.pyc', '.claude/skills/a/.DS_Store',
    '.claude/hooks/node_modules/lib/index.js', '.claude/plugins/local/p/.git/HEAD',
    '.config/deja/token', '.config/watch/.env',
]


class TestSync(Caso):
    def setUp(self):
        super().setUp()
        self.kit = os.path.join(os.path.dirname(self.home), 'kit')
        self.esp = os.path.join(self.kit, 'espelho')
        os.makedirs(self.kit)
        self.fontes({})

    # --- helpers ---
    def escreve(self, rel, conteudo='x', raiz=None):
        p = os.path.join(raiz or self.home, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb' if isinstance(conteudo, bytes) else 'w') as f:
            f.write(conteudo)
        return p

    def fontes(self, dados):
        base = {'programas': [], 'repositorios': [],
                'credenciais': ['~/.config/deja/token', '~/.config/watch/.env']}
        base.update(dados)
        self.escreve('fontes.json', json.dumps(base), raiz=self.kit)

    def repo(self, rel, remote=None):
        p = os.path.join(self.home, rel)
        os.makedirs(p)
        subprocess.run(['/usr/bin/git', 'init', '-q', p], check=True, env=self.env)
        if remote:
            subprocess.run(['/usr/bin/git', '-C', p, 'remote', 'add', 'origin', remote],
                           check=True, env=self.env)
        return p

    def sync(self):
        codigo, saida = self.roda('sync', '--kit', self.kit)
        self.assertEqual(codigo, 0, saida)
        return saida

    def no_kit(self, rel):
        return os.path.join(self.esp, rel)

    def le(self, caminho):
        with open(caminho) as f:
            return f.read()

    def manifesto(self):
        with open(os.path.join(self.kit, 'manifesto.json')) as f:
            return json.load(f)

    def foto(self):
        r = {}
        for d, subs, arqs in os.walk(self.kit):
            for n in subs + arqs:
                p = os.path.join(d, n)
                if os.path.islink(p):
                    r[p] = 'link:' + os.readlink(p)
                elif os.path.isfile(p):
                    with open(p, 'rb') as f:
                        r[p] = f.read()
        return r

    # --- testes ---
    def test_copia_gerenciados_no_mesmo_caminho(self):
        for rel in GERENCIADOS:
            self.escreve(rel, 'conteudo de ' + rel)
        self.sync()
        for rel in GERENCIADOS:
            self.assertEqual(self.le(self.no_kit(rel)), 'conteudo de ' + rel, rel)

    def test_keybindings_ausente_nao_quebra(self):
        self.escreve('.claude/settings.json', '{}')
        self.sync()
        self.assertTrue(os.path.exists(self.no_kit('.claude/settings.json')))
        self.assertFalse(os.path.exists(self.no_kit('.claude/keybindings.json')))

    def test_nao_gerenciado_nao_entra(self):
        self.escreve('.claude/settings.json', '{}')
        self.escreve('.claude/history.jsonl', 'h')
        self.escreve('.config/outro/x', 'o')
        self.sync()
        self.assertFalse(os.path.exists(self.no_kit('.claude/history.jsonl')))
        self.assertFalse(os.path.exists(self.no_kit('.config/outro')))

    def test_exclusoes_e_credenciais_nunca_entram(self):
        for rel in GERENCIADOS + FORA:
            self.escreve(rel, 'SEGREDO' if rel in FORA else 'ok')
        self.sync()
        for rel in FORA:
            self.assertFalse(os.path.lexists(self.no_kit(rel)), rel)
        for rel, v in self.foto().items():
            if isinstance(v, bytes):
                self.assertNotIn(b'SEGREDO', v, rel)
        self.assertTrue(os.path.exists(self.no_kit('.claude/skills/a/SKILL.md')))

    def test_sobra_some_do_espelho(self):
        self.escreve('.claude/skills/a/SKILL.md')
        self.escreve('.claude/skills/velha/SKILL.md')
        self.escreve('.claude/agents/y.md')
        self.sync()
        os.remove(os.path.join(self.home, '.claude/skills/velha/SKILL.md'))
        os.rmdir(os.path.join(self.home, '.claude/skills/velha'))
        os.remove(os.path.join(self.home, '.claude/agents/y.md'))
        self.sync()
        self.assertTrue(os.path.exists(self.no_kit('.claude/skills/a/SKILL.md')))
        self.assertFalse(os.path.exists(self.no_kit('.claude/skills/velha')))
        self.assertFalse(os.path.exists(self.no_kit('.claude/agents/y.md')))

    def test_sobra_previa_no_kit_some(self):
        self.escreve('.claude/skills/a/SKILL.md')
        self.escreve('espelho/.claude/skills/fantasma/SKILL.md', raiz=self.kit)
        self.sync()
        self.assertFalse(os.path.exists(self.no_kit('.claude/skills/fantasma')))

    def test_link_para_fora_vira_copia(self):
        alvo = self.escreve('fora/ferramenta/SKILL.md', 'real')
        self.escreve('fora/solto.md', 'arquivo real')
        os.makedirs(os.path.join(self.home, '.claude/skills'))
        os.symlink(os.path.dirname(alvo), os.path.join(self.home, '.claude/skills/ferramenta'))
        os.symlink(os.path.join(self.home, 'fora/solto.md'),
                   os.path.join(self.home, '.claude/skills/solto.md'))
        self.sync()
        d = self.no_kit('.claude/skills/ferramenta')
        self.assertFalse(os.path.islink(d))
        self.assertEqual(self.le(os.path.join(d, 'SKILL.md')), 'real')
        f = self.no_kit('.claude/skills/solto.md')
        self.assertFalse(os.path.islink(f))
        self.assertEqual(self.le(f), 'arquivo real')

    def test_link_para_repositorio_fica_link_com_marcador(self):
        r = self.repo('Code/meurepo', 'git@github.com:eu/meurepo.git')
        self.escreve('Code/meurepo/skills/s/SKILL.md', 'no repo')
        self.fontes({'repositorios': [{'caminho': '~/Code/meurepo', 'depois': ''}]})
        os.makedirs(os.path.join(self.home, '.claude/skills'))
        os.symlink(os.path.join(r, 'skills/s'), os.path.join(self.home, '.claude/skills/s'))
        self.sync()
        l = self.no_kit('.claude/skills/s')
        self.assertTrue(os.path.islink(l))
        self.assertEqual(os.readlink(l), '__HOME__/Code/meurepo/skills/s')

    def test_texto_troca_home_binario_intacto(self):
        self.escreve('.claude/hooks/h.sh', 'cd %s/Code && ls %s/x\n' % (self.home, self.home))
        binario = b'\x89PNG\xff\xfe\x00' + self.home.encode() + b'\x00\xff'
        self.escreve('.claude/skills/a/img.png', binario)
        self.sync()
        self.assertEqual(self.le(self.no_kit('.claude/hooks/h.sh')),
                         'cd __HOME__/Code && ls __HOME__/x\n')
        with open(self.no_kit('.claude/skills/a/img.png'), 'rb') as f:
            self.assertEqual(f.read(), binario)

    def test_mcp_json_so_global_e_por_projeto(self):
        proj = os.path.join(self.home, 'Code/proj')
        self.escreve('.claude.json', json.dumps({
            'oauthAccount': {'email': 'NAOVAZA'},
            'numStartups': 42,
            'mcpServers': {'g': {'command': '%s/bin/g' % self.home}},
            'projects': {
                proj: {'mcpServers': {'p': {'command': 'p'}}, 'history': ['NAOVAZA']},
                os.path.join(self.home, 'semmcp'): {'allowedTools': []},
            },
        }))
        self.sync()
        texto = self.le(self.no_kit('mcp.json'))
        self.assertNotIn('NAOVAZA', texto)
        self.assertNotIn('numStartups', texto)
        self.assertNotIn(self.home, texto)
        mcp = json.loads(texto)
        self.assertEqual(set(mcp), {'global', 'porProjeto'})
        self.assertEqual(mcp['global'], {'g': {'command': '__HOME__/bin/g'}})
        self.assertEqual(mcp['porProjeto'], {'__HOME__/Code/proj': {'p': {'command': 'p'}}})

    def test_manifesto_plugins_e_marketplaces(self):
        self.escreve('.claude/settings.json', json.dumps(
            {'enabledPlugins': {'um@mk': True, 'dois@mk': False}}))
        self.escreve('.claude/plugins/installed_plugins.json', json.dumps({'version': 2, 'plugins': {
            'um@mk': [{'scope': 'user', 'version': '1.2.3', 'installPath': self.home + '/c/um'}],
            'dois@mk': [{'scope': 'user', 'version': '0.9.0', 'installPath': self.home + '/c/dois'}],
        }}))
        self.escreve('.claude/plugins/known_marketplaces.json', json.dumps({
            'mk': {'source': {'source': 'github', 'repo': 'eu/mk'},
                   'installLocation': self.home + '/.claude/plugins/marketplaces/mk'},
        }))
        self.sync()
        m = self.manifesto()
        plugins = {p['id']: p for p in m['plugins']}
        self.assertEqual(set(plugins), {'um@mk', 'dois@mk'})
        self.assertEqual(plugins['um@mk']['versao'], '1.2.3')
        self.assertIs(plugins['um@mk']['ligado'], True)
        self.assertIs(plugins['dois@mk']['ligado'], False)
        self.assertEqual(m['marketplaces'], [{'nome': 'mk', 'fonte': {'source': 'github', 'repo': 'eu/mk'}}])

    def test_manifesto_programas_com_versao_ou_null(self):
        self.stub('jq', 'jq-1.7.1\n')
        self.fontes({'programas': [
            {'nome': 'jq', 'versao': 'jq --version', 'instalar': 'brew install jq'},
            {'nome': 'sumido', 'versao': 'sumido --version', 'instalar': 'brew install sumido'},
        ]})
        self.sync()
        progs = {p['nome']: p for p in self.manifesto()['programas']}
        self.assertIn('1.7.1', progs['jq']['versao'])
        self.assertIsNone(progs['sumido']['versao'])
        self.assertEqual(progs['jq']['instalar'], 'brew install jq')

    def test_manifesto_repositorios_e_credenciais(self):
        self.repo('Code/r1', 'https://github.com/eu/r1.git')
        self.fontes({'repositorios': [{'caminho': '~/Code/r1', 'depois': 'make'}]})
        self.sync()
        m = self.manifesto()
        self.assertEqual(len(m['repositorios']), 1)
        r = m['repositorios'][0]
        self.assertEqual(r['caminho'], '__HOME__/Code/r1')
        self.assertEqual(r['remote'], 'https://github.com/eu/r1.git')
        creds = [c.replace('__HOME__', '~') for c in m['credenciais']]
        self.assertEqual(sorted(creds), ['~/.config/deja/token', '~/.config/watch/.env'])

    def test_credencial_so_caminho_sem_conteudo(self):
        self.escreve('.config/deja/token', 'SEGREDO123')
        self.escreve('.config/deja/config.toml', 'ok')
        self.sync()
        with open(os.path.join(self.kit, 'manifesto.json')) as f:
            self.assertNotIn('SEGREDO123', f.read())

    def test_repositorio_sem_remote_avisa_e_fica_fora(self):
        self.repo('Code/semremote')
        self.repo('Code/comremote', 'git@x:y/z.git')
        self.fontes({'repositorios': [{'caminho': '~/Code/semremote', 'depois': ''},
                                      {'caminho': '~/Code/comremote', 'depois': ''}]})
        saida = self.sync()
        self.assertIn('Code/semremote', saida)
        caminhos = [r['caminho'] for r in self.manifesto()['repositorios']]
        self.assertEqual(caminhos, ['__HOME__/Code/comremote'])

    def test_sync_duas_vezes_nao_muda_kit(self):
        for rel in GERENCIADOS:
            self.escreve(rel, 'c %s %s' % (rel, self.home))
        self.escreve('fora/f.md', 'alvo')
        os.symlink(os.path.join(self.home, 'fora/f.md'), os.path.join(self.home, '.claude/agents/l.md'))
        self.escreve('.claude.json', json.dumps({'mcpServers': {'g': {}}, 'projects': {}}))
        self.stub('jq', 'jq-1.7.1\n')
        self.fontes({'programas': [{'nome': 'jq', 'versao': 'jq --version', 'instalar': ''}]})
        self.sync()
        antes = self.foto()
        self.assertIn(os.path.join(self.kit, 'manifesto.json'), antes)
        self.sync()
        self.assertEqual(self.foto(), antes)
