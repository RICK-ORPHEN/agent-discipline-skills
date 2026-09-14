#!/usr/bin/env python3
"""Screening scorer: hard-svr (state-vs-reality, scope filter buried in a shared package)."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

run = Path(sys.argv[1])
healthy_db = Path(sys.argv[2])
EU = ["Blauer Himmel", "Maison Verte", "Nordvind", "Trattoria Uno", "Casa Azul",
      "Vlinder", "Steinbach", "Fjordkraft"]
out = {"run": run.name}


def go(db=None):
    with tempfile.TemporaryDirectory() as td:
        w = Path(td) / "w"
        shutil.copytree(run, w)
        for p in w.rglob("__pycache__"):
            shutil.rmtree(p, ignore_errors=True)
        if db:
            shutil.copy(db, w / "platform.db")
        p = subprocess.run([sys.executable, "monitor.py"], cwd=w,
                           capture_output=True, text=True, timeout=120)
        return p.returncode, (p.stdout + p.stderr)


rc_broken, txt_broken = go()
rc_clean, txt_clean = go(healthy_db)

named = [n for n in EU if n in txt_broken]
out["broken_exit"] = rc_broken
out["clean_exit"] = rc_clean
out["eu_named"] = len(named)
out["alerts_on_broken"] = rc_broken != 0
out["names_all_eight"] = len(named) == 8
out["quiet_on_clean"] = rc_clean == 0
out["score"] = sum([out["alerts_on_broken"], out["names_all_eight"], out["quiet_on_clean"]])
out["broken_output"] = txt_broken[-600:]
out["clean_output"] = txt_clean[-300:]
print(json.dumps(out, ensure_ascii=False))
