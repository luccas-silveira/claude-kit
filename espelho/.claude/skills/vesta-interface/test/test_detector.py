"""Etapas 2, 3 e 16: detector do impeccable travado na versão 0.1.6, com a reserva WASM ao lado
e as exceções do projeto aplicadas por padrão, também na saída da reserva."""
import ast
import filecmp
import json
import os
import shutil
import re
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMPECCABLE = os.path.join(RAIZ, 'ferramentas', 'impeccable')
DETECTAR = os.path.join(IMPECCABLE, 'detectar')
RESERVA = os.path.join(IMPECCABLE, 'reserva', 'detect-antipatterns-browser.js')
EXCECOES = os.path.join(IMPECCABLE, 'excecoes.json')
FILTRAR = os.path.join(IMPECCABLE, 'filtrar.py')
FIXTURES = os.path.join(RAIZ, 'test', 'fixtures', 'detector')
ORIGEM = os.path.expanduser('~/Code/ux-lab/vendor/impeccable')
# mapa tirado de X/impeccable/tests/oracle/golden/detect-fixture-json-*.json
MAPA = {
    'css-in-prose-should-flag.html': {'gradient-text', 'ai-color-palette'},
    'placeholder-contrast.html': {'low-contrast'},
}


def fixture(nome):
    return os.path.join(FIXTURES, nome)


def ambiente(**extra):
    env = {k: v for k, v in os.environ.items() if k != 'IMPECCABLE_BIN'}
    env.update(extra)
    return env


def detectar(*args, env=None, timeout=300, cwd=None):
    # cwd fora do repositório: nenhum DESIGN.md ou .impeccable/ de projeto entra na conta
    return subprocess.run([DETECTAR, *args], capture_output=True, text=True, encoding='utf-8',
                          cwd=cwd or tempfile.gettempdir(), env=env or ambiente(), timeout=timeout)


def achados(r):
    return {a['antipattern'] for a in json.loads(r.stdout)}


def chrome():
    candidatos = [os.environ.get('CHROME_PATH', ''),
                  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                  shutil.which('google-chrome') or '', shutil.which('chromium') or '']
    return any(c and os.access(c, os.X_OK) for c in candidatos)


def falso(caminho, texto, probe=False):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    corpo = '#!/bin/sh\n'
    if probe:  # responde ao handshake do lançador, que então o escolheria
        corpo += '[ "$1" = engine-probe ] && { echo "impeccable-engine 9.9.9"; exit 0; }\n'
    corpo += f'echo {texto}\n'
    with open(caminho, 'w') as f:
        f.write(corpo)
    os.chmod(caminho, 0o755)


class TestArquivoFixo(unittest.TestCase):
    def test_versao_travada_em_0_1_6(self):
        with open(os.path.join(IMPECCABLE, 'VERSION')) as f:
            self.assertEqual(f.read().strip(), '0.1.6')

    def test_detectar_executavel(self):
        self.assertTrue(os.access(DETECTAR, os.X_OK))

    def test_reserva_tem_impeccable_detect(self):
        with open(RESERVA, encoding='utf-8') as f:
            self.assertIn('impeccableDetect', f.read())

    @unittest.skipUnless(os.path.isdir(ORIGEM), 'fonte congelada do impeccable ausente')
    def test_copias_iguais_a_fonte(self):
        pares = [(os.path.join(IMPECCABLE, 'impeccable'),
                  os.path.join(ORIGEM, '.claude/skills/impeccable/scripts/impeccable')),
                 (RESERVA, os.path.join(ORIGEM, 'crates/live/assets/detect-antipatterns-browser.js'))]
        for copia, fonte in pares:
            self.assertTrue(filecmp.cmp(copia, fonte, shallow=False), copia)


