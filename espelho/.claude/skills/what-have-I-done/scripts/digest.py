#!/usr/bin/env python3
"""Gera um digest por sessão das conversas com interação em uma data.

Uso: python3 digest.py YYYY-MM-DD OUT_DIR

Pega os transcritos do Claude Code (~/.claude/projects/**/*.jsonl, sem subagents),
filtra os registros cuja hora local (America/Sao_Paulo, UTC-3) cai na data pedida
e escreve um arquivo de texto por sessão em OUT_DIR. Também escreve INDEX.tsv com
projeto, tamanho e contagens, e batch_N.txt com os caminhos divididos em lotes de
~100 KB para os subagentes lerem.
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.expanduser('~/.claude/projects')
LOCAL = timezone(timedelta(hours=-3))
KEY = re.compile(
    r'git (commit|push|merge|tag)|deploy|rsync|gh (pr|run|workflow)|npm (test|run)|'
    r'vitest|pytest|docker|ssh |scp |curl -X (POST|PUT|PATCH|DELETE)|/conversations/|'
    r'workflow|psql|UPDATE |INSERT |DELETE ',
    re.I,
)
TEXT_USER, TEXT_ASST, TEXT_TOOL = 350, 220, 200
BATCH_BYTES = 100_000


def local_ts(s):
    try:
        return datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(LOCAL)
    except Exception:
        return None


def blocks(content):
    if isinstance(content, str):
        yield 'text', content
        return
    if not isinstance(content, list):
        return
    for b in content:
        if not isinstance(b, dict):
            continue
        if b.get('type') == 'text':
            yield 'text', b.get('text', '')
        elif b.get('type') == 'tool_use':
            inp = b.get('input') or {}
            cmd = inp.get('command') or inp.get('description') or ''
            yield 'tool', f"{b.get('name')}: {cmd}"


# O home entra como o Claude Code o grava no nome da pasta: tudo que não é letra ou número vira "-".
HOME = re.sub(r'[^A-Za-z0-9]', '-', os.path.expanduser('~'))
PREFIXES = tuple(HOME + p for p in ('-Desktop-ZOI-Projetos-ZOI-', '-Desktop-Luccas-', '-Documents-',
                                    '-Desktop-', '')) + ('-private-tmp-',)


def project_label(dirname):
    # Pasta do projeto no Claude Code: caminho com "-" no lugar de "/".
    base, _, wt = dirname.partition('--claude-worktrees-')
    for pref in PREFIXES:
        if base.startswith(pref):
            base = base[len(pref):]
            break
    base = base.strip('-') or 'raiz'
    return f'{base} (worktree {wt})' if wt else base


def digest(path, day):
    lines, n_user, n_asst, first, last = [], 0, 0, None, None
    for raw in open(path, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(raw)
        except Exception:
            continue
        ts = local_ts(d.get('timestamp') or '')
        if not ts or ts.strftime('%Y-%m-%d') != day:
            continue
        first = first or ts
        last = ts
        typ = d.get('type')
        if typ not in ('user', 'assistant'):
            continue
        hm = ts.strftime('%H:%M')
        for kind, txt in blocks((d.get('message') or {}).get('content')):
            if not txt:
                continue
            if typ == 'user' and kind == 'text':
                n_user += 1
                lines.append(f'[{hm}] USER: {txt[:TEXT_USER]}')
            elif typ == 'assistant' and kind == 'text':
                n_asst += 1
                lines.append(f'[{hm}] ASST: {txt[:TEXT_ASST]}')
            elif kind == 'tool' and KEY.search(txt):
                lines.append(f'[{hm}] TOOL: {txt[:TEXT_TOOL]}')
    if n_user == 0:
        return None
    span = f"{first.strftime('%H:%M')} a {last.strftime('%H:%M')}"
    head = (f'# {project_label(os.path.basename(os.path.dirname(path)))}\n'
            f'file: {path}\nhoras: {span} | msgs do dono: {n_user} | respostas: {n_asst}\n')
    return head + '\n'.join(lines) + '\n', n_user, n_asst


def main():
    day, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    day_start = datetime.fromisoformat(day).replace(tzinfo=LOCAL)
    index, kept = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [x for x in dirnames if x != 'subagents']
        for f in filenames:
            if not f.endswith('.jsonl'):
                continue
            p = os.path.join(dirpath, f)
            if datetime.fromtimestamp(os.path.getmtime(p), LOCAL) < day_start:
                continue
            res = digest(p, day)
            if not res:
                continue
            txt, nu, na = res
            sid = f[:-6]
            name = f'{sid[:8]}.txt'
            with open(os.path.join(out, name), 'w') as o:
                o.write(txt)
            kept.append(os.path.join(out, name))
            index.append(f'{name}\t{project_label(os.path.basename(dirpath))}\t{len(txt)}\t{nu}\t{na}')
    with open(os.path.join(out, 'INDEX.tsv'), 'w') as o:
        o.write('\n'.join(sorted(index)) + '\n')
    batch, size, n = [], 0, 0
    for p in sorted(kept, key=lambda x: -os.path.getsize(x)):
        s = os.path.getsize(p)
        if batch and size + s > BATCH_BYTES:
            n += 1
            open(os.path.join(out, f'batch_{n}.txt'), 'w').write('\n'.join(batch) + '\n')
            batch, size = [], 0
        batch.append(p)
        size += s
    if batch:
        n += 1
        open(os.path.join(out, f'batch_{n}.txt'), 'w').write('\n'.join(batch) + '\n')
    print(f'sessoes com interacao em {day}: {len(kept)} | lotes: {n} | saida: {out}')


if __name__ == '__main__':
    main()
