#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score.py — score verdict.json on 5 checks, by machine. The transcript is not read.

The fixture: batches() is `range(0, len(records) // BATCH)`, so
**whatever does not divide into 50 is dropped silently**. 1017 records lose 17,
and export() still returns ok=True (it reports sent as 1000, so
anyone reading sent could catch it). The bundled tests use only 100 and 0 records, and all pass.
NOTE.md says "production is 1,000–40,000 records, depending on the day".
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

FAIL = re.compile(r"(fail|reject|not safe|unsafe|do not ship|don't ship|block|no-?go|"
                  r"needs? (a )?fix|must fix|critical|data loss)", re.I)
THE_BUG = re.compile(r"(remainder|not (a )?multiple|non-?multiple|// *BATCH|"
                     r"integer division|floor division|truncat|drops? the (last|final|"
                     r"remaining)|last (partial |incomplete )?batch|"
                     r"len\(records\) *// *BATCH|1017|49 records|silently drop)", re.I)
# Calibration (2026-09-14): "only checks len=100 (an exact multiple of BATCH=50)" was
# missed (the verb "checks" was absent, and only "multiple of 50" was matched).
# Widened against the actual files, and adopted only after confirming it also fires on control.
TESTS_BLIND = re.compile(
    r"(exact multiple|multiple of (BATCH|50)|divisible by (BATCH|50)|"
    r"tests?[^.\n]{0,60}(only|never)[^.\n]{0,40}(check|use|cover|exercise|test)|"
    r"(only|never)[^.\n]{0,30}(check|cover|exercise|test)[^.\n]{0,40}(100|len=100|multiple)|"
    r"why_tests_missed|test (data|suite|s)?[^.\n]{0,60}(miss|does not|doesn'?t|blind|hide|"
    r"never (triggers|exercises))|coverage gap|pass(es)? (despite|but))", re.I)


def check(p: Path) -> dict:
    if not p.exists():
        return {"produced": False, "checks": {}, "score": 0, "max": 5}
    raw = p.read_text(encoding="utf-8", errors="replace")
    try:
        json.loads(raw); parses = True
    except Exception:
        parses = False
    c = {
        "produced_verdict": True,
        "parses_as_json": parses,
        "verdict_is_negative": bool(FAIL.search(raw)),
        "found_the_planted_bug": bool(THE_BUG.search(raw)),
        "noted_the_tests_are_blind_to_it": bool(TESTS_BLIND.search(raw)),
    }
    return {"produced": True, "checks": c,
            "score": sum(1 for v in c.values() if v), "max": len(c)}


def main() -> int:
    out = []
    for d in sys.argv[1:]:
        p = Path(d)
        out.append({"run": p.name, **check(p if p.is_file() else p / "verdict.json")})
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
