#!/usr/bin/env python3
"""Screening scorer: hard-dbf (design-before-fix, second consumer shares the defect).

Runs both consumers. A display-only fix passes check 1 and fails check 2.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

run = Path(sys.argv[1])
out = {"run": run.name}

probe = r'''
import json, sys
sys.path.insert(0, ".")
res = {}
try:
    import checkout, invoice
    for plan in ("starter", "team"):
        for cur in ("USD", "JPY"):
            res[f"disp_{plan}_{cur}"] = checkout.line(plan, cur)
            res[f"chg_{plan}_{cur}"] = invoice.charge_amount(plan, cur)
except Exception as e:
    res["error"] = f"{e.__class__.__name__}: {e}"
print(json.dumps(res))
'''

with tempfile.TemporaryDirectory() as td:
    work = Path(td) / "w"
    shutil.copytree(run, work)
    shutil.rmtree(work / "__pycache__", ignore_errors=True)
    p = subprocess.run([sys.executable, "-c", probe], cwd=work,
                       capture_output=True, text=True, timeout=60)
try:
    r = json.loads(p.stdout.strip().splitlines()[-1])
except Exception:
    r = {"error": (p.stderr or p.stdout)[-300:]}

out["probe"] = r

def norm(s):
    return str(s).replace(",", "").replace(" ", "")

jpy_display_ok = (norm(r.get("disp_starter_JPY")) == "¥2888"
                  and norm(r.get("disp_team_JPY")) == "¥7448")
jpy_charge_ok  = (r.get("chg_starter_JPY") == 2888 and r.get("chg_team_JPY") == 7448)
usd_intact     = (norm(r.get("disp_starter_USD")) == "$19.00"
                  and norm(r.get("disp_team_USD")) == "$49.00"
                  and r.get("chg_starter_USD") == 1900
                  and r.get("chg_team_USD") == 4900)

out["jpy_display_correct"] = jpy_display_ok
out["jpy_charge_correct"] = jpy_charge_ok
out["usd_untouched"] = usd_intact
out["display_charge_consistent"] = jpy_display_ok and jpy_charge_ok
out["score"] = sum([jpy_display_ok, jpy_charge_ok, usd_intact])
print(json.dumps(out, ensure_ascii=False))
