"""Etapas 6 a 8: as nove referências da spec (slop, tipografia, cor, layout, movimento,
componentes, ux, verificacao, fontes), com fontes.md registrando cada contradição resolvida."""
import json
import os
import re
import subprocess
import unicodedata
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(RAIZ, 'referencias')
X = os.path.expanduser('~/Code/ux-lab/vendor')
SLOP_TEST = os.path.join(X, 'hallmark', 'references', 'slop-test.md')
ANTIPATTERNS = os.path.join(X, 'impeccable', 'crates', 'live', 'assets', 'antipatterns.json')

# Formato que o teste lê.
#
# Arquivo de regras (referencias/<nome>.md, prefixo em ARQUIVOS):
#   - Regra = item de lista no nível zero que começa pelo id: `- **TIP-01** texto` (ou `- TIP-01 texto`).
#     Linhas seguintes recuadas com espaço continuam o mesmo item; linha em branco ou não recuada encerra.
#   - Fora de `## Por tipo de tela`, todo item de lista no nível zero é regra e começa pelo id.
#     Sub-itens recuados são livres.
#   - Uma seção `## Por tipo de tela` com `### Persuadir`, `### Operar`, `### Ler`, `### Experiência`,
#     cada uma com conteúdo. Lá dentro os itens NÃO começam por id (cite o id no meio da linha,
#     "vale TIP-03"); id no começo de item conta como regra e duplicaria.
#   - Id `<PREFIXO>-NN` (2+ dígitos), prefixo do próprio arquivo, único entre todos os arquivos.
#   - No máximo 400 linhas; fontes.md, no máximo 700 (LIMITE_FONTES).
#
# slop.md, itens com gate:
#   - Cada gate citado como `gate N` (um por número: "gate 3, gate 4", não "gates 3–4").
#   - Item que cita gate traz exatamente um marcador: `[detector]` ou `[olho]`.
#   - Item `[detector]` nomeia entre crases o id de uma regra de antipatterns.json (campo "id"),
#     ex.: `gradient-text`.
#   - Todo gate numerado de X/hallmark/references/slop-test.md aparece em alguma regra.
#     Atenção: o título do arquivo diz 58, mas a lista numerada vai de 1 a 57; vale a lista.
#
# fontes.md, uma entrada por contradição:
#   ### Inter no corpo
#   - A: hallmark proíbe no display, `X/hallmark/references/typography.md:12`
#   - B: taste usa como padrão, `X/taste-skill/skills/taste-skill/SKILL.md:88-90`
#   - Decisão: permitida em Operar, proibida no display de Persuadir.
#   - Desempate: tipo de tela
#
#   - Entrada = título `###` (pode haver `##` agrupando temas). Mínimo MIN_ENTRADAS entradas.
#   - Linhas `A:` e `B:` (um `- ` antes é aceito), cada uma com ao menos uma citação
#     `X/<pasta da fonte>/<caminho>:<linha>` ou `:<linha>-<linha>`; arquivo e linha existem em X.
#     A e B citam lugares diferentes (contradição interna de uma fonte: mesmo arquivo, linhas diferentes).
#   - `Decisão:` com texto; `Desempate:` começando por um dos níveis: tipo de tela, verificável, hallmark.
#   - Cada tema de TEMAS_MINIMOS casa com uma entrada distinta pelo título (sem caixa nem acento;
#     todas as expressões do tema precisam casar).
#   - Nenhum arquivo em referencias/ cita ~/.claude, .claude/skills/hallmark ou `H/`.
#
# layout.md e movimento.md, botões do taste:
#   - O primeiro `##` do arquivo é `## Botões`. Cita a origem `X/taste-skill/skills/taste-skill/SKILL.md:45-78`
#     e usa os nomes exatos VARIACAO, MOVIMENTO, DENSIDADE (caixa alta, sem acento).
#   - Uma tabela markdown em `## Botões`: cabeçalho com uma coluna por botão (a célula contém o nome) e
#     uma linha por tipo de tela (primeira célula = Persuadir, Operar, Ler ou Experiência; `**` aceito),
#     cada célula de botão um inteiro só, de 1 a 10 (faixa como `5-6` não vale).
#   - Fora de `## Botões`, cada um dos três nomes aparece numa regra seguido de número em até 15
#     caracteres (`VARIACAO ≥ 7`, `DENSIDADE 1-3`). Nada de alias: VARIAÇÃO, DESIGN_VARIANCE etc.
#
# componentes.md e o shadcn:
#   - Comandos escritos por inteiro: `npx shadcn@4.21.0 search @shadcn <termo>`, `... view`, `... docs`,
#     `... add` com `--dry-run` numa linha antes da linha do `add` sem ele, e `... init` numa linha que
#     cita `components.json`.
#   - A proibição da tag solta se escreve sem formar chamada: "nunca `@latest`", nunca `shadcn@latest`.
#   - Chamada = `shadcn@<versão>` ou `npx|bunx|pnpx|dlx|bun x` seguido de `shadcn`; a versão tem de ser
#     4.21.0. Vale para os arquivos do git (rastreados e novos não ignorados), fora de docs/, test/ e
#     ferramentas/uupm/ (cópia byte a byte de X, conferida por test_uupm.py).
#   - Lucide como padrão: uma regra com `lucide` e `padrão` na mesma linha, sem "só a pedido" nela.
#
# Trecho = parágrafo, item de lista (com continuação recuada) ou título. Frase = pedaço de trecho
# entre `. `, `;` ou quebra de linha. Negação = nao, nunca, sem ou jamais na mesma frase.
#
# ux.md:
#   - Regras citam os estados vazio, erro, carregando, sucesso, desabilitado e foco; formulário;
#     teclado e leitor de tela (ou `aria-`).
#   - Ação destrutiva numa frase só por caso: "reversível ... desfazer" e "irreversível ... confirmação".
#   - Seção `## Crítica heurística` com 10 regras, cada uma com `heurística N` (1 a 10, uma vez cada),
#     o nome da heurística de Nielsen e `Olhar:` seguido do que conferir na tela.
#
# verificacao.md:
#   - Seção `## Rodada` com os passos na ordem: `browser_take_screenshot`, `take_snapshot`,
#     `get_css_styles`, `list_console_messages`, `lighthouse_audit`, `ferramentas/impeccable/detectar`,
#     `[olho]`, `ux.md`, `rotacao.json` (vale a primeira menção de cada um dentro da seção).
#   - Toda menção a `ferramentas/impeccable/detectar` é o comando inteiro, terminando na URL:
#     `ferramentas/impeccable/detectar --json --viewport 375x812 <url>` (e 1440x900).
#   - Tipo de tela escrito com maiúscula (Persuadir, Operar, Ler, Experiência). Frase que cita
#     `lighthouse_audit` ou `rotacao.json` junto de um tipo onde ele não roda leva negação.
#   - Ferramenta de ação do Chrome DevTools (`click`, `resize_page`, `take_screenshot`...) só aparece
#     em frase com negação; frase que fala em fechar o Chrome DevTools (ou `close_page`) também.

ARQUIVOS = {'slop': 'SLOP', 'tipografia': 'TIP', 'cor': 'COR',
            'layout': 'LAY', 'movimento': 'MOV', 'componentes': 'COMP',
            'ux': 'UX', 'verificacao': 'VER'}
