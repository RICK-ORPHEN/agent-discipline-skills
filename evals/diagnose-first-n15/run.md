# How to re-run this eval

1. `python3 make_fixture.py runs/<arm>-<n>` per run directory, 15 per arm.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full and follow it", pointing at a copy
     of `skills/diagnose-first/SKILL.md` placed **outside** the run tree.
3. `python3 score.py <run dir>` per run.

**Verify the scorer first**: run it over each directory in `calibration/` and compare with
`calibration/expected.json`. Six cases: a full table and a bulleted list pass; all five faults
named without counts, four of five paired, a plan-reuse-only answer, and a table with one wrong
count all fail.

The primary is **produced the population**: all five faults, each paired with its own count,
within the same line or 100 characters. The count has to be *next to the fault it belongs to* —
the measure this replaces required only that the digits appear somewhere in the file, which a
timestamp can satisfy.

Two checks in here saturate at 15/15 in both arms — catching the silent success, and saying the
ticket is not the whole story. They are kept for continuity. **Do not build a rubric out of
checks like those**: a capable model notices, every time, and a noticing rubric reports a null
no matter what the skill does. The difference lives in whether the numbers are attached to the
faults.

Keep `score.py` outside any directory reachable from a run directory.

Two traps this harness fell into earlier, still worth avoiding:

- **Do not name the deliverable `findings.md`.** Some runners refuse report-shaped filenames
  from a sub-agent, and a missing file scores as a failure — silently, and unevenly across arms.
- **Calibrate every pattern against real texts before reporting a number**, and confirm a
  widened pattern still fires on the control arm.
