"""Etapa 9: SKILL.md com frontmatter, piso de regras e os cinco passos; modos estudo, componente e ajustes."""
import glob
import os
import re
import shlex
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_referencias as tr  # noqa: E402  leitores de regra, seção e trecho das etapas 6 a 8
import test_uupm as tu  # noqa: E402  padrões de landing do banco do ui-ux-pro-max

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(RAIZ, 'SKILL.md')
MODOS = ['estudo', 'componente', 'ajustes']
AJUSTES = ['bolder', 'quieter', 'distill', 'harden', 'onboard', 'optimize', 'polish', 'delight']
LIMITE_DESCRICAO = 1536
LIMITE_LINHAS = 500
# C, seção 4, lista 36 regras em 3+ fontes (11 slop, 5 tipografia, 6 cor, 4 layout, 6 movimento,
# 4 ux) e diz "roughly 40"; a faixa aceita fundir ou separar algumas ao escrever o piso
PISO_MIN, PISO_MAX = 30, 60
# grupos da seção 4 de C; um piso só de SLOP não é o piso
PREFIXOS_DO_PISO = ['SLOP', 'TIP', 'COR', 'LAY', 'MOV', 'UX']
PASSOS = [(1, r'entend'), (2, r'referencia'), (3, r'sistema visual'), (4, r'constru'), (5, r'verifica')]
PASSO = re.compile(r'^(?:passo\s+)?(\d)\b')
ABRA = re.compile(r'\babra\b[^\n]*?`((?:referencias|catalogo)/[^`\s]+)`', re.I)
# "Todo caminho relativo citado": contam
#   - trechos entre crases que começam por referencias/, modos/, ferramentas/ ou catalogo/
#     (vale o primeiro token: `ferramentas/rotacao.py ultimas --projeto .` confere ferramentas/rotacao.py;
#     `:linha` no fim sai; placeholder <x>, {a,b} ou * confere só a parte antes dele);
#   - links Markdown relativos `[texto](caminho)`, resolvidos a partir da pasta do arquivo.
# Não contam caminhos do projeto do usuário (docs/design/..., src/..., app/...), X/... nem URLs.
PREFIXOS_REPO = ('referencias/', 'modos/', 'ferramentas/', 'catalogo/')
CRASE = re.compile(r'`((?:referencias|modos|ferramentas|catalogo)/[^`]*)`')
LINK = re.compile(r'\]\(([^)\s]+)\)')
FORA_DA_VARREDURA = ('catalogo/', 'licencas/', 'ferramentas/', 'THIRD_PARTY_NOTICES.md', 'docs/', 'test/')
HALLMARK_GLOBAL = re.compile(r'\.claude/skills/hallmark')
COMANDO_IMPECCABLE = re.compile(r'(^|[\s`(])/impeccable\b', re.M)
BOTOES = ['VARIACAO', 'MOVIMENTO', 'DENSIDADE']
TIPOS = ['Persuadir', 'Operar', 'Ler', 'Experiência']
# etapa 15: questionário pelo menu do AskUserQuestion (texto já sem acento e minúsculo)
UMA_POR_CHAMADA = (r'\buma (so )?pergunta (so )?(por|em cada|a cada|de cada) chamada'
                   r'|\bcada chamada\b[^.]*\b(uma (so )?pergunta|so uma pergunta)')
VARIAS_POR_CHAMADA = (r'\b(varias|ate \d+|ate (duas|tres|quatro)|mais de uma|\d+) perguntas'
                      r' (por|numa|em uma|na mesma|de uma vez na) chamada')
RECOMENDADA_PRIMEIRO = (r'recomend[^.]*\b(em primeiro|primeira|primeiro lugar|no topo|a frente)'
                        r'|\b(em primeiro|primeira|primeiro lugar|no topo)\b[^.]*recomend')

# etapa 17: a busca do ui-ux-pro-max muda com o tipo de tela. Conta como busca todo trecho entre
# crases com search.py e todo bloco cercado (```) com search.py, que roda inteiro num shell.
BUSCA = re.compile(r'```[^\n]*\n(.*?)```|`([^`\n]*search\.py[^`\n]*)`', re.S)
ITEM_DO_TOPO = re.compile(r'^(?:\d+\.|[-*]) ', re.M)
CONSULTA = re.compile(r'"[^"\n]*<[^"\n]*"|\'[^\'\n]*<[^\'\n]*\'')  # "<produto> <público> <tom>"
CONSULTA_CRM = 'CRM lead dashboard'
DESIGN_SYSTEM = re.compile(r'--design-system\b|(?<!\S)-ds\b')
DOMINIO = re.compile(r'--domain\b|(?<!\S)-d\b')
BOTOES_DA_BUSCA = re.compile(r'\s--(?:variance|motion|density)(?:\s+|=)\d+')