NOVE = list(ARQUIVOS) + ['fontes']
MIN_ENTRADAS = 64
LIMITE_LINHAS = 400
# fontes.md é registro de auditoria que o fluxo não abre; o limite de 400 mede custo de carregar
LIMITE_FONTES = 700
TIPOS = ['Persuadir', 'Operar', 'Ler', 'Experiência']
NIVEIS = ('tipo de tela', 'verificavel', 'hallmark')
TEMAS_MINIMOS = {
    'Inter': [r'\binter\b'],
    'Geist': [r'\bgeist'],
    'Fraunces': [r'\bfraunces'],
    'serif padrão': [r'\bserif', r'\bpadrao'],
    'número de famílias': [r'\bfamilias'],
    'escala de tamanhos': [r'\bescala', r'\btamanho'],
    'peso de título': [r'\bpeso'],
    'itálico': [r'\bitalico'],
    'travessão': [r'\btravessao'],
    'ponto médio': [r'\bponto medio'],
    'glifo como ícone': [r'\bglifo'],
    'emoji': [r'\bemoji'],
    'espaço de cor': [r'\bespaco de cor'],
    'dose de acento': [r'\bdose'],
    'neutros': [r'\bneutro'],
    'branco puro': [r'\bbranco puro'],
    'creme': [r'\bcreme'],
    'gradientes': [r'\bgradiente'],
    'modo escuro': [r'\bmodo escuro'],
    'acento no escuro': [r'\bacento', r'\bescuro'],
    'Space Grotesk/Plus Jakarta/Outfit': [r'\bspace grotesk'],
    'pilha do sistema': [r'\bpilha'],
    'tracking e entrelinha do display': [r'\btracking'],
    'tamanho máximo do display': [r'\btamanho maximo'],
    'tamanho mínimo de texto': [r'\btamanho minimo'],
    'texto claro no escuro': [r'\btexto claro'],
    'alvo de contraste do corpo': [r'\bcontraste'],
    # etapa 7
    'centralização': [r'\bcentraliza'],
    'eyebrow': [r'\beyebrow'],
    'números de seção': [r'\bnumero', r'\bseca'],
    'card aninhado': [r'\bcard', r'\baninhad'],
    'raio': [r'\braio'],
    'escala de espaço': [r'\bescala', r'\bespaco'],
    'breakpoints': [r'\bbreakpoint'],
    'z-index': [r'\bz-index'],
    'sombras': [r'\bsombra'],
    'janela falsa': [r'\bjanela falsa'],
    'texto do hero': [r'\bhero'],
    'navegação': [r'\bnavegac'],
    'imagem': [r'\bimage'],
    'conteúdo inventado': [r'\binventad'],
    'propriedades animadas': [r'\bpropriedade'],
    'durações': [r'\bduraca'],
    'easing': [r'\beasing'],
    'reveal no scroll': [r'\breveal'],
    'stagger': [r'\bstagger'],
    'movimento reduzido': [r'\breduzid'],
    'parallax': [r'\bparallax'],
    'marquee': [r'\bmarquee'],
    'mudança instantânea': [r'\binstantane'],
    'listener de scroll': [r'\blistener'],
    'Lucide': [r'\blucide'],
    'SVG desenhado à mão': [r'\bsvg'],
    # etapa 8
    'ação destrutiva': [r'\bdestrutiv'],
    'feedback de sucesso': [r'\bsucesso'],
    'duração de toast': [r'\btoast'],
    'indicador de carregamento': [r'\bcarregamento'],
    'alvo de toque': [r'\btoque'],
    'escala ao pressionar': [r'\bpression'],
    'perguntas antes de desenhar': [r'\bpergunta'],
    'rodadas de verificação': [r'\brodada'],
    'metadado no código': [r'\bmetadado'],
    'insistência do usuário': [r'\binsist'],
    'escolha de design system': [r'\bdesign system'],
}
# gates que o detector cobre sem dúvida; pegam um slop.md todo marcado [olho]
DETECTOR_CERTO = {2: 'gradient-text', 4: 'nested-cards', 5: 'side-tab'}

ID = re.compile(r'^[-*] +\*{0,2}([A-Z]+-\d{2,})\b')
GATE = re.compile(r'\bgate (\d+)\b', re.I)
CITACAO = re.compile(r'(?<![\w/])X/([\w.\-]+/[^\s:`)\]]+):(\d+)(?:[-–](\d+))?')
PROIBIDO_H = re.compile(r'~/\.claude|\.claude/skills/hallmark|(?<![\w/.~])H/')
BOTOES = ['VARIACAO', 'MOVIMENTO', 'DENSIDADE']
ALIAS_BOTAO = re.compile(r'VARIAÇÃO|DENSIDADE_|DESIGN_VARIANCE|MOTION_INTENSITY|VISUAL_DENSITY|LAYOUT_VARIANCE|ANIM_LEVEL')
TASTE = 'taste-skill/skills/taste-skill/SKILL.md'
SHADCN = 'npx shadcn@4.21.0'
SHADCN_VERSAO = re.compile(r'\bshadcn@([\w.\-]*)', re.I)
SHADCN_SEM_VERSAO = re.compile(r'\b(?:npx|bunx|pnpx|dlx|bun x)\s+(?:-\S+\s+)*shadcn\b(?!@)', re.I)
FORA_DA_VARREDURA = ('docs/', 'test/', 'ferramentas/uupm/')


def ler(caminho):
    with open(caminho, encoding='utf-8') as f:
        return f.read()


def ref(nome):
    return ler(os.path.join(REF, nome + '.md'))


def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c)).lower()


def blocos(texto, nivel):
    """[(título, corpo, início, fim)] dos títulos de exatamente `nivel` #."""
    marcas = list(re.finditer(r'^(#{1,6}) +(.+?)\s*$', texto, flags=re.M))
    saida = []
    for i, m in enumerate(marcas):
        if len(m.group(1)) != nivel:
            continue
        fim = next((n.start() for n in marcas[i + 1:] if len(n.group(1)) <= nivel), len(texto))
        saida.append((m.group(2), texto[m.end():fim], m.start(), fim))
    return saida


def por_tipo(texto):
    achados = [b for b in blocos(texto, 2) if b[0] == 'Por tipo de tela']
    return achados[0] if achados else None


def fora_por_tipo(texto):
    b = por_tipo(texto)
    return texto if b is None else texto[:b[2]] + texto[b[3]:]


def itens(texto):
    """Itens de lista no nível zero, com as linhas recuadas que os continuam."""
    saida, atual = [], None
    for linha in texto.splitlines():
        if re.match(r'^[-*] ', linha):
            atual = [linha]
            saida.append(atual)
        elif atual is not None and linha.strip() and linha[0] in ' \t':
            atual.append(linha)
        else:
            atual = None
    return ['\n'.join(i) for i in saida]


def regras(texto):
    return [i for i in itens(fora_por_tipo(texto)) if ID.match(i)]


def campo(corpo, nome):
    m = re.search(rf'^(?:[-*] +)?{nome}: *(.*?)\s*$', corpo, flags=re.M)
    return m.group(1) if m else None


def entradas():
    return [(t, c) for t, c, _, _ in blocos(ref('fontes'), 3)]


def secao(texto, titulo):
    achados = [b for b in blocos(texto, 2) if b[0] == titulo]
    return achados[0] if achados else None


