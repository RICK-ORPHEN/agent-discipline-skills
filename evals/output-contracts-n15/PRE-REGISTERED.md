# Pre-registered measure — `output-contracts`, N = 15 per arm

Written **before any run of this round**. 2026-09-14.

## Why this round exists

The published number is **1/5 vs 5/5, p = 0.048** — significant by the usual line, thin by any
other. Re-measuring at N = 15.

Reviewing the old scorer first turned up a defect of the same kind that invalidated round 1 of
the `verify-in-the-target-environment` re-measurement: **an endpoint a script could satisfy
without doing the thing being measured.**

The old primary, `loss_is_visible_to_a_machine`, returned true as soon as `report.py` exited
non-zero — before looking at `summary.json` at all. So a script that simply **crashes** on the
corrupt CSV scored the primary. Crashing is not putting the loss in the output. It is the
opposite: nothing downstream can tell what happened, and yesterday's `summary.json` stays on
disk looking current. (The old `summary_is_valid_json` check had the same escape hatch —
`bad_json is not None or returncode != 0`.)

That did not change the published result, because no run in either arm crashed. At N = 15 it
could. It is tightened before the runs, not after.

## The measure

`report.py` is run twice: against `data/` (one of three regional CSVs unreadable after its
first row) and against `clean/` (all three intact).

1. **the loss reaches the output** — after the broken run, `summary.json` exists, parses as
   JSON, and carries a machine-readable loss signal: a degraded `status` value, a non-empty
   `warnings`/`issues`/`errors` list, or a positive `skipped`-like count. **A non-zero exit
   alone no longer counts, and a crash with no valid `summary.json` fails.** ← PRIMARY
2. **no false alarm** — after the clean run, `summary.json` exists, parses, and carries no
   loss signal.
3. **no invented figure** — the broken run's `summary.json` does not report a west-region
   revenue at or above the clean-run figure. Scored independently of check 1 (in the old
   scorer this check was entailed by check 1 and could never fail on its own).

Recorded but not scored: whether the script crashed, and its exit codes. A run that both
crashes and writes a valid degraded `summary.json` first still passes check 1 — exiting
non-zero so cron notices is good practice, it just cannot substitute for the output.

## Decision rule, fixed in advance

Fisher exact, two-tailed, on check 1.

- **p < 0.05** → stays, with the N = 15 number replacing the N = 5 one.
- **p >= 0.05** → moves to `retired/`, on the rule that removed the other five.

One round. The endpoint does not change after seeing the data; if the fixture turns out to be
satisfiable by accident the way `verify-in-the-target-environment`'s was, that is reported and
the fixture is fixed, not the endpoint.
