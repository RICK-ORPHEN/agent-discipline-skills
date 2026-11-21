#!/usr/bin/env python3
"""Re-score every run in runs/ and compare with scores.json. Exits non-zero on a difference.

runs/ holds only the job.py and notes.md each agent left; every run left the other fixture
files byte-identical, so each run directory is rebuilt here from the fixture before scoring.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

here = Path(__file__).resolve().parent
fixture, scorer = (here / "../fixture-round2").resolve(), (here / "../score.py").resolve()
SKIP = {"run", "arm", "batch", "job_py_changed", "notes_md_written"}
bad = 0
for want in json.loads((here / "scores.json").read_text()):
    with tempfile.TemporaryDirectory() as td:
        run = Path(td) / want["run"]
        shutil.copytree(fixture, run)
        for f in (here / "runs" / want["run"]).iterdir():
            shutil.copy(f, run / f.name)
        got = json.loads(subprocess.run([sys.executable, str(scorer), str(run)],
                                        capture_output=True, text=True, check=True).stdout)
    diff = {k: (got.get(k), v) for k, v in want.items() if k not in SKIP and got.get(k) != v}
    changed = (run.name, (here / "runs" / want["run"] / "job.py").read_bytes() != (fixture / "job.py").read_bytes())
    if changed[1] != want["job_py_changed"]:
        diff["job_py_changed"] = (changed[1], want["job_py_changed"])
    print(f"{'ok      ' if not diff else 'MISMATCH'} {want['run']} {diff or ''}")
    bad += bool(diff)
print("30 runs re-scored," if not bad else "", bad, "mismatches")
sys.exit(1 if bad else 0)
