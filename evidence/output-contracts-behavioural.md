# Evidence — `output-contracts` (second measurement, behavioural)

> **Superseded.** N = 5 at p = 0.048, and the scorer's primary counted a plain crash
> as "the loss is visible". Re-measured at N = 15 with that loophole closed first:
> `output-contracts-n15.md`. The direction held; the control arm turned out better
> than 1/5. Kept unedited.

**This overturns the earlier null.** The first measurement scored a write-up and found almost
nothing. This one runs the artifact and finds the skill decisive on the one check that matters.

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 5 per arm ·
Harness: `evals/output-contracts-behavioural/`

## What changed about the fixture

The first version asked for a **markdown report for managers** and scored the prose. Both arms
disclosed the corrupt region in words, 5/5, and the only movement was whether the word
`DEGRADED` appeared. Conclusion at the time: near null.

This version asks for **a script the ops team runs nightly from cron**. Same corrupt input —
one of three regional CSVs is unreadable after its first row — but the deliverable is
`report.py`, and the scorer runs it: once against the broken data, once against a clean copy.
There is no human reading a caveat at the end of a cron job.

## Result

| Arm | Mean | Runs |
|---|---|---|
| No skill | **4.2 / 5** | 4, 4, 4, 4, 5 |
| With the skill | **5.0 / 5** | 5, 5, 5, 5, 5 |

| Check | No skill | With |
|---|---|---|
| the script runs and writes valid JSON | 5 / 5 | 5 / 5 |
| **the loss is visible to a machine** | **1 / 5** | **5 / 5** |
| no false alarm on clean input | 5 / 5 | 5 / 5 |
| did not invent a number for the missing region | 5 / 5 | 5 / 5 |

**Four of five control scripts produce a `summary.json` that a machine cannot tell apart from
a clean night.** They are not careless: every one of them handles the corrupt bytes without
crashing, skips the unparseable rows rather than guessing, logs a warning to stderr, and
exits 0. The west region simply comes out low — 8 units where the real figure is higher — and
nothing in the JSON says so. The stderr line goes to cron's mail, which is where warnings go
to die.

Every treatment script puts the loss *in the output*: a `status` of `DEGRADED`, a non-empty
`warnings` array, a per-region `rows_skipped` count, or a non-zero exit. All five. And none of
them cried wolf on the clean copy.

## Why the first measurement was wrong

It scored the wrong artifact. Asked for prose, a capable model writes the caveat every time —
so the rubric saturated and the skill looked redundant. Asked for a program, the same model
writes one that swallows the loss four times in five. **The disclosure the model performs in
its own voice does not survive being turned into code**, and that is exactly the transition
where it matters.

`evidence/output-contracts.md` (the first run) is kept, unedited, with this file linked from
it. A null that came from a badly chosen deliverable is worth keeping visible.

## What this means for the other nulls

Three skills were scored on prose and reported null: this one, `state-vs-reality`, and
`tool-contract-first`. One of the three has now flipped. **The other two should be assumed
unmeasured until they are re-run against a runnable artifact**, not assumed ineffective.

## Method note

The scorer was wrong first, in the direction that flattered the control arm's opposite: it
looked for the word "warning" anywhere in the JSON, so a script that always carries an empty
`"warnings": []` — the better design — was scored as raising a false alarm on clean input,
0/5 for the treatment arm. Fixed by reading the structure rather than the text: a non-zero
exit, a degraded `status` value, a non-empty issue list, or a positive skipped count.

The fixture also had to be rebuilt once: the generator used `$1` after a `shift`, so two of
the three CSVs were written empty and the first ten runs were scored against data that did
not contain the case being tested. Those runs were discarded.

Reproduce: see `evals/output-contracts-behavioural/run.md`. `results.json` holds the ten scored runs.
