from base import Caso


class TestCli(Caso):
    def test_sem_argumento_mostra_uso(self):
        codigo, saida = self.roda()
        self.assertEqual(codigo, 2, saida)
        self.assertIn('sync', saida)
        self.assertIn('instalar', saida)

    def test_instalar_sem_claude_recusa(self):
        codigo, saida = self.roda('instalar')
        self.assertNotEqual(codigo, 0, saida)
        self.assertIn('Claude Code', saida)
        self.assertNotIn('Traceback', saida)

    def test_instalar_checa_claude_antes_de_tudo(self):
        for nome in ('brew', 'npm', 'uv', 'git', 'go', 'docker', 'curl'):
            self.stub(nome)
        codigo, _ = self.roda('instalar')
        self.assertNotEqual(codigo, 0)
        self.assertEqual(self.chamadas(), [])

    def test_install_sh_repassa_para_instalar(self):
        codigo, saida = self.roda_sh('install.sh')
        self.assertEqual((codigo, saida), self.roda('instalar'))
        self.assertNotEqual(codigo, 0)
        self.assertIn('Claude Code', saida)

    def test_install_sh_repassa_argumentos(self):
        codigo, saida = self.roda_sh('install.sh', '--help')
        self.assertEqual(codigo, 0, saida)
        self.assertIn('instalar', saida)

    def test_sync_sh_repassa_para_sync(self):
        codigo, saida = self.roda_sh('sync.sh', '--help')
        self.assertEqual((codigo, saida), self.roda('sync', '--help'))
        self.assertEqual(codigo, 0, saida)
        self.assertIn('sync', saida)
