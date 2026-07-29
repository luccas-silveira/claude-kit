# -*- coding: utf-8 -*-
"""Etapa 5 — LLM-judge (orquestrado pelo skill): classifica TODAS as conversas
(desfecho + categoria de vazamento + produto). Aqui ficam os passos DETERMINISTICOS:
preparar chunks, renderizar prompt, e AGREGAR os resultados em metricas."""
import collections
import glob
import json
import math
import os

from .config import paths

TOOL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT = os.path.join(TOOL_DIR, "prompts", "judge.md")

DROP_LABELS = {
    "A_preco": "Preço / concorrência", "B_documento": "Fricção ao pedir doc/dados",
    "C_audio_sem_cta": "Áudio/catálogo sem CTA", "D_credito": "Crédito reprovado/sem limite",
    "E_empresa_demorou": "Empresa demorou / não respondeu", "F_vou_pensar": "'Vou pensar' e sumiu",
    "G_outro": "Outro", "NA": "—",
}


def _abs(x):
    return os.path.abspath(x)


def prep(cfg):
    p = paths(cfg)
    convs = sorted(glob.glob(os.path.join(p["convs"], "*.md")))
    n = cfg["judge"]["chunks"]
    size = max(1, math.ceil(len(convs) / n))
    chunks = [convs[i:i + size] for i in range(0, len(convs), size)]
    jdir = os.path.join(p["base"], "judge_out")
    os.makedirs(jdir, exist_ok=True)
    man = {}
    for idx, ch in enumerate(chunks, 1):
        lp = os.path.join(jdir, ".judge_chunk_%02d_files.txt" % idx)
        open(lp, "w", encoding="utf-8").write("\n".join(_abs(x) for x in ch))
        man[idx] = {"files": len(ch), "list": _abs(lp), "out": _abs(os.path.join(jdir, "judge_%02d.json" % idx))}
    json.dump(man, open(os.path.join(jdir, ".judge_manifest.json"), "w"), indent=2)
    print("%d conversas -> %d chunks (%s/)" % (len(convs), len(chunks), jdir))
    return man


def render_prompt(cfg, chunk_num):
    p = paths(cfg)
    jdir = os.path.join(p["base"], "judge_out")
    man = json.load(open(os.path.join(jdir, ".judge_manifest.json")))
    info = man[str(chunk_num)]
    tpl = open(PROMPT, encoding="utf-8").read()
    return (tpl.replace("{{DOMAIN}}", cfg.get("domain_context", ""))
               .replace("{{LIST_PATH}}", info["list"]).replace("{{OUT_PATH}}", info["out"]))


def aggregate(cfg):
    p = paths(cfg)
    jdir = os.path.join(p["base"], "judge_out")
    rows = []
    for f in sorted(glob.glob(os.path.join(jdir, "judge_*.json"))):
        try:
            rows += json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print("aviso: %s ilegivel (%s)" % (f, e))
    n = len(rows)
    if not n:
        print("nenhuma classificacao encontrada em %s" % jdir)
        return None
    by_outcome = collections.Counter(r.get("outcome") for r in rows)
    by_product = collections.Counter(r.get("product") for r in rows)
    leads = [r for r in rows if r.get("outcome") != "nao_lead"]
    by_drop = collections.Counter(r.get("drop_off") for r in leads if r.get("drop_off") not in (None, "NA"))
    last_emp = sum(1 for r in leads if r.get("last_speaker") == "EMPRESA")
    agg = {"total": n, "leads": len(leads),
           "by_outcome": dict(by_outcome.most_common()),
           "by_product": dict(by_product.most_common()),
           "by_drop_off": dict(by_drop.most_common()),
           "last_msg_empresa_pct": round(100.0 * last_emp / len(leads), 1) if leads else 0}
    json.dump(agg, open(os.path.join(jdir, "judge_aggregate.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    lines = ["# Classificacao em lote (LLM-judge) — %d conversas\n" % n,
             "## Desfecho", *["- %s: %d" % (k, v) for k, v in by_outcome.most_common()],
             "\n## Onde vaza (categoria, só leads)",
             *["- %s — %s: %d" % (k, DROP_LABELS.get(k, k), v) for k, v in by_drop.most_common()],
             "\n## Produto", *["- %s: %d" % (k, v) for k, v in by_product.most_common()],
             "\n- Última msg da EMPRESA (lead largado): %s%%" % agg["last_msg_empresa_pct"]]
    open(os.path.join(jdir, "JUDGE_AGG.md"), "w", encoding="utf-8").write("\n".join(lines))
    print("OK: %d classificadas -> %s/JUDGE_AGG.md" % (n, jdir))
    return agg
