# Evidence — `state-vs-reality`

> **Re-measured behaviourally; the null holds.** This file scored prose. A second run
> that scores a *running monitor* reached the same answer: 5/5 in both arms.
> See `state-vs-reality-behavioural.md`. The same method overturned the null for
> `output-contracts`, so this one is not an artifact of scoring the wrong artifact.

**Result: near null on this fixture.** Published as measured.

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 5 per arm ·
Harness: `evals/state-vs-reality/`

## The fixture

A nightly sync and an hourly health check both import the same scope helper,
`WHERE status = 'active'`. Eight of twenty integrations sit at `status='error'`, frozen a
month ago. Because they are filtered out before either job looks, the sync has written
*twenty-one consecutive nights* of `rows_synced=12, errors=0, success`, and the status page
has stayed green the whole time. The ticket asks "is the sync working or not?" and carries a
decoy: the retry count was raised from 2 to 3 last month for a similar complaint.

## Result

| Arm | Mean | Runs |
|---|---|---|
| No skill | **5.2 / 6** | 5, 5, 5, 5, 6 |
| With the skill | **5.4 / 6** | 5, 5, 5, 6, 6 |

| Check | No skill | With |
|---|---|---|
| said the sync is not working for some customers | 5 / 5 | 5 / 5 |
| named the shared `status = 'active'` filter | 5 / 5 | 5 / 5 |
| noted that **both** readers share that filter | 5 / 5 | 5 / 5 |
| **counted the actual damage** (8 of 20 / 40%) | **3 / 5** | **5 / 5** |
| called the green status an artifact of scope | 3 / 5 | 2 / 5 |
| dismissed the retry decoy | 3 / 5 | 2 / 5 |

Ten runs out of ten found the filter, said the success record was meaningless, and refused
the decoy fix. The skill's only visible contribution is its reporting rule — *if you write
"fixed", count the actual damage* — which moved from 3 of 5 to 5 of 5.

## The pattern this makes visible

This is the second near-null in a row, and together with the two skills that did move, the
shape is consistent:

| Skill | Effect | What the skill asks for |
|---|---|---|
| `diagnose-first` | large, no overlap | **an action the model skips**: tabulate the population before opening the code |
| `handoff-script-hygiene` | moderate | **an action the model omits**: add a port-443 fallback |
| `output-contracts` | near null | a way of judging evidence already in hand |
| `state-vs-reality` | near null | a way of reading evidence already in hand |

**These skills pay when they require an action that would otherwise not be taken. They pay
very little when they only ask the model to reason well about material already in front of
it.** A capable model already reasons well. What it does not do on its own is go and get the
data it was not asked for, or add the route nobody mentioned.

That is a finding about the skills, not about the fixtures — and it points at the same fix in
both cases: the value of `state-vs-reality` and `output-contracts` has to be carried by
something the agent must *do* (run the unscoped count; emit a machine-checkable verdict), not
by the prose around it. Until they are rewritten that way, their measured effect on a capable
model is close to zero, and this file says so.

## What this does not show

One fixture, one model, five runs per arm. The evidence here is handed to the agent in one
directory; a real investigation has to find it first, and that is where `diagnose-first`'s
effect lived. A fixture where the unscoped count is *available but not adjacent* would test
this skill harder, and has not been built.

Reproduce: see `evals/state-vs-reality/run.md`. `results.json` holds the ten scored runs.
