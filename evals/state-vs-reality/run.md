# How to re-run this eval

1. `python3 make_fixture.py runs/<arm>-<n>` per run directory.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full (and the references/procedure.md
     it points to) and follow it", pointing at `../../skills/state-vs-reality/SKILL.md`.
3. `python3 score.py runs/*` — reads `answer.txt` in each directory.

Read the per-check table. Nine of the twelve cells are 5/5 in both arms; the whole measured
difference is whether the answer put a number on the damage.

If you want a fixture that tests this skill harder, move the unscoped count out of the
directory — the effect that showed up elsewhere came from having to go and get data nobody
asked for, not from reading what was already on the desk.
