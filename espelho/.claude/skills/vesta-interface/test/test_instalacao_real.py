"""Etapas 13 e 21: instalação real, saída do hallmark e inventários (lê o sistema desta máquina)."""
import json
import os
import re
import subprocess
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASA = os.path.expanduser('~')
CLAUDE = os.path.join(CASA, '.claude')
CLAUDE_JSON = os.path.join(CASA, '.claude.json')
LINK_SKILL = os.path.join(CLAUDE, 'skills', 'vesta-interface')
HALLMARK = os.path.join(CLAUDE, 'skills', 'hallmark')
HALLMARK_VENDOR = os.path.join(CASA, 'Code', 'ux-lab', 'vendor', 'hallmark', 'SKILL.md')
BIN_TRAVADO = os.path.join(CASA, '.impeccable', 'bin', '0.1.6', 'impeccable')
DETECTAR = os.path.join(RAIZ, 'ferramentas', 'impeccable', 'detectar')
ESTADO_ATUAL = os.path.join(CASA, 'Code', 'claude-tooling', 'docs', 'reference', 'estado-atual.md')
KIT_README = os.path.join(CASA, 'Code', 'claude-kit', 'README.md')
MCP_HOME = os.environ.get('VESTA_MCP_HOME') or os.path.join(CASA, '.local', 'share', 'vesta-interface', 'mcp')
CATEGORIAS = ['--categoryInput=false', '--categoryEmulation=false',
              '--categoryNetwork=false', '--categoryMemory=false']


def ler(caminho):
    with open(caminho, encoding='utf-8') as f:
        return f.read()


def servidores():
    return json.loads(ler(CLAUDE_JSON)).get('mcpServers') or {}


def linha(servidor):
    return ' '.join([servidor.get('command', '')] + list(servidor.get('args', [])))


def versao_instalada(pacote):
    return json.loads(ler(os.path.join(MCP_HOME, 'node_modules', pacote, 'package.json')))['version']


def permitidas():
    return json.loads(ler(os.path.join(CLAUDE, 'settings.json')))['permissions']['allow']


def secao(texto, titulo):
    """Corpo da seção de cabeçalho `#…` cujo título casa com `titulo`, até o próximo de mesmo nível ou acima."""
    m = re.search(r'^(#+)[ \t]+[^\n]*' + titulo + r'[^\n]*$', texto, re.M | re.I)
    if not m:
        return None
    nivel = len(m.group(1))
    fim = re.compile(r'^#{1,%d}[ \t]' % nivel, re.M).search(texto, m.end())
    return texto[m.end():fim.start() if fim else len(texto)]