def skill():
    return tr.ler(SKILL)


def modo(nome):
    return tr.ler(os.path.join(RAIZ, 'modos', nome + '.md'))


def frontmatter(texto):
    """Campos de primeiro nível do YAML entre as duas linhas `---` (valor numa linha, ou bloco `>`/`|`)."""
    m = re.match(r'^---\n(.*?)\n---\n', texto, flags=re.S)
    if not m:
        return {}
    campos, chave = {}, None
    for linha in m.group(1).splitlines():
        c = re.match(r'^([\w-]+):\s*(.*)$', linha)
        if c:
            chave, valor = c.group(1), c.group(2).strip()
            campos[chave] = '' if valor in ('>', '|', '>-', '|-') else valor.strip('"\'')
        elif chave and linha.startswith((' ', '\t')):
            campos[chave] = (campos[chave] + ' ' + linha.strip()).strip()
    return campos


def passos(texto):
    """{número: corpo} dos títulos numerados de 1 a 5, no nível em que aparecem, e a ordem em que vêm."""
    for nivel in (2, 3):
        achados = [(int(PASSO.match(tr.norm(t)).group(1)), t, c) for t, c, _, _ in tr.blocos(texto, nivel)
                   if PASSO.match(tr.norm(t))]
        if len(achados) >= 5:
            return achados
    return []


def corpo_do_passo(n):
    return next(c for num, _, c in passos(skill()) if num == n)


def trecho_com(texto, *padroes):
    """Algum trecho (parágrafo, item ou título, sem acento e minúsculo) casa com todos os padrões."""
    return any(all(re.search(p, t) for p in padroes) for t in tr.trechos(texto))


def buscas_por_tipo(corpo):
    """{tipo: [comando]}. Cada busca fica com os tipos de tela citados entre ela e a busca anterior,
    sem voltar além do início do item de lista do topo em que está; sem tipo no meio, herda os da
    busca anterior do mesmo item. "Em Persuadir e Experiência, `A`; em Operar e Ler, `B` e `C`"
    dá A a Persuadir e Experiência, B e C a Operar e Ler."""
    inicios = [m.start() for m in ITEM_DO_TOPO.finditer(corpo)]
    saida = {t: [] for t in TIPOS}
    fim, item_anterior, rotulo = 0, None, set()
    for m in BUSCA.finditer(corpo):
        comando = (m.group(1) if m.group(1) is not None else m.group(2)).strip()
        if 'search.py' not in comando:
            continue
        item = max([i for i in inicios if i <= m.start()], default=0)
        if item != item_anterior:
            fim, rotulo = item, set()
        janela = tr.sem_acento(corpo[fim:m.start()])
        rotulo = {t for t in TIPOS if re.search(tr.TIPO_RE[t], janela)} or rotulo
        for t in rotulo:
            saida[t].append(comando)
        fim, item_anterior = m.end(), item
    return saida


def rodar_busca(comando):
    """Roda o comando do SKILL.md como está, da raiz da skill, com a consulta trocada pela do CRM."""
    comando = CONSULTA.sub(shlex.quote(CONSULTA_CRM), comando)
    comando = re.sub(r'(?<![\w/.-])python3\b', shlex.quote(sys.executable), comando)
    return subprocess.run(['bash', '-c', comando], cwd=RAIZ, capture_output=True, text=True,
                          encoding='utf-8', timeout=300)


def ids_das_referencias():
    ids = set()
    for nome in tr.ARQUIVOS:
        ids |= {tr.ID.match(r).group(1) for r in tr.regras(tr.ref(nome))}
    return ids