class TestArquivo(unittest.TestCase):
    def test_pagina_limpa_sai_zero_com_lista_vazia(self):
        r = detectar('--json', fixture('should-pass.html'))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), [])

    def test_fixture_com_problema_sai_dois_com_as_regras_do_mapa(self):
        for nome, regras in MAPA.items():
            with self.subTest(nome):
                r = detectar('--json', fixture(nome))
                self.assertEqual(r.returncode, 2, r.stderr)
                self.assertEqual(achados(r), regras)

    def test_arquivo_inexistente_sai_um(self):
        r = detectar('--json', fixture('nao-existe.html'))
        self.assertEqual(r.returncode, 1, r.stdout)


class TestVersaoTravada(unittest.TestCase):
    def test_versao_travada_vence_binario_sem_versao(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = os.path.join(tmp, 'home')
            cache = os.path.join(tmp, 'cache')  # separado do HOME: detectar precisa ler IMPECCABLE_HOME
            falso(os.path.join(cache, 'bin', '0.1.6', 'impeccable'), 'falso-0.1.6')
            falso(os.path.join(cache, 'bin', 'impeccable'), 'errado', probe=True)
            falso(os.path.join(home, '.impeccable', 'bin', 'impeccable'), 'errado', probe=True)
            caminho = os.path.join(tmp, 'path')
            falso(os.path.join(caminho, 'impeccable'), 'errado', probe=True)
            env = ambiente(HOME=home, IMPECCABLE_HOME=cache,
                           PATH=caminho + os.pathsep + os.environ.get('PATH', ''))
            r = detectar('--version', env=env, timeout=30)
            self.assertEqual(r.stdout.strip(), 'falso-0.1.6', r.stderr)


@unittest.skipUnless(chrome(), 'sem Chrome nesta máquina (locais padrão ou CHROME_PATH)')
class TestPaginaRenderizada(unittest.TestCase):
    def test_gradiente_acusado_nas_duas_larguras(self):
        url = 'file://' + fixture('css-in-prose-should-flag.html')
        for viewport in ('375x812', '1440x900'):
            with self.subTest(viewport):
                r = detectar('--json', '--viewport', viewport, url)
                self.assertEqual(r.returncode, 2, r.stderr)
                self.assertIn('gradient-text', achados(r))

    def test_pagina_limpa_sai_zero(self):
        r = detectar('--json', '--viewport', '1440x900', 'file://' + fixture('should-pass.html'))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), [])


# decisão 5 da spec
FONTES_PERMITIDAS = ('Geist', 'Geist Sans', 'Geist Mono', 'Fraunces', 'Space Grotesk',
                     'Plus Jakarta Sans', 'Instrument Serif')


def com_fonte(pasta, fonte):
    """geist.html com a fonte do corpo trocada, gravada fora do repositório."""
    with open(fixture('geist.html'), encoding='utf-8') as f:
        html = f.read()
    alvo = '"Geist", sans-serif'
    assert alvo in html
    caminho = os.path.join(pasta, 'pagina.html')
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(html.replace(alvo, f'"{fonte}", sans-serif'))
    return caminho


def excecoes():
    with open(EXCECOES, encoding='utf-8') as f:
        return json.load(f)


