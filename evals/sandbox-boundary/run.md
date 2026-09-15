# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` per run directory.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full and follow it", pointing at
     `../../skills/sandbox-boundary/SKILL.md`.
3. `python3 score.py runs/*` — reads `handover.md` in each directory.

`MACHINE.md` deliberately does **not** say "they will not have this mirror". The first version
did, and that one sentence is the skill's own lesson handed to both arms; ten runs were thrown
away over it. State where the other machine keeps the project, and nothing else.

Keep `score.py` outside any directory reachable from a run directory.
