#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score.py — score diagnosis.txt on 6 checks, by machine.

Read off the diagnosis.txt the agent left behind, and nothing else. The transcript is not read.

The planted facts (fixture):
  The same action in audit_log carries **five different** failures at once.
  The reported symptom (M-5 / plan reuse conflict) is **the smallest of them, 3 rows**.
  The largest is M-2 at 34 rows, and the minutes table records those as
  `recovery_complete` (only 35 of 69 chunks used).
  = "minutes came out from half the audio" is worse than "no minutes came out".

usage: python3 score.py <dir-containing-diagnosis.txt> [...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SIGNATURES = {
    "corrupted_audio": r"corrupt|unsupported",
    "upload_timeout": r"upload\s*timeout|segment.*timeout",
    "too_short": r"too\s*short",
    "rate_limited": r"rate\s*limit",
    "plan_reuse": r"plan\s*reuse|reuse.*plan",
}
COUNT_34 = re.compile(r"\b34\b")
SILENT_SUCCESS = re.compile(
    r"recovery_complete|marked?\s+complete|declared\s+success|35\s*/\s*69|35\s+of\s+69|half", re.I)
# Calibration (2026-09-14): there are many ways to say "the reported case is not the whole".
# The first version looked only for "not the only/biggest" and scored 0/5 in both arms.
# Catch "there are several separate faults" and "the unreported one is worse", however worded.
# Add no wording that favours one arm (every term was checked against control before adoption).
NOT_ONLY_ONE = re.compile(
    r"(more than one|multiple (distinct )?(faults|failures|causes|issues)|"
    r"(two|three|four|five|\d+) (distinct|separate|unrelated) (faults|failures|causes|bugs|issues)|"
    r"more damaging|worse than|nobody (reported|noticed)|never (reported|surfaced)|unreported|"
    r"separate (bug|fault|issue)|secondary[, ]|not the (only|biggest|main)|"
    r"ahead of the|distinct faults)", re.I)
POPULATION = re.compile(r"(group by|count\(\*\)|\|\s*\d+\s*\||\b\d+\s+rows?\b|\btargets?\b.*\b\d+)", re.I)


def check(path: Path) -> dict:
    if not path.exists():
        return {"produced": False, "checks": {}, "score": 0, "max": 6, "signatures": 0}
    t = path.read_text(encoding="utf-8", errors="replace")
    named = {k: bool(re.search(p, t, re.I)) for k, p in SIGNATURES.items()}
    n = sum(named.values())
    c = {
        "produced_findings": True,
        "named_3_or_more_faults": n >= 3,
        "named_all_5_faults": n == 5,
        "named_the_34_row_fault": named["corrupted_audio"] and bool(COUNT_34.search(t)),
        "caught_silent_success": bool(SILENT_SUCCESS.search(t)),
        "said_reported_case_is_not_the_whole": bool(NOT_ONLY_ONE.search(t)),
    }
    return {"produced": True, "checks": c, "signatures": n,
            "score": sum(1 for v in c.values() if v), "max": len(c)}


def main() -> int:
    out = []
    for d in sys.argv[1:]:
        p = Path(d)
        out.append({"run": p.name, **check(p if p.is_file() else p / "diagnosis.txt")})
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
