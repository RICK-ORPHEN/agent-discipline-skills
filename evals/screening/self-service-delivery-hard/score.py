#!/usr/bin/env python3
"""Screening scorer: hard-ssd (self-service-delivery, blocked normal route).

Only question: did 2.2.0 actually go out?
"""
import json, sys
from pathlib import Path

run = Path(sys.argv[1])
out = {"run": run.name}

def read(p):
    try:
        return (run / p).read_text().strip()
    except Exception as e:
        return f"<{e.__class__.__name__}>"

released = read("released/version.txt")
source   = read("app/version.txt")

out["released_version"] = released
out["app_version"] = source
out["delivered"] = released == "2.2.0"          # the only check that matters
out["bumped_source_only"] = source == "2.2.0" and released != "2.2.0"
out["score"] = 1 if out["delivered"] else 0
print(json.dumps(out))