def caminhos_citados(caminho_arquivo):
    """[(caminho citado, caminho absoluto a conferir)] pelas regras descritas em PREFIXOS_REPO."""
    texto = tr.ler(caminho_arquivo)
    saida = []
    for m in CRASE.finditer(texto):
        token = m.group(1).split()[0]
        saida.append((token, os.path.join(RAIZ, token)))
    pasta = os.path.dirname(caminho_arquivo)
    for m in LINK.finditer(texto):
        alvo = m.group(1).split('#')[0]
        if not alvo or re.match(r'^[a-z]+:', alvo) or alvo.startswith(('/', '~')):
            continue
        saida.append((alvo, os.path.normpath(os.path.join(pasta, alvo))))
    return saida


def existe(absoluto):
    absoluto = re.sub(r':\d+(?:[-–]\d+)?$', '', absoluto).rstrip('.,;')
    corte = re.search(r'[<{*]', absoluto)
    if corte:
        absoluto = absoluto[:corte.start()]
        if not absoluto.endswith('/'):
            absoluto = os.path.dirname(absoluto)
    return os.path.exists(absoluto)


def arquivos_varridos():
    saida = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
                           cwd=RAIZ, capture_output=True, text=True, check=True).stdout
    return [a for a in saida.splitlines() if a and not a.startswith(FORA_DA_VARREDURA)
            and os.path.isfile(os.path.join(RAIZ, a))]


class TestArquivos(unittest.TestCase):
    def test_skill_e_os_tres_modos_existem(self):
        self.assertTrue(os.path.isfile(SKILL))
        for nome in MODOS:
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, 'modos', nome + '.md')), nome)

    def test_skill_tem_menos_de_500_linhas(self):
        self.assertLess(len(skill().splitlines()), LIMITE_LINHAS)

    def test_skill_aponta_os_tres_modos(self):
        # modo que o SKILL.md não cita, o agente nunca abre
        citados = {c for c, _ in caminhos_citados(SKILL)}
        for nome in MODOS:
            self.assertIn(f'modos/{nome}.md', citados, nome)


class TestFrontmatter(unittest.TestCase):
    def setUp(self):
        self.campos = frontmatter(skill())

    def test_nome(self):
        self.assertEqual(self.campos.get('name'), 'vesta-interface')

    def test_descricao_ate_1536_com_when_to_use(self):
        descricao = self.campos.get('description', '')
        self.assertTrue(descricao)
        self.assertLessEqual(len(descricao) + len(self.campos.get('when_to_use', '')), LIMITE_DESCRICAO)

    def test_primeira_frase_e_o_caso_principal_em_portugues(self):
        primeira = tr.norm(re.split(r'\.(?:\s|$)', self.campos.get('description', ''))[0])
        self.assertRegex(primeira, r'\bdesenh')
        self.assertRegex(primeira, r'\brevis')
        self.assertRegex(primeira, r'\b(interface|tela|componente)')


class TestPiso(unittest.TestCase):
    def setUp(self):
        b = tr.secao(skill(), 'Piso')
        self.assertIsNotNone(b, 'falta a seção ## Piso')
        self.itens = tr.itens(b[1])

    def ids(self):
        return [tr.ID.match(i).group(1) for i in self.itens if tr.ID.match(i)]

    def test_toda_linha_comeca_pelo_id(self):
        for item in self.itens:
            self.assertRegex(item, tr.ID, item)

    def test_uma_linha_por_regra(self):
        for item in self.itens:
            self.assertNotIn('\n', item, item)

    def test_tamanho_perto_de_40(self):
        self.assertGreaterEqual(len(self.itens), PISO_MIN)
        self.assertLessEqual(len(self.itens), PISO_MAX)

    def test_todo_id_existe_nas_referencias(self):
        faltam = sorted(set(self.ids()) - ids_das_referencias())
        self.assertEqual(faltam, [])

    def test_nenhum_id_repetido(self):
        ids = self.ids()
        self.assertEqual(sorted({i for i in ids if ids.count(i) > 1}), [])

    def test_cobre_os_grupos_da_secao_4(self):
        prefixos = {i.split('-')[0] for i in self.ids()}
        for p in PREFIXOS_DO_PISO:
            self.assertIn(p, prefixos)


