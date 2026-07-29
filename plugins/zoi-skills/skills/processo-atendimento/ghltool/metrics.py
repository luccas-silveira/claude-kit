# -*- coding: utf-8 -*-
"""Etapa 3 — Metricas DETERMINISTICAS (sem LLM): quem larga, SLA de 1a resposta,
latencia, silencio. Roda sobre o export bruto e/ou o dataset limpo."""
import json
import os
import statistics
from datetime import datetime, timezone

from .config import paths

SLA_MINUTES = 120


def parse_dt(v):
    if not v:
        return None
    if isinstance(v, (int, float)):
        return datetime.fromtimestamp(v / 1000, tz=timezone.utc)
    s = str(v).strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _events(conv, noise):
    out = []
    for m in conv.get("messages", []):
        if m.get("channel") in noise:
            continue
        dt = parse_dt(m.get("date") or m.get("dateAdded"))
        if dt is None:
            continue
        d = (m.get("direction") or "").lower()
        if d not in ("inbound", "outbound"):
            d = "inbound" if (m.get("speaker") or "").upper() in ("LEAD", "CLIENTE") else "outbound"
        content = bool((m.get("text") or m.get("body") or "").strip()) or bool(m.get("attachments"))
        out.append({"dt": dt, "dir": d, "content": content})
    out.sort(key=lambda x: x["dt"])
    return out


def _conv(conv, noise):
    ev = _events(conv, noise)
    if not ev:
        return None
    inb = [e for e in ev if e["dir"] == "inbound"]
    out = [e for e in ev if e["dir"] == "outbound"]
    r = {"id": conv.get("conversation_id") or conv.get("id"), "n_in": len(inb), "n_out": len(out),
         "last_is_ours": ev[-1]["dir"] == "outbound", "two_way": bool(inb and out),
         "first_response_min": None, "never_replied": False, "max_silence_h": None}
    if inb:
        t0 = inb[0]["dt"]
        fo = next((e["dt"] for e in ev if e["dir"] == "outbound" and e["dt"] >= t0), None)
        if fo is None:
            r["never_replied"] = True
        else:
            r["first_response_min"] = (fo - t0).total_seconds() / 60.0
    if len(ev) >= 2:
        r["max_silence_h"] = max((ev[i + 1]["dt"] - ev[i]["dt"]).total_seconds() / 3600.0
                                 for i in range(len(ev) - 1))
    return r


def _dist(vals):
    if not vals:
        return {}
    vals = sorted(vals)
    return {"n": len(vals), "median": round(statistics.median(vals), 1),
            "p90": round(vals[int(0.9 * (len(vals) - 1))], 1),
            "mean": round(statistics.mean(vals), 1), "max": round(max(vals), 1)}


def _pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def fmt_min(m):
    if m is None:
        return "—"
    return "%.0f min" % m if m < 60 else ("%.1f h" % (m / 60) if m < 1440 else "%.1f dias" % (m / 1440))


def compute(in_path, noise):
    rows = [r for r in (_conv(json.loads(l), noise) for l in open(in_path, encoding="utf-8") if l.strip()) if r]
    n = len(rows)
    tw = [r for r in rows if r["two_way"]]
    hi = [r for r in rows if r["n_in"] > 0]
    lo = [r for r in rows if r["last_is_ours"]]
    lotw = [r for r in tw if r["last_is_ours"]]
    nev = [r for r in hi if r["never_replied"]]
    frt = [r["first_response_min"] for r in rows if r["first_response_min"] is not None]
    sil = [r["max_silence_h"] for r in rows if r["max_silence_h"] is not None]
    return {"input": in_path, "conversations": n, "two_way": len(tw), "with_inbound": len(hi),
            "last_msg_ours": {"count": len(lo), "pct_all": _pct(len(lo), n), "pct_two_way": _pct(len(lotw), len(tw))},
            "never_replied_by_us": {"count": len(nev), "pct_of_inbound": _pct(len(nev), len(hi))},
            "first_response_time_min": _dist(frt),
            "first_response_within_2h_pct": _pct(len([x for x in frt if x <= SLA_MINUTES]), len(frt)),
            "max_silence_hours": _dist(sil), "sla_minutes": SLA_MINUTES}


def _report(a):
    frt, sil = a["first_response_time_min"], a["max_silence_hours"]
    return f"""# Metricas de Atendimento (deterministicas)

Fonte: `{a['input']}` · {a['conversations']} conversas · SLA alvo: {a['sla_minutes']} min

## Quem larga a conversa
- Ultima msg foi NOSSA: {a['last_msg_ours']['count']}/{a['conversations']} = **{a['last_msg_ours']['pct_all']}%** (todas) · {a['last_msg_ours']['pct_two_way']}% (two-way)
- Empresa NUNCA respondeu: {a['never_replied_by_us']['count']} ({a['never_replied_by_us']['pct_of_inbound']}% das com inbound)

## 1a resposta da empresa
- Mediana {fmt_min(frt.get('median'))} · p90 {fmt_min(frt.get('p90'))} · pior {fmt_min(frt.get('max'))}
- Dentro de 2h: **{a['first_response_within_2h_pct']}%**

## Silencio (maior gap)
- Mediana {sil.get('median','—')} h · p90 {sil.get('p90','—')} h · max {sil.get('max','—')} h

_Computado, nao estimado._
"""


def run(cfg):
    p = paths(cfg)
    noise = set(cfg["cleaning"]["channel_noise"])
    targets = [(os.path.join(p["ghl_export"], "conversations.jsonl"), p["ghl_export"]),
               (os.path.join(p["process_dataset"], "conversations_clean.jsonl"), p["process_dataset"])]
    results = {}
    for in_path, outdir in targets:
        if not os.path.exists(in_path):
            continue
        a = compute(in_path, noise)
        json.dump({"aggregate": a}, open(os.path.join(outdir, "metrics.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        open(os.path.join(outdir, "METRICAS.md"), "w", encoding="utf-8").write(_report(a))
        results[in_path] = a
        print("OK %s: ultima-msg-nossa %s%% | 1a resp mediana %s | <2h %s%%"
              % (os.path.basename(in_path), a["last_msg_ours"]["pct_all"],
                 fmt_min(a["first_response_time_min"].get("median")), a["first_response_within_2h_pct"]))
    return results
