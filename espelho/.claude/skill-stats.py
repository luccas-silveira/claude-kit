#!/usr/bin/env python3
"""Conta invocações de skill nos transcripts do Claude Code.

Uso:  python3 ~/.claude/skill-stats.py [--by-project] [--csv] [--since YYYY-MM-DD]

Fonte: ~/.claude/projects/*/*.jsonl
- tool_use name="Skill"  -> o modelo escolheu sozinho (auto)
- <command-name>/x       -> você digitou a barra (slash)
"""
import json, sys, re, collections
from pathlib import Path

ROOT = Path.home() / ".claude" / "projects"
CMD = re.compile(r"<command-name>/([\w:-]+)</command-name>")
# comandos nativos do CLI, não skills — some com --all
BUILTIN = {"clear", "model", "effort", "exit", "compact", "doctor", "plugin", "cost",
           "reload-plugins", "statusline", "terminal-setup", "help", "config", "resume",
           "login", "logout", "memory", "review", "vim", "add-dir", "agents", "context"}

args = sys.argv[1:]
by_project = "--by-project" in args
as_csv = "--csv" in args
since = None
if "--since" in args:
    since = args[args.index("--since") + 1]
NO_RUN = "--no-run" in args  # usado pelo test_skill_stats.py para importar sem varrer

# (skill, projeto, origem) -> contagem;  skill -> [primeira, ultima]
counts = collections.Counter()
span = {}


def bare_name(skill):
    """Remove prefixo 'plugin:' — installed_skills() já é sempre bare."""
    return skill.rsplit(":", 1)[-1]


def record(skill, project, source, ts):
    skill = bare_name(skill)
    if skill in BUILTIN and "--all" not in args:
        return
    counts[(skill, project, source)] += 1
    day = (ts or "")[:10]
    if not day:
        return
    lo, hi = span.get(skill, (day, day))
    span[skill] = (min(lo, day), max(hi, day))


METRICS_DIR = Path.home() / ".claude" / "metrics"


def esc(v):
    """Escapa valor de label conforme o formato de exposição do Prometheus."""
    return v.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def short_project(raw_dir, cwd):
    """Nome curto do projeto.

    O nome do diretório em ~/.claude/projects/ troca '/' e '_' pelo mesmo '-',
    então não dá para reverter por corte. Quando o transcript traz o cwd real,
    o basename dele é o nome verdadeiro da pasta.
    """
    if cwd:
        name = Path(cwd.rstrip("/")).name
        if name:
            return name
    return raw_dir


def skill_description(path):
    """Texto da 'description' do frontmatter YAML do SKILL.md.

    Escrito a mao: nao ha parser de YAML na stdlib e nenhum instalado. Precisa
    dar conta de tres formas que aparecem de verdade no disco:
      description: texto numa linha so
      description: "texto entre aspas"
      description: >          (ou |)  seguido de linhas indentadas
    O bloco dobrado e usado pelas seis skills do ponytail e pelas seis do
    caveman; parser de linha unica devolveria vazio justo nas mais pesadas.
    """
    try:
        linhas = path.read_text(errors="replace").splitlines()
    except OSError:
        return ""
    if not linhas or linhas[0].strip() != "---":
        return ""
    for i, linha in enumerate(linhas[1:], start=1):
        if linha.strip() == "---":
            return ""  # fim do frontmatter sem description
        if not linha.startswith("description:"):
            continue
        valor = linha[len("description:"):].strip()
        if valor not in (">", "|", ">-", "|-"):
            # valor inteiro entre aspas: tira. Aspas soltas no meio ficam.
            if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
                valor = valor[1:-1]
            return valor
        # bloco: junta as linhas seguintes enquanto estiverem indentadas
        partes = []
        for seguinte in linhas[i + 1:]:
            if seguinte.strip() == "---":
                break
            if seguinte.strip() and not seguinte[:1].isspace():
                break  # proxima chave, em coluna zero
            partes.append(seguinte.strip())
        return " ".join(p for p in partes if p)
    return ""


