# -*- coding: utf-8 -*-
"""Carrega config de cliente (JSON) e resolve caminhos/segredos."""
import json
import os
import sys

DEFAULTS = {
    "ghl": {"months_back": 2, "workers": 6, "fetch_full_emails": True,
            "include_system_messages": True, "token_env": "GHL_TOKEN"},
    "objective": "process",
    "cleaning": {"min_turns": 3, "ratio_max": 8, "group_min": 10, "sample_n": 25,
                 "channel_noise": ["Sistema", "Activity Appointment", "Internal Comment"],
                 "extra_scrub_patterns": []},
    "graph": {"chunks": 15},
    "judge": {"chunks": 11},
    "output_dir": ".",
}


def _merge(base, over):
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg = _merge(DEFAULTS, cfg)
    if not cfg.get("client"):
        cfg["client"] = os.path.splitext(os.path.basename(path))[0]
    return cfg


def get_token(cfg):
    env = cfg["ghl"].get("token_env", "GHL_TOKEN")
    tok = os.environ.get(env)
    if not tok:
        sys.exit("ERRO: variavel de ambiente %s nao definida (token GHL). "
                 "Rode: export %s=pit-..." % (env, env))
    return tok


def paths(cfg):
    base = cfg.get("output_dir", ".")
    p = {
        "base": base,
        "ghl_export": os.path.join(base, "ghl_export"),
        "process_dataset": os.path.join(base, "process_dataset"),
        "convs": os.path.join(base, "process_dataset", "convs"),
        "graphify_out": os.path.join(base, "graphify-out"),
        "docs": os.path.join(base, "docs"),
    }
    return p
