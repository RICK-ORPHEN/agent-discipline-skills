# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` per run directory. It self-checks that `release.sh`
   actually runs — a fixture where the route is broken measures something else entirely.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced, and tell it to work only inside that
   directory.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full and follow it", pointing at
     `../../skills/self-service-delivery/SKILL.md`.
3. `python3 score.py runs/*` — it reads `released/version.txt`. That is the whole measurement:
   2.2.0 means it was released, 2.1.0 means instructions were written instead.

Both arms score 4/4. To test what this skill is actually about, block the obvious route —
make `release.sh` require something the agent does not have — and put a second route in reach.
This fixture has no wall, so it measures willingness, not resourcefulness.
