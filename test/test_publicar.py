import datetime
import os
import subprocess

from test_sync import KitCaso

GIT = '/usr/bin/git'


class Publicar(KitCaso):
    """Kit é repositório git com origin num bare local; primeiro commit já publicado."""
    def setUp(self):
        super().setUp()
        self.bare = os.path.join(os.path.dirname(self.home), 'remoto.git')
        self.git('init', '-q', '--bare', self.bare, cwd=None)
        self.git('init', '-q', '-b', 'master')
        self.git('config', 'user.name', 'Teste')
        self.git('config', 'user.email', 't@t')
        self.git('remote', 'add', 'origin', self.bare)
        self.git('add', '-A')
        self.git('commit', '-q', '-m', 'inicio')
        self.git('push', '-q', '-u', 'origin', 'master')
        self.escreve('.claude/settings.json', '{"a": 1}')

    def git(self, *args, cwd=True):
        r = subprocess.run([GIT, *args], cwd=self.kit if cwd else None, env=self.env,
                           capture_output=True, text=True, check=True)
        return r.stdout.strip()

    def remoto(self):
        return self.git('--git-dir', self.bare, 'rev-parse', 'master', cwd=None)

    def local(self):
        return self.git('rev-parse', 'HEAD')

    def pub(self, *extra, entrada=None):
        return self.roda('sync', '--kit', self.kit, *extra, entrada=entrada)

    def test_mostra_status_diff_e_pergunta(self):
        codigo, saida = self.pub(entrada='n\n')
        self.assertEqual(codigo, 0, saida)
        self.assertIn('?? espelho/', saida)          # git status --short
        self.assertIn('manifesto.json', saida)
        self.assertIn('Publicar? [s/N]', saida)

    def test_diff_stat_de_arquivo_rastreado(self):
        self.pub('--sim')
        self.escreve('.claude/settings.json', '{"a": 2}')
        codigo, saida = self.pub(entrada='n\n')
        self.assertEqual(codigo, 0, saida)
        self.assertIn(' M espelho/.claude/settings.json', saida)
        self.assertIn('1 file changed', saida)       # git diff --stat

    def test_resposta_vazia_nao_publica(self):
        antes_l, antes_r = self.local(), self.remoto()
        codigo, saida = self.pub(entrada='\n')
        self.assertEqual(codigo, 0, saida)
        self.assertIn('Publicar? [s/N]', saida)
        self.assertEqual((self.local(), self.remoto()), (antes_l, antes_r))

    def test_resposta_n_nao_publica(self):
        antes_l, antes_r = self.local(), self.remoto()
        codigo, saida = self.pub(entrada='n\n')
        self.assertEqual(codigo, 0, saida)
        self.assertIn('Publicar? [s/N]', saida)
        self.assertEqual((self.local(), self.remoto()), (antes_l, antes_r))

    def test_resposta_s_commita_e_empurra(self):
        antes = self.remoto()
        codigo, saida = self.pub(entrada='s\n')
        self.assertEqual(codigo, 0, saida)
        self.assertNotEqual(self.local(), antes)
        self.assertEqual(self.remoto(), self.local())
        self.assertEqual(self.git('rev-parse', 'HEAD~1'), antes)   # um commit só
        msg = self.git('log', '-1', '--format=%s')
        self.assertTrue(msg.startswith('espelho: ' + datetime.date.today().isoformat()), msg)
        arquivos = self.git('show', '--name-only', '--format=', 'HEAD').splitlines()
        self.assertIn('espelho/.claude/settings.json', arquivos)
        self.assertIn('manifesto.json', arquivos)

    def test_commit_so_leva_espelho_e_manifesto(self):
        self.escreve('solto.txt', 'fora', raiz=self.kit)
        self.pub(entrada='s\n')
        self.assertTrue(self.git('log', '-1', '--format=%s').startswith('espelho: '))
        arquivos = self.git('show', '--name-only', '--format=', 'HEAD').splitlines()
        self.assertNotIn('solto.txt', arquivos)

    def test_sem_mudanca_nada_mudou_sem_pergunta(self):
        self.pub('--sim')
        antes = self.local()
        codigo, saida = self.pub(entrada='s\n')
        self.assertEqual(codigo, 0, saida)
        self.assertIn('nada mudou', saida)
        self.assertNotIn('Publicar?', saida)
        self.assertEqual(self.local(), antes)

    def test_sim_pula_pergunta_e_publica(self):
        codigo, saida = self.pub('--sim', entrada='')
        self.assertEqual(codigo, 0, saida)
        self.assertNotIn('Publicar?', saida)
        self.assertEqual(self.remoto(), self.local())
        self.assertTrue(self.git('log', '-1', '--format=%s').startswith('espelho: '))

    def test_falha_de_push_sai_com_erro_e_mostra_git(self):
        self.git('remote', 'set-url', 'origin', os.path.join(self.kit, 'naoexiste.git'))
        codigo, saida = self.pub('--sim')
        self.assertNotEqual(codigo, 0, saida)
        self.assertIn('naoexiste.git', saida)
        self.assertRegex(saida, r'(fatal|error):')


class KitSemGit(KitCaso):
    def test_kit_sem_git_so_copia_sem_perguntar(self):
        self.escreve('.claude/settings.json', '{}')
        codigo, saida = self.roda('sync', '--kit', self.kit, entrada='')
        self.assertEqual(codigo, 0, saida)
        self.assertNotIn('Publicar?', saida)
        self.assertTrue(os.path.exists(self.no_kit('.claude/settings.json')))
