# Evidence — `state-vs-reality` (second measurement, behavioural)

**The null holds.** Re-run on the standard that overturned `output-contracts`, this skill still
shows no effect: 5/5 in both arms, every check.

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 5 per arm ·
Harness: `evals/state-vs-reality-v2/`

## What changed about the fixture

The first version asked for an *answer to a ticket* and scored the prose. This one asks for
**a monitor the ops team runs hourly**, and the scorer runs it: once against a database where
8 of 20 integrations have been stuck for a month, once against a healthy copy.

The trap is sitting in the directory. `scope.py` exports `integrations_in_scope()` —
`WHERE status = 'active'` — which is what the sync job uses, and `sync_runs` has twenty-one
consecutive nights of `rows_synced=12, errors=0, success`. Importing that helper is the
obvious move: it is right there, it is named "in scope", and it returns twelve rows that all
look fine.

## Result

| Arm | Mean | Runs |
|---|---|---|
| No skill | **5.0 / 5** | 5, 5, 5, 5, 5 |
| With the skill | **5.0 / 5** | 5, 5, 5, 5, 5 |

| Check (all measured by running the produced `monitor.py`) | No skill | With |
|---|---|---|
| exits non-zero on the broken database | 5 / 5 | 5 / 5 |
| names the eight that were left out | 5 / 5 | 5 / 5 |
| stays quiet on the healthy database | 5 / 5 | 5 / 5 |
| did not inherit the scope filter | 5 / 5 | 5 / 5 |

Not one run imported the helper. Every control run said, unprompted, that `sync_runs.result`
is the job's own bookkeeping over whatever the filter let through, read the full
`integrations` table instead, and exited 1 naming the eight stuck customers.

## Why this result matters more than another null

`output-contracts` flipped when it was re-measured this way. If the behavioural method simply
favoured the treatment arm, this one would have flipped too. It did not. **The method
discriminates; the skill does not** — at least on this failure and this model.

The two results together are the strongest statement in this directory:

- where the skill's rule has to survive being turned into code that runs unattended
  (`output-contracts`: put the loss in the output, not in stderr), the model needs telling —
  4 of 5 fail without it
- where the rule is about not trusting a number in front of you (`state-vs-reality`), the
  model already does not trust it — 10 of 10, in prose and in code

## What this does not show

One fixture, one model, five runs per arm. The trap here is visible: `scope.py` is a small
file in the same directory and the filter is its only content. A shared helper buried in a
package, used by six call sites, with the filter three layers down, is a harder version of
the same test and has not been built. The first measurement's limitation applies too — the
evidence is handed over in one directory rather than having to be found.

Reproduce: see `evals/state-vs-reality-v2/run.md`. `results.json` holds the ten scored runs.
