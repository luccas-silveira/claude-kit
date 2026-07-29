# -*- coding: utf-8 -*-
"""Etapa 2 — Limpeza/qualificacao para extracao de processo.

Pipeline: ruido de canal -> scrub de corpo (tracking/anexo->tag/vcard) ->
manter turns>=N (texto real) -> dropar outlier ratio>=R -> dedup por template (top-N).
Parametros vem de cfg['cleaning']. extra_scrub_patterns permite boilerplate do tenant.
"""
import json
import os
import re
import collections

from .config import paths

ATTACH_RE = re.compile(r'type message:\s*([a-zA-Z]+)(?:\s+name file:\s*(\S+))?', re.I)
VCARD_RE = re.compile(r'BEGIN:VCARD.*?END:VCARD', re.I)
VCARD_FN_RE = re.compile(r'FN:(.+?)(?=\s+[A-Z][A-Z0-9-]*[:;=]|\s*END:VCARD|$)', re.I)
KIND_MAP = {"audio": "audio", "image": "imagem", "photo": "imagem", "video": "video",
            "document": "documento", "file": "documento", "contact": "contato",
            "sticker": "sticker", "location": "localizacao"}
JUNK_PATTERNS = [
    r'✅?\s*Sent from another device\s*✅?', r'Sent From API', r'\bforwarded\b',
    r'⚠️\s*Contact manually changed the sending number\.?',
    r'🔁\s*Number switched from \d+ to \d+',
    r'🚀\s*Novo lead atribuído.*', r'reply\s*message:\s*',
]


def make_scrub(extra_patterns):
    junk = JUNK_PATTERNS + list(extra_patterns or [])

    def scrub(body):
        if not body:
            return "", False
        s = re.sub(r'\s+', ' ', body.replace("\r", " ")).strip()
        tag = ""
        vc = VCARD_RE.search(s)
        if vc:
            fn = VCARD_FN_RE.search(vc.group(0))
            name = fn.group(1).strip() if fn else ""
            name = re.split(r'\s*(?:;|item\d|TEL[;:=]|waid=)', name, flags=re.I)[0].strip()
            tag = "[contato: %s]" % name if name else "[contato]"
            s = re.sub(r'(?:type message:\s*contact\s*)?BEGIN:VCARD.*?END:VCARD', ' ', s, flags=re.I)
        else:
            m = ATTACH_RE.search(s)
            if m:
                kind, fname = (m.group(1) or "").lower(), m.group(2)
                label = KIND_MAP.get(kind, kind or "anexo")
                tag = "[%s: %s]" % (label, fname.strip().rstrip(".,;")) if fname else "[%s]" % label
                s = ATTACH_RE.sub(" ", s)
        s = re.split(r'Source:\s*\w+', s, maxsplit=1, flags=re.I)[0]
        for pat in junk:
            s = re.sub(pat, ' ', s, flags=re.I)
        s = re.sub(r'\s+', ' ', s).strip()
        has_text = bool(s)
        text = (s + " " + tag).strip() if (s and tag) else (s or tag)
        return text, has_text
    return scrub


def norm_entry(s):
    return re.sub(r'\W+', ' ', (s or "").lower()).strip()[:55]


def run(cfg):
    cl = cfg["cleaning"]
    noise = set(cl["channel_noise"])
    scrub = make_scrub(cl.get("extra_scrub_patterns"))
    p = paths(cfg)
    in_path = os.path.join(p["ghl_export"], "conversations.jsonl")
    out_dir = p["process_dataset"]
    convs_dir = p["convs"]
    os.makedirs(convs_dir, exist_ok=True)

    convs = [json.loads(l) for l in open(in_path, encoding="utf-8") if l.strip()]
    report = {"stages": []}

    def stage(name, n):
        report["stages"].append({"stage": name, "conversations": n})
        print("  %-30s %d" % (name, n))

    stage("0. entrada", len(convs))

    def clean_msgs(c):
        out = []
        for m in c["messages"]:
            if m.get("channel") in noise:
                continue
            text, has_text = scrub(m.get("body") or m.get("text") or "")
            if not text:
                continue
            out.append({"date": m.get("date"), "channel": m.get("channel"),
                        "speaker": "CLIENTE" if m.get("direction") == "inbound" else "EMPRESA",
                        "direction": m.get("direction"), "text": text, "has_text": has_text})
        out.sort(key=lambda x: x.get("date") or "")
        return out

    def turns(msgs):
        t, last = 0, None
        for m in msgs:
            if m["has_text"] and m["direction"] != last:
                t += 1
                last = m["direction"]
        return t

    def io(msgs):
        i = sum(1 for m in msgs if m["has_text"] and m["direction"] == "inbound")
        o = sum(1 for m in msgs if m["has_text"] and m["direction"] == "outbound")
        return i, o

    def depth(msgs):
        return sum(1 for m in msgs if m["has_text"])

    cleaned = [(c, m) for c, m in ((c, clean_msgs(c)) for c in convs) if m]
    stage("1-2. apos scrub", len(cleaned))
    deep = [(c, m) for c, m in cleaned if turns(m) >= cl["min_turns"]]
    stage("3. turns>=%d" % cl["min_turns"], len(deep))
    kept = [(c, m) for c, m in deep if not (io(m)[0] > 0 and io(m)[1] / io(m)[0] >= cl["ratio_max"])]
    stage("4. drop ratio>=%d:1" % cl["ratio_max"], len(kept))

    groups = collections.defaultdict(list)
    for c, m in kept:
        fi = next((x["text"] for x in m if x["direction"] == "inbound" and x["has_text"]), None)
        groups[norm_entry(fi) if fi else "__noinb_%s" % c["conversation_id"]].append((c, m))
    sampled = []
    for items in groups.values():
        if len(items) >= cl["group_min"]:
            sampled += sorted(items, key=lambda cm: depth(cm[1]), reverse=True)[:cl["sample_n"]]
        else:
            sampled += items
    stage("5. apos dedup (N=%d)" % cl["sample_n"], len(sampled))

    jsonl = os.path.join(out_dir, "conversations_clean.jsonl")
    total_msgs = 0
    with open(jsonl, "w", encoding="utf-8") as jf:
        for c, msgs in sampled:
            pub = [{"date": m["date"], "channel": m["channel"], "speaker": m["speaker"], "text": m["text"]} for m in msgs]
            total_msgs += len(pub)
            rec = {"conversation_id": c["conversation_id"], "type": c.get("type"),
                   "contact": c.get("contact"),
                   "date_first_message": pub[0]["date"] if pub else None,
                   "date_last_message": pub[-1]["date"] if pub else None,
                   "message_count": len(pub), "messages": pub}
            jf.write(json.dumps(rec, ensure_ascii=False) + "\n")
            with open(os.path.join(convs_dir, "%s.md" % c["conversation_id"]), "w", encoding="utf-8") as mf:
                ct = c.get("contact") or {}
                mf.write("# Conversa %s\n\n- Contato: %s\n- Mensagens: %d\n\n"
                         % (c["conversation_id"], ct.get("name") or "-", len(pub)))
                for m in pub:
                    mf.write("**%s** (%s):\n%s\n\n" % (m["speaker"], m.get("date") or "-", m["text"]))

    report["final"] = {"conversations": len(sampled), "messages": total_msgs, "config": cl}
    json.dump(report, open(os.path.join(out_dir, "cleaning_report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("OK: %d conversas, %d mensagens -> %s" % (len(sampled), total_msgs, jsonl))
    return report
