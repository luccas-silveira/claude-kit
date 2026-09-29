"""Etapa 0: README cita a spec, .gitignore básico e cópia de segurança do hallmark em ux-lab/vendor."""
import filecmp
import os
import subprocess
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = 'docs/vesta/specs/2026-09-28-vesta-interface-design.md'
COPIA = os.path.expanduser('~/Code/ux-lab/vendor/hallmark')
ORIGEM = os.path.expanduser('~/.claude/skills/hallmark')
ARQUIVOS_HALLMARK = 107  # contagem de H em 2026-09-28; H some na etapa 13


def ignorado(caminho):
    # excludesFile vazio: só o .gitignore do repositório conta, não o global do usuário
    r = subprocess.run(['git', '-c', 'core.excludesFile=/dev/null', 'check-ignore', '-q', caminho],
                       cwd=RAIZ, capture_output=True)
    return r.returncode == 0


class TestReadme(unittest.TestCase):
    def test_readme_cita_spec(self):
        with open(os.path.join(RAIZ, 'README.md'), encoding='utf-8') as f:
            self.assertIn(SPEC, f.read())


class TestGitignore(unittest.TestCase):
    def test_arquivo_existe(self):
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, '.gitignore')))

    def test_ignora_pycache_em_qualquer_pasta(self):
        self.assertTrue(ignorado('__pycache__/x.pyc'))
        self.assertTrue(ignorado('test/__pycache__/test_esqueleto.cpython-313.pyc'))

    def test_ignora_ds_store_em_qualquer_pasta(self):
        self.assertTrue(ignorado('.DS_Store'))
        self.assertTrue(ignorado('docs/.DS_Store'))

    def test_nao_ignora_codigo(self):
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, '.gitignore')))
        self.assertFalse(ignorado('test/test_esqueleto.py'))
        self.assertFalse(ignorado('README.md'))


class TestCopiaHallmark(unittest.TestCase):
    def test_skill_md_na_raiz_da_copia(self):
        self.assertTrue(os.path.isfile(os.path.join(COPIA, 'SKILL.md')))

    def test_sem_pasta_aninhada(self):
        # cp -R rodado duas vezes cria hallmark/hallmark
        self.assertTrue(os.path.isdir(COPIA))
        self.assertFalse(os.path.exists(os.path.join(COPIA, 'hallmark')))

    def test_copia_tem_todos_os_arquivos(self):
        # .DS_Store fora da conta: o Finder cria sozinho ao abrir a pasta
        total = sum(len([a for a in arquivos if a != '.DS_Store'])
                    for _, _, arquivos in os.walk(COPIA))
        self.assertEqual(total, ARQUIVOS_HALLMARK)

    @unittest.skipUnless(os.path.isdir(ORIGEM), 'H já foi removido; a cópia é a única fonte')
    def test_skill_md_igual_ao_original(self):
        self.assertTrue(filecmp.cmp(os.path.join(COPIA, 'SKILL.md'),
                                    os.path.join(ORIGEM, 'SKILL.md'), shallow=False))


if __name__ == '__main__':
    unittest.main()