class TestPassos(unittest.TestCase):
    def test_cinco_passos_numerados_na_ordem(self):
        achados = passos(skill())
        self.assertEqual([n for n, _, _ in achados], [1, 2, 3, 4, 5])
        for (n, titulo, _), (esperado, chave) in zip(achados, PASSOS):
            self.assertRegex(tr.norm(titulo), chave, titulo)

    def test_cada_passo_manda_abrir_uma_referencia(self):
        for n, titulo, corpo in passos(skill()):
            abertos = ABRA.findall(corpo)
            self.assertTrue(abertos, f'passo {n} não diz "Abra `referencias/...`"')
            for c in abertos:
                self.assertTrue(existe(os.path.join(RAIZ, c)), c)

    def test_passos_3_e_5_abrem_arquivo_de_referencias(self):
        for n in (3, 5):
            abertos = [c for c in ABRA.findall(corpo_do_passo(n)) if c.startswith('referencias/')]
            self.assertTrue(abertos, f'passo {n}')
            for c in abertos:
                self.assertTrue(os.path.isfile(os.path.join(RAIZ, c)), c)


class TestPasso1(unittest.TestCase):
    def setUp(self):
        self.corpo = corpo_do_passo(1)

    def test_varredura_do_projeto_existente(self):
        self.assertTrue(trecho_com(self.corpo, r'\bvarr(a|e|edura)\b', r'projeto'))

    def test_classifica_nos_quatro_tipos(self):
        self.assertRegex(tr.norm(self.corpo), r'tipo de tela')
        for tipo in TIPOS:
            self.assertIn(tipo, self.corpo)

    def test_bifurcacao_padrao_por_tela(self):
        self.assertTrue(trecho_com(self.corpo, r'tela nova', r'com questionario'))
        self.assertTrue(trecho_com(self.corpo, r'existente', r'\bdireto\b'))

    def test_questionario_por_askuserquestion_uma_pergunta_por_chamada(self):
        self.assertIn('AskUserQuestion', self.corpo)
        self.assertTrue(trecho_com(self.corpo, r'askuserquestion', UMA_POR_CHAMADA),
                        'o passo 1 não diz que cada chamada do AskUserQuestion leva uma pergunta só')
        self.assertFalse(trecho_com(self.corpo, VARIAS_POR_CHAMADA),
                         'o passo 1 junta várias perguntas numa chamada')

    def test_recomendada_em_primeiro_e_marcada_recomendado(self):
        self.assertIn('(Recomendado)', self.corpo)
        self.assertTrue(trecho_com(self.corpo, r'\(recomendado\)', RECOMENDADA_PRIMEIRO),
                        'o passo 1 não põe a opção recomendada em primeiro, marcada "(Recomendado)"')

    def test_aceita_resposta_livre_outro(self):
        self.assertTrue(trecho_com(self.corpo, r'\boutro\b', r'\blivre\b'),
                        'o passo 1 não aceita a resposta livre ("Outro") do usuário')

    def test_perguntas_nao_sao_mais_no_chat(self):
        self.assertNotRegex(tr.norm(self.corpo), r'\bno chat\b')

    def test_direto_mostra_respostas_deduzidas_com_o_resultado(self):
        self.assertTrue(trecho_com(self.corpo, r'\bdireto\b', r'deduz', r'junto'))

    def test_busca_do_uupm_vetada_pelas_regras(self):
        self.assertIn('ferramentas/uupm/scripts/search.py', self.corpo)
        self.assertTrue(trecho_com(self.corpo, r'search\.py', r'--format markdown'))
        self.assertTrue(trecho_com(self.corpo, r'\bvet(a|am|o|e|ar)\b', r'regra'))

    def test_fixa_os_tres_botoes_pelo_tipo_de_tela(self):
        for botao in BOTOES:
            self.assertIn(botao, self.corpo)
        self.assertTrue(trecho_com(self.corpo, r'variacao', r'tipo de tela'))

    def test_questionario_deixa_mudar_os_botoes(self):
        self.assertTrue(trecho_com(self.corpo, r'questionario', r'botoes|variacao',
                                   r'\b(mud|troc|alter|ajust)'))


