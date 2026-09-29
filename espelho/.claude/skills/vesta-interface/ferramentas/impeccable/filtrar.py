#!/usr/bin/env python3
"""Aplica excecoes.json à saída da reserva (window.impeccableDetectAsync()), como o detectar faz.

Uso: filtrar.py [saida.json]   (sem arquivo, lê do stdin). Sai 0 sem achado e 2 com achado.
A reserva não preenche ignoreValue: em overused-font o nome da fonte está só em detail,
"Primary font: geist (100% of text)".
"""
import json
import os
import re
import sys


def valor(achado):
    return (achado.get('ignoreValue') or re.sub(r'^[^:]*:\s*|\s*\(.*$', '', achado.get('detail', ''))).lower()


def main():
    pasta = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(pasta, 'excecoes.json'), encoding='utf-8') as f:
        liberados = {(e['regra'], e['valor'].lower()) for e in json.load(f)}
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8') as f:
            itens = json.load(f)
    else:
        itens = json.load(sys.stdin)
    saida = []
    for item in itens:
        resto = [a for a in item['findings'] if (a['type'], valor(a)) not in liberados]
        if resto:
            saida.append({**item, 'findings': resto})
    print(json.dumps(saida, ensure_ascii=False, indent=2))
    return 2 if saida else 0


if __name__ == '__main__':
    sys.exit(main())
