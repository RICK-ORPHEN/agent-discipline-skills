# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` per run directory.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full and follow it", pointing at
     `../../skills/tool-contract-first/SKILL.md`.
3. `python3 score.py runs/*` — reads `result.txt` in each directory.

**Keep `score.py` out of any directory the agent can reach from its run directory.** One run
here walked up the tree, found the scorer, and graded itself against it. Put the scorers in a
sibling folder outside the eval tree and pass absolute paths to the runs only.

**Do not let the prompt state the behaviour you are measuring.** The first version of this
fixture ended "confirm that visitors are now seeing v3" — which is the skill's whole lesson,
handed to both arms. Ten runs had to be thrown away.