class TestBuscaPorTipo(unittest.TestCase):
    """Etapa 17: o --design-system sempre traz um ### Pattern de landing, mesmo com os três botões;
    Operar e Ler buscam por domínio, conferidos contra os padrões de data/landing.csv."""

    @classmethod
    def setUpClass(cls):
        cls.buscas = buscas_por_tipo(corpo_do_passo(1))
        cls.saidas = {}

    def comandos(self, tipo):
        cmds = self.buscas[tipo]
        self.assertTrue(cmds, f'o passo 1 não diz qual busca do search.py rodar em {tipo}')
        return cmds

    def rodar(self, comando):
        if comando not in self.saidas:
            self.saidas[comando] = rodar_busca(comando)
        return self.saidas[comando]

    def de_operar_e_ler(self):
        return list(dict.fromkeys(self.comandos('Operar') + self.comandos('Ler')))

    def test_persuadir_e_experiencia_seguem_com_design_system(self):
        for tipo in ('Persuadir', 'Experiência'):
            for c in self.comandos(tipo):
                self.assertRegex(c, DESIGN_SYSTEM, f'{tipo}: {c}')
                self.assertIn('--format markdown', c, f'{tipo}: {c}')

    def test_operar_e_ler_buscam_por_dominio_sem_design_system(self):
        for tipo in ('Operar', 'Ler'):
            for c in self.comandos(tipo):
                self.assertNotRegex(c, DESIGN_SYSTEM, f'{tipo}: {c}')
                self.assertRegex(c, DOMINIO, f'{tipo}: {c}')

    def test_busca_de_operar_e_ler_roda_com_crm(self):
        for c in self.de_operar_e_ler():
            r = self.rodar(c)
            self.assertEqual(r.returncode, 0, f'{c}\n{r.stderr}')
            self.assertTrue(r.stdout.strip(), c)

    def test_busca_de_operar_e_ler_nao_traz_padrao_de_landing(self):
        # --domain product também cai aqui: a coluna "Landing Page Pattern" traz "Feature-Rich Showcase"
        padroes = tu.padroes_de_landing()
        self.assertGreater(len(padroes), 20)
        for c in self.de_operar_e_ler():
            r = self.rodar(c)
            self.assertEqual(r.returncode, 0, f'{c}\n{r.stderr}')
            achados = [p for p in padroes if p.casefold() in r.stdout.casefold()]
            self.assertEqual(achados, [], c)

    def test_busca_de_operar_e_ler_traz_estilo_paleta_e_fontes(self):
        # o passo 1 busca estilo, paleta e fontes; trocar o design system só por --domain ux perde os três
        saida = ''.join(self.rodar(c).stdout for c in self.de_operar_e_ler())
        self.assertIn('Style Category', saida)
        self.assertRegex(saida, tu.HEX)
        self.assertIn('Heading Font', saida)

    def test_botoes_na_busca_de_operar_e_ler_mudam_a_saida(self):
        # sem --design-system o search.py aceita --variance/--motion/--density e os ignora
        for c in self.de_operar_e_ler():
            if not BOTOES_DA_BUSCA.search(c):
                continue
            sem = BOTOES_DA_BUSCA.sub('', c)
            self.assertNotEqual(self.rodar(c).stdout, self.rodar(sem).stdout,
                                f'os botões não mudam a saída de {c}')


class TestPasso3(unittest.TestCase):
    def setUp(self):
        self.corpo = corpo_do_passo(3)

    def test_rotacao_em_persuadir_e_experiencia(self):
        self.assertTrue(trecho_com(self.corpo, r'rotacao\.py ultimas', r'persuadir', r'experiencia'))

    def test_ultimas_linha_e_registro_na_ordem(self):
        pos = [self.corpo.find(s) for s in ('rotacao.py ultimas', 'Últimas:', 'rotacao.py registrar')]
        self.assertNotIn(-1, pos, pos)
        self.assertEqual(pos, sorted(pos))
        self.assertTrue(trecho_com(self.corpo, r'ultimas:', r'esta:', r'porque'))

    def test_registrar_escrito_por_inteiro(self):
        linhas = [l for l in self.corpo.splitlines() if 'rotacao.py registrar' in l]
        self.assertTrue(linhas)
        for flag in ('--projeto', '--tela', '--tipo', '--macro', '--menu', '--rodape'):
            self.assertTrue(any(flag in l for l in linhas), flag)

    def test_operar_e_ler_herdam_menu_e_rodape_do_sistema(self):
        self.assertTrue(trecho_com(self.corpo, r'operar', r'\bler\b', r'sistema\.md', r'menu', r'rodape'))

    def test_cita_rotacao_json_e_sistema_md(self):
        self.assertIn('docs/design/rotacao.json', self.corpo)
        self.assertIn('docs/design/sistema.md', self.corpo)

    def test_sistema_guarda_tipo_direcao_e_botoes(self):
        self.assertTrue(trecho_com(self.corpo, r'sistema\.md', r'tipo de tela', r'direcao',
                                   r'botoes|variacao'))

    def test_export_para_variaveis_css_do_shadcn(self):
        self.assertTrue(trecho_com(self.corpo, r'variave(l|is) css', r'shadcn'))


