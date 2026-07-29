---
name: agent-model-policy
description: Model-selection policy for ANY subagent/Task dispatch. Use BEFORE dispatching, delegating, spawning, or fanning out subagents — single or parallel — including every superpowers flow (subagent-driven-development, dispatching-parallel-agents, executing-plans, requesting-code-review) and any direct Task/agent dispatch. Decides which Claude model each agent runs on. Triggers on: dispatch a subagent, delegate a task, parallel agents, spawn an agent, Explore agent, code reviewer agent, "which model for this agent", filling a `model:` field.
---

# Agent Model Policy

When dispatching any subagent (Task tool, superpowers flows, parallel fan-out),
**always set the `model:` field explicitly** — an omitted model silently
inherits the session's most expensive model.

Pick the model by the agent's role:

| Role | Model | Examples |
|---|---|---|
| **Routine research / reading / exploration** (read-only) | `claude-haiku-4-5` | Explore-type agents, codebase search, reading files to gather context, doc/spec review, "find where X is", summarizing sources |
| **Implementation** | `claude-opus-4-8` | implementer subagent, fix subagent, writing/editing code, building a feature |
| **Review** | `claude-opus-4-8` | per-task review, code review, whole-branch review, security/correctness review |

## Rules

- Default the bulk of work (the high-volume read/search/gather agents) to **Haiku** — that's where the cost lives.
- Implementation and review go to **Opus 4.8** — quality over cost on the few tasks that matter.
- One genuinely-harder exception is fine: if a "routine" read is actually subtle reasoning, bump it up — and say so in one line.
- This policy overrides any vaguer "use the least powerful model" guidance in other skills.

## Why this exists

The default behavior leans on Sonnet for routine agents, which is slow and
costly for read/search work. Haiku handles that fine; Opus is reserved for the
implementation and review steps where correctness pays off.
