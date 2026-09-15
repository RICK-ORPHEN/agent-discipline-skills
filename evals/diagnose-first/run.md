# How to re-run this eval

1. `python3 make_fixture.py runs/<arm>-<n>` for each run directory.
2. Give your agent `PROMPT.md` with `<RUNDIR>` replaced by that directory.
   - **control**: the prompt alone.
   - **treatment**: the same prompt, preceded by "read this skill file in full and follow it"
     and the path to `../../skills/diagnose-first/SKILL.md`.
   - Same model, same count, both arms.
3. `python3 score.py runs/*` — it reads `diagnosis.txt` in each directory.
4. Read the per-check table, not only the mean. Here the whole difference sits in one line:
   whether the largest fault is named **with its row count**.

Two traps this harness already fell into, worth avoiding:

- **Do not name the deliverable `findings.md`.** Some runners refuse report-shaped filenames
  from a sub-agent, and a missing file scores as a failure — silently, and unevenly across arms.
- **Calibrate every keyword check against the actual texts before reporting a number**, and
  confirm a widened pattern still fires on the control arm. A pattern tuned while looking only
  at the treatment arm measures the pattern, not the skill.