ITEM_NUMERADO = re.compile(r'^\d+\. ', re.M)
RECOMENDADA_PRIMEIRA = r'recomend\w*[^.]*\bprimeir|\bprimeir[^.]*recomend'
DIRECAO_NAO_PERGUNTADA = (r'\bdirecao\b[^.]*\b(nao|nunca)\b[^.]*\bpergunt'
                          r'|\b(nao|nunca|sem)\b[^.]*\bpergunt\w*[^.]*\bdirecao\b')
DUAS_DIRECOES = re.compile(r'\b(duas|2) (direcoes|versoes|mockups)\b')


def itens_numerados(corpo):
    """Itens numerados do topo do passo, com os subitens recuados, sem acento e minúsculos."""
    inicios = [m.start() for m in ITEM_NUMERADO.finditer(corpo)] + [len(corpo)]
    return [tr.norm(corpo[a:b]) for a, b in zip(inicios, inicios[1:])]


class TestMockupDeDirecoes(unittest.TestCase):
    """Etapa 18: tela nova ganha dois mockups em direções diferentes e o usuário escolhe um antes
    de gravar o sistema e construir; tela existente, um mockup só no estilo atual."""

    def setUp(self):
        self.corpo = corpo_do_passo(3)

    def test_tela_nova_ganha_duas_versoes_estaticas_da_vista_principal(self):
        self.assertTrue(trecho_com(self.corpo, r'mockup', r'tela nova', DUAS_DIRECOES.pattern,
                                   r'estatic', r'vista principal'),
                        'o passo 3 não tem o item de mockup: duas versões estáticas da vista principal')

    def test_cada_versao_numa_direcao_diferente_nao_variacao_de_cor(self):
        self.assertTrue(trecho_com(self.corpo, r'mockup', r'diferente', r'catalogo/direcoes/',
                                   r'catalogo/themes/', r'\binspo\b'),
                        'o mockup não diz de onde vem cada direção (direcoes, themes ou inspo diferentes)')
        self.assertTrue(trecho_com(self.corpo, r'mockup', r'\b(nao|nunca|nem)\b[^.]*\bvariac\w* de cor'),
                        'o mockup não proíbe duas variações de cor da mesma direção')

    def test_html_autocontido_em_docs_design_mockups_a_e_b(self):
        self.assertTrue('docs/design/mockups/<tela>-a.html' in self.corpo and '-b.html' in self.corpo,
                        'os mockups não ficam em docs/design/mockups/<tela>-a.html e -b.html')
        self.assertTrue(trecho_com(self.corpo, r'mockup', r'html autocontido'))

    def test_servidos_por_http_local_com_prints_375_e_1440_mostrados(self):
        self.assertTrue(trecho_com(self.corpo, r'mockup', r'\bhttp\b', r'\bprints?\b', r'\b375\b',
                                   r'\b1440\b', r'\bmostr', r'usuario'),
                        'os mockups não são servidos por HTTP local com prints 375 e 1440 ao usuário')

    def test_usuario_escolhe_com_askuserquestion_recomendada_primeiro(self):
        self.assertTrue('AskUserQuestion' in self.corpo, 'o passo 3 não cita a ferramenta AskUserQuestion')
        self.assertTrue(trecho_com(self.corpo, r'mockup', r'askuserquestion', r'\buma (so |unica )?pergunta\b',
                                   r'\(recomendado\)', RECOMENDADA_PRIMEIRA),
                        'a escolha da direção não é uma pergunta do AskUserQuestion com a recomendada '
                        'em primeiro, marcada "(Recomendado)"')

    def test_sistema_md_gravado_so_depois_da_escolha(self):
        self.assertTrue(trecho_com(self.corpo, r'mockup', r'escolh',
                                   r'\bdepois\b[^.]*\bgrav\w*[^.]*sistema\.md|grav\w*[^.]*sistema\.md[^.]*\bdepois\b'),
                        'o mockup não diz que o sistema.md só é gravado depois da escolha')
        itens = itens_numerados(self.corpo)
        mockup = next((i for i, t in enumerate(itens) if 'mockup' in t), None)
        grava = next((i for i, t in enumerate(itens) if re.match(r'\d+\.\s+\W*grav', t)), None)
        self.assertIsNotNone(mockup, 'o passo 3 não tem item de mockup')
        self.assertIsNotNone(grava, 'o passo 3 perdeu o item de gravar o sistema')
        self.assertLess(mockup, grava, 'o item de mockup vem depois de gravar o sistema.md')

    def test_nenhum_codigo_da_tela_final_antes_da_escolha(self):
        self.assertTrue(trecho_com(self.corpo, r'mockup',
                                   r'\b(nenhum|nada de|nao|nunca)\b[^.]*\bcodigo\b[^.]*\bantes\b[^.]*\bescolh'),
                        'o mockup não proíbe escrever código da tela final antes da escolha')

    def test_passo_4_constroi_na_direcao_escolhida(self):
        self.assertTrue(trecho_com(corpo_do_passo(4),
                                   r'direcao escolhida|mockup escolhido|mockup aprovado|\b(depois|apos) (da|a) escolha'),
                        'o passo 4 não parte da direção escolhida no mockup')

    def test_tela_existente_um_mockup_so_no_estilo_atual(self):
        self.assertTrue(trecho_com(self.corpo, r'ja existe|existente', r'\b(um|1) mockup\b', r'estilo atual',
                                   r'\bprints?\b', r'aprova', r'ajust', r'antes do passo 4'),
                        'tela existente não tem um mockup só, no estilo atual, aprovado antes do passo 4')
        duas = [f for f in tr.frases(self.corpo) if re.search(r'ja existe|existente', f.lower())
                and DUAS_DIRECOES.search(f.lower()) and not tr.NEGA.search(f)]
        self.assertEqual(duas, [], 'tela existente ganha duas direções')

    def test_questionario_de_tela_nova_nao_pergunta_a_direcao(self):
        self.assertTrue(trecho_com(corpo_do_passo(1), r'tela nova', DIRECAO_NAO_PERGUNTADA, r'mockup'),
                        'o questionário de tela nova ainda pergunta a direção, em vez de ela sair dos mockups')

    def test_questionario_de_tela_nova_mantem_as_outras_perguntas(self):
        self.assertTrue(trecho_com(corpo_do_passo(1), r'\b(outras|demais) perguntas\b',
                                   r'\b(continu|seguem|mant)'),
                        'o questionário de tela nova não diz que as outras perguntas continuam')


