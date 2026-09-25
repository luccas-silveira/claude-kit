import os

from test_sync import BLOQUEIO, KitCaso

ALVO = '.claude/skills/a/SKILL.md'
SEGREDOS = {
    'ghp': 'ghp_' + 'A1b2C3d4E5' * 3 + 'F6g7H8',
    'sk': 'sk-' + 'a1B2c3D4e5' * 4,
    'jwt': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36',
    'chave_privada': '-----BEGIN RSA PRIVATE KEY-----',
    'api_key': 'api_key = "%s"' % ('k9' * 16),
}


class TestBarreiras(KitCaso):
    def setUp(self):
        super().setUp()
        self.escreve('.claude/settings.json', '{}')
        self.escreve(ALVO, 'limpo\n')
        self.sync()  # espelho/ e manifesto.json prévios
        self.antes = self.foto()

    def barra(self, esperado_no_texto):
        # arquivo novo limpo: uma barreira que roda depois de escrever deixaria rastro
        self.escreve('.claude/agents/novo.md', 'novo\n')
        codigo, saida = self.roda('sync', '--kit', self.kit)
        self.assertNotEqual(codigo, 0, saida)
        for t in esperado_no_texto:
            self.assertIn(t, saida)
        self.assertEqual(self.foto(), self.antes, 'kit mudou')
        return saida

    def barra_segredo(self, segredo):
        self.escreve(ALVO, 'linha um\nlinha dois\nx %s y\nfim\n' % segredo)
        saida = self.barra([ALVO])
        self.assertRegex(saida, r'SKILL\.md\D{0,12}3\b')

    def test_segredo_ghp(self):
        self.barra_segredo(SEGREDOS['ghp'])

    def test_segredo_sk(self):
        self.barra_segredo(SEGREDOS['sk'])

    def test_segredo_jwt(self):
        self.barra_segredo(SEGREDOS['jwt'])

    def test_segredo_chave_privada(self):
        self.barra_segredo(SEGREDOS['chave_privada'])

    def test_segredo_api_key(self):
        self.barra_segredo(SEGREDOS['api_key'])

    def test_termo_bloqueado_em_arquivo_sem_diferenciar_maiusculas(self):
        self.escreve(BLOQUEIO, 'outro\nClienteSecreto\n')
        self.escreve(ALVO, 'a\nb\nfala do clienteSECRETO aqui\n')
        saida = self.barra([ALVO])
        self.assertRegex(saida, r'SKILL\.md\D{0,12}3\b')

    def test_termo_bloqueado_no_manifesto(self):
        self.repo('Code/r', 'git@github.com:eu/acmecorp-painel.git')
        self.fontes({'repositorios': [{'caminho': '~/Code/r', 'depois': ''}]})
        self.antes = self.foto()  # fontes.json mudou no teste, não no sync
        self.escreve(BLOQUEIO, 'AcmeCorp\n')
        saida = self.barra([])
        self.assertIn('manifesto', saida.lower())

    def test_sem_bloqueio_recusa_e_diz_onde_criar(self):
        os.remove(os.path.join(self.home, BLOQUEIO))
        self.barra(['.config/claude-kit/bloqueio.txt'])

    def test_texto_limpo_passa(self):
        self.escreve(BLOQUEIO, '\n  \nClienteSecreto\n\n')  # linha vazia não barra tudo
        quase = ('ghp_curto sk-curto eyJabc api_key = "curta" '
                 '-----BEGIN PUBLIC KEY----- cliente e secreto separados\n')
        self.escreve(ALVO, quase)
        self.sync()
        self.assertEqual(self.le(self.no_kit(ALVO)), quase)
        self.assertTrue(os.path.exists(os.path.join(self.kit, 'manifesto.json')))
