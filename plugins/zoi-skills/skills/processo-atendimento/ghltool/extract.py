# -*- coding: utf-8 -*-
"""Etapa 1 — Extracao de conversas do GoHighLevel (API v2).

Paralelo (ThreadPool) + cache incremental (por conversationId+dateUpdated) +
User-Agent de browser (Cloudflare bane o urllib) + retry com backoff (429/5xx/timeout).
"""
import json
import os
import sys
import time
import concurrent.futures
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone

from .config import get_token, paths

API_BASE = "https://services.leadconnectorhq.com"
API_VERSION = "2021-04-15"
PAGE_LIMIT = 100
REQUEST_PAUSE = 0.05
MAX_RETRIES = 5
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

CHANNEL = {
    "TYPE_SMS": "SMS", "TYPE_CUSTOM_SMS": "SMS/WhatsApp", "TYPE_CUSTOM_PROVIDER_SMS": "SMS/WhatsApp",
    "TYPE_WHATSAPP": "WhatsApp", "TYPE_EMAIL": "Email", "TYPE_CUSTOM_EMAIL": "Email",
    "TYPE_CUSTOM_PROVIDER_EMAIL": "Email", "TYPE_CALL": "Ligacao", "TYPE_VOICEMAIL": "Voicemail",
    "TYPE_FACEBOOK": "Facebook", "TYPE_INSTAGRAM": "Instagram", "TYPE_GMB": "Google Business",
    "TYPE_LIVE_CHAT": "Webchat", "TYPE_WEBCHAT": "Webchat", "TYPE_REVIEW": "Review",
    "TYPE_ACTIVITY": "Sistema", "TYPE_ACTIVITY_CONTACT": "Sistema", "TYPE_ACTIVITY_OPPORTUNITY": "Sistema",
}
_SYSTEM_TYPES = {"TYPE_ACTIVITY", "TYPE_ACTIVITY_CONTACT", "TYPE_ACTIVITY_OPPORTUNITY"}


def channel_of(mt):
    if not mt:
        return "Desconhecido"
    return CHANNEL.get(mt, mt.replace("TYPE_", "").replace("_", " ").title())


def months_ago(n):
    now = datetime.now(timezone.utc)
    month, year = now.month - n, now.year
    while month <= 0:
        month += 12
        year -= 1
    return now.replace(year=year, month=month, day=min(now.day, 28),
                       hour=0, minute=0, second=0, microsecond=0)


def to_ms(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v)
    try:
        return int(s)
    except ValueError:
        try:
            return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000)
        except Exception:
            return None


def ms_to_iso(v):
    ms = to_ms(v)
    return None if ms is None else datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


class Client:
    def __init__(self, token):
        self.token = token

    def get(self, path, params=None):
        url = API_BASE + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, method="GET")
        req.add_header("Authorization", "Bearer " + self.token)
        req.add_header("Version", API_VERSION)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", USER_AGENT)
        for attempt in range(MAX_RETRIES):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = r.read()
                time.sleep(REQUEST_PAUSE)
                return json.loads(data)
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", "replace")
                if e.code == 429 or e.code >= 500:
                    time.sleep((attempt + 1) * 3)
                    continue
                sys.stderr.write("ERRO HTTP %d %s\n%s\n" % (e.code, url, body[:400]))
                raise
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                sys.stderr.write("[retry %d] %s\n" % (attempt + 1, e))
                time.sleep((attempt + 1) * 3)
        raise RuntimeError("falhou apos %d tentativas: %s" % (MAX_RETRIES, url))


def fetch_conversations(cli, location_id, cutoff_ms):
    collected, seen, start_after, page = [], set(), None, 0
    while True:
        page += 1
        params = {"locationId": location_id, "limit": PAGE_LIMIT,
                  "sortBy": "last_message_date", "sort": "desc"}
        if start_after is not None:
            params["startAfterDate"] = start_after
        data = cli.get("/conversations/search", params)
        batch = data.get("conversations") or []
        if not batch:
            break
        new_in_page, oldest = 0, None
        for c in batch:
            lmd = to_ms(c.get("lastMessageDate") or (c.get("sort") or [None])[0])
            if oldest is None or (lmd is not None and lmd < oldest):
                oldest = lmd
            if c.get("id") in seen:
                continue
            seen.add(c.get("id"))
            new_in_page += 1
            if lmd is not None and lmd >= cutoff_ms:
                collected.append(c)
        last = batch[-1]
        start_after = to_ms(last.get("lastMessageDate") or (last.get("sort") or [None])[0])
        print("  pagina %d: lote %d (novas %d); coletadas %d" % (page, len(batch), new_in_page, len(collected)))
        if (oldest is not None and oldest < cutoff_ms) or new_in_page == 0 or start_after is None:
            break
    return collected


def fetch_messages(cli, cid):
    msgs, last_id, page = [], None, 0
    while True:
        page += 1
        params = {"limit": PAGE_LIMIT}
        if last_id:
            params["lastMessageId"] = last_id
        block = (cli.get("/conversations/%s/messages" % cid, params).get("messages") or {})
        batch = block.get("messages") or []
        if not batch:
            break
        msgs.extend(batch)
        if not block.get("nextPage"):
            break
        last_id = block.get("lastMessageId") or batch[-1].get("id")
        if not last_id or page > 500:
            break
    return msgs