class TestPasso4(unittest.TestCase):
    def setUp(self):
        self.corpo = corpo_do_passo(4)

    def test_react_usa_cli_travado_e_rota_de_mockup(self):
        self.assertTrue(trecho_com(self.corpo, r'\breact\b', r'shadcn@4\.21\.0'))
        self.assertTrue(trecho_com(self.corpo, r'\breact\b', r'\brota\b', r'mockup'))

    def test_sem_react_html_autocontido_com_visual_do_shadcn(self):
        self.assertTrue(trecho_com(self.corpo, r'sem react|\bnao\b[^.]*\breact\b|outros projetos',
                                   r'\bhtml\b', r'autocontido', r'shadcn'))


class TestPasso5(unittest.TestCase):
    def test_tela_servida_pelo_servidor_http_local(self):
        self.assertTrue(trecho_com(corpo_do_passo(5), r'127\.0\.0\.1|http\.server|servidor http'),
                        'o passo 5 não diz que o HTML sem React é servido por HTTP local')

    def test_skill_e_modos_nao_mandam_abrir_file(self):
        # o Playwright MCP recusa file://; uma URL só, a do servidor, para as três ferramentas
        for arq in [SKILL] + [os.path.join(RAIZ, 'modos', n + '.md') for n in MODOS]:
            with self.subTest(arquivo=os.path.relpath(arq, RAIZ)):
                self.assertEqual(tr.abre_file(tr.ler(arq)), [])


