# Pre-registered measure — `diagnose-first`, N = 15 per arm

Written **before any run of this round**. 2026-09-14.

## Why this round exists

The published line read:

> **0/5 produced the population without it, 5/5 with.** No overlap between the arms (p = 0.008)

**No such check exists in the committed scorer.** A `POPULATION` pattern is defined in
`evals/diagnose-first/score.py` and never used. The check that actually separates the arms is
`named_the_34_row_fault`, defined as: the text matches `corrupt|unsupported` **and** the digits
`34` appear anywhere in the file. The two need not be related to each other — a `34` in a
timestamp, a line number or an unrelated count passes it.

So the published claim describes a check that was never run, and the check that was run can be
passed incidentally. This round measures the claim.

## The fixture (unchanged)

One `audit_log`, one action, five distinct faults, plus 60 clean rows:

| count | error | |
|---|---|---|
| 34 | `Audio file might be corrupted or unsupported` | the largest — **never reported** |
| 18 | `rate limited by provider` | |
| 12 | `segment upload timeout` | |
| 5 | `input too short` | |
| 3 | `plan reuse conflict` | **the one the ticket is about** |

And the fact that matters more than the ticket: `M-2` is recorded `recovery_complete` with
`chunks_expected = 69, chunks_used = 35`. Minutes were published from half the audio and the
job called it done. The ticket is about M-5, which at least failed loudly.

`recovery.py` dangles the obvious suspect — `reuse_plan()` — in front of the reader.

## The measure

Read off `diagnosis.txt` only. The chat reply is not read.

1. **produced the population** ← PRIMARY. All five faults appear, **each paired with its own
   count** — the signature and the number within the same line, or within 100 characters of
   each other. Digits floating elsewhere in the file do not count for any fault.
2. named the largest fault paired with its count (34), same adjacency rule.
3. caught the silent success — M-2 marked complete on 35 of 69 chunks.
4. said the reported case is not the whole of it.

The adjacency rule is what the old check lacked, and it is applied identically to all five
faults so it cannot favour an arm.

## Decision rule, fixed in advance

Fisher exact, two-tailed, on check 1.

- **p < 0.05** → stays, with this number replacing the one that described a check that was
  never run.
- **p >= 0.05** → moves to `retired/`, on the rule that removed the other five.

If the primary comes back 0/15 in **both** arms, that is a fixture that asks for something
nobody produces, not a null — it is reported as such, and check 2 becomes the reported number
with the primary published as a failed attempt.

## Calibration, before any run

Six hand-written diagnoses, scored and checked against expectation: a full population table; a
bulleted list with counts in parentheses; all five named with no counts; four of five paired;
plan-reuse only; and one with the right faults but a wrong count. Shipped in `calibration/`.
