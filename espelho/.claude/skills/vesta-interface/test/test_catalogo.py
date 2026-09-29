"""Etapa 5: catálogo em catalogo/ (componentes, macroestruturas, temas, gêneros do hallmark e 3 direções do taste-skill)."""
import os
import re
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(RAIZ, 'catalogo')
X = os.path.expanduser('~/Code/ux-lab/vendor')
REFS = os.path.join(X, 'hallmark', 'references')
TASTE = os.path.join(X, 'taste-skill', 'skills')
REGISTRO = os.path.join(X, 'ui', 'apps', 'v4', 'registry', 'new-york-v4', 'ui')

CONTAGENS = {'components': 50, 'macrostructures': 21, 'themes': 5, 'genres': 4, 'direcoes': 3}
APOIO = ['macrostructures.md', 'component-cookbook.md', 'hero-enrichment.md', 'assets.md',
         'custom-craft.md', 'floating-nav.md']
TEMAS = ['carnival', 'cobalt', 'grid', 'hum', 'lumen']
TEMAS_INEXISTENTES = ['Studio', 'Bloom', 'Midnight']
DIRECOES = {'minimalista': 'minimalist-skill', 'sofisticada': 'soft-skill', 'brutalista': 'brutalist-skill'}

LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)')
EXTERNO = re.compile(r'^(https?:|mailto:|#)')
# texto abaixo de 12px: 10/11px, text-[≤11px], rem abaixo de 0.75 (0.7rem = 11.2px também conta).
# rem precedido de '-' fica de fora: é subtração ou negativo, nunca tamanho de texto
# (sofisticada tem `rounded-[calc(2rem-0.375rem)]`, um raio)
PEQUENO = [re.compile(r'\b(10|11)(\.\d+)?px'),
           re.compile(r'text-\[(\d|10|11)(\.\d+)?px\]'),
           re.compile(r'(?<![\d.\-])0\.(?:[0-6]\d*|7(?:[0-4]\d*)?)rem')]
# formato exigido: `shadcn: navigation-menu, sheet` numa linha própria, logo abaixo do título
SHADCN = re.compile(r'^shadcn: ([a-z0-9-]+(?:, [a-z0-9-]+)*)$')


def ler(caminho):
    with open(caminho, encoding='utf-8') as f:
        return f.read()


def mds(pasta):
    return sorted(a for a in os.listdir(pasta) if a.endswith('.md'))


def todos_md():
    for pasta, _, arquivos in os.walk(CAT):
        for a in arquivos:
            if a.endswith('.md'):
                yield os.path.join(pasta, a)


def links(caminho):
    return [a for a in LINK.findall(ler(caminho)) if not EXTERNO.match(a)]


def direcao(nome):
    return ler(os.path.join(CAT, 'direcoes', nome + '.md'))


class TestContagens(unittest.TestCase):
    def test_contagens(self):
        for pasta, n in CONTAGENS.items():
            with self.subTest(pasta=pasta):
                self.assertTrue(os.path.isdir(os.path.join(CAT, pasta)), f'catalogo/{pasta} não existe')
                self.assertEqual(len(mds(os.path.join(CAT, pasta))), n)

    def test_direcoes_com_os_nomes_do_plano(self):
        self.assertEqual(mds(os.path.join(CAT, 'direcoes')), sorted(n + '.md' for n in DIRECOES))

    def test_arquivos_de_apoio_e_readme(self):
        for a in APOIO + ['README.md']:
            with self.subTest(arquivo=a):
                self.assertTrue(os.path.isfile(os.path.join(CAT, a)))

    @unittest.skipUnless(os.path.isdir(REFS), 'X/hallmark/references sumiu; nomes sem como conferir')
    def test_mesmos_arquivos_que_o_hallmark(self):
        for pasta in ['components', 'macrostructures', 'themes', 'genres']:
            with self.subTest(pasta=pasta):
                self.assertEqual(mds(os.path.join(CAT, pasta)), mds(os.path.join(REFS, pasta)))


