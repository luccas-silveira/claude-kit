"""Espelho do setup de Claude Code: `sync` copia do home para o kit, `instalar` faz o inverso."""
import argparse
import shutil
import sys


def sync(args):
    return 0


def instalar(args):
    if not shutil.which('claude'):
        print('Claude Code não encontrado no PATH. Instale o Claude Code antes.', file=sys.stderr)
        return 1
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog='espelho.py')
    sub = p.add_subparsers(dest='cmd')
    sub.add_parser('sync', help='copia o setup do home para o kit').set_defaults(fn=sync)
    sub.add_parser('instalar', help='instala o setup do kit no home').set_defaults(fn=instalar)
    args = p.parse_args(argv)
    if not args.cmd:
        p.print_usage(sys.stderr)
        return 2
    return args.fn(args)


if __name__ == '__main__':
    sys.exit(main())
