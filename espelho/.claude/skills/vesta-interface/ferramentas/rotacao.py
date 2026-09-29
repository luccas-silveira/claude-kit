#!/usr/bin/env python3
"""Rotação de macroestrutura, menu e rodapé entre telas de Persuadir e Experiência (R7 da spec).

Grava em <projeto>/docs/design/rotacao.json: lista, mais novo primeiro, no máximo 20 entradas.
Operar e Ler gravam sem conferir: numa tela de app, menu e rodapé se repetem de propósito.
"""
import argparse
import json
import os
import sys

TIPOS = ['Persuadir', 'Operar', 'Ler', 'Experiência']
GIRAM = ('Persuadir', 'Experiência')
CAMPOS = ('macro', 'menu', 'rodape')
LIMITE = 20
JANELA = 3


def caminho(projeto):
    return os.path.join(projeto, 'docs', 'design', 'rotacao.json')


def ler(projeto):
    try:
        with open(caminho(projeto), encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def ultimas(entradas):
    return [e for e in entradas if e['tipo'] in GIRAM][:JANELA]


def linha(e):
    return f"{e['tela']} ({e['tipo']}): macro {e['macro']}, menu {e['menu']}, rodape {e['rodape']}"


def registrar(a):
    entradas = ler(a.projeto)
    nova = {'tela': a.tela, 'tipo': a.tipo, 'macro': a.macro, 'menu': a.menu, 'rodape': a.rodape}
    if a.tipo in GIRAM:
        repetidos = [f"{c} {nova[c]} (igual a {e['tela']})"
                     for e in ultimas(entradas) for c in CAMPOS if e[c] == nova[c]]
        if repetidos:
            print('Recusado, repete as 3 últimas de Persuadir/Experiência: ' + '; '.join(repetidos),
                  file=sys.stderr)
            return 1
    os.makedirs(os.path.dirname(caminho(a.projeto)), exist_ok=True)
    with open(caminho(a.projeto), 'w', encoding='utf-8') as f:
        json.dump([nova] + entradas[:LIMITE - 1], f, ensure_ascii=False, indent=2)
        f.write('\n')
    print('Registrado: ' + linha(nova))
    return 0


def mostrar(a):
    achadas = ultimas(ler(a.projeto))
    print('\n'.join(linha(e) for e in achadas) if achadas else 'Nenhuma tela de Persuadir/Experiência registrada.')
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest='comando', required=True)
    r = sub.add_parser('registrar', help='grava a tela; recusa repetição em Persuadir/Experiência')
    r.add_argument('--projeto', default='.')
    r.add_argument('--tela', required=True)
    r.add_argument('--tipo', required=True, choices=TIPOS)
    for c in CAMPOS:
        r.add_argument('--' + c, required=True)
    r.set_defaults(fazer=registrar)
    u = sub.add_parser('ultimas', help='imprime as 3 últimas de Persuadir/Experiência')
    u.add_argument('--projeto', default='.')
    u.set_defaults(fazer=mostrar)
    a = p.parse_args()
    return a.fazer(a)


if __name__ == '__main__':
    sys.exit(main())
