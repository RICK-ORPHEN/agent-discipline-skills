#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score.py — score answer.txt on 6 checks, by machine. The transcript is not read.

The fixture: sync and health_check share the same scope.py (`WHERE status = 'active'`), so
the 8 broken rows (of 20) **disappear from both at once**. The nightly job records
"12 rows / 0 errors / success" 21 nights running, and the status page stays green.
The ticket carries a decoy (retry was raised 2→3 last month).
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

NOT_WORKING = re.compile(r"(not (working|syncing)|is broken|silently (skip|skipp)|"
                         r"never (attempted|synced|reached)|excluded|filtered out|"
                         r"not being synced|skipping)", re.I)
FILTER = re.compile(r"(status\s*=\s*'active'|active[- ]only|scope\.py|"
                    r"integrations_in_scope|WHERE clause|shared (filter|scope|helper))", re.I)
REAL_NUMBER = re.compile(r"(8 of 20|8/20|8 out of 20|40\s*%|eight of the twenty|"
                         r"12 of 20|12/20|only (the )?12)", re.I)
ARTIFACT = re.compile(r"(0 attempted|never (counted|attempted)|artifact|"
                      r"true but|accurate for what it looked at|"
                      r"(success|green|healthy)[^.\n]{0,80}(because|since)[^.\n]{0,80}"
                      r"(filter|scope|excluded)|"
                      r"(excluded|filtered)[^.\n]{0,80}(so|hence|therefore)[^.\n]{0,60}"
                      r"(0|zero|no) error)", re.I)
BOTH_READERS = re.compile(r"(both|health[_ ]check[^.\n]{0,60}same|same[^.\n]{0,40}"
                          r"(helper|scope|filter)[^.\n]{0,60}(health|status page)|"
                          r"status page[^.\n]{0,80}same)", re.I)
DECOY = re.compile(r"(retry|RETRY)[^.\n]{0,60}(red herring|unrelated|could not have|"
                   r"couldn't have|is not the cause|did not|doesn't address)", re.I)


def check(p: Path) -> dict:
    if not p.exists():
        return {"produced": False, "checks": {}, "score": 0, "max": 6}
    t = p.read_text(encoding="utf-8", errors="replace")
    c = {
        "produced_answer": True,
        "says_sync_not_working": bool(NOT_WORKING.search(t)),
        "names_the_shared_filter": bool(FILTER.search(t)),
        "gives_the_real_number": bool(REAL_NUMBER.search(t)),
        "calls_green_an_artifact_of_scope": bool(ARTIFACT.search(t)),
        "notes_both_readers_share_it": bool(BOTH_READERS.search(t)),
    }
    return {"produced": True, "checks": c, "dismissed_decoy": bool(DECOY.search(t)),
            "score": sum(1 for v in c.values() if v), "max": len(c)}


def main() -> int:
    out = []
    for d in sys.argv[1:]:
        p = Path(d)
        out.append({"run": p.name, **check(p if p.is_file() else p / "answer.txt")})
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