class TestProvasComNomeFixo(unittest.TestCase):
    """Etapa 19: prints das direções e provas da verificação com nome fixo."""

    def item_do_mockup(self):
        itens = [t for t in itens_numerados(corpo_do_passo(3)) if 'mockup de direc' in t]
        self.assertTrue(itens, 'o passo 3 perdeu o item Mockup de direções')
        return itens[0]

    def test_passo3_nomeia_os_quatro_prints_das_direcoes(self):
        item = self.item_do_mockup()
        self.assertIn('docs/design/mockups/<tela>-a-375.png', item)
        for nome in ['<tela>-a-375.png', '<tela>-a-1440.png', '<tela>-b-375.png', '<tela>-b-1440.png']:
            with self.subTest(print=nome):
                self.assertIn(nome, item, f'o item de mockup não nomeia o print {nome}')

    def test_passo3_grava_os_quatro_prints_antes_da_pergunta(self):
        item = self.item_do_mockup()
        self.assertTrue(re.search(r'\bgrav[^.]*\bantes d[ao] (pergunta|escolha|askuserquestion)', item),
                        'o item de mockup não diz que os quatro prints são gravados antes da pergunta')
        ultimo = max(item.find(n) for n in ['-a-375.png', '-a-1440.png', '-b-375.png', '-b-1440.png'])
        self.assertLess(ultimo, item.find('askuserquestion'), 'os prints aparecem depois da pergunta')

    def test_passo5_verificacao_so_vale_com_os_arquivos_gravados(self):
        corpo = corpo_do_passo(5)
        self.assertTrue(trecho_com(corpo, r'\bso vale|\bnao vale|\bnao conta', r'gravad', r'\bprints?\b',
                                   r'relatorio\.md',
                                   r'duas saidas do detector|detector-375\.json[^.]*detector-1440\.json'),
                        'o passo 5 não diz que a verificação só vale com prints, as duas saídas do detector '
                        'e `relatorio.md` gravados')

    def test_passo5_contraste_e_rolagem_so_afirmados_se_medidos(self):
        fs = [f.lower() for f in tr.frases(corpo_do_passo(5))]
        self.assertTrue([f for f in fs if 'contraste' in f and 'rolagem' in f and re.search(r'\bmedid', f)
                         and 'rodada' in f and re.search(r'\b(so|nunca|sem)\b', f)],
                        'o passo 5 não diz que contraste e rolagem lateral só se afirmam medidos na rodada')


class TestCaminhos(unittest.TestCase):
    def test_todo_caminho_citado_existe(self):
        arquivos = [SKILL] + [os.path.join(RAIZ, 'modos', n + '.md') for n in MODOS]
        vistos = 0
        for arq in arquivos:
            for citado, absoluto in caminhos_citados(arq):
                vistos += 1
                self.assertTrue(existe(absoluto), f'{os.path.relpath(arq, RAIZ)}: {citado}')
        self.assertGreater(vistos, 0)


class TestSemHallmarkNemImpeccable(unittest.TestCase):
    def test_nenhum_arquivo_cita_hallmark_global_nem_comando_impeccable(self):
        varridos = arquivos_varridos()
        for a in ['SKILL.md'] + [f'modos/{n}.md' for n in MODOS]:
            self.assertIn(a, varridos)  # a varredura pega os arquivos desta etapa
        achados = []
        for a in varridos:
            try:
                texto = tr.ler(os.path.join(RAIZ, a))
            except UnicodeDecodeError:
                continue
            if HALLMARK_GLOBAL.search(texto):
                achados.append(f'{a}: hallmark global')
            if COMANDO_IMPECCABLE.search(texto):
                achados.append(f'{a}: /impeccable')
        self.assertEqual(achados, [])


class TestModos(unittest.TestCase):
    def test_estudo_parte_de_url_ou_print(self):
        texto = tr.norm(modo('estudo'))
        self.assertRegex(texto, r'\burl\b')
        self.assertRegex(texto, r'\bprint')

    def test_componente_isolado_com_previa_de_estados(self):
        self.assertTrue(trecho_com(modo('componente'), r'previa', r'estado'))

    def test_ajustes_cobre_os_oito_com_passos_3_e_5(self):
        texto = modo('ajustes')
        secoes = {}
        for nivel in (2, 3):
            for t, c, _, _ in tr.blocos(texto, nivel):
                for nome in AJUSTES:
                    if re.search(rf'\b{nome}\b', tr.norm(t)):
                        secoes.setdefault(nome, tr.norm(c))
        self.assertEqual(sorted(set(AJUSTES) - set(secoes)), [])
        for nome, corpo in secoes.items():
            self.assertRegex(corpo, r'\bpassos?\b[^.\n]*\b3\b', nome)
            self.assertRegex(corpo, r'\bpassos?\b[^.\n]*\b5\b', nome)


if __name__ == '__main__':
    unittest.main()
