"""Etapa 4: LICENSE próprio, THIRD_PARTY_NOTICES.md com as 8 fontes e textos de licença em licencas/."""
import filecmp
import os
import re
import subprocess
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X = os.path.expanduser('~/Code/ux-lab/vendor')
NOTICES = os.path.join(RAIZ, 'THIRD_PARTY_NOTICES.md')

# Formato que o teste lê em THIRD_PARTY_NOTICES.md, uma seção por fonte:
#
#   ## impeccable
#   Licença: Apache-2.0
#   Repositório: https://github.com/pbakaus/impeccable
#   Commit: 9d715cc
#   Arquivos: licencas/impeccable-LICENSE, licencas/impeccable-NOTICE.md
#
# - Título exato `## <fonte>`, com a fonte escrita como nas chaves de FONTES.
# - Campos em linhas próprias começando por `Licença:`, `Repositório:`, `Commit:` (um `- ` antes é aceito).
# - Licença em SPDX (`MIT`, `Apache-2.0`). Repositório sem `.git` no fim. Commit com 7+ hex.
# - Arquivos de licença citados como caminho `licencas/<nome>` (texto solto ou link markdown).
# - inspo: sem Repositório, Commit nem arquivo; a seção diz "sem código copiado".
FONTES = {
    # fonte: (licença, repositório, pasta em X ou None, arquivo de licença na pasta)
    'hallmark': ('MIT', 'https://github.com/Nutlope/hallmark', None, None),
    'taste-skill': ('MIT', 'https://github.com/Leonxlnx/taste-skill', 'taste-skill', 'LICENSE'),
    'impeccable': ('Apache-2.0', 'https://github.com/pbakaus/impeccable', 'impeccable', 'LICENSE'),
    'ui-ux-pro-max': ('MIT', 'https://github.com/nextlevelbuilder/ui-ux-pro-max-skill',
                      'ui-ux-pro-max-skill', 'LICENSE'),
    'shadcn/ui': ('MIT', 'https://github.com/shadcn-ui/ui', 'ui', 'LICENSE.md'),
    'chrome-devtools-mcp': ('Apache-2.0', 'https://github.com/ChromeDevTools/chrome-devtools-mcp',
                            'chrome-devtools-mcp', 'LICENSE'),
    'playwright-mcp': ('Apache-2.0', 'https://github.com/microsoft/playwright-mcp', 'playwright-mcp', 'LICENSE'),
}
HALLMARK_COMMIT = '13ac0ec'  # não é clone; conferido por igualdade do SKILL.md remoto
TODAS = list(FONTES) + ['inspo']


def secoes():
    with open(NOTICES, encoding='utf-8') as f:
        texto = f.read()
    partes = re.split(r'^## +(.+?)\s*$', texto, flags=re.M)
    return {partes[i]: partes[i + 1] for i in range(1, len(partes), 2)}


def campo(secao, nome):
    m = re.search(rf'^(?:[-*] +)?{nome}: *(.+?)\s*$', secao, flags=re.M)
    return m.group(1) if m else None


def citados(secao):
    return re.findall(r'licencas/[\w.\-]+', secao)


def head(pasta):
    return subprocess.run(['git', '-C', os.path.join(X, pasta), 'rev-parse', 'HEAD'],
                          capture_output=True, text=True, check=True).stdout.strip()


class TestLicencaPropria(unittest.TestCase):
    def test_mit_de_luccas_silveira_2026(self):
        with open(os.path.join(RAIZ, 'LICENSE'), encoding='utf-8') as f:
            texto = f.read()
        self.assertTrue(texto.startswith('MIT License'))
        self.assertIn('Copyright (c) 2026 luccas-silveira', texto)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', texto)


