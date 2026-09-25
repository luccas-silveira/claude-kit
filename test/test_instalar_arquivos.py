import glob
import json
import os
import re
import tarfile

from test_sync import KitCaso


class InstalarCaso(KitCaso):
    """Kit montado à mão (formato do sync) + HOME falso com conteúdo prévio + stub claude."""
    def setUp(self):
        super().setUp()
        self.stub('claude')
        e = lambda rel, c='x': self.escreve(rel, c, raiz=self.esp)
        e('.claude/settings.json', '{"hooks": "__HOME__/.claude/hooks/h.sh"}\n')
        e('.claude/skills/a/SKILL.md', 'skill a em __HOME__/Code\n')
        e('.claude/agents/x.md', 'agente novo\n')
        e('.config/deja/config.toml', 'db = "__HOME__/.deja"\n')
        e('.claude/helpers/bin.dat', b'\x00\xff__HOME__\x00')
        os.makedirs(os.path.join(self.home, 'Code/repo/skills/s'))
        e('.claude/skills/s', '')
        os.remove(self.no_kit('.claude/skills/s'))
        os.symlink('__HOME__/Code/repo/skills/s', self.no_kit('.claude/skills/s'))
        self.escreve('mcp.json', json.dumps({
            'global': {'g': {'command': '__HOME__/bin/g'}},
            'porProjeto': {'__HOME__/Code/proj': {'p': {'command': 'p'}}},
        }), raiz=self.esp)
        self.escreve('manifesto.json', json.dumps({
            'plugins': [], 'marketplaces': [], 'programas': [], 'repositorios': [],
            'credenciais': ['~/.config/deja/token', '~/.config/watch/.env'],
        }), raiz=self.kit)
        # HOME com conteúdo prévio
        self.escreve('.claude/settings.json', 'VELHO')
        self.escreve('.claude/skills/extra/SKILL.md', 'extra')
        self.escreve('.claude/agents/velho.md', 'velho')
        self.escreve('.claude/CLAUDE.md', 'meu claude.md')
        self.escreve('.claude/memory/general.md', 'memoria')
        self.escreve('.claude/skills/synced/s1/SKILL.md', 'synced')
        self.escreve('.claude/projects/p/sessao.jsonl', 'sessao')
        self.escreve('.config/deja/token', 'SEGREDO')
        self.escreve('.config/watch/.env', 'K=V')
        self.proj = os.path.join(self.home, 'Code/proj')
        self.escreve('.claude.json', json.dumps({
            'numStartups': 7, 'oauthAccount': {'email': 'a@b'},
            'mcpServers': {'g': {'command': 'antigo'}, 'extra': {'command': 'e'}},
            'projects': {self.proj: {'mcpServers': {'p': {'command': 'x'}, 'sobra': {}},
                                     'history': ['h1']},
                         '/outro': {'allowedTools': ['t']}},
        }))

    def instala(self):
        codigo, saida = self.roda('instalar', '--kit', self.kit)
        self.assertEqual(codigo, 0, saida)
        return saida

    def arq(self, rel):
        return os.path.join(self.home, rel)

    def tars(self):
        return sorted(glob.glob(os.path.join(self.home, 'claude-espelho-*.tar.gz')))

    def claude_json(self):
        with open(self.arq('.claude.json')) as f:
            return json.load(f)

    def foto_home(self):
        r = {}
        for d, subs, arqs in os.walk(self.home):
            for n in subs + arqs:
                p = os.path.join(d, n)
                if n.startswith('claude-espelho-') or p == self.log:
                    continue
                if os.path.islink(p):
                    r[p] = 'link:' + os.readlink(p)
                elif os.path.isfile(p):
                    with open(p, 'rb') as f:
                        r[p] = f.read()
                else:
                    r[p] = 'dir'
        return r