def installed_skills():
    """{nome: (origem, caminho)} das skills no disco, uma por (plugin, nome).

    Plugin em cache tem várias versões (claude-mem tem 3). Fica a de diretório
    modificado mais recentemente — comparar nome de versão não serve porque
    parte dos plugins versiona por hash de commit.

    O caminho do SKILL.md vai junto porque skill_description() precisa ler o
    arquivo para medir quanto contexto a skill custa.
    """
    found = {}  # (plugin, nome) -> (mtime, origem, caminho)
    for p in (Path.home() / ".claude" / "skills").glob("*/SKILL.md"):
        found[("", p.parent.name)] = (0, "local", p)
    cache = Path.home() / ".claude" / "plugins" / "cache"
    for p in cache.glob("*/*/*/**/skills/*/SKILL.md"):
        rel = p.relative_to(cache).parts
        plugin, version, name = rel[1], rel[2], p.parent.name
        mtime = (cache / rel[0] / plugin / version).stat().st_mtime
        key = (plugin, name)
        if key not in found or mtime > found[key][0]:
            found[key] = (mtime, "plugin", p)
    return {name: (origin, p) for (_, name), (_, origin, p) in found.items()}


def render_prom(counts, installed):
    """Texto completo do arquivo .prom."""
    out = [
        "# HELP claude_skill_invocations_total Invocacoes de skill contadas nos transcripts ainda em disco (janela movel, nao total vitalicio - transcripts antigos sao podados pelo Claude Code e o total pode cair)",
        "# TYPE claude_skill_invocations_total counter",
    ]
    for (skill, project, source), n in sorted(counts.items()):
        out.append(
            f'claude_skill_invocations_total{{skill="{esc(skill)}",'
            f'project="{esc(project)}",source="{esc(source)}"}} {n}'
        )
    out += [
        "# HELP claude_skill_installed Skill presente no disco",
        "# TYPE claude_skill_installed gauge",
    ]
    for skill, (origin, _) in sorted(installed.items()):
        out.append(
            f'claude_skill_installed{{skill="{esc(skill)}",origin="{esc(origin)}"}} 1'
        )
    out += [
        "# HELP claude_skill_context_tokens Tokens que a skill ocupa no system prompt, estimados por caractere/4 (aproximacao, nao contagem exata)",
        "# TYPE claude_skill_context_tokens gauge",
    ]
    for skill, (origin, path) in sorted(installed.items()):
        n = len(skill + skill_description(path)) // 4
        out.append(
            f'claude_skill_context_tokens{{skill="{esc(skill)}",'
            f'origin="{esc(origin)}"}} {n}'
        )
    return "\n".join(out) + "\n"


def write_prom(text, path):
    """Escreve e renomeia. Leitura concorrente nunca vê arquivo pela metade."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".prom.tmp")
    tmp.write_text(text)
    tmp.replace(path)


def main():
    for f in sorted(ROOT.glob("**/*.jsonl")):
        raw_dir = f.relative_to(ROOT).parts[0]
        file_cwd = None
        with f.open(errors="replace") as fh:
            for line in fh:
                if '"Skill"' not in line and "<command-name>" not in line:
                    continue  # filtro barato antes do json.loads
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                ts = d.get("timestamp", "")
                if since and ts[:10] < since:
                    continue
                if file_cwd is None:
                    file_cwd = d.get("cwd")
                project = short_project(raw_dir, file_cwd)
                content = (d.get("message") or {}).get("content")
                if isinstance(content, list):
                    for b in content:
                        if (
                            isinstance(b, dict)
                            and b.get("type") == "tool_use"
                            and b.get("name") == "Skill"
                        ):
                            name = (b.get("input") or {}).get("skill")
                            if name:
                                record(name, project, "auto", ts)
                elif isinstance(content, str):
                    m = CMD.search(content)
                    if m:
                        record(m.group(1), project, "slash", ts)

    if "--prom" in args:
        write_prom(render_prom(counts, installed_skills()), METRICS_DIR / "skills.prom")
        print(f"{METRICS_DIR / 'skills.prom'}: {len(counts)} series")
        return

    if not counts:
        sys.exit("nenhuma invocação encontrada")

    if as_csv:
        print("skill,projeto,origem,n")
        for (s, p, o), n in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"{s},{p},{o},{n}")
        sys.exit()

    total = collections.Counter()
    auto = collections.Counter()
    projects = collections.defaultdict(collections.Counter)
    for (s, p, o), n in counts.items():
        total[s] += n
        if o == "auto":
            auto[s] += n
        projects[s][p] += n

    print(f"{'skill':32} {'n':>5} {'auto%':>6}  período              projetos")
    for s, n in total.most_common():
        lo, hi = span.get(s, ("?", "?"))
        top = ", ".join(f"{p}({c})" for p, c in projects[s].most_common(3 if by_project else 1))
        print(f"{s:32} {n:5} {100*auto[s]//n:5}%  {lo}..{hi}  {top}")
    print(f"\n{len(total)} skills, {sum(total.values())} invocações")


if __name__ == "__main__" and not NO_RUN:
    main()