class TestSecoes(unittest.TestCase):
    def test_uma_secao_por_fonte(self):
        s = secoes()
        for fonte in TODAS:
            with self.subTest(fonte=fonte):
                self.assertIn(fonte, s)

    def test_licenca_e_repositorio_certos(self):
        s = secoes()
        for fonte, (licenca, repo, _, _) in FONTES.items():
            with self.subTest(fonte=fonte):
                self.assertEqual(campo(s[fonte], 'Licença'), licenca)
                self.assertEqual(campo(s[fonte], 'Repositório'), repo)

    def test_todas_citam_commit(self):
        s = secoes()
        for fonte in FONTES:
            with self.subTest(fonte=fonte):
                self.assertRegex(campo(s[fonte], 'Commit') or '', r'^[0-9a-f]{7,40}$')

    def test_hallmark_cita_commit_do_nutlope(self):
        self.assertEqual(campo(secoes()['hallmark'], 'Commit'), HALLMARK_COMMIT)

    def test_inspo_isento_e_diz_por_que(self):
        inspo = secoes()['inspo']
        self.assertIn('sem código copiado', inspo)
        self.assertIsNotNone(campo(inspo, 'Licença'))


class TestCommitsDosClones(unittest.TestCase):
    def test_commit_bate_com_head_do_clone(self):
        s = secoes()
        for fonte, (_, _, pasta, _) in FONTES.items():
            if pasta is None:
                continue
            with self.subTest(fonte=fonte):
                if not os.path.isdir(os.path.join(X, pasta, '.git')):
                    self.skipTest(f'{X}/{pasta} sumiu; commit de {fonte} sem como conferir')
                commit = campo(s[fonte], 'Commit') or ''
                self.assertGreaterEqual(len(commit), 7)
                self.assertTrue(head(pasta).startswith(commit), f'{fonte}: {commit} != HEAD')


class TestArquivosDeLicenca(unittest.TestCase):
    def test_toda_fonte_com_codigo_cita_arquivo(self):
        s = secoes()
        for fonte in FONTES:
            with self.subTest(fonte=fonte):
                self.assertTrue(citados(s[fonte]), f'{fonte} não cita licencas/...')

    def test_todo_citado_existe_e_nao_esta_vazio(self):
        with open(NOTICES, encoding='utf-8') as f:
            caminhos = set(citados(f.read()))
        self.assertTrue(caminhos)
        for caminho in caminhos:
            with self.subTest(caminho=caminho):
                completo = os.path.join(RAIZ, caminho)
                self.assertTrue(os.path.isfile(completo))
                self.assertGreater(os.path.getsize(completo), 0)

    def test_texto_citado_igual_a_licenca_da_fonte(self):
        s = secoes()
        for fonte, (_, _, pasta, arquivo) in FONTES.items():
            if pasta is None:
                continue
            with self.subTest(fonte=fonte):
                origem = os.path.join(X, pasta, arquivo)
                if not os.path.isfile(origem):
                    self.skipTest(f'{origem} sumiu; texto de {fonte} sem como conferir')
                iguais = [c for c in citados(s[fonte])
                          if os.path.isfile(os.path.join(RAIZ, c))
                          and filecmp.cmp(os.path.join(RAIZ, c), origem, shallow=False)]
                self.assertTrue(iguais, f'nenhum arquivo citado por {fonte} é cópia de {arquivo}')

    def test_hallmark_traz_texto_mit(self):
        citado = citados(secoes()['hallmark'])
        self.assertTrue(citado)
        with open(os.path.join(RAIZ, citado[0]), encoding='utf-8') as f:
            texto = f.read()
        self.assertIn('MIT License', texto)
        self.assertIn('Permission is hereby granted', texto)

    def test_inspo_nao_cita_arquivo(self):
        self.assertEqual(citados(secoes()['inspo']), [])


class TestNoticeImpeccable(unittest.TestCase):
    COPIA = os.path.join(RAIZ, 'licencas', 'impeccable-NOTICE.md')

    def test_notice_citado_na_secao(self):
        self.assertIn('licencas/impeccable-NOTICE.md', citados(secoes()['impeccable']))

    @unittest.skipUnless(os.path.isfile(os.path.join(X, 'impeccable', 'NOTICE.md')),
                         'X/impeccable/NOTICE.md sumiu; cópia sem como conferir')
    def test_notice_copiado_byte_a_byte(self):
        self.assertTrue(filecmp.cmp(self.COPIA, os.path.join(X, 'impeccable', 'NOTICE.md'), shallow=False))


if __name__ == '__main__':
    unittest.main()