class TestLinks(unittest.TestCase):
    def test_nenhum_link_para_site(self):
        self.assertTrue(os.path.isdir(CAT), 'catalogo/ não existe')
        for caminho in todos_md():
            for alvo in links(caminho):
                with self.subTest(arquivo=os.path.relpath(caminho, CAT), alvo=alvo):
                    self.assertNotIn('site/', alvo)

    def test_tokens_css_legitimo_fica(self):
        self.assertIn('tokens.css', ler(os.path.join(CAT, 'components', 's3-sticky-pinned.md')))

    def test_todo_link_relativo_existe_dentro_do_repo(self):
        vistos = 0
        for caminho in todos_md():
            for alvo in links(caminho):
                vistos += 1
                with self.subTest(arquivo=os.path.relpath(caminho, CAT), alvo=alvo):
                    destino = os.path.realpath(os.path.join(os.path.dirname(caminho), alvo.split('#')[0]))
                    self.assertTrue(destino.startswith(RAIZ + os.sep), f'{alvo} sai do repositório')
                    self.assertTrue(os.path.exists(destino), f'{alvo} não existe')
        self.assertGreater(vistos, 0, 'nenhum link relativo encontrado em catalogo/')


class TestReadme(unittest.TestCase):
    def setUp(self):
        self.texto = ler(os.path.join(CAT, 'README.md'))

    def test_lista_os_cinco_temas(self):
        for tema in TEMAS:
            with self.subTest(tema=tema):
                self.assertIn(f'themes/{tema}.md', self.texto)

    def test_avisa_temas_inexistentes(self):
        for nome in TEMAS_INEXISTENTES:
            with self.subTest(nome=nome):
                self.assertIn(nome, self.texto)
        self.assertIn('não existe', self.texto)


class TestDirecoes(unittest.TestCase):
    def test_comeca_com_bloco_limites(self):
        for nome in DIRECOES:
            with self.subTest(direcao=nome):
                texto = direcao(nome)
                linhas = [l for l in texto.splitlines() if l.strip()]
                self.assertRegex(linhas[0], r'^(#{1,6} +|\*\*)Limites')
                bloco = re.split(r'^#{1,6} ', texto.split('\n', 1)[1], maxsplit=1, flags=re.M)[0]
                self.assertIn('4.5:1', bloco)
                self.assertIn('12px', bloco)
                self.assertIn('acessibilidade', bloco.lower())
                self.assertIn('não cede', bloco)

    def test_sem_texto_abaixo_de_12px(self):
        for nome in DIRECOES:
            texto = direcao(nome)
            for padrao in PEQUENO:
                with self.subTest(direcao=nome, padrao=padrao.pattern):
                    self.assertEqual([m.group(0) for m in padrao.finditer(texto)], [])

    def test_sem_frontmatter_de_skill(self):
        for nome in DIRECOES:
            with self.subTest(direcao=nome):
                texto = direcao(nome)
                self.assertFalse(texto.startswith('---'))
                self.assertNotRegex(texto, r'(?m)^name:')

    @unittest.skipUnless(os.path.isdir(TASTE), 'X/taste-skill sumiu; conteúdo sem como conferir')
    def test_conteudo_da_skill_certa(self):
        for nome, skill in DIRECOES.items():
            with self.subTest(direcao=nome):
                titulo = re.search(r'(?m)^# .+$', ler(os.path.join(TASTE, skill, 'SKILL.md'))).group(0)
                self.assertIn(titulo, direcao(nome))


class TestShadcn(unittest.TestCase):
    def linhas(self):
        self.assertTrue(os.path.isdir(os.path.join(CAT, 'components')), 'catalogo/components não existe')
        for caminho in todos_md():
            for i, linha in enumerate(ler(caminho).splitlines()):
                if 'shadcn:' in linha.lower():
                    yield caminho, i, linha

    def test_formato_da_linha(self):
        for caminho, i, linha in self.linhas():
            with self.subTest(arquivo=os.path.relpath(caminho, CAT), linha=i + 1):
                self.assertRegex(linha, SHADCN)

    def test_logo_abaixo_do_titulo(self):
        for caminho, i, _ in self.linhas():
            with self.subTest(arquivo=os.path.relpath(caminho, CAT), linha=i + 1):
                antes = [l for l in ler(caminho).splitlines()[:i] if l.strip()]
                self.assertTrue(antes and antes[-1].startswith('#'), 'linha shadcn: não segue o título')
                self.assertEqual(sum(l.startswith('#') for l in antes), 1, 'linha shadcn: fora do primeiro título')

    @unittest.skipUnless(os.path.isdir(REGISTRO), 'X/ui sumiu; nomes shadcn sem como conferir')
    def test_nomes_existem_no_registro(self):
        registro = {a[:-4] for a in os.listdir(REGISTRO) if a.endswith('.tsx')}
        for caminho, i, linha in self.linhas():
            m = SHADCN.match(linha)
            for nome in (m.group(1).split(', ') if m else []):
                with self.subTest(arquivo=os.path.relpath(caminho, CAT), nome=nome):
                    self.assertIn(nome, registro)


if __name__ == '__main__':
    unittest.main()
