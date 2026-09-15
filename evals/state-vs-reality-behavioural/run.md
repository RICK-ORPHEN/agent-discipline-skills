# How to re-run this eval

1. `python3 make_fixture.py runs/<arm>-<n>` per run directory.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full (and the references/procedure.md
     it points to) and follow it", pointing at `../../skills/state-vs-reality/SKILL.md`.
3. `python3 score.py runs/*` — it **runs each produced `monitor.py`** against the broken
   database and the healthy one, and scores exit codes and output. It never greps prose.

Both arms score 5/5. That is the finding, and it is worth more than another prose null:
the same behavioural method **overturned** the null for `output-contracts`, so it is not a
method that simply flatters the treatment arm.

To make a harder version: bury the shared filter behind a package with several call sites so
that reading one small file no longer reveals it.

Keep `score.py` outside any directory reachable from a run directory.
