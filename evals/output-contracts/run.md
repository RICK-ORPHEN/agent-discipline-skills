# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` per run directory.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full (and the work-contract.yaml
     next to it) and follow it", pointing at `../../skills/output-contracts/SKILL.md`.
3. `python3 score.py runs/*` — reads `summary.md` in each directory.

Read the per-check table. The mean hides the finding here: disclosure is 5/5 in **both** arms,
and the entire difference is the verdict line.

Known limit of this fixture, kept deliberately: the loss is loud and free to admit. A fixture
that actually tests this skill has to make the workaround *look like the finished deliverable*.
