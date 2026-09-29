"""Etapa 11: contrato com a Vesta; os caminhos da vesta-interface que ela cita existem aqui."""
import os
import re
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VESTA = os.path.expanduser('~/Code/vesta')
CITANTES = ['skill/mockup.md', 'skill/execucao.md', 'install.sh']
MINIMOS = ['SKILL.md', 'referencias/verificacao.md', 'catalogo/direcoes/']
# `vesta-interface/<caminho>` ou caminho que começa por uma pasta desta skill
CAMINHO = re.compile(r'vesta-interface/([\w./-]+)'
                     r'|(?<![\w/.-])((?:referencias|catalogo|modos|ferramentas)/[\w./-]*)')


def ler_vesta(rel):
    with open(os.path.join(VESTA, rel)) as f:
        return f.read()


def citados():
    achados = set()
    for rel in CITANTES:
        for m in CAMINHO.finditer(ler_vesta(rel)):
            achados.add((m.group(1) or m.group(2)).rstrip('.'))
    return achados


@unittest.skipUnless(os.path.isdir(VESTA), '~/Code/vesta ausente')
class TestVestaAcoplada(unittest.TestCase):
    def test_mockup_cita_vesta_interface(self):
        self.assertTrue('vesta-interface' in ler_vesta('skill/mockup.md'), 'skill/mockup.md da Vesta não cita vesta-interface')

    def test_vesta_cita_os_caminhos_minimos(self):
        faltam = sorted(set(MINIMOS) - citados())
        self.assertEqual(faltam, [], 'a Vesta não cita estes caminhos da vesta-interface')

    def test_todo_caminho_citado_existe(self):
        citas = citados()
        self.assertTrue(citas, 'a Vesta não cita nenhum caminho da vesta-interface')
        faltam = sorted(c for c in citas if not os.path.exists(os.path.join(RAIZ, c)))
        self.assertEqual(faltam, [], 'a Vesta cita caminhos que não existem na vesta-interface')

    def test_diretorio_de_direcoes_tem_direcao(self):
        direcoes = [n for n in os.listdir(os.path.join(RAIZ, 'catalogo', 'direcoes')) if n.endswith('.md')]
        self.assertTrue(direcoes)

    def test_install_da_vesta_confere_a_pasta_que_o_daqui_cria(self):
        with open(os.path.join(RAIZ, 'install.sh')) as f:
            self.assertTrue('skills/vesta-interface"' in f.read(), 'install.sh daqui não liga skills/vesta-interface')
        self.assertTrue('vesta-interface' in ler_vesta('install.sh'), 'install.sh da Vesta não confere a vesta-interface')


if __name__ == '__main__':
    unittest.main()
