#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ghli — CLI do pipeline de estudo de processo de atendimento (GHL).

Passos DETERMINISTICOS (Python puro, stdlib):
  init           cria um config de cliente a partir do template
  extract        Etapa 1 — puxa conversas do GHL (paralelo + cache)
  clean          Etapa 2 — limpa/qualifica para extracao de processo
  metrics        Etapa 3 — metricas deterministicas (SLA, quem larga, silencio)
  graph-prep     Etapa 4a — prepara chunks p/ extracao do grafo (subagents)
  graph-status   Etapa 4b — lista chunks faltando (auto-retry)
  graph-prompt   imprime o prompt de extracao de um chunk (com vocabulario)
  graph-merge    junta os chunks em um extract.json
  judge-prep     Etapa 5a — prepara chunks p/ o LLM-judge
  judge-prompt   imprime o prompt do judge de um chunk
  judge-aggregate Etapa 5b — agrega as classificacoes em metricas
  all            roda os passos deterministicos (extract->clean->metrics)

Passos com IA (grafo, judge, docs) sao orquestrados pelo SKILL Claude Code
(processo-atendimento), que usa graph-prep/prompt/status e judge-prep/prompt/aggregate.

Uso:
  python3 ghli.py <comando> --config clients/<cliente>.json [--chunk N]
  GHL_TOKEN=pit-... python3 ghli.py extract --config clients/instaltech.json
"""
import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ghltool import config, extract, clean, metrics, graph, judge  # noqa: E402

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))


def cmd_init(args):
    name = args.name
    dst = os.path.join(TOOL_DIR, "clients", "%s.json" % name)
    if os.path.exists(dst) and not args.force:
        sys.exit("ja existe: %s (use --force)" % dst)
    shutil.copy(os.path.join(TOOL_DIR, "clients", "_template.json"), dst)
    print("criado: %s — edite location_id, vocabulary e domain_context." % dst)


def main():
    ap = argparse.ArgumentParser(prog="ghli")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init"); pi.add_argument("name"); pi.add_argument("--force", action="store_true")

    for c in ("extract", "clean", "metrics", "graph-prep", "graph-status",
              "graph-merge", "judge-prep", "judge-aggregate", "all"):
        sp = sub.add_parser(c); sp.add_argument("--config", required=True)

    for c in ("graph-prompt", "judge-prompt"):
        sp = sub.add_parser(c); sp.add_argument("--config", required=True)
        sp.add_argument("--chunk", type=int, required=True)

    args = ap.parse_args()
    if args.cmd == "init":
        return cmd_init(args)

    cfg = config.load_config(args.config)
    c = args.cmd
    if c == "extract":
        extract.run(cfg)
    elif c == "clean":
        clean.run(cfg)
    elif c == "metrics":
        metrics.run(cfg)
    elif c == "graph-prep":
        graph.prep(cfg)
    elif c == "graph-status":
        sys.exit(1 if graph.status(cfg) else 0)
    elif c == "graph-merge":
        graph.merged_extract(cfg)
    elif c == "graph-prompt":
        print(graph.render_prompt(cfg, args.chunk))
    elif c == "judge-prep":
        judge.prep(cfg)
    elif c == "judge-prompt":
        print(judge.render_prompt(cfg, args.chunk))
    elif c == "judge-aggregate":
        judge.aggregate(cfg)
    elif c == "all":
        extract.run(cfg); clean.run(cfg); metrics.run(cfg)
        print("\nPassos deterministicos OK. Para grafo/judge/docs, rode o skill "
              "'processo-atendimento' (usa graph-prep/judge-prep).")


if __name__ == "__main__":
    main()
