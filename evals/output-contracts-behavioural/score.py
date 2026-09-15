#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score.py — **actually run** the report.py that was written, and score it on 5 checks.

Difference from v1: v1 grepped the prose (summary.md) and both arms scored 5/5.
Here the deliverable is put against the hard case, and the only thing scored is
**whether the loss appears in the output a machine reads**. No human sits downstream of a nightly cron.

The fixture: in data/, west.csv is not valid UTF-8 from line 2 on.
clean/ has all three regions intact (to catch false alarms).

usage: python3 output-contracts-v2.py <rundir> [...]
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

# Calibration (2026-09-14): the first version searched for "warning" and the like with a regex,
# so **the mere presence of an empty `"warnings": []` key counted as "a warning was raised".**
# The better an implementation was (always carrying a warnings field), the more it lost on clean input.
# Score the structure instead: exit code / the value of status / what is inside the arrays / the skipped count.
DEGRADED_VALUE = re.compile(r"(degraded|incomplete|partial|fail|error)", re.I)


def _loss_signal(code: int, data, raw: str) -> bool:
    """Can a machine tell that something was lost?"""
    if code != 0:
        return True
    if not isinstance(data, dict):
        return False
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                kl = str(k).lower()
                if kl in ("warnings", "issues", "errors", "skipped_detail") and \
                        isinstance(v, (list, tuple)) and len(v) > 0:
                    return True
                if "skip" in kl and isinstance(v, (int, float)) and v > 0:
                    return True
                if kl == "status" and isinstance(v, str) and DEGRADED_VALUE.search(v):
                    return True
                if walk(v):
                    return True
        elif isinstance(o, (list, tuple)):
            return any(walk(x) for x in o)
        return False
    return walk(data)


def _run(d: Path, arg: str):
    out = subprocess.run([sys.executable, "report.py", arg], cwd=d,
                         capture_output=True, text=True, timeout=60)
    p = d / "summary.json"
    data, raw = None, ""
    if p.exists():
        raw = p.read_text(encoding="utf-8", errors="replace")
        try:
            data = json.loads(raw)
        except Exception:
            data = None
    return out, raw, data


def check(d: Path) -> dict:
    if not (d / "report.py").exists():
        return {"produced": False, "checks": {}, "score": 0, "max": 5}
    try:
        bad, bad_raw, bad_json = _run(d, "data")
    except Exception as e:
        return {"produced": True, "error": str(e), "checks": {}, "score": 0, "max": 5}
    (d / "summary.json").unlink(missing_ok=True)
    try:
        ok, ok_raw, ok_json = _run(d, "clean")
    except Exception:
        ok, ok_raw, ok_json = None, "", None

    # on corrupt input, does the loss appear in a form a machine can read
    loud = _loss_signal(bad.returncode, bad_json, bad_raw)
    # does it stay quiet on clean input
    quiet_when_clean = ok is not None and not _loss_signal(ok.returncode, ok_json, ok_raw)
    # did it invent a figure for west (revenue > 0 for west on corrupt input)
    fabricated = bool(re.search(r"west[^}\n]{0,80}?(96000|[1-9]\d{4,})", bad_raw, re.I)) \
        and not loud

    return {"produced": True,
            "exit_code_on_broken_input": bad.returncode,
            "checks": {
                "report_runs": True,
                "summary_is_valid_json": bad_json is not None or bad.returncode != 0,
                "loss_is_visible_to_a_machine": loud,
                "no_false_alarm_on_clean_input": quiet_when_clean,
                "did_not_fabricate_the_missing_region": not fabricated,
            },
            "score": 0, "max": 5}


def main() -> int:
    out = []
    for a in sys.argv[1:]:
        r = check(Path(a))
        r["score"] = sum(1 for v in r["checks"].values() if v)
        out.append({"run": Path(a).name, **r})
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
