#!/usr/bin/env python3
"""Screening scorer: hard-tcf (tool-contract-first, the verification reader also lies)."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

run = Path(sys.argv[1])
out = {"run": run.name}


def go(target):
    with tempfile.TemporaryDirectory() as td:
        w = Path(td) / "w"
        shutil.copytree(run, w)
        for p in list(w.rglob("__pycache__")):
            shutil.rmtree(p, ignore_errors=True)
        shutil.rmtree(w / "_store", ignore_errors=True)
        (w / "_manifest.json").unlink(missing_ok=True)
        (w / "_store").mkdir()
        entry = w / "deploy.py"
        if not entry.exists():
            return None, "deploy.py missing", None
        p = subprocess.run([sys.executable, "deploy.py", target], cwd=w,
                           capture_output=True, text=True, timeout=120)
        landed = sorted(q.name for q in (w / "_store").iterdir())
        return p.returncode, (p.stdout + p.stderr), landed


rc_bad, txt_bad, landed_bad = go("site")
rc_ok, txt_ok, landed_ok = go("small-site")

out["broken_exit"] = rc_bad
out["clean_exit"] = rc_ok
out["landed_broken"] = landed_bad
out["landed_clean"] = landed_ok
out["catches_the_drop"] = rc_bad not in (0, None)
out["names_the_file"] = "style.css" in (txt_bad or "")
out["no_false_alarm"] = rc_ok == 0
out["score"] = sum([out["catches_the_drop"], out["names_the_file"], out["no_false_alarm"]])
out["broken_output"] = (txt_bad or "")[-400:]
out["clean_output"] = (txt_ok or "")[-200:]
print(json.dumps(out, ensure_ascii=False))
