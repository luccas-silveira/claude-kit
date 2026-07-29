# -*- coding: utf-8 -*-
"""Etapa 4 — Grafo (orquestrado pelo skill). Aqui ficam os passos DETERMINISTICOS:
preparar chunks p/ os subagents, checar quais faltam (auto-retry), e renderizar o
prompt de extracao com o vocabulario canonico do cliente."""
import glob
import json
import math
import os

from .config import paths

TOOL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT = os.path.join(TOOL_DIR, "prompts", "graph_extract.md")


def _abs(path):
    return os.path.abspath(path)


def prep(cfg):
    p = paths(cfg)
    convs = sorted(glob.glob(os.path.join(p["convs"], "*.md")))
    n = cfg["graph"]["chunks"]
    size = max(1, math.ceil(len(convs) / n))
    chunks = [convs[i:i + size] for i in range(0, len(convs), size)]
    gdir = p["graphify_out"]
    os.makedirs(gdir, exist_ok=True)
    man = {}
    for idx, ch in enumerate(chunks, 1):
        lp = os.path.join(gdir, ".chunk_%02d_files.txt" % idx)
        open(lp, "w", encoding="utf-8").write("\n".join(_abs(x) for x in ch))
        man[idx] = {"files": len(ch), "list": _abs(lp),
                    "out": _abs(os.path.join(gdir, ".graphify_chunk_%02d.json" % idx))}
    json.dump(man, open(os.path.join(gdir, ".chunks_manifest.json"), "w"), indent=2)
    print("%d conversas -> %d chunks (%s/)" % (len(convs), len(chunks), gdir))
    return man


def status(cfg):
    p = paths(cfg)
    total = cfg["graph"]["chunks"]
    gdir = p["graphify_out"]
    missing = []
    for i in range(1, total + 1):
        f = os.path.join(gdir, ".graphify_chunk_%02d.json" % i)
        ok = False
        if os.path.exists(f):
            try:
                ok = bool(json.load(open(f, encoding="utf-8")).get("nodes"))
            except Exception:
                ok = False
        if not ok:
            missing.append(i)
    print("chunks: %d/%d ok | faltando: %s" % (total - len(missing), total, missing or "nenhum"))
    return missing


def render_prompt(cfg, chunk_num):
    """Retorna o prompt do subagent de extracao para um chunk, ja com vocabulario."""
    p = paths(cfg)
    man = json.load(open(os.path.join(p["graphify_out"], ".chunks_manifest.json")))
    info = man[str(chunk_num)]
    v = cfg["vocabulary"]
    vocab = "\n".join("  %s: %s" % (k, ", ".join(v.get(k, []))) for k in
                      ("products", "stages", "objections", "payment", "intents"))
    tpl = open(PROMPT, encoding="utf-8").read()
    return (tpl.replace("{{DOMAIN}}", cfg.get("domain_context", ""))
               .replace("{{VOCAB}}", vocab)
               .replace("{{CHUNK}}", str(chunk_num))
               .replace("{{TOTAL}}", str(cfg["graph"]["chunks"]))
               .replace("{{LIST_PATH}}", info["list"])
               .replace("{{OUT_PATH}}", info["out"]))


def merged_extract(cfg):
    """Junta os chunks em um extract.json (nodes deduplicados por id)."""
    p = paths(cfg)
    gdir = p["graphify_out"]
    nodes, edges, hyper, seen = [], [], [], set()
    for c in sorted(glob.glob(os.path.join(gdir, ".graphify_chunk_*.json"))):
        d = json.load(open(c, encoding="utf-8"))
        for nlist, target in ((d.get("nodes", []), nodes),):
            for nd in nlist:
                if nd["id"] not in seen:
                    seen.add(nd["id"])
                    target.append(nd)
        edges += d.get("edges", [])
        hyper += d.get("hyperedges", [])
    out = {"nodes": nodes, "edges": edges, "hyperedges": hyper, "input_tokens": 0, "output_tokens": 0}
    path = os.path.join(gdir, ".graphify_extract.json")
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    print("merge: %d nos unicos, %d edges, %d hyperedges -> %s" % (len(nodes), len(edges), len(hyper), path))
    return out
