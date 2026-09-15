# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` per run directory. It self-checks that the stale
   `MIN_PRIORITY = "high"` filter is present — without it there is no bug to find.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced, and tell it to work only inside that
   directory.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full and follow it", pointing at
     `../../skills/design-before-fix/SKILL.md`.
3. `python3 score.py runs/*` — it **runs the fixed code**: reseeds the three stuck jobs,
   signs a new user up, drains the worker, and counts the outbox. Four letters means the
   delivery path was fixed; one means only the symptom was.

The scorer reseeds the backlog itself, so it does not matter whether the agent drained the
queue while testing. Build that in — several runs here did drain it.

Both arms score 4/4. The bait (a commented-out direct send, labelled with the month it was
replaced) was taken by nobody.
