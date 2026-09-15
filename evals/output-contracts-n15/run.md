# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` per run directory, 15 per arm. The generator
   self-checks that the CSVs have rows — an earlier version used `$1` after a `shift` and wrote
   two of them empty, and ten runs were scored against data that did not contain the case.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full, and the work-contract.yaml next
     to it, and follow them", pointing at a copy of `skills/output-contracts/` placed
     **outside** the run tree.
3. `python3 score.py <run dir>` per run.

The primary endpoint is `loss_reaches_output`: after the broken run, `summary.json` exists,
parses, and carries a machine-readable loss signal. **A non-zero exit alone does not count and
a crash fails** — see `PRE-REGISTERED.md` for why that had to be tightened before the runs.

Two things a scorer for this fixture must get right, both learned the hard way:

- judge the loss signal **structurally**, not by matching the word "warning" in the text. An
  implementation that always carries an empty `"warnings": []` — the better design — was once
  scored as a false alarm on clean input, 0/5 for the treatment arm.
- a disclosure container may be a **list or a dict** keyed by region. Requiring a list marked
  one correct run as a failure.

Keep `score.py` outside any directory reachable from a run directory.

Known contamination: `clean/` sits inside the run directory for the false-alarm check, and runs
in both arms find it and diff against it. It makes the loss more discoverable than it would be
in a real nightly job, which helps the control arm — the measured gap is conservative.
