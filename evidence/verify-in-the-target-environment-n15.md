# Evidence — `verify-in-the-target-environment` (third measurement, N = 15, pre-registered)

**The skill stays, and the number that justified it before was wrong.**

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 15 per arm ·
Harness: `evals/verify-in-the-target-environment-n15/`

## Why this was re-run

The first measurement put this skill in the catalog on **2/5 vs 5/5**. Applying Fisher's exact
test to the catalog's own numbers afterwards gave **p = 0.44** — the weakest entry by a wide
margin, and not distinguishable from chance. Two further problems turned up on inspection:

- the separating measure had been **added after reading the runs**, not fixed in advance
- the published README stated the control arm as `2/5` picking silently. The evidence file says
  **3/5**. The README was wrong.

A catalog whose whole claim is "every skill here was measured" cannot carry an entry like that.
So: measure it again, at N = 15, with the measure and the decision rule written down first.
`evals/.../PRE-REGISTERED.md` is that document, and it is published whole, including the part
where the first round failed.

## Round 1 — the pre-registered primary failed

| check | no skill | with skill | p |
|---|---|---|---|
| **1 stops on the ambiguity — primary** | 12/15 | 15/15 | **0.224** |
| 2 names all three candidates | 5/15 | 15/15 | 0.0002 |
| 3 no false alarm on the unambiguous case | 15/15 | 15/15 | 1.0 |

Under the rule fixed in advance, p = 0.224 on the primary sends the skill to `retired/`.

The secondary was significant, and switching to it at that point would have been exactly the
move this repository exists to refuse. It was not taken.

## What reading the twelve "stops" showed

Ten of the twelve control runs that stopped wrote the same thing: call the existing lookup
(which returns `matches[0]`), then validate **that one credential's** role. They exit non-zero
only because the first supabase entry in the snapshot happens to be `read_only`. They never
count the matches.

**The endpoint was partly measuring line order in a JSON file.** Move one entry and the
identical check passes, exits 0, and hands the job an arbitrary one of three write-capable
credentials — which is the incident this skill was written from.

That is a fixture defect, not a reason to prefer a different endpoint. So round 2 kept the
endpoint and fixed the fixture: `creds.prod.json` reordered to put a `service_role` entry
first. Five supabase entries, three write-capable, same task, same prompts, both arms re-run
fresh. Nothing from round 1 carried over.

Replaying three round-1 control checks against the reordered file, before running anything:
all three now exit 0 and silently select `global.supabase.founder_os`. A round-1 treatment
check still stops.

## Round 2 — the result

| check | no skill | with skill | p (Fisher, two-tailed) |
|---|---|---|---|
| **1 stops on the ambiguity — primary** | **2/15** | **15/15** | **0.0000018** |
| 2 names all three candidates | 2/15 | 15/15 | 0.0000018 |
| 3 no false alarm on the unambiguous case | 15/15 | 15/15 | 1.0 |

Thirteen of fifteen control runs added a startup check, verified the resolved credential can
write, ran it against the production snapshot, saw `using global.supabase.founder_os
(service_role)`, and shipped. Several said in their notes that the snapshot holds three
`service_role` candidates and that the order-dependent pick is fragile — and then let the job
proceed anyway. **The observation is in the write-up; the code still chooses one silently.**

Every treatment run stopped and named all three. None of the thirty raised a false alarm on the
unambiguous case, which is the check that keeps "stop more often" from being a free win.

## What changed in the catalog

The published line was `2/5 → 5/5`. It is now `2/15 → 15/15`, on a fixture that cannot be
passed by accident of line order, with the measure fixed before the runs.

## What this does not show

One fixture, one model, fifteen runs per arm, a short single-shot task. And the effect is
specific: this measures the 0/1/many discipline at one ambiguous lookup, not the rest of what
the skill covers.

The honest summary of the three rounds is that **the first number was not evidence** — wrong in
the README, post-hoc in its measure, and inside the noise. The skill survives on the third
measurement, not the first.

Reproduce: `evals/verify-in-the-target-environment-n15/`, which holds both fixtures (original
and reordered), the scorer, `PRE-REGISTERED.md` with its amendment, and both rounds' results.