class TestSnapshot(InstalarCaso):
    def test_tar_criado_e_citado_na_ultima_linha(self):
        saida = self.instala()
        t = self.tars()
        self.assertEqual(len(t), 1, saida)
        self.assertRegex(os.path.basename(t[0]), r'^claude-espelho-\d{8}-\d{6}\.tar\.gz$')
        self.assertIn(t[0], saida.strip().splitlines()[-1])

    def test_tar_guarda_estado_anterior(self):
        self.instala()
        with tarfile.open(self.tars()[0]) as tar:
            nomes = [re.sub(r'^\./', '', n) for n in tar.getnames()]
            self.assertIn('.claude/skills/extra/SKILL.md', nomes)
            self.assertIn('.claude.json', nomes)
            m = [m for m in tar.getmembers() if m.name.endswith('.claude/settings.json')][0]
            self.assertEqual(tar.extractfile(m).read(), b'VELHO')


class TestArquivos(InstalarCaso):
    def test_texto_com_home_local(self):
        self.instala()
        self.assertEqual(self.le(self.arq('.claude/settings.json')),
                         '{"hooks": "%s/.claude/hooks/h.sh"}\n' % self.home)
        self.assertEqual(self.le(self.arq('.claude/skills/a/SKILL.md')),
                         'skill a em %s/Code\n' % self.home)
        self.assertEqual(self.le(self.arq('.config/deja/config.toml')),
                         'db = "%s/.deja"\n' % self.home)

    def test_binario_intacto(self):
        self.instala()
        with open(self.arq('.claude/helpers/bin.dat'), 'rb') as f:
            self.assertEqual(f.read(), b'\x00\xff__HOME__\x00')

    def test_pasta_gerenciada_perde_o_extra(self):
        self.instala()
        self.assertFalse(os.path.exists(self.arq('.claude/skills/extra')))
        self.assertFalse(os.path.exists(self.arq('.claude/agents/velho.md')))
        self.assertEqual(self.le(self.arq('.claude/agents/x.md')), 'agente novo\n')

    def test_intocados(self):
        self.instala()
        for rel, c in [('.claude/CLAUDE.md', 'meu claude.md'),
                       ('.claude/memory/general.md', 'memoria'),
                       ('.claude/skills/synced/s1/SKILL.md', 'synced'),
                       ('.claude/projects/p/sessao.jsonl', 'sessao'),
                       ('.config/deja/token', 'SEGREDO'),
                       ('.config/watch/.env', 'K=V')]:
            self.assertEqual(self.le(self.arq(rel)), c, rel)

    def test_link_vira_link_com_home_local(self):
        self.instala()
        l = self.arq('.claude/skills/s')
        self.assertTrue(os.path.islink(l))
        self.assertEqual(os.readlink(l), os.path.join(self.home, 'Code/repo/skills/s'))

    def test_segunda_execucao_igual(self):
        self.instala()
        antes = self.foto_home()
        self.instala()
        self.assertEqual(self.foto_home(), antes)
        self.assertEqual(len(self.tars()), 2)


class TestMcp(InstalarCaso):
    def test_mcp_global_e_por_projeto_iguais_ao_espelho(self):
        self.instala()
        cj = self.claude_json()
        self.assertEqual(cj['mcpServers'], {'g': {'command': '%s/bin/g' % self.home}})
        self.assertEqual(cj['projects'][self.proj]['mcpServers'], {'p': {'command': 'p'}})
        self.assertNotIn('__HOME__/Code/proj', cj['projects'])

    def test_outras_chaves_preservadas(self):
        self.instala()
        cj = self.claude_json()
        self.assertEqual(cj['numStartups'], 7)
        self.assertEqual(cj['oauthAccount'], {'email': 'a@b'})
        self.assertEqual(cj['projects'][self.proj]['history'], ['h1'])
        self.assertEqual(cj['projects']['/outro'], {'allowedTools': ['t']})

    def test_claude_json_ausente_e_criado(self):
        os.remove(self.arq('.claude.json'))
        self.instala()
        cj = self.claude_json()
        self.assertEqual(cj['mcpServers'], {'g': {'command': '%s/bin/g' % self.home}})
        self.assertEqual(cj['projects'][self.proj]['mcpServers'], {'p': {'command': 'p'}})