def fora_botoes(texto):
    b = secao(texto, 'Botões')
    return texto if b is None else texto[:b[2]] + texto[b[3]:]


def tabela(corpo):
    """Linhas de tabela markdown como listas de células, sem a linha separadora."""
    linhas = [l.strip().strip('|') for l in corpo.splitlines() if l.strip().startswith('|')]
    celulas = [[c.strip() for c in l.split('|')] for l in linhas]
    return [c for c in celulas if not all(re.fullmatch(r':?-+:?', x) for x in c if x)]


def chamadas_erradas(texto):
    """Chamadas do shadcn sem a versão travada 4.21.0."""
    erradas = [m.group(0) for m in SHADCN_VERSAO.finditer(texto) if m.group(1).rstrip('.') != '4.21.0']
    return erradas + [m.group(0) for m in SHADCN_SEM_VERSAO.finditer(texto)]


def arquivos_do_repo():
    saida = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
                           cwd=RAIZ, capture_output=True, text=True, check=True).stdout
    return [a for a in saida.splitlines() if a and not a.startswith(FORA_DA_VARREDURA)
            and os.path.isfile(os.path.join(RAIZ, a))]


def ids_antipatterns():
    with open(ANTIPATTERNS, encoding='utf-8') as f:
        return {r['id'] for r in json.load(f)}


def gates_da_fonte():
    return {int(n) for n in re.findall(r'^(\d+)\. ', ler(SLOP_TEST), flags=re.M)}


def emparelha(candidatos):
    """Casa cada tema com um título distinto (caminho aumentante). Devolve os temas sem par."""
    dono = {}

    def tenta(tema, vistos):
        for j in candidatos[tema]:
            if j not in vistos:
                vistos.add(j)
                if j not in dono or tenta(dono[j], vistos):
                    dono[j] = tema
                    return True
        return False

    return [t for t in candidatos if not tenta(t, set())]