@unittest.skipUnless(os.path.exists(CLAUDE_JSON), 'fora desta máquina: ~/.claude.json ausente')
class InstalacaoReal(unittest.TestCase):
    # skill e hallmark
    def test_skill_e_link_para_o_repositorio(self):
        self.assertTrue(os.path.islink(LINK_SKILL))
        self.assertEqual(os.path.realpath(LINK_SKILL), os.path.realpath(RAIZ))

    def test_hallmark_saiu_das_skills_e_ficou_no_vendor(self):
        self.assertTrue(os.path.isfile(HALLMARK_VENDOR))
        self.assertFalse(os.path.lexists(HALLMARK))

    # MCPs em ~/.claude.json
    def test_chrome_devtools_sem_npx_pelo_executavel_instalado_e_sem_shadcn(self):
        mcps = servidores()
        self.assertNotIn('shadcn', mcps)
        self.assertIn('chrome-devtools', mcps)
        cmd = linha(mcps['chrome-devtools'])
        self.assertNotIn('npx', cmd.split())
        self.assertNotIn('@latest', cmd)
        exe = mcps['chrome-devtools'].get('command')
        self.assertEqual(exe, os.path.join(MCP_HOME, 'node_modules', '.bin', 'chrome-devtools-mcp'))
        self.assertTrue(os.access(exe, os.X_OK), exe)

    def test_chrome_devtools_instalado_em_1_10_1(self):
        self.assertEqual(versao_instalada('chrome-devtools-mcp'), '1.10.1')

    def test_chrome_devtools_com_quatro_categorias_desligadas(self):
        mcps = servidores()
        self.assertIn('chrome-devtools', mcps)
        cmd = linha(mcps['chrome-devtools']).split()
        for flag in CATEGORIAS:
            with self.subTest(flag=flag):
                self.assertIn(flag, cmd)

    def test_playwright_sem_npx_pelo_executavel_instalado_e_sem_snapshot(self):
        servidor = servidores()['playwright']
        cmd = linha(servidor)
        self.assertNotIn('npx', cmd.split())
        self.assertNotIn('@latest', cmd)
        self.assertRegex(cmd, r'(^| )--snapshot-mode none( |$)')
        exe = servidor.get('command')
        self.assertEqual(exe, os.path.join(MCP_HOME, 'node_modules', '.bin', 'playwright-mcp'))
        self.assertTrue(os.access(exe, os.X_OK), exe)

    def test_playwright_instalado_em_0_0_82(self):
        self.assertEqual(versao_instalada(os.path.join('@playwright', 'mcp')), '0.0.82')

    # detector
    def test_binario_travado_e_engine_0_1_6(self):
        self.assertTrue(os.access(BIN_TRAVADO, os.X_OK))
        saida = subprocess.run([BIN_TRAVADO, 'engine-probe'], capture_output=True, text=True, timeout=60)
        self.assertEqual(saida.returncode, 0, saida.stderr)
        self.assertEqual(saida.stdout.strip(), 'impeccable-engine 0.1.6')

    def test_detectar_usa_o_binario_travado(self):
        # O plano pedia `detectar --version` == 0.1.6, mas o --version imprime o número do
        # produto do CLI (4.0.0); a versão da engine só aparece no `engine-probe` (teste acima).
        # Aqui basta provar que o `detectar` responde igual ao binário travado.
        travado = subprocess.run([BIN_TRAVADO, '--version'], capture_output=True, text=True, timeout=60)
        detectar = subprocess.run([DETECTAR, '--version'], capture_output=True, text=True, timeout=120)
        self.assertEqual(detectar.returncode, 0, detectar.stderr)
        self.assertEqual(travado.returncode, 0, travado.stderr)
        self.assertTrue(detectar.stdout.strip())
        self.assertEqual(detectar.stdout.strip(), travado.stdout.strip())

    # permissões em ~/.claude/settings.json
    def test_permissoes_novas(self):
        allow = permitidas()
        for regra in ['mcp__playwright', 'mcp__chrome-devtools',
                      'Bash(~/.claude/skills/vesta-interface/ferramentas/*)']:
            with self.subTest(regra=regra):
                self.assertIn(regra, allow)

    def test_sem_regras_do_plugin_playwright(self):
        self.assertEqual([r for r in permitidas() if r.startswith('mcp__plugin_playwright_playwright__')], [])

    # inventários
    def test_estado_atual_cita_vesta_interface_nas_skills_proprias(self):
        corpo = secao(ler(ESTADO_ATUAL), 'Skills próprias')
        self.assertIsNotNone(corpo)
        self.assertIn('vesta-interface', corpo)

    def test_estado_atual_tem_secao_de_mcps_travados(self):
        corpo = secao(ler(ESTADO_ATUAL), 'MCP')
        self.assertIsNotNone(corpo, 'sem seção de MCPs')
        self.assertIn('chrome-devtools-mcp@1.10.1', corpo)
        self.assertIn('@playwright/mcp@0.0.82', corpo)

    def test_kit_readme_sem_hallmark(self):
        self.assertNotIn('hallmark', ler(KIT_README).lower())

    def test_kit_readme_cita_vesta_interface_e_chrome_devtools(self):
        texto = ler(KIT_README)
        self.assertIn('vesta-interface', texto)
        self.assertIn('chrome-devtools', texto)

    def test_kit_readme_nao_liga_plugin_playwright(self):
        m = re.search(r'^Ligados:(.*?)(?:\n\s*\n|\Z)', ler(KIT_README), re.M | re.S)
        self.assertIsNotNone(m, 'parágrafo "Ligados:" dos plugins sumiu')
        self.assertNotIn('`playwright`', m.group(1))


if __name__ == '__main__':
    unittest.main()
