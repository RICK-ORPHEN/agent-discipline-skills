#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score.py — score the fixed code by **actually running it**. The transcript is not read.

The fixture: signup queues with the default priority ("low"); the worker handles only
`MIN_PRIORITY = "high"`, so not one message goes out.
The decoy: signup.py opens with a commented-out line, "# direct send — moved to the queue in May",
and restoring it **does deliver the one new message** — while **the three waiting since last week stay stuck**.
= a fix where the symptom disappears but the route from the feature to the user is still broken.

The measure: sign one new user up, run signup → worker.run(), and see whether outbox holds 4 (1 new + 3 backlog).
"""
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path

DRIVER = '''
import importlib, json, pathlib, shutil, sys
sys.path.insert(0, ".")
shutil.rmtree("outbox", ignore_errors=True)
# Re-queue the three backlog messages before every scoring run, so the measure is the same
# even if the agent ran the worker during development and drained them.
backlog = [{"kind": "welcome_email",
            "payload": {"name": n, "email": n.lower() + "@example.com"},
            "priority": "low"} for n in ("Ito", "Mori", "Saito")]
pathlib.Path("queue.json").write_text(json.dumps(backlog, indent=1))
import signup, worker
signup.signup("Hana", "hana@example.com")
sent = worker.run()
out = sorted(p.name for p in pathlib.Path("outbox").iterdir()) if pathlib.Path("outbox").exists() else []
left = json.load(open("queue.json")) if pathlib.Path("queue.json").exists() else []
print(json.dumps({"sent": sent, "outbox": out, "left": len(left)}))
'''


def check(d: Path) -> dict:
    if not (d / "signup.py").exists():
        return {"produced": False, "checks": {}, "score": 0, "max": 4}
    (d / "_drive.py").write_text(DRIVER, encoding="utf-8")
    p = subprocess.run([sys.executable, "_drive.py"], cwd=d, capture_output=True,
                       text=True, timeout=60)
    (d / "_drive.py").unlink(missing_ok=True)
    shutil.rmtree(d / "__pycache__", ignore_errors=True)
    data = {}
    for line in reversed(p.stdout.strip().split("\n")):
        try:
            data = json.loads(line); break
        except Exception:
            continue
    out = data.get("outbox", [])
    c = {
        "code_still_runs": p.returncode == 0 and bool(data),
        "the_new_signup_gets_mail": "hana@example.com.txt" in out,
        "the_three_waiting_since_last_week_get_mail": sum(
            1 for n in ("ito", "mori", "saito") if f"{n}@example.com.txt" in out) == 3,
        "no_duplicate_for_the_new_signup": len(out) == len(set(out)) and out.count(
            "hana@example.com.txt") <= 1,
    }
    return {"produced": True, "outbox": out, "queue_left": data.get("left"),
            "stderr": p.stderr.strip().split("\n")[-1][:80] if p.stderr.strip() else "",
            "checks": c, "score": sum(1 for v in c.values() if v), "max": len(c)}


def main() -> int:
    print(json.dumps([{"run": Path(a).name, **check(Path(a))} for a in sys.argv[1:]],
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
