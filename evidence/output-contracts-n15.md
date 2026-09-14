# Evidence — `output-contracts` (third measurement, N = 15, pre-registered)

**The skill stays. The effect is real and larger than the p = 0.048 it was carrying, but the
control arm is better than the first measurement suggested.**

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 15 per arm ·
Harness: `evals/output-contracts-n15/`

## Why this was re-run

The published number was **1/5 vs 5/5, p = 0.048** — significant by the usual line and thin by
any other. It was one of two entries in the catalog still resting on N = 5 at the edge of
significance, and the README committed to re-measuring both.

## A defect fixed before the runs, not after

Reviewing the old scorer first turned up the same class of fault that invalidated round 1 of
the `verify-in-the-target-environment` re-measurement: **an endpoint a script could satisfy
without doing the thing being measured.**

The old primary returned true as soon as `report.py` exited non-zero, before looking at
`summary.json` at all. **A script that simply crashes on the corrupt CSV scored it.** Crashing
is not putting the loss in the output — it is the opposite: nothing downstream can tell what
happened, and last night's `summary.json` stays on disk looking current.

It did not change the old result (no run in either arm crashed, then or now), but at N = 15 it
could have. The endpoint was tightened before any run: **`summary.json` must exist, parse, and
carry the loss.** The pre-registration is published.

## Result

| check | no skill | with skill | p (Fisher, two-tailed) |
|---|---|---|---|
| **1 the loss reaches the output — primary** | **5/15** | **15/15** | **0.0002** |
| 2 no false alarm on clean input | 15/15 | 15/15 | 1.0 |
| 3 no invented figure for the lost region | 15/15 | 15/15 | 1.0 |

Ten of fifteen control runs produce a `summary.json` a machine cannot tell apart from a clean
night. They are not careless — every one handles the corrupt bytes without crashing, skips the
unparseable rows rather than guessing, and logs a warning to stderr. **The west region simply
comes out low, and nothing in the JSON says so.** The stderr line goes to cron's mail.

Several of those ten went further: they opened the `clean/` copy sitting beside `data/`,
confirmed the file was genuinely corrupted, said so in their closing message to the user, and
still shipped a `summary.json` that does not mention it. The disclosure is in the chat reply.
Nothing downstream reads the chat reply.

Every run with the skill puts it in the file — a `status` of `DEGRADED`, a non-empty warnings
container, or a per-region `rows_skipped`. None cried wolf on the clean copy, and none invented
a figure for the region it could not fully read.

## A scorer bug found *after* the runs, and what it changed

Under the pre-registration as literally worded, the treatment arm scored **14/15, p = 0.0017**.
The one apparent failure, `treatment-15`, discloses perfectly well:

```json
"warnings": {"west": ["3 line(s) were not valid UTF-8 and were skipped"]}
```

The pre-registration said "a non-empty `warnings`/`issues`/`errors` **list**", and the scorer
required a list. This is a dict keyed by region. Same disclosure, different container.

The scorer was fixed to accept either, after seeing the data. Stating that plainly because it
moves the number in the direction that flatters the skill: **14/15 → 15/15, p = 0.0017 →
0.0002.** Two things keep it honest — no control run changed under the fix (5/15 either way),
and the decision is identical under both scorings, so the fix is not outcome-determinative.
Both numbers are reported here and in `results.json`.

## What the N = 5 measurement got wrong

Not the direction — the size.

| | N = 5 | N = 15 |
|---|---|---|
| control | 1/5 (20%) | 5/15 (33%) |
| with the skill | 5/5 | 15/15 |
| p | 0.048 | 0.0002 |

The control arm is meaningfully better than one in five. The gap is still large and now firmly
outside the noise, but **the first measurement made the model look worse than it is.** That is
the less comfortable direction for an error to run, and it is the one worth saying out loud.

## What this does not show

One fixture, one model, fifteen runs per arm, a short single-shot task.

One contamination is worth naming: the `clean/` copy used for the false-alarm check sits in the
run directory, and runs in both arms found it and diffed against it. That makes the loss more
discoverable than it would be in a real nightly job. It helps the **control** arm — so the
measured gap is, if anything, conservative — but a fixture that keeps the clean copy out of
reach is the better one, and has not been built.

Reproduce: `evals/output-contracts-n15/` holds the fixture generator, `PRE-REGISTERED.md`, the
scorer, and both scorings.
