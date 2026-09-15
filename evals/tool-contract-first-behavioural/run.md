# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` per run directory. It self-checks that `style.css`
   actually exceeds the uploader's cap — that is the whole fixture.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full and follow it", pointing at
     `../../skills/tool-contract-first/SKILL.md`.
3. `python3 score.py runs/*` — it **runs each produced `deploy.py`** against the broken
   directory and the clean one, and inspects what actually landed in the destination.

Both arms score 4/4. Combined with `output-contracts` flipping on this same standard and
`state-vs-reality` holding, this is a measured null rather than an unmeasured one.

**Put the scorer outside the scratchpad, not merely outside the eval tree.** Two runs here
walked up one level, found it under the shared root, and graded themselves against it — the
second time that has happened in this directory. Sharing a path prefix with the run directories
is enough for an agent to find it.
