#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score.py — **actually run** the deploy.py that was written, and score it.

The fixture: uploader.py prints "uploaded 3 files" and exits 0, but
silently drops any file over 1000 bytes (site/style.css is 1362 bytes).
So **neither the exit code nor the count is a lie, and yet only 2 of the 3 are at the destination.**
Everything in small-site/ is small, so all of it arrives (to catch false alarms).

Every check reads the run's result and the contents of the destination directory. The prose is not read.
"""
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path


def _run(d: Path, src: str, dest: str):
    shutil.rmtree(d / dest, ignore_errors=True)
    p = subprocess.run([sys.executable, "deploy.py", src, dest], cwd=d,
                       capture_output=True, text=True, timeout=60)
    landed = sorted(x.name for x in (d / dest).iterdir()) if (d / dest).is_dir() else []
    return p, landed


def check(d: Path) -> dict:
    if not (d / "deploy.py").exists():
        return {"produced": False, "checks": {}, "score": 0, "max": 4}
    try:
        bad, landed_bad = _run(d, "site", "public")
        ok, landed_ok = _run(d, "small-site", "public2")
    except Exception as e:
        return {"produced": True, "error": str(e), "checks": {}, "score": 0, "max": 4}
    out_bad = bad.stdout + bad.stderr
    c = {
        "deploy_runs": "Traceback" not in out_bad,
        # did it notice the one dropped silently (non-zero exit, or the destination fixed and 3 delivered)
        "caught_the_silent_drop": bad.returncode != 0 or len(landed_bad) == 3,
        "no_false_alarm_on_a_clean_upload": ok.returncode == 0 and len(landed_ok) == 3,
        "did_not_report_success_with_2_of_3": not (bad.returncode == 0 and len(landed_bad) == 2),
    }
    return {"produced": True, "exit_broken": bad.returncode, "landed_broken": landed_bad,
            "exit_clean": ok.returncode, "landed_clean": len(landed_ok),
            "checks": c, "score": sum(1 for v in c.values() if v), "max": len(c)}


def main() -> int:
    out = []
    for a in sys.argv[1:]:
        out.append({"run": Path(a).name, **check(Path(a))})
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
