"""Etapas 10 e 21: install.sh liga a skill, instala e registra os MCPs travados (sem npx) e baixa o detector."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALL = os.path.join(RAIZ, 'install.sh')
# {mcp}: VESTA_MCP_HOME; os MCPs rodam do executável instalado lá, sem npx
CHROME = ('{mcp}/node_modules/.bin/chrome-devtools-mcp --headless --isolated --no-usage-statistics '
          '--no-performance-crux --categoryInput=false --categoryEmulation=false '
          '--categoryNetwork=false --categoryMemory=false')
PLAYWRIGHT = '{mcp}/node_modules/.bin/playwright-mcp --headless --snapshot-mode none --user-data-dir {home}/.cache/claude-navegador'
VERSOES = {'@playwright/mcp': '0.0.82', 'chrome-devtools-mcp': '1.10.1'}
GUARDADO = re.compile(r'^vesta-interface\.antes-da-vesta-interface-\d+$')

# claude falso: grava os argumentos, guarda os nomes adicionados e recusa como o real recusaria
CLAUDE_FALSO = r'''#!/bin/sh
echo "$@" >> "$CLAUDE_LOG"
[ "$1" = mcp ] || exit 0
acao=$2; shift 2
nome=; sep=0; pula=0
for a do
  if [ $pula = 1 ]; then pula=0; continue; fi
  case $a in
    --) sep=1 ;;
    --scope|-s) pula=1 ;;
    -*) ;;
    *) if [ $sep = 0 ]; then
         [ -z "$nome" ] || { echo "executável sem -- antes" >&2; exit 1; }
         nome=$a
       fi ;;
  esac
done
touch "$CLAUDE_NOMES"
case $acao in
  add)
    if grep -qx "$nome" "$CLAUDE_NOMES"; then echo "$nome já existe" >&2; exit 1; fi
    echo "$nome" >> "$CLAUDE_NOMES" ;;
  remove)
    grep -qx "$nome" "$CLAUDE_NOMES" || { echo "$nome não encontrado" >&2; exit 1; }
    grep -vx "$nome" "$CLAUDE_NOMES" > "$CLAUDE_NOMES.t" || true
    mv "$CLAUDE_NOMES.t" "$CLAUDE_NOMES" ;;
esac
'''

# npm falso: grava os argumentos (uma linha por chamada) e, no install, cria em <prefix>/node_modules
# o executável de cada pacote e o package.json com a versão pedida; com NPM_FALHA=1, falha sem criar nada
NPM_FALSO = r'''#!{python}
import json, os, sys
args = sys.argv[1:]
with open(os.environ['NPM_LOG'], 'a') as f:
    f.write(json.dumps(args) + '\n')
if os.environ.get('NPM_FALHA') == '1':
    sys.stderr.write('npm ERR! code ETIMEDOUT\n')
    sys.exit(1)
prefix, pacotes, pula = None, [], False
for i, a in enumerate(args):
    if pula:
        pula = False
    elif a == '--prefix':
        prefix, pula = args[i + 1], True
    elif a.startswith('--prefix='):
        prefix = a.split('=', 1)[1]
    elif not a.startswith('-') and a not in ('install', 'i', 'add'):
        pacotes.append(a)
if prefix is None or not ({{'install', 'i', 'add'}} & set(args)):
    sys.exit(0)
bins = {{'@playwright/mcp': 'playwright-mcp', 'chrome-devtools-mcp': 'chrome-devtools-mcp'}}
for spec in pacotes:
    corte = spec.rfind('@')
    nome, versao = (spec[:corte], spec[corte + 1:]) if corte > 0 else (spec, '')
    pasta = os.path.join(prefix, 'node_modules', nome)
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, 'package.json'), 'w') as f:
        json.dump({{'name': nome, 'version': versao}}, f)
    if nome in bins:
        exe = os.path.join(prefix, 'node_modules', '.bin', bins[nome])
        os.makedirs(os.path.dirname(exe), exist_ok=True)
        with open(exe, 'w') as f:
            f.write('#!/bin/sh\nexit 0\n')
        os.chmod(exe, 0o755)
'''


def executavel(caminho, corpo):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, 'w') as f:
        f.write(corpo)
    os.chmod(caminho, 0o755)


class Instalador(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp())
        self.home_dir = os.path.join(self.tmp, 'home')
        self.home = os.path.join(self.home_dir, '.claude')
        os.makedirs(self.home)  # sem skills/: o install.sh cria
        self.claude_json({'mcpServers': {'inspo': {'command': 'x'}}})
        self.log = os.path.join(self.tmp, 'claude.log')
        self.nomes = os.path.join(self.tmp, 'claude.nomes')
        self.bin = os.path.join(self.tmp, 'bin')
        executavel(os.path.join(self.bin, 'claude'), CLAUDE_FALSO)
        self.log_npm = os.path.join(self.tmp, 'npm.log')
        executavel(os.path.join(self.bin, 'npm'), NPM_FALSO.format(python=sys.executable))
        self.mcp_home = os.path.join(self.tmp, 'mcp')
        # binário travado já no cache: detectar --version não baixa nada
        self.cache = os.path.join(self.tmp, 'cache')
        self.log_imp = os.path.join(self.tmp, 'impeccable.log')
        executavel(os.path.join(self.cache, 'bin', '0.1.6', 'impeccable'),
                   f'#!/bin/sh\necho "$@" >> "{self.log_imp}"\necho falso-0.1.6\n')

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def p(self, *partes):
        return os.path.join(self.home, *partes)

    def claude_json(self, dados):
        with open(os.path.join(self.home_dir, '.claude.json'), 'w') as f:
            json.dump(dados, f)

    def ambiente(self, **extra):
        env = {k: v for k, v in os.environ.items() if k != 'IMPECCABLE_BIN'}
        env.update(HOME=self.home_dir, CLAUDE_HOME=self.home,
                   PATH=os.pathsep.join([self.bin, os.path.dirname(sys.executable),
                                         '/usr/bin', '/bin', '/usr/sbin', '/sbin']),
                   CLAUDE_LOG=self.log, CLAUDE_NOMES=self.nomes,
                   NPM_LOG=self.log_npm, VESTA_MCP_HOME=self.mcp_home,
                   IMPECCABLE_HOME=self.cache,
                   IMPECCABLE_DOWNLOAD_BASE='http://127.0.0.1:9')  # nunca rede de verdade
        env.update(extra)
        return {k: v for k, v in env.items() if v is not None}  # None tira a variável

    def executar(self, **extra):
        return subprocess.run(['bash', INSTALL], env=self.ambiente(**extra), cwd=self.tmp,
                              capture_output=True, text=True, timeout=120)

    def rodar(self, **extra):
        r = self.executar(**extra)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout + r.stderr

    def chamadas_npm(self):
        if not os.path.exists(self.log_npm):
            return []
        with open(self.log_npm) as f:
            return [json.loads(l) for l in f]

    def installs(self):
        return [a for a in self.chamadas_npm() if {'install', 'i', 'add'} & set(a)]

    def registrado(self, nome):
        """Argumentos depois do `--` no `mcp add` de `nome`."""
        add = [c for c in self.chamadas() if c.startswith(f'mcp add --scope user {nome} -- ')]
        self.assertEqual(len(add), 1, self.chamadas())
        return add[0].split(' -- ', 1)[1].split()

    def chamadas(self):
        if not os.path.exists(self.log):
            return []
        with open(self.log) as f:
            return f.read().splitlines()

    def avisos(self, saida):
        return [l for l in saida.splitlines() if l.startswith('aviso:')]

    def guardados(self):
        return [n for n in os.listdir(self.p('skills')) if '.antes-da-vesta-interface-' in n]

    def assertLigado(self):
        link = self.p('skills', 'vesta-interface')
        self.assertTrue(os.path.islink(link))
        self.assertEqual(os.path.realpath(link), os.path.realpath(RAIZ))

    # link da skill
    def test_cria_link_da_skill_para_o_repositorio(self):
        self.rodar()
        self.assertLigado()

    def test_segunda_execucao_nao_muda_o_link_nem_guarda_copia(self):
        self.rodar()
        antes = os.readlink(self.p('skills', 'vesta-interface'))
        self.rodar()
        self.assertLigado()
        self.assertEqual(os.readlink(self.p('skills', 'vesta-interface')), antes)
        self.assertEqual(self.guardados(), [])

    def test_pasta_real_no_lugar_e_guardada_com_sufixo(self):
        os.makedirs(self.p('skills', 'vesta-interface'))
        with open(self.p('skills', 'vesta-interface', 'SKILL.md'), 'w') as f:
            f.write('antiga')
        self.rodar()
        self.assertLigado()
        guardados = self.guardados()
        self.assertEqual(len(guardados), 1, guardados)
        self.assertRegex(guardados[0], GUARDADO)
        with open(self.p('skills', guardados[0], 'SKILL.md')) as f:
            self.assertEqual(f.read(), 'antiga')

    # MCPs
    def test_claude_falso_recusa_add_sem_separador_e_remove_de_nome_ausente(self):
        env = self.ambiente()
        add = subprocess.run(['claude', 'mcp', 'add', '--scope', 'user', 'x', '/opt/bin/y', '--z'],
                             env=env, capture_output=True)
        rm = subprocess.run(['claude', 'mcp', 'remove', '--scope', 'user', 'x'],
                            env=env, capture_output=True)
        self.assertEqual((add.returncode, rm.returncode), (1, 1))

    def test_registra_chrome_devtools_com_flags_travadas(self):
        self.rodar()
        self.assertIn('mcp add --scope user chrome-devtools -- ' + CHROME.format(mcp=self.mcp_home),
                      self.chamadas())

    def test_troca_playwright_com_flags_travadas(self):
        self.rodar()
        self.assertIn('mcp add --scope user playwright -- '
                      + PLAYWRIGHT.format(mcp=self.mcp_home, home=self.home_dir), self.chamadas())

    # MCPs instalados por npm, sem npx (etapa 21)
    def test_npm_instala_as_duas_versoes_exatas_na_pasta_de_vesta_mcp_home(self):
        self.rodar()
        installs = self.installs()
        self.assertTrue(installs, self.chamadas_npm())
        for args in installs:
            with self.subTest(args=args):
                i = args.index('--prefix') if '--prefix' in args else -1
                prefixo = args[i + 1] if i >= 0 else next(
                    (a.split('=', 1)[1] for a in args if a.startswith('--prefix=')), None)
                self.assertEqual(prefixo, self.mcp_home)
        pedidos = [a for args in installs for a in args]
        for nome, versao in VERSOES.items():
            with self.subTest(nome):
                self.assertIn(f'{nome}@{versao}', pedidos)

    def test_npm_nao_recebe_pacote_sem_versao_exata(self):
        self.rodar()
        pacotes = [a for args in self.installs() for a in args
                   if not a.startswith('-') and a not in ('install', 'i', 'add', self.mcp_home)]
        self.assertTrue(pacotes)
        for spec in pacotes:
            with self.subTest(spec):
                self.assertRegex(spec, r'^(@[^/@]+/)?[^@]+@\d+\.\d+\.\d+$')

    def test_sem_vesta_mcp_home_usa_pasta_fixa_no_home(self):
        self.rodar(VESTA_MCP_HOME=None)
        padrao = os.path.join(self.home_dir, '.local', 'share', 'vesta-interface', 'mcp')
        self.assertIn('mcp add --scope user chrome-devtools -- ' + CHROME.format(mcp=padrao),
                      self.chamadas())
        self.assertTrue(os.access(os.path.join(padrao, 'node_modules', '.bin', 'playwright-mcp'), os.X_OK))

    def test_npm_falhou_instalador_sai_com_erro_e_nao_registra_mcp(self):
        r = self.executar(NPM_FALHA='1')
        self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(self.chamadas_npm())
        self.assertEqual([c for c in self.chamadas() if c.startswith('mcp add')], [])

    def test_nenhum_registro_usa_npx(self):
        self.rodar()
        self.assertTrue(self.chamadas())
        self.assertEqual([c for c in self.chamadas() if 'npx' in c.split()], [])

    def test_executavel_registrado_existe_na_pasta_dos_mcps(self):
        self.rodar()
        for nome, exe in (('chrome-devtools', 'chrome-devtools-mcp'), ('playwright', 'playwright-mcp')):
            with self.subTest(nome):
                cmd = self.registrado(nome)[0]
                self.assertEqual(cmd, os.path.join(self.mcp_home, 'node_modules', '.bin', exe))
                self.assertTrue(os.access(cmd, os.X_OK), cmd)

    def test_remove_antes_de_adicionar_e_tolera_primeira_remocao(self):
        self.rodar()  # sai 0 embora o claude falso recuse as duas remoções
        chamadas = self.chamadas()
        for nome in ('chrome-devtools', 'playwright'):
            with self.subTest(nome):
                rm = f'mcp remove --scope user {nome}'
                self.assertIn(rm, chamadas)
                add = next(i for i, c in enumerate(chamadas)
                           if c.startswith(f'mcp add --scope user {nome} '))
                self.assertLess(chamadas.index(rm), add)

    def test_segunda_execucao_readiciona_sem_erro(self):
        self.rodar()
        self.rodar()  # o claude falso recusa add de nome que já existe
        with open(self.nomes) as f:
            self.assertEqual(sorted(f.read().split()), ['chrome-devtools', 'playwright'])

    def test_shadcn_nao_vira_mcp(self):
        self.rodar()
        self.assertEqual([c for c in self.chamadas() if 'shadcn' in c], [])

    def test_nenhum_argumento_usa_latest(self):
        self.rodar()
        self.assertTrue(self.chamadas())
        self.assertEqual([c for c in self.chamadas() if '@latest' in c], [])

    # CLAUDE.md
    def test_nao_mexe_no_claude_md(self):
        texto = '# meu CLAUDE.md\n\nregra qualquer\n'
        with open(self.p('CLAUDE.md'), 'w') as f:
            f.write(texto)
        self.rodar()
        self.assertFalse(os.path.islink(self.p('CLAUDE.md')))
        with open(self.p('CLAUDE.md')) as f:
            self.assertEqual(f.read(), texto)

    # detector
    def test_chama_detectar_version_com_binario_em_cache(self):
        saida = self.rodar()
        with open(self.log_imp) as f:
            self.assertIn('--version', f.read().split())
        self.assertEqual([a for a in self.avisos(saida) if 'impeccable' in a.lower()], [])

    def test_download_do_detector_falha_sem_derrubar_a_instalacao(self):
        vazio = os.path.join(self.tmp, 'cache-vazio')  # sem binário: o lançador tenta baixar
        saida = self.rodar(IMPECCABLE_HOME=vazio)
        self.assertTrue([a for a in self.avisos(saida) if 'impeccable' in a.lower()], saida)
        self.assertLigado()
        self.assertIn('mcp add --scope user chrome-devtools -- ' + CHROME.format(mcp=self.mcp_home),
                      self.chamadas())

    # inspo
    def test_sem_inspo_avisa_e_nao_falha(self):
        self.claude_json({'mcpServers': {'outro': {'command': 'x'}}})
        saida = self.rodar()
        self.assertTrue([a for a in self.avisos(saida) if 'inspo' in a], saida)

    def test_sem_claude_json_avisa_e_nao_falha(self):
        os.remove(os.path.join(self.home_dir, '.claude.json'))
        saida = self.rodar()
        self.assertTrue([a for a in self.avisos(saida) if 'inspo' in a], saida)

    def test_com_inspo_nao_avisa(self):
        saida = self.rodar()
        self.assertEqual(self.avisos(saida), [], saida)


if __name__ == '__main__':
    unittest.main()
