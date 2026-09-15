# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` for each run directory you want.
2. Give your agent the text of `PROMPT.md`, with `<RUNDIR>` replaced by that directory.
   - **control arm**: the prompt alone.
   - **treatment arm**: the same prompt, preceded by "read this skill file in full and
     follow it" and the path to `../../skills/handoff-script-hygiene/SKILL.md`.
   - Use the same model, the same number of runs, in both arms. Five is the minimum that
     shows variance; it is not enough to call a one-point difference.
3. `python3 score.py runs/*` — it reads `deliver.command` in each directory and prints JSON.
4. Compare the arms per check, not only by the mean. The mean hides which line did the work.

`score.py` needs `bash` (and `zsh`, if any run chose it) on PATH. A shell it cannot run is
reported as **unverified**, and unverified never counts as a pass.
