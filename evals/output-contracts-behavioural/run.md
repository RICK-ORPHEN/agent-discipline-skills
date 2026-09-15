# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` per run directory. **The script self-checks that the
   CSVs actually have rows** — the first version of this generator wrote two of them empty
   (`$1` used after a `shift`) and ten runs were scored against data that did not contain the
   case being tested.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full (and the work-contract.yaml next
     to it) and follow it", pointing at `../../skills/output-contracts/SKILL.md`.
3. `python3 score.py runs/*` — it **runs each produced `report.py`** twice: against the broken
   data and against the clean copy. It never greps the write-up.

The deliverable has to be something that runs. Asked for prose, both arms disclose the loss
every time and the rubric saturates — that is what the first version of this eval measured, and
why it reported a null. Asked for a cron script, four of five control runs write output a
machine cannot distinguish from a clean night.

Judge the loss signal **structurally**: non-zero exit, a degraded `status` value, a non-empty
issues list, or a positive skipped count. Matching the word "warning" in the text counts an
empty `"warnings": []` — the better design — as a false alarm.

Keep `score.py` outside any directory reachable from a run directory.