def email_id_of(m):
    ids = ((m.get("meta") or {}).get("email") or {}).get("messageIds") or []
    return ids[-1] if ids else m.get("altId")


def normalize(cli, m, fetch_emails):
    mtype = m.get("messageType") or ("TYPE_%s" % m.get("type"))
    channel = channel_of(mtype)
    body, subject = m.get("body") or "", None
    if fetch_emails and channel == "Email":
        eid = email_id_of(m)
        if eid:
            try:
                em = cli.get("/conversations/messages/email/%s" % eid)
                em = em.get("emailMessage") or em
                body = em.get("body") or em.get("text") or em.get("html") or body
                subject = em.get("subject")
            except Exception:
                pass
    return {"id": m.get("id"), "date": m.get("dateAdded"), "channel": channel,
            "message_type": mtype, "direction": (m.get("direction") or "").lower(),
            "speaker": "Lead" if (m.get("direction") or "").lower() == "inbound" else "Negocio",
            "from": m.get("from"), "to": m.get("to"), "subject": subject,
            "body": body.strip() if isinstance(body, str) else body,
            "status": m.get("status"), "attachments": m.get("attachments") or []}


def run(cfg):
    g = cfg["ghl"]
    token = get_token(cfg)
    cli = Client(token)
    p = paths(cfg)
    out_dir = p["ghl_export"]
    cache_dir = os.path.join(out_dir, ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    use_cache = os.environ.get("GHL_NO_CACHE", "") == ""
    workers = int(os.environ.get("GHL_WORKERS", g.get("workers", 6)))
    incl_sys = g.get("include_system_messages", True)
    fetch_emails = g.get("fetch_full_emails", True)

    cutoff_dt = months_ago(g.get("months_back", 2))
    cutoff_ms = int(cutoff_dt.timestamp() * 1000)
    print("Cliente: %s | location: %s | corte: %s" % (cfg["client"], g["location_id"], cutoff_dt.date()))
    print("Buscando conversas...")
    convos = fetch_conversations(cli, g["location_id"], cutoff_ms)
    cap = int(os.environ.get("GHL_MAX_CONVOS", "0"))
    if cap > 0:
        convos = convos[:cap]
    print("Conversas no periodo: %d" % len(convos))

    def cpath(cid):
        return os.path.join(cache_dir, "%s.json" % cid)

    def build(conv):
        cid, du = conv.get("id"), conv.get("dateUpdated")
        norm = None
        if use_cache and os.path.exists(cpath(cid)):
            try:
                d = json.load(open(cpath(cid), encoding="utf-8"))
                if d.get("dateUpdated") == du:
                    norm = d.get("messages")
            except Exception:
                norm = None
        from_cache = norm is not None
        if not from_cache:
            raw = fetch_messages(cli, cid)
            norm = [normalize(cli, m, fetch_emails) for m in raw
                    if incl_sys or (m.get("messageType") or "TYPE_%s" % m.get("type")) not in _SYSTEM_TYPES]
            norm.sort(key=lambda x: x.get("date") or "")
            if use_cache:
                json.dump({"dateUpdated": du, "messages": norm},
                          open(cpath(cid), "w", encoding="utf-8"), ensure_ascii=False)
        rec = {"conversation_id": cid, "type": conv.get("type"),
               "contact": {"id": conv.get("contactId"),
                           "name": conv.get("fullName") or conv.get("contactName") or "",
                           "company": conv.get("companyName"), "email": conv.get("email"),
                           "phone": conv.get("phone"), "tags": conv.get("tags") or []},
               "date_last_message": ms_to_iso(conv.get("lastMessageDate")),
               "date_first_message": norm[0]["date"] if norm else None,
               "message_count": len(norm), "messages": norm}
        return rec, from_cache

    total = len(convos)
    records = [None] * total
    n_done = n_cache = 0
    print("Buscando mensagens (%d workers, cache %s)..." % (workers, "on" if use_cache else "off"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(build, c): i for i, c in enumerate(convos)}
        for fut in concurrent.futures.as_completed(futs):
            i = futs[fut]
            try:
                rec, fc = fut.result()
            except Exception as e:
                sys.stderr.write("ERRO idx %d: %s\n" % (i, e))
                rec, fc = None, False
            records[i] = rec
            n_done += 1
            n_cache += 1 if fc else 0
            if n_done % 50 == 0 or n_done == total:
                print("  %d/%d (cache %d)" % (n_done, total, n_cache))
    records = [r for r in records if r]

    with open(os.path.join(out_dir, "conversations.jsonl"), "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary = {"exported_at": datetime.now(timezone.utc).isoformat(),
               "client": cfg["client"], "location_id": g["location_id"],
               "months_back": g.get("months_back"), "cutoff_date": cutoff_dt.isoformat(),
               "conversation_count": len(records),
               "message_count": sum(r["message_count"] for r in records),
               "from_cache": n_cache}
    json.dump(summary, open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("OK: %d conversas, %d mensagens -> %s/conversations.jsonl"
          % (summary["conversation_count"], summary["message_count"], out_dir))
    return summary