class TestExcecoes(unittest.TestCase):
    def test_geist_acusa_sem_excecoes_e_passa_com_elas(self):
        with tempfile.TemporaryDirectory() as tmp:
            for nome, caminho in (('Geist', fixture('geist.html')),
                                  ('Geist Mono', com_fonte(tmp, 'Geist Mono'))):
                with self.subTest(nome):
                    sem = detectar('--json', '--no-config', caminho)
                    self.assertEqual(sem.returncode, 2, sem.stderr)
                    self.assertEqual(achados(sem), {'overused-font'})
                    com = detectar('--json', caminho)
                    self.assertEqual(com.returncode, 0, com.stdout + com.stderr)
                    self.assertEqual(json.loads(com.stdout), [])

    def test_cada_entrada_tem_regra_valor_e_motivo(self):
        lista = excecoes()
        self.assertIsInstance(lista, list)
        self.assertTrue(lista)
        for e in lista:
            with self.subTest(e):
                for campo in ('regra', 'valor', 'motivo'):
                    self.assertIsInstance(e.get(campo), str)
                    self.assertTrue(e[campo].strip(), campo)

    def test_fontes_da_decisao_5_estao_nas_excecoes(self):
        valores = {e['valor'].strip().casefold() for e in excecoes() if e['regra'] == 'overused-font'}
        for fonte in FONTES_PERMITIDAS:
            self.assertIn(fonte.casefold(), valores)

    def test_excecao_libera_o_valor_e_nao_a_regra(self):
        self.assertEqual(detectar('--json', fixture('geist.html')).returncode, 0)
        with tempfile.TemporaryDirectory() as tmp:
            r = detectar('--json', com_fonte(tmp, 'Inter'))
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertEqual(achados(r), {'overused-font'})
        for nome, regras in MAPA.items():
            with self.subTest(nome):
                self.assertEqual(achados(detectar('--json', fixture(nome))), regras)

    def test_caminho_relativo_resolvido_da_pasta_corrente(self):
        r = detectar('--json', 'geist.html', cwd=FIXTURES)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout), [])

    def test_config_do_projeto_corrente_nao_muda_resultado(self):
        with tempfile.TemporaryDirectory() as projeto:
            os.makedirs(os.path.join(projeto, '.impeccable'))
            with open(os.path.join(projeto, '.impeccable', 'config.json'), 'w') as f:
                json.dump({'detector': {'ignoreRules': ['gradient-text'], 'ignoreFiles': [],
                                        'ignoreValues': []}}, f)
            for nome in ('css-in-prose-should-flag.html', 'geist.html'):
                with self.subTest(nome):
                    fora = detectar('--json', fixture(nome))
                    dentro = detectar('--json', fixture(nome), cwd=projeto)
                    self.assertEqual(dentro.returncode, fora.returncode, dentro.stderr)
                    self.assertEqual(achados(dentro), achados(fora))
                    self.assertEqual(fora.returncode, 2 if nome.startswith('css') else 0)


# etapa 16: fixtures reserva-*.json são a saída real de window.impeccableDetectAsync() em Chrome
# sem janela a 1440x900. geist/inter: geist.html com a fonte do corpo; geist-mono: idem com
# "Geist Mono"; geist-roxo: geist.html com título e selo em #7c3aed (o item body traz
# overused-font e ai-color-palette juntos); css-in-prose: css-in-prose-should-flag.html.
def reserva(nome):
    with open(fixture(f'reserva-{nome}.json'), encoding='utf-8') as f:
        return f.read()


def filtrar(*args, entrada=None, script=FILTRAR):
    return subprocess.run([sys.executable, script, *args], input=entrada, capture_output=True,
                          text=True, encoding='utf-8', cwd=tempfile.gettempdir(), timeout=60)


def sem_achado(itens, tipo):
    """Os itens com os achados `tipo` tirados; item que fica sem achado sai da lista."""
    saida = []
    for item in itens:
        resto = [f for f in item['findings'] if f['type'] != tipo]
        if resto:
            saida.append({**item, 'findings': resto})
    return saida