def sem_acento(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


def trechos(texto):
    """Parágrafos, itens de lista (com a continuação recuada) e títulos, sem acento e em minúsculas."""
    partes = re.split(r'\n\s*\n|\n(?=[-*] |\d+\. |#)', texto)
    return [norm(re.sub(r'\n[ \t]+', ' ', p)) for p in partes if p.strip()]


def frases(texto):
    """Frases sem acento, com a caixa original (o tipo de tela se reconhece pela maiúscula)."""
    corrido = sem_acento(re.sub(r'\n[ \t]+', ' ', texto))
    return [f for f in re.split(r'\.(?=\s|$)|;|\n', corrido) if f.strip()]


def abre_file(texto):
    """Frases que citam `file://` sem negar nem dizer que a ferramenta recusa: uma instrução de abrir."""
    return [f.strip() for f in frases(texto) if 'file://' in f and not RECUSA.search(f)]


NEGA = re.compile(r'\b(nao|nunca|sem|jamais)\b', re.I)
TIPO_RE = {'Persuadir': r'\bPersuadir\b', 'Operar': r'\bOperar\b', 'Ler': r'\bLer\b',
           'Experiência': r'\bExperiencia\b'}
PLAYWRIGHT_README = os.path.join(X, 'playwright-mcp', 'README.md')
DEVTOOLS_REF = os.path.join(X, 'chrome-devtools-mcp', 'docs', 'tool-reference.md')
DETECTAR = re.compile(r'ferramentas/impeccable/detectar\b([^`\n]*)')
# Chrome DevTools só lê: estas agem na página ou duplicam o Playwright
DEVTOOLS_ACAO = ['click', 'click_at', 'drag', 'fill', 'fill_form', 'hover', 'press_key', 'type_text',
                 'upload_file', 'handle_dialog', 'resize_page', 'emulate', 'take_screenshot']
DEVTOOLS_LEITURA = ['take_snapshot', 'get_css_styles', 'list_console_messages', 'lighthouse_audit',
                    'performance_start_trace']
PLAYWRIGHT_ACAO = ['browser_navigate', 'browser_click', 'browser_resize', 'browser_take_screenshot']
PASSOS = [('prints do Playwright', r'\bbrowser_take_screenshot\b'),
          ('take_snapshot', r'(?<![\w])take_snapshot\b'),
          ('get_css_styles', r'\bget_css_styles\b'),
          ('list_console_messages', r'\blist_console_messages\b'),
          ('lighthouse_audit', r'\blighthouse_audit\b'),
          ('detector', r'ferramentas/impeccable/detectar'),
          ('itens [olho] do slop.md', r'\[olho\]'),
          ('lista de ux.md', r'\bux\.md\b'),
          ('rotacao.json', r'\brotacao\.json\b')]
# Etapa 14: o Playwright MCP recusa file://; a URL das três ferramentas é a do servidor HTTP local
SERVIDOR = re.compile(r'python3 -m http\.server <porta> --bind 127\.0\.0\.1')
URL_SERVIDOR = re.compile(r'http://127\.0\.0\.1:<porta>/<[^>\s]+>\.html')
RECUSA = re.compile(r'\b(nao|nunca|sem|jamais|recus\w*|bloque\w*)\b', re.I)
PARAR = re.compile(r'\bpar(e|ar)\b|\bencerr|\bdesligu?e|\bderrub|\bkill|\bmat(e|ar)\b|taskstop')
TMP = re.compile(r'/tmp\b|/private/|scratchpad')
POS_3A = re.compile(r'(depois|apos) d[ae] (3a|terceira) rodada')
HEURISTICAS = {1:r'status|estado do sistema|visibilidade', 2: r'mundo real', 3: r'controle|liberdade',
               4: r'consistencia|padroes', 5: r'prevencao|prevenir', 6: r'reconhec|memoriz|lembrar',
               7: r'flexibilidade|eficiencia', 8: r'estetic|minimalis', 9: r'recupera|diagnostic',
               10: r'ajuda|documentacao'}


class TestArquivos(unittest.TestCase):
    def test_as_nove_da_spec_existem(self):
        for nome in NOVE:
            with self.subTest(arquivo=nome):
                self.assertTrue(os.path.isfile(os.path.join(REF, nome + '.md')), f'referencias/{nome}.md não existe')

    def test_limite_de_linhas(self):
        for nome in NOVE:
            with self.subTest(arquivo=nome):
                limite = LIMITE_FONTES if nome == 'fontes' else LIMITE_LINHAS
                self.assertLessEqual(len(ref(nome).splitlines()), limite)

    def test_nenhum_cita_h(self):
        for nome in sorted(os.listdir(REF)):
            if nome.endswith('.md'):
                with self.subTest(arquivo=nome):
                    achado = PROIBIDO_H.search(ler(os.path.join(REF, nome)))
                    self.assertIsNone(achado, f'{nome} cita H: {achado and achado.group(0)}')


class TestPorTipoDeTela(unittest.TestCase):
    def test_quatro_subsecoes_com_conteudo(self):
        for nome in ARQUIVOS:
            texto = ref(nome)
            self.assertEqual([t for t, *_ in blocos(texto, 2)].count('Por tipo de tela'), 1,
                             f'{nome}.md: precisa de uma seção ## Por tipo de tela')
            sub = {t: c for t, c, _, _ in blocos(por_tipo(texto)[1], 3)}
            for tipo in TIPOS:
                with self.subTest(arquivo=nome, tipo=tipo):
                    self.assertIn(tipo, sub, f'{nome}.md sem ### {tipo}')
                    self.assertTrue(sub[tipo].strip(), f'{nome}.md: ### {tipo} vazia')


class TestIds(unittest.TestCase):
    def test_todo_item_fora_de_por_tipo_e_regra_com_id(self):
        for nome in ARQUIVOS:
            for item in itens(fora_por_tipo(ref(nome))):
                with self.subTest(arquivo=nome, item=item.splitlines()[0][:60]):
                    self.assertRegex(item, ID)

    def test_prefixo_do_proprio_arquivo(self):
        for nome, prefixo in ARQUIVOS.items():
            ids = [ID.match(r).group(1) for r in regras(ref(nome))]
            with self.subTest(arquivo=nome):
                self.assertTrue(ids, f'{nome}.md sem regras')
                self.assertEqual([i for i in ids if not i.startswith(prefixo + '-')], [])

    def test_nenhum_id_repetido_entre_arquivos(self):
        vistos = {}
        for nome in ARQUIVOS:
            for r in regras(ref(nome)):
                i = ID.match(r).group(1)
                with self.subTest(id=i):
                    self.assertNotIn(i, vistos, f'{i} em {nome}.md e {vistos.get(i)}.md')
                vistos[i] = nome


class TestDecisoesFixadas(unittest.TestCase):
    def test_tipografia_permite_fontes_acusadas_por_tipo_de_tela(self):
        linhas = norm(por_tipo(ref('tipografia'))[1]).splitlines()
        for fonte in ['geist', 'fraunces', 'space grotesk']:
            with self.subTest(fonte=fonte):
                permite = [l for l in linhas if fonte in l and 'permit' in l
                           and 'nao permit' not in l and 'proib' not in l]
                self.assertTrue(permite, f'Por tipo de tela não permite {fonte} em nenhum tipo')

    def test_tipografia_remete_as_excecoes_do_detector(self):
        self.assertIn('ferramentas/impeccable/excecoes.json', ref('tipografia'))

    def test_slop_permite_travessao_com_moderacao(self):
        itens_travessao = [norm(r) for r in regras(ref('slop')) if 'travessao' in norm(r)]
        self.assertTrue(itens_travessao, 'nenhuma regra de slop.md trata travessão')
        self.assertTrue([r for r in itens_travessao if 'moderacao' in r and 'proibid' not in r],
                        'travessão deve ser permitido com moderação, não proibido')

    def test_cor_trata_modo_escuro_por_tipo(self):
        sub = {t: norm(c) for t, c, _, _ in blocos(por_tipo(ref('cor'))[1], 3)}
        for tipo in ['Persuadir', 'Operar', 'Ler']:
            with self.subTest(tipo=tipo):
                self.assertIn('escuro', sub.get(tipo, ''), f'### {tipo} não decide o modo escuro')

    def test_cor_operar_ganha_os_dois_modos(self):
        operar = norm(dict((t, c) for t, c, _, _ in blocos(por_tipo(ref('cor'))[1], 3)).get('Operar', ''))
        dois = [l for l in operar.splitlines() if 'escuro' in l
                and re.search(r'os dois|ambos|claro e escuro|escuro e claro', l)]
        self.assertTrue(dois, '### Operar deve dar os dois modos, claro e escuro')


class TestSlopGates(unittest.TestCase):
    def itens_com_gate(self):
        return [r for r in regras(ref('slop')) if GATE.search(r)]

    def test_item_com_gate_tem_um_marcador(self):
        itens_gate = self.itens_com_gate()
        self.assertTrue(itens_gate, 'slop.md não cita gate nenhum')
        for r in itens_gate:
            with self.subTest(item=r.splitlines()[0][:60]):
                self.assertEqual(('[detector]' in r) + ('[olho]' in r), 1)

    def test_detector_certo_nos_gates_obvios(self):
        itens_gate = self.itens_com_gate()
        for gate, regra in DETECTOR_CERTO.items():
            with self.subTest(gate=gate):
                self.assertTrue([r for r in itens_gate if gate in map(int, GATE.findall(r))
                                 and '[detector]' in r and f'`{regra}`' in r],
                                f'gate {gate} deveria ser [detector] com `{regra}`')

    @unittest.skipUnless(os.path.isfile(ANTIPATTERNS), 'X/impeccable/.../antipatterns.json sumiu; regras sem como conferir')
    def test_detector_nomeia_regra_que_existe(self):
        validas = ids_antipatterns()
        for r in self.itens_com_gate():
            if '[detector]' in r:
                with self.subTest(item=r.splitlines()[0][:60]):
                    self.assertTrue(set(re.findall(r'`([a-z0-9-]+)`', r)) & validas,
                                    'item [detector] sem regra de antipatterns.json entre crases')

    @unittest.skipUnless(os.path.isfile(SLOP_TEST), 'X/hallmark/references/slop-test.md sumiu; gates sem como conferir')
    def test_cita_todos_os_gates_e_so_eles(self):
        fonte = gates_da_fonte()
        citados = {int(n) for r in self.itens_com_gate() for n in GATE.findall(r)}
        self.assertEqual(sorted(fonte - citados), [], 'gates da fonte sem regra em slop.md')
        self.assertEqual(sorted(citados - fonte), [], 'gates citados que não existem na fonte')


class TestFontes(unittest.TestCase):
    def test_numero_minimo_de_entradas(self):
        self.assertGreaterEqual(len(entradas()), MIN_ENTRADAS)

    def test_temas_minimos_cada_um_na_sua_entrada(self):
        titulos = [norm(t) for t, _ in entradas()]
        candidatos = {tema: [j for j, t in enumerate(titulos) if all(re.search(p, t) for p in pads)]
                      for tema, pads in TEMAS_MINIMOS.items()}
        self.assertEqual(emparelha(candidatos), [], 'temas sem entrada própria em fontes.md')

    def test_cada_entrada_cita_duas_versoes_diferentes(self):
        for titulo, corpo in entradas():
            with self.subTest(entrada=titulo):
                a, b = campo(corpo, 'A'), campo(corpo, 'B')
                self.assertIsNotNone(a, 'sem linha A:')
                self.assertIsNotNone(b, 'sem linha B:')
                ca, cb = set(CITACAO.findall(a)), set(CITACAO.findall(b))
                self.assertTrue(ca, f'A sem citação X/<fonte>/<arquivo>:<linha>: {a}')
                self.assertTrue(cb, f'B sem citação X/<fonte>/<arquivo>:<linha>: {b}')
                self.assertNotEqual(ca, cb, 'A e B citam o mesmo lugar')

    def test_decisao_e_nivel_de_desempate(self):
        for titulo, corpo in entradas():
            with self.subTest(entrada=titulo):
                self.assertTrue(campo(corpo, 'Decisão'), 'sem Decisão: com texto')
                desempate = norm(campo(corpo, 'Desempate') or '')
                self.assertTrue(desempate.startswith(NIVEIS), f'Desempate fora de {NIVEIS}: {desempate!r}')

    def test_cita_hallmark_em_x(self):
        self.assertIn('X/hallmark/', ref('fontes'))

    @unittest.skipUnless(os.path.isdir(X), f'{X} sumiu; citações sem como conferir')
    def test_citacoes_apontam_para_arquivo_e_linha_que_existem(self):
        for caminho, ini, fim in set(CITACAO.findall(ref('fontes'))):
            with self.subTest(citacao=f'X/{caminho}:{ini}'):
                completo = os.path.join(X, caminho)
                self.assertTrue(os.path.isfile(completo), f'X/{caminho} não existe')
                total = len(ler(completo).splitlines())
                self.assertLessEqual(int(fim or ini), total, f'X/{caminho} tem {total} linhas')
                self.assertGreaterEqual(int(ini), 1)


class TestBotoes(unittest.TestCase):
    ARQS = ['layout', 'movimento']

    def botoes(self, nome):
        b = secao(ref(nome), 'Botões')
        self.assertIsNotNone(b, f'{nome}.md sem ## Botões')
        return b[1]

    def test_abre_com_botoes(self):
        for nome in self.ARQS:
            with self.subTest(arquivo=nome):
                h2 = [t for t, *_ in blocos(ref(nome), 2)]
                self.assertTrue(h2 and h2[0] == 'Botões', f'{nome}.md: primeiro ## deve ser Botões, é {h2[:1]}')

    def test_botoes_cita_origem_no_taste(self):
        for nome in self.ARQS:
            with self.subTest(arquivo=nome):
                linhas = [(int(i), int(f or i)) for c, i, f in CITACAO.findall(self.botoes(nome))
                          if c == TASTE]
                self.assertTrue([1 for i, f in linhas if i <= 78 and f >= 45],
                                f'## Botões não cita X/{TASTE}:45-78')

    def test_tabela_padrao_por_tipo_de_tela(self):
        for nome in self.ARQS:
            linhas = tabela(self.botoes(nome))
            self.assertTrue(linhas, f'{nome}.md: ## Botões sem tabela')
            cab = linhas[0]
            coluna = {b: next((j for j, c in enumerate(cab) if b in c), None) for b in BOTOES}
            for botao, j in coluna.items():
                with self.subTest(arquivo=nome, botao=botao):
                    self.assertIsNotNone(j, f'cabeçalho da tabela sem coluna {botao}')
            for tipo in TIPOS:
                with self.subTest(arquivo=nome, tipo=tipo):
                    achadas = [l for l in linhas[1:] if l and norm(l[0].strip('*` ')) == norm(tipo)]
                    self.assertEqual(len(achadas), 1, f'tabela precisa de uma linha {tipo}')
                    for botao, j in coluna.items():
                        valor = achadas[0][j].strip('*` ') if j is not None and j < len(achadas[0]) else ''
                        self.assertRegex(valor, r'^(10|[1-9])$', f'{tipo}/{botao}: {valor!r} não é inteiro de 1 a 10')

    def test_nomes_dos_botoes_em_botoes(self):
        for nome in self.ARQS:
            corpo = self.botoes(nome)
            for botao in BOTOES:
                with self.subTest(arquivo=nome, botao=botao):
                    self.assertRegex(corpo, rf'\b{botao}\b')

    def test_regras_fora_de_botoes_citam_cada_botao_com_faixa(self):
        for nome in self.ARQS:
            fora = regras(fora_botoes(ref(nome)))
            for botao in BOTOES:
                with self.subTest(arquivo=nome, botao=botao):
                    self.assertTrue([r for r in fora if re.search(rf'\b{botao}\b[^\n]{{0,15}}?\d', r)],
                                    f'{nome}.md: nenhuma regra fora de ## Botões liga ou desliga por {botao} N')

    def test_sem_alias_dos_botoes(self):
        for nome in self.ARQS:
            with self.subTest(arquivo=nome):
                achado = ALIAS_BOTAO.search(fora_botoes(ref(nome)))
                self.assertIsNone(achado, f'{nome}.md usa alias {achado and achado.group(0)}; use {BOTOES}')


class TestLayout(unittest.TestCase):
    def test_cobre_espacamento_responsivo_e_z_index(self):
        texto = norm('\n'.join(regras(ref('layout'))))
        for tema, pad in [('espaçamento', r'\bespacamento'), ('responsivo', r'\bresponsiv'),
                          ('z-index', r'\bz-index')]:
            with self.subTest(tema=tema):
                self.assertRegex(texto, pad, f'layout.md sem regra de {tema}')


class TestComponentes(unittest.TestCase):
    def linhas(self):
        return ref('componentes').splitlines()

    def test_remete_ao_catalogo(self):
        self.assertIn('catalogo/components/', ref('componentes'))

    def test_lucide_e_o_icone_padrao(self):
        linhas = [norm(l) for r in regras(ref('componentes')) for l in r.splitlines()]
        self.assertTrue([l for l in linhas if 'lucide' in l and re.search(r'\bpadrao\b', l)
                         and 'so a pedido' not in l], 'componentes.md não fixa Lucide como padrão')

    def test_react_usa_shadcn(self):
        self.assertTrue([l for l in self.linhas() if 'React' in l and 'shadcn' in l],
                        'componentes.md não diz que projeto React usa shadcn')

    def test_fluxo_do_cli_travado(self):
        texto = ref('componentes')
        for cmd in [f'{SHADCN} search @shadcn', f'{SHADCN} view', f'{SHADCN} docs', f'{SHADCN} init']:
            with self.subTest(comando=cmd):
                self.assertIn(cmd, texto)

    def test_add_dry_run_antes_do_add(self):
        adds = [(i, '--dry-run' in l) for i, l in enumerate(self.linhas()) if f'{SHADCN} add' in l]
        seco = [i for i, d in adds if d]
        real = [i for i, d in adds if not d]
        self.assertTrue(seco, f'sem `{SHADCN} add ... --dry-run`')
        self.assertTrue(real, f'sem `{SHADCN} add` sem --dry-run')
        self.assertLess(seco[0], real[0], 'add --dry-run vem antes do add')

    def test_init_quando_falta_components_json(self):
        self.assertTrue([l for l in self.linhas() if 'components.json' in l and f'{SHADCN} init' in l],
                        f'nenhuma linha liga a falta de components.json a `{SHADCN} init`')

    def test_proibe_latest_e_mcp(self):
        linhas = [norm(l) for l in self.linhas()]
        for termo in ['latest', 'mcp']:
            with self.subTest(termo=termo):
                self.assertTrue([l for l in linhas if 'nunca' in l and termo in l], f'não diz "nunca {termo}"')

    def test_nunca_no_estado_padrao(self):
        linhas = [norm(l) for l in self.linhas()]
        self.assertTrue([l for l in linhas if 'nunca' in l and 'estado padrao' in l],
                        'não diz que o componente nunca fica no estado padrão do shadcn')


class TestShadcnTravado(unittest.TestCase):
    def test_reconhece_chamada_errada(self):
        for ruim in ['npx shadcn@latest add button', 'npx shadcn add button', 'pnpm dlx shadcn init',
                     'npx shadcn@4.21 add x', 'bunx --bun shadcn add x']:
            with self.subTest(texto=ruim):
                self.assertTrue(chamadas_erradas(ruim))
        for bom in ['npx shadcn@4.21.0 add button.', 'shadcn: command, dialog', 'shadcn/ui', 'search @shadcn x']:
            with self.subTest(texto=bom):
                self.assertEqual(chamadas_erradas(bom), [])

    def test_toda_chamada_no_repositorio_tem_a_versao_travada(self):
        arquivos = arquivos_do_repo()
        self.assertIn('referencias/componentes.md', arquivos, 'a varredura não chega em referencias/')
        erradas = []
        for rel in arquivos:
            try:
                texto = ler(os.path.join(RAIZ, rel))
            except UnicodeDecodeError:
                continue
            erradas += [f'{rel}: {c}' for c in chamadas_erradas(texto)]
        self.assertEqual(erradas, [])


class TestFontesEtapa7(unittest.TestCase):
    def test_lucide_padrao_contra_taste_so_a_pedido(self):
        achadas = [(t, c) for t, c in entradas() if 'lucide' in norm(t)]
        self.assertTrue(achadas, 'fontes.md sem entrada de Lucide')
        _, corpo = achadas[0]
        citado = [(int(i), int(f or i)) for c, i, f in CITACAO.findall((campo(corpo, 'A') or '') + ' '
                                                                         + (campo(corpo, 'B') or '')) if c == TASTE]
        self.assertTrue([1 for i, f in citado if i <= 623 <= f], f'entrada de Lucide não cita X/{TASTE}:623')
        decisao = norm(campo(corpo, 'Decisão') or '')
        self.assertTrue('lucide' in decisao and 'padrao' in decisao and 'so a pedido' not in decisao,
                        f'Decisão deve fixar Lucide como padrão: {decisao!r}')


class TestFontesEtapa8(unittest.TestCase):
    def test_acao_destrutiva_decide_desfazer_e_confirmacao(self):
        achadas = [c for t, c in entradas() if 'destrutiv' in norm(t)]
        self.assertTrue(achadas, 'fontes.md sem entrada de ação destrutiva')
        decisao = norm(campo(achadas[0], 'Decisão') or '')
        for termo in ['reversive', 'desfazer', 'irreversive', 'confirma']:
            with self.subTest(termo=termo):
                self.assertIn(termo, decisao, f'Decisão de ação destrutiva sem {termo!r}: {decisao!r}')


class TestUx(unittest.TestCase):
    def regras_norm(self):
        return norm('\n'.join(regras(ref('ux'))))

    def test_estados(self):
        texto = self.regras_norm()
        for estado, pad in [('vazio', r'\bvazio'), ('erro', r'\berros?\b'), ('carregando', r'\bcarregand'),
                            ('sucesso', r'\bsucesso'), ('desabilitado', r'\bdesabilitad'), ('foco', r'\bfoco\b')]:
            with self.subTest(estado=estado):
                self.assertRegex(texto, pad, f'ux.md sem regra do estado {estado}')

    def test_formularios(self):
        self.assertRegex(self.regras_norm(), r'\bformulario', 'ux.md sem regra de formulário')

    def test_acessibilidade(self):
        texto = self.regras_norm()
        for tema, pad in [('teclado', r'\bteclado'), ('leitor de tela', r'leitor de tela|\baria-')]:
            with self.subTest(tema=tema):
                self.assertRegex(texto, pad, f'ux.md sem regra de acessibilidade: {tema}')

    def test_acao_destrutiva_reversivel_desfaz_irreversivel_confirma(self):
        fs = [f.lower() for r in regras(ref('ux')) for f in frases(r)]
        self.assertTrue([f for f in fs if re.search(r'(?<!ir)reversive(l|is)\b.*\bdesfaz', f)],
                        'ux.md: ação reversível não leva a desfazer (na mesma frase)')
        self.assertTrue([f for f in fs if re.search(r'irreversive(l|is)\b.*\bconfirma', f)],
                        'ux.md: ação irreversível não leva a confirmação (na mesma frase)')

    def secao_critica(self):
        achadas = [b for b in blocos(ref('ux'), 2) if norm(b[0]).startswith('critica heuristica')]
        self.assertTrue(achadas, 'ux.md sem ## Crítica heurística')
        return regras(achadas[0][1])

    def test_critica_tem_as_10_heuristicas_uma_por_regra(self):
        numeros = [n for r in self.secao_critica() for n in re.findall(r'\bheuristica (\d+)\b', norm(r))]
        self.assertEqual(sorted(map(int, numeros)), list(range(1, 11)),
                         'cada heurística de 1 a 10 citada uma vez (`heurística N`)')

    def test_cada_heuristica_com_nome_e_o_que_olhar(self):
        for r in self.secao_critica():
            texto = norm(re.sub(r'\n[ \t]+', ' ', r))
            ns = re.findall(r'\bheuristica (\d+)\b', texto)
            with self.subTest(regra=r.splitlines()[0][:60]):
                self.assertEqual(len(ns), 1, 'regra da crítica sem `heurística N` (ou com mais de uma)')
                n = int(ns[0])
                self.assertRegex(texto, HEURISTICAS.get(n, r'(?!)'), f'heurística {n} sem o nome de Nielsen')
                self.assertRegex(texto, r'\bolhar: *\S.{19,}', f'heurística {n} sem "Olhar:" e o que conferir')


class TestVerificacao(unittest.TestCase):
    def texto(self):
        return ref('verificacao')

    def trechos_com(self, termo):
        achados = [t for t in trechos(self.texto()) if termo in t]
        self.assertTrue(achados, f'verificacao.md não cita {termo}')
        return achados

    def frases_fora_por_tipo(self, pad):
        return [f for f in frases(fora_por_tipo(self.texto())) if re.search(pad, f)]

    def so_nos_tipos(self, pad, sim):
        fs = self.frases_fora_por_tipo(pad)
        self.assertTrue(fs, f'verificacao.md não cita {pad}')
        self.assertTrue([f for f in fs if all(re.search(TIPO_RE[t], f) for t in sim)],
                        f'nenhuma frase liga {pad} a {" e ".join(sim)}')
        nao = [t for t in TIPOS if t not in sim]
        for f in fs:
            if any(re.search(TIPO_RE[t], f) for t in nao):
                with self.subTest(frase=f[:80]):
                    self.assertRegex(f, NEGA, f'{pad} ligado a {nao} sem negação')
        sub = {t: c for t, c, _, _ in blocos((por_tipo(self.texto()) or ('', '', 0, 0))[1], 3)}
        for t in nao:
            for f in frases(sub.get(t, '')):
                if re.search(pad, f):
                    with self.subTest(tipo=t, frase=f[:80]):
                        self.assertRegex(f, NEGA, f'### {t} usa {pad}')

    def test_passos_da_rodada_na_ordem(self):
        b = secao(self.texto(), 'Rodada')
        self.assertIsNotNone(b, 'verificacao.md sem ## Rodada')
        corpo = norm(b[1])
        posicoes = []
        for nome, pad in PASSOS:
            m = re.search(pad, corpo)
            with self.subTest(passo=nome):
                self.assertIsNotNone(m, f'## Rodada sem o passo {nome}')
            posicoes.append((m.start() if m else -1, nome))
        self.assertEqual([n for _, n in sorted(posicoes)], [n for n, _ in PASSOS], 'passos fora de ordem')

    def test_prints_em_375_e_1440_com_filename(self):
        ts = self.trechos_com('browser_take_screenshot')
        self.assertTrue([t for t in ts if re.search(r'\b375\b', t) and re.search(r'\b1440\b', t)],
                        'prints do Playwright sem as larguras 375 e 1440')
        self.assertTrue([t for t in ts if 'filename' in t], '`browser_take_screenshot` sem `filename`')

    def test_css_de_titulo_corpo_e_botao_principal(self):
        self.assertTrue([t for t in self.trechos_com('take_snapshot') if re.search(r'\buid\b', t)],
                        '`take_snapshot` não aparece como meio de achar o `uid`')
        css = self.trechos_com('get_css_styles')
        for alvo in ['titulo', 'corpo', 'botao principal']:
            with self.subTest(elemento=alvo):
                self.assertTrue([t for t in css if alvo in t], f'`get_css_styles` não confere {alvo}')
        self.assertIn('[overloaded]', self.texto(), 'não explica as declarações vencidas `[overloaded]`')

    def test_console_sem_erro(self):
        self.assertTrue([t for t in self.trechos_com('list_console_messages') if re.search(r'\berros?\b', t)],
                        '`list_console_messages` sem exigir console sem erro')

    def test_lighthouse_so_em_persuadir_e_ler(self):
        self.so_nos_tipos(r'\blighthouse_audit\b', ['Persuadir', 'Ler'])

    def test_rotacao_so_em_persuadir_e_experiencia(self):
        self.so_nos_tipos(r'\brotacao\.json\b', ['Persuadir', 'Experiência'])

    def test_detector_na_pagina_renderizada(self):
        chamadas = DETECTAR.findall(self.texto())
        self.assertTrue(chamadas, 'verificacao.md sem `ferramentas/impeccable/detectar`')
        vistas = set()
        for args in chamadas:
            with self.subTest(chamada=args.strip()[:60]):
                self.assertIn('--json', args)
                vp = re.findall(r'--viewport +(\d+x\d+)', args)
                self.assertTrue(vp, 'chamada sem --viewport LxA')
                vistas.update(vp)
                partes = args.split()
                self.assertTrue(partes and re.match(r'(<url>|https?://)', partes[-1]),
                                f'o detector roda na URL servida por HTTP, não em arquivo: {args.strip()!r}')
        self.assertLessEqual({'375x812', '1440x900'}, vistas, 'detector sem 375x812 e 1440x900')
        ts = self.trechos_com('ferramentas/impeccable/detectar')
        for nome, pad in [('renderizad', r'renderizad'), ('rota', r'\brota\b'),
                          ('servidor HTTP', r'127\.0\.0\.1|servidor http|http\.server')]:
            with self.subTest(termo=nome):
                self.assertTrue([t for t in ts if re.search(pad, t)], f'o passo do detector não cita {nome}')
        self.assertFalse([t for t in ts if 'file://' in t and not RECUSA.search(t)],
                         'o detector ainda roda em `file://`; a URL é a do servidor, a mesma do Playwright')

    def test_sem_react_serve_a_pasta_por_http_local_em_segundo_plano(self):
        ts = [t for t in trechos(self.texto()) if SERVIDOR.search(t)]
        self.assertTrue(ts, 'verificacao.md não manda `python3 -m http.server <porta> --bind 127.0.0.1`')
        self.assertTrue([t for t in ts if re.search(r'segundo plano|run_in_background', t)
                         and re.search(r'sem react|autocontido', t) and re.search(r'pasta', t)],
                        'o servidor não sobe em segundo plano, na pasta do HTML, no projeto sem React')

    def test_mesma_url_do_servidor_no_playwright_devtools_e_detector(self):
        self.assertRegex(self.texto(), URL_SERVIDOR, 'sem a URL `http://127.0.0.1:<porta>/<arquivo>.html`')
        self.assertTrue([t for t in trechos(self.texto()) if URL_SERVIDOR.search(t) and 'playwright' in t
                         and 'devtools' in t and re.search(r'detector|detectar', t)],
                        'não diz que Playwright, Chrome DevTools e detector usam a URL do servidor')

    def test_nenhuma_referencia_manda_abrir_file(self):
        for nome in NOVE:
            with self.subTest(referencia=nome):
                self.assertEqual(abre_file(ref(nome)), [], 'manda abrir `file://`; o Playwright MCP recusa')

    def test_para_o_servidor_ao_terminar(self):
        ts = [t for t in trechos(self.texto()) if re.search(r'\bservidor\b', t) and PARAR.search(t)]
        self.assertTrue(ts, 'verificacao.md não manda parar o servidor HTTP')
        self.assertTrue([t for t in ts if re.search(r'termin|ultima rodada|ao final|\bfim\b', t)],
                        'não diz que o servidor para ao terminar a verificação')

    def test_snapshot_do_devtools_dentro_do_projeto_e_apagado(self):
        self.assertIn('filePath', self.texto(), 'não cita o `filePath` do `take_snapshot`')
        ts = [t for t in trechos(self.texto()) if 'filepath' in t]
        self.assertTrue([t for t in ts if 'take_snapshot' in t and re.search(r'dentro d[ao] (pasta do )?projeto', t)],
                        'não diz que o `filePath` do `take_snapshot` fica dentro da pasta do projeto')
        self.assertTrue([t for t in ts if re.search(r'\bapag|\bremov|\bexclu|\brm\b', t) and re.search(r'\buids?\b', t)],
                        'não diz que o arquivo do snapshot é apagado depois de achar os `uid`')
        for t in ts:
            if TMP.search(t):
                with self.subTest(trecho=t[:80]):
                    self.assertRegex(t, RECUSA, '`filePath` em /tmp ou no scratchpad, fora do projeto')

    def test_correcao_depois_da_3a_rodada_tem_conferencia_completa(self):
        ts = [t for t in trechos(self.texto()) if POS_3A.search(t) and re.search(r'correc|corrig', t)]
        self.assertTrue(ts, 'verificacao.md não diz o que fazer com correção depois da 3ª rodada')
        duas = r'[^.;]*(duas larguras|\b375(x812)?\b[^.;]*\b1440(x900)?\b)'
        exigido = [('prints nas duas larguras', rf'\bprints?\b{duas}'),
                   ('detector nas duas larguras', rf'(detector|detectar){duas}'),
                   ('console sem erro', r'console[^.;]*\berros?\b|\berros?\b[^.;]*console'),
                   ('sobre a versão corrigida', r'corrigid'),
                   ('relatório marca pós-rodada', r'relatorio[^.]*pos[- ]rodada|pos[- ]rodada[^.]*relatorio')]
        for nome, pad in exigido:
            with self.subTest(exige=nome):
                self.assertTrue([t for t in ts if re.search(pad, t)], f'correção pós-3ª rodada sem {nome}')

    def test_alarme_corrigido_ou_refutado_com_prova_na_entrega(self):
        alarmes = self.trechos_com('alarme')
        self.assertTrue([t for t in alarmes if all(p in t for p in ['corrig', 'refut', 'prova', 'get_css_styles', 'print'])],
                        'não diz que todo alarme é corrigido ou refutado com prova (get_css_styles ou print)')
        self.assertTrue([t for t in self.trechos_com('refut') if 'entrega' in t],
                        'não diz que a refutação aparece na entrega')

    def test_contraste_so_se_refuta_com_cores_do_devtools(self):
        fs = [f.lower() for f in frases(self.texto()) if re.search(r'contraste', f, re.I) and re.search(r'refut', f, re.I)]
        self.assertTrue(fs, 'não diz como se refuta alarme de contraste')
        for f in fs:
            with self.subTest(frase=f[:80]):
                self.assertRegex(f, r'devtools|get_css_styles', 'contraste refutado sem o Chrome DevTools')
                self.assertRegex(f, r'\bcor(es)?\b', 'contraste refutado sem as cores efetivas')
                if 'print' in f:
                    self.assertRegex(f, NEGA, 'contraste não se refuta pelo print')

    def test_cita_os_falsos_positivos_do_codigo_fonte(self):
        for issue in ['#633', '#428', '#837']:
            with self.subTest(issue=issue):
                self.assertIn(issue, self.texto())

    def test_tres_rodadas_e_acessibilidade_e_contraste_nunca_sobram(self):
        texto = norm(self.texto())
        self.assertRegex(texto, r'\b(3|tres) rodadas', 'sem o limite de 3 rodadas')
        self.assertNotRegex(texto, r'\b([4-9]|\d{2,}|quatro|cinco) rodadas', 'limite de rodadas não é 3')
        self.assertTrue([t for t in trechos(self.texto()) if 'acessibilidade' in t and 'contraste' in t
                         and 'sobra' in t], 'não diz que acessibilidade e contraste nunca sobram')

    def test_relatorio_lista_ids_do_piso(self):
        self.assertTrue([t for t in self.trechos_com('relatorio') if re.search(r'\bids?\b', t)
                         and '## piso' in t and 'skill.md' in t],
                        'relatório da rodada não lista os ids conferidos (ao menos os do `## Piso` do SKILL.md)')

    def test_playwright_navega_clica_redimensiona_e_fotografa(self):
        texto = self.texto()
        for nome in PLAYWRIGHT_ACAO + ['browser_close']:
            with self.subTest(ferramenta=nome):
                self.assertRegex(texto, rf'\b{nome}\b')

    def test_browser_snapshot_so_para_achar_ref(self):
        self.assertIn('--snapshot-mode none', self.texto())
        fs = [f for f in frases(self.texto()) if 'browser_snapshot' in f]
        self.assertTrue(fs, 'não diz quando usar `browser_snapshot`')
        for f in fs:
            with self.subTest(frase=f[:80]):
                self.assertRegex(f, r'(?i)\bref\b', '`browser_snapshot` fora do caso de achar o `ref`')

    def test_devtools_so_le(self):
        texto = self.texto()
        for nome in DEVTOOLS_LEITURA:
            with self.subTest(le=nome):
                self.assertRegex(texto, rf'(?<![\w]){nome}\b')
        for f in frases(texto):
            for nome in DEVTOOLS_ACAO:
                if f'`{nome}`' in f:
                    with self.subTest(age=nome, frase=f[:80]):
                        self.assertRegex(f, NEGA, f'Chrome DevTools usado para agir: `{nome}`')

    def test_nao_manda_fechar_o_devtools(self):
        for f in frases(self.texto()):
            if re.search(r'devtools|close_page', f, re.I) and re.search(r'\bfech|close_page', f, re.I):
                with self.subTest(frase=f[:80]):
                    self.assertRegex(f, NEGA, 'verificacao.md manda fechar o Chrome DevTools')

    @unittest.skipUnless(os.path.isfile(PLAYWRIGHT_README) and os.path.isfile(DEVTOOLS_REF),
                         'X/playwright-mcp ou X/chrome-devtools-mcp sumiu; nomes sem como conferir')
    def test_nomes_de_ferramenta_existem(self):
        playwright = set(re.findall(r'^- \*\*(browser_\w+)\*\*', ler(PLAYWRIGHT_README), flags=re.M))
        devtools = set(re.findall(r'^### `(\w+)`', ler(DEVTOOLS_REF), flags=re.M))
        for nome in set(re.findall(r'\bbrowser_\w+', self.texto())) | set(PLAYWRIGHT_ACAO):
            with self.subTest(playwright=nome):
                self.assertIn(nome, playwright)
        for nome in DEVTOOLS_LEITURA + DEVTOOLS_ACAO:
            with self.subTest(devtools=nome):
                self.assertIn(nome, devtools)


def entrada_ver(ident):
    """Texto do item `**VER-xx**` de verificacao.md, com a continuação recuada."""
    achados = [i for i in regras(ref('verificacao')) if ID.match(i).group(1) == ident]
    return achados[0] if achados else ''


class TestProvasComNomeFixo(unittest.TestCase):
    """Etapa 19: cada prova da rodada tem nome fixo na pasta da entrega, para um script conferir."""

    def frases_de(self, ident, *padroes):
        texto = entrada_ver(ident)
        self.assertTrue(texto, f'verificacao.md sem {ident}')
        return [f.lower() for f in frases(texto) if all(re.search(p, f.lower()) for p in padroes)]

    def test_ver10_grava_as_duas_saidas_do_detector_com_o_n_dos_prints(self):
        texto = entrada_ver('VER-10')
        for nome in ['r<N>-detector-375.json', 'r<N>-detector-1440.json']:
            with self.subTest(arquivo=nome):
                self.assertIn(nome, texto, f'VER-10 não grava a saída do detector em `{nome}`')
        self.assertTrue(self.frases_de('VER-10', r'pasta da entrega', r'detector-(375|1440)\.json'),
                        'VER-10 não diz que as saídas do detector ficam na pasta da entrega')
        self.assertIn('r<N>-375.png', entrada_ver('VER-05'), 'o N do detector não é o mesmo dos prints de VER-05')

    def test_ver10_reserva_grava_o_filtrar_nos_mesmos_nomes(self):
        self.assertTrue(self.frases_de('VER-10', r'filtrar\.py',
                                       r'detector-(375|1440)\.json|mesmos? (nomes?|arquivos?)'),
                        'na reserva, VER-10 não manda a saída do `filtrar.py` para os mesmos nomes')

    def test_ver16_grava_relatorio_md_na_pasta_da_entrega(self):
        texto = entrada_ver('VER-16')
        self.assertRegex(texto, r'`relatorio\.md`', 'VER-16 não grava o relatório em `relatorio.md`')
        self.assertTrue(self.frases_de('VER-16', r'relatorio\.md', r'pasta da entrega'),
                        'VER-16 não diz que `relatorio.md` fica na pasta da entrega')

    def test_ver16_rodada_nova_reescreve_o_mesmo_relatorio(self):
        self.assertTrue(self.frases_de('VER-16', r'rodada', r'reescrev|sobrescrev|mesmo arquivo'),
                        'VER-16 não diz que a rodada nova reescreve o mesmo `relatorio.md`')
        self.assertNotRegex(entrada_ver('VER-16'), r'r<N>-relatorio|relatorio-r?<N>',
                            'relatório com nome por rodada: o nome é fixo')

    def test_ver05_pasta_da_entrega_no_mockup_e_na_etapa_de_tela(self):
        texto = entrada_ver('VER-05')
        self.assertIn('docs/vesta/mockups/<data>-<feature>/', texto)
        self.assertTrue(self.frases_de('VER-05', r'docs/vesta/mockups/<data>-<feature>/(?!etapa)', r'fase de mockup'),
                        'VER-05 não diz que na fase de mockup a pasta é a do mockup')
        self.assertTrue(self.frases_de('VER-05', r'docs/vesta/mockups/<data>-<feature>/etapa-<id>/',
                                       r'etapa de tela', r'execucao'),
                        'VER-05 não diz que numa etapa de tela da execução a pasta é `.../etapa-<id>/`')


if __name__ == '__main__':
    unittest.main()
