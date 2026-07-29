---
name: root-cause
description: Disciplined loop to find and CONFIRM the root cause of a bug before fixing it — rank falsifiable hypotheses, prove or disprove each against ground truth (logs, the data store, a deterministic repro, a captured trace), loop until one is confirmed, then write a fix plan. Runs mostly autonomously. Use when a bug's cause is non-obvious, when a "looks correct" code reading is not enough, when you must not guess at a fix, or when the user says "find the root cause", "what's actually causing this", "confirm before fixing", or "don't just patch it".
---

# Root-cause — confirm before you fix

The discipline: **never write a fix on an unconfirmed hypothesis.** A bug is solved when *ground truth* — not code reading — proves what causes it. Code "looking correct" is the most common way to confirm the wrong thing.

Runs mostly autonomously: work the loop solo (investigate → hypothesize → confirm → plan) and present the confirmed cause + the plan. Surface ranked hypotheses in passing if the user is around (their domain knowledge re-ranks instantly), but don't block on it.

## The loop

1. **Don't start cold.** Read existing research / handoff / issue notes / memory — what's known, what's already been ruled out. Don't redo finished work.

2. **Investigate wide.** Read the wiring (search/graph), and especially use **git history as regression framing**: if it worked at state X and broke at Y, diff `X..Y` — the cause usually lives in what changed. Map the subsystem before theorizing.

3. **Rank 3–5 falsifiable hypotheses.** Each must carry a prediction: *"if X is the cause, then `<observable in the data>` will be Z."* No prediction → it's a vibe; sharpen or drop it. A hypothesis you can't test against evidence is useless here.

4. **Confirm against GROUND TRUTH — not code.** Go to the real evidence and read the smoking gun. Change one variable at a time; make the data pick the hypothesis, don't pick the one you like. Sources, roughly in order of reach:
   - **Logs / traces** from the actual run (prod or repro).
   - **State / data store** — the actual values at the moment of failure (DB rows, persisted/checkpointed state, queues).
   - **A deterministic repro** — the fastest sharp pass/fail signal you can build (the `diagnose` skill covers building one).
   - **A captured trace** of the failing request/event, replayed in isolation.

5. **Gate.**
   - **Confirmed** → write a **fix PLAN** (reviewable). Confirmation is not permission to start coding.
   - **Disproven** → loop to step 3 with what the test revealed; new evidence re-ranks.

6. **Repeat until one hypothesis is confirmed by evidence.** Then plan.

## When existing observability can't tell you — INSTRUMENT

If no current log/row/trace distinguishes the live hypotheses, add a *tagged* probe (e.g. `[DEBUG-xyz]`), re-run the exact trigger, read it, then remove it. A blind spot in the data is itself a finding — fix the observability, then continue. Don't guess to fill the gap.

## Failure modes (each burned a real session)

- **"The code looks right" → confirmed the wrong cause.** Code reading is a hypothesis *source*, never a confirmation. Only evidence confirms.
- **Ground truth can still mislead — account for the instrument.** A missing log is NOT proof of absence: check the log *level/filter* (an INFO line dropped by a WARNING-level prod logger reads as "the code never ran"). A repro that "passes" may be a test artifact, not the real path.
- **Stale / wrong-scope state.** You may be reading a later or different state than the failing one (a subflow's scope, a post-reset snapshot). Confirm you're looking at the failure's actual state.
- **Fixing before confirming.** A plausible patch on an unconfirmed cause wastes the fix *and* hides the real bug. The gate exists for exactly this.

## Output

Present: the **confirmed root cause** with the specific evidence that proves it (the log line, the row, the `X..Y` diff), the hypotheses ruled out and how, and a **fix plan**. Stop there unless told to implement.
