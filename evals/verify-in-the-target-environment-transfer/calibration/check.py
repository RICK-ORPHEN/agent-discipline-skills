#!/usr/bin/env python3
"""Score every calibration case and compare with expected.json. Exits non-zero on a mismatch."""
import json, subprocess, sys
from pathlib import Path

here = Path(__file__).resolve().parent
expected = json.loads((here / "expected.json").read_text())
bad = 0
for case, want in expected.items():
    got = json.loads(subprocess.run([sys.executable, str(here.parent / "score.py"), str(here / case)],
                                    capture_output=True, text=True, check=True).stdout)
    diff = {k: (got[k], v) for k, v in want.items() if got[k] != v}
    print(f"{'ok      ' if not diff else 'MISMATCH'} {case} {diff or ''}")
    bad += bool(diff)
cases = {p.name for p in here.iterdir() if p.is_dir()}
if cases != set(expected):
    print("cases without an expectation, or the reverse:", sorted(cases ^ set(expected)))
    bad += 1
sys.exit(1 if bad else 0)
