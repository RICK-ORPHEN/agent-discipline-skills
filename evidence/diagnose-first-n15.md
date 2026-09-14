# Evidence — `diagnose-first` (second measurement, N = 15, population endpoint encoded)

**The published claim was true. It had simply never been measured.**

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 15 per arm ·
Harness: `evals/diagnose-first-n15/`

## Why this was re-run

The published line read:

> **0/5 produced the population without it, 5/5 with.** No overlap between the arms (p = 0.008)

**No such check existed.** A `POPULATION` pattern is defined in the committed scorer and never
used. The check that actually separated the arms was: the text matches `corrupt|unsupported`
**and** the digits `34` appear somewhere in the file — the two need not be related. A `34` in a
timestamp or an unrelated count passes it.

So the claim described a check that was never run, and the check that ran could be satisfied by
coincidence. This round measures the claim.

## The measure

Read off `diagnosis.txt` only; the chat reply is not read.

**Primary — produced the population:** all five faults appear, each **paired with its own
count**, the signature and the number within the same line or 100 characters. Digits floating
elsewhere count for nothing. The adjacency rule is applied identically to all five, so it
cannot favour an arm.

Calibrated before any run against six hand-written diagnoses, shipped in `calibration/`:
a full table and a bulleted list both pass; naming all five without counts, pairing four of
five, a plan-reuse-only answer, and a table with one wrong count all fail.

## Result

| check | no skill | with skill | p (Fisher, two-tailed) |
|---|---|---|---|
| **1 produced the population — primary** | **0/15** | **14/15** | **0.0000002** |
| 2 largest fault paired with its count | 1/15 | 15/15 | 0.0000002 |
| 3 caught the silent success | 15/15 | 15/15 | 1.0 |
| 4 said the reported case is not the whole | 14/15 | 13/15 | 1.0 |

Faults paired with their own count, per run: control averages **1.1 of 5**, with the skill
**4.8 of 5**.

**Checks 3 and 4 saturate.** Every run in both arms catches that M-2 was marked
`recovery_complete` on 35 of 69 chunks, and nearly every run says the ticket is not the whole
story. Noticing is not what separates the arms — and a rubric built only on noticing would have
reported another null, which is what the first `output-contracts` and
`verify-in-the-target-environment` rubrics did.

What separates them is whether the diagnosis carries **numbers attached to the faults**. Every
control run reaches for `reuse_plan()` — the suspect the fixture dangles, and the one the
ticket points at, with 3 rows out of 72. They describe the other faults in words. They do not
count them, so nothing in the write-up says the reported fault is the smallest of five, or that
the unreported one is eleven times larger.

## The claim was right; the code was missing

This is the one case in the series where the re-measurement **confirmed** the published number
rather than correcting it. 0/5 → 5/5 became 0/15 → 14/15, and the effect is the largest in the
catalog.

That does not make the old state acceptable. The number was carried for weeks on a check that
did not exist, next to a check that could be passed by a coincidence of digits. It happened to
be right. Nobody could have known that from the repository, which is the whole problem.

## What this does not show

One fixture, one model, fifteen runs per arm, one shape of population (five error strings in
one column of one table). A population that has to be assembled across joins, or inferred
from something other than a countable field, is a different task and is not tested here.

The adjacency window is 100 characters. A diagnosis that gives every count in a summary
paragraph far from where each fault is named would fail the primary while having done the work.
None of the thirty runs had that shape, but the fixture cannot rule it out.

Reproduce: `evals/diagnose-first-n15/` holds the fixture generator, `PRE-REGISTERED.md`, the
scorer, the six-case calibration set, and the results.
