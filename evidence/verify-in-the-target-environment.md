# Evidence — `verify-in-the-target-environment`

**Result: null on the pre-registered rubric. A clean effect when the produced code is
executed instead of read.** Both reported; which is which is stated.

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 5 per arm ·
Harness: `evals/verify-in-target/`

## The fixture

A credential lookup that returns `matches[0]`. The dev credential file has exactly one
supabase entry, so locally it is always right. The production snapshot has five, and the
first is `read_only` — while the README says the job needs the one that can write. Filtering
by role does not settle it either: production has **three** `service_role` supabase
credentials belonging to different systems.

The task: add a startup check so the job stops with a clear message if the credential it needs
is not available, then write notes. Nothing mentions environments, ambiguity, or verification.

## Result — the rubric written before the runs

| Arm | Mean | Runs |
|---|---|---|
| No skill | **5.0 / 5** | 5, 5, 5, 5, 5 |
| With the skill | **5.0 / 5** | 5, 5, 5, 5, 5 |

Ten out of ten opened the production snapshot, counted the five matches, and said plainly that
`matches[0]` would hand the job a read-only credential. Not one rested on the local run. On
*noticing*, the skill changed nothing.

## What the produced code actually does

Each run wrote a startup check. Running each one against the production snapshot:

| | stops on the three-way ambiguity | silently picks one of the three |
|---|---|---|
| No skill | **2 / 5** | **3 / 5** |
| With the skill | **5 / 5** | 0 / 5 |

Three control runs narrowed the ambiguity away. They filtered to the write-capable role,
found three candidates for different systems, took the first — `global.supabase.founder_os` —
and exited 0 with `using global.supabase.founder_os (service_role)`. Their notes say the right
thing; their code does the old thing one layer up. Every treatment run stopped and named all
three candidates instead.

This is the skill's own rule — *for any lookup whose answer depends on the environment, plan
for 0 / 1 / many* — and it shows up in behaviour, not in prose.

**This measure was not pre-registered.** It was added after reading the runs, like the one in
`independent-verifier.md`.

## The harness lesson, which matters more than this result

Two skills in a row measured null on their rubric and non-null when the artifact was executed.
The rubrics kept asking **"did it notice?"** — and a capable model always notices. What these
skills change is **what the code does at the point where the answer is ambiguous**.

Every rubric in this directory that scores prose is therefore weaker than it looks. Where a
skill produces a runnable artifact, the scorer should run it against the hard case and record
the exit code, not grep the write-up for the right words. The three earlier nulls
(`output-contracts`, `state-vs-reality`, `tool-contract-first`) were all scored on prose; at
least one of them deserves a second pass on this standard before its null is trusted.

## What this does not show

One fixture, one model, five runs per arm, and a post-hoc measure. The ambiguity here is
handed over in a file the agent can read; the incident the skill came from involved a resolver
whose ambiguity only appeared in an environment nobody could run.

Reproduce: see `evals/verify-in-target/run.md`. `results.json` holds the ten rubric scores.
