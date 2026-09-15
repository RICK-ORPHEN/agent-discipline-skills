# How to re-run this eval

1. Copy `batcher.py`, `test_batcher.py`, `NOTE.md` into each `runs/<arm>-<n>/`.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full and follow it", pointing at
     `../../skills/independent-verifier/SKILL.md`.
3. `python3 score.py runs/*` — reads `verdict.json` in each directory.

`score.py` covers the pre-registered rubric only: valid JSON, a negative verdict, the planted
bug, and the test-coverage gap. **Both arms hit all of it.** The difference this skill makes is
not in there — it is whether the verdict discloses that no independent model was actually used,
which was measured separately, after the fact, and is reported as post-hoc in `EVIDENCE.md`.

If you re-run this, decide *before* the runs whether disclosure is part of the rubric. Adding a
check after seeing the outputs is how a harness starts flattering the thing it measures — it is
disclosed here rather than hidden, but it is still a weaker result than the others.

Keep `score.py` outside any directory reachable from a run directory.