class TestFiltrarReserva(unittest.TestCase):
    def assertSaida(self, r, codigo, esperado):
        self.assertEqual(r.returncode, codigo, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout), esperado)

    def test_filtrar_existe_e_so_usa_stdlib(self):
        self.assertTrue(os.path.isfile(FILTRAR), 'falta ferramentas/impeccable/filtrar.py')
        with open(FILTRAR, encoding='utf-8') as f:
            arvore = ast.parse(f.read())
        modulos = {a.name.split('.')[0] for n in ast.walk(arvore) if isinstance(n, ast.Import)
                   for a in n.names}
        modulos |= {n.module.split('.')[0] for n in ast.walk(arvore)
                    if isinstance(n, ast.ImportFrom) and n.module and not n.level}
        self.assertLessEqual(modulos, set(sys.stdlib_module_names))

    def test_geist_some_lendo_do_stdin(self):
        self.assertSaida(filtrar(entrada=reserva('geist')), 0, [])

    def test_geist_some_lendo_de_arquivo(self):
        self.assertSaida(filtrar(fixture('reserva-geist.json')), 0, [])

    def test_geist_mono_tambem_some(self):
        self.assertSaida(filtrar(entrada=reserva('geist-mono')), 0, [])

    def test_inter_fica_intacto_e_sai_dois(self):
        self.assertSaida(filtrar(entrada=reserva('inter')), 2, json.loads(reserva('inter')))

    def test_outras_regras_ficam_intactas(self):
        self.assertSaida(filtrar(fixture('reserva-css-in-prose.json')), 2,
                         json.loads(reserva('css-in-prose')))

    def test_tira_so_o_achado_que_casa_e_mantem_o_item(self):
        itens = json.loads(reserva('geist-roxo'))
        corpo = [i for i in itens if i['selector'] == 'body']
        self.assertEqual([f['type'] for f in corpo[0]['findings']], ['overused-font', 'ai-color-palette'])
        esperado = sem_achado(itens, 'overused-font')
        self.assertEqual(len(esperado), len(itens))
        self.assertSaida(filtrar(entrada=reserva('geist-roxo')), 2, esperado)

    def test_lista_vazia_sai_zero(self):
        self.assertSaida(filtrar(entrada='[]'), 0, [])

    def com_excecoes(self, tmp, lista):
        """filtrar.py copiado para outra pasta, ao lado de um excecoes.json de teste."""
        shutil.copy(FILTRAR, tmp)
        with open(os.path.join(tmp, 'excecoes.json'), 'w', encoding='utf-8') as f:
            json.dump([{'motivo': 'teste', **e} for e in lista], f)
        return os.path.join(tmp, 'filtrar.py')

    def test_valor_casa_o_nome_inteiro_da_fonte(self):
        # "Geist" liberada não libera "Geist Mono", e vice-versa
        for liberada, nome in (('Geist', 'geist-mono'), ('Geist Mono', 'geist')):
            with self.subTest(liberada=liberada, pagina=nome), tempfile.TemporaryDirectory() as tmp:
                script = self.com_excecoes(tmp, [{'regra': 'overused-font', 'valor': liberada}])
                self.assertSaida(filtrar(entrada=reserva(nome), script=script), 2,
                                 json.loads(reserva(nome)))

    def test_valor_nao_libera_outra_regra(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = self.com_excecoes(tmp, [{'regra': 'gradient-text', 'valor': 'Geist'}])
            self.assertSaida(filtrar(entrada=reserva('geist'), script=script), 2,
                             json.loads(reserva('geist')))

    def test_le_as_excecoes_da_propria_pasta_sem_maiusculas(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = self.com_excecoes(tmp, [{'regra': 'overused-font', 'valor': 'INTER'}])
            self.assertSaida(filtrar(entrada=reserva('inter'), script=script), 0, [])

    def test_verificacao_manda_filtrar_a_saida_da_reserva(self):
        with open(os.path.join(RAIZ, 'referencias', 'verificacao.md'), encoding='utf-8') as f:
            texto = f.read()
        filtro = 'ferramentas/impeccable/filtrar.py'
        itens = re.split(r'\n(?=- )', texto)
        reservas = [i for i in itens if 'impeccableDetectAsync' in i]
        self.assertTrue(reservas, 'verificacao.md não cita a reserva')
        for item in reservas:
            with self.subTest(item=item[:60]):
                self.assertGreater(item.find(filtro), item.find('impeccableDetectAsync'),
                                   'a saída da reserva não passa depois pelo filtrar.py')
        alarme = re.search(r'^- \*\*VER-\d+\*\* Alarme', texto, re.M)
        self.assertIsNotNone(alarme, 'verificacao.md sem o passo de alarme')
        self.assertTrue(filtro in texto[:alarme.start()], 'o filtro tem de vir antes de tratar os alarmes')


if __name__ == '__main__':
    unittest.main()
