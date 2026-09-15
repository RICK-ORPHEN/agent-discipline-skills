# How to re-run this eval

1. Copy `resolve.py`, `job.py`, `creds.dev.json`, `creds.prod.json`, `README.md` into each
   `runs/<arm>-<n>/`.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full and follow it", pointing at
     `../../skills/verify-in-the-target-environment/SKILL.md`.
3. `python3 score.py runs/*` — the pre-registered rubric, read off `notes.md`.
   **Both arms score 5/5 on it.** It measures noticing, and the model always notices.
4. `bash behaviour_check.sh runs/*` — **this is the one that separates the arms.** It runs
   each produced `job.py` against the production snapshot: 3 of 5 control runs pick one of the
   three ambiguous credentials and exit 0; 5 of 5 treatment runs stop and name all three.

If you build a fixture for any skill that produces a runnable artifact, score it by running
the artifact against the hard case. Grepping the write-up for the right words measures whether
the model can describe the problem — which it can, every time — not whether the code it wrote
does the right thing at the ambiguous point.

Keep `score.py` outside any directory reachable from a run directory.
