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

    def test_mcp_de_npm_tem_quem_instale(self):
        """MCP que roda de uma pasta npm local precisa de um programa que instale essa pasta."""
        with open(os.path.join(ESPELHO, 'mcp.json'), encoding='utf-8') as f:
            servidores = json.load(f)['global']
        instalar = ' '.join(p['instalar'] for p in manifesto()['programas']).replace(
            '$HOME', '__HOME__')
        orfaos = [n for n, s in servidores.items() if '/node_modules/.bin/' in s.get('command', '')
                  and s['command'].split('/node_modules/')[0] not in instalar]
        self.assertEqual(orfaos, [])

    def test_app_detectado_sem_depender_do_brew(self):
        """App instalado fora do Homebrew conta como instalado; senão o brew tenta por cima."""
        with open(os.path.join(KIT, 'fontes.json'), encoding='utf-8') as f:
            comandos = {p['nome']: p['versao'] for p in json.load(f)['programas']}
        versoes = {p['nome']: p['versao'] for p in manifesto()['programas']}
        for nome in ['supacode', 'knobler']:
            self.assertNotIn('brew list', comandos[nome], nome)
            self.assertIsNotNone(versoes[nome], nome)

    def test_vesta_e_link_para_o_clone(self):
        """Link, não cópia: é o clone que o `vesta.py atualizar` avança."""
        link = os.path.join(ESPELHO, '.claude/skills/vesta')
        self.assertTrue(os.path.islink(link), 'skills/vesta virou cópia')
        self.assertEqual(os.readlink(link), '__HOME__/Code/vesta/skill')
        remotes = [r['remote'] for r in manifesto()['repositorios']]
        self.assertTrue(any('luccas-silveira/vesta' in r for r in remotes), remotes)

    def test_ponte_do_whatsapp_vira_servico(self):
        depois = {r['caminho'].rsplit('/', 1)[-1]: r['depois'] for r in manifesto()['repositorios']}
        self.assertIn('./servico.sh', depois['whatsapp-mcp'])

    def test_manifesto_sem_termo_bloqueado(self):
        self.assertTrue(os.path.isfile(MANIFESTO), 'manifesto.json ausente')
        if not os.path.isfile(BLOQUEIO):
            self.skipTest('sem ' + BLOQUEIO)
        with open(BLOQUEIO, encoding='utf-8') as f:
            termos = [t.strip().lower() for t in f if t.strip()]
        with open(MANIFESTO, encoding='utf-8') as f:
            texto = f.read().lower()
        self.assertEqual([t for t in termos if t in texto], [])

    def test_kit_sem_caminho_da_zoi(self):
        """O kit não carrega a pasta de trabalho da ZOI: nem em arquivo, nem no manifesto, nem em link."""
        termos = [b'Projetos_ZOI', b'2. ZOI']
        achados = []
        for d, nomes, arqs in os.walk(ESPELHO):
            for n in nomes + arqs:
                p = os.path.join(d, n)
                rel = os.path.relpath(p, ESPELHO)
                if os.path.islink(p):
                    if 'ZOI' in os.readlink(p):
                        achados.append(rel + ' -> ' + os.readlink(p))
                    continue
                if os.path.isfile(p):
                    with open(p, 'rb') as f:
                        dados = f.read()
                    if any(t in dados for t in termos):
                        achados.append(rel)
        with open(MANIFESTO, 'rb') as f:
            if any(t in f.read() for t in termos):
                achados.append('manifesto.json')
        self.assertEqual(achados, [])

    def test_destino_dos_repositorios(self):
        repos = {r['caminho']: r['remote'] for r in manifesto()['repositorios']}
        self.assertEqual(repos.get('__HOME__/Code/automaster'),
                         'https://github.com/zoi-tech/automaster.git')
        self.assertEqual(repos.get('__HOME__/Code/ghl-docs'),
                         'https://github.com/luccas-silveira/ghl-docs.git')

    def test_marketplace_zoi_aponta_para_o_clone_do_automaster(self):
        mkt = json.loads(ler('.claude/settings.json'))['extraKnownMarketplaces']['zoi']
        caminhos = [r['caminho'] for r in manifesto()['repositorios']
                    if r['remote'].rstrip('/').removesuffix('.git').endswith('/automaster')]
        self.assertEqual(caminhos, ['__HOME__/Code/automaster'])
        self.assertEqual(mkt['source']['path'], caminhos[0])

    def test_skill_ghl_api_docs_usa_a_pasta_ao_lado(self):
        link = os.path.join(ESPELHO, '.claude/skills/ghl-api-docs/docs')
        self.assertTrue(os.path.islink(link), 'skills/ghl-api-docs/docs não é link')
        self.assertEqual(os.readlink(link), '__HOME__/Code/ghl-docs')
        self.assertNotIn('Documents/ghl-docs', ler('.claude/skills/ghl-api-docs/SKILL.md'))


if __name__ == '__main__':
    unittest.main()
