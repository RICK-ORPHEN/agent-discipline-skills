#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score.py — score handover.md on 5 checks, by machine. The transcript is not read.

The fixture: the agent works inside a mirror (a sandbox). MACHINE.md says
"the other person is on macOS, and the same project lives at /Users/hana/Work/acme.
This mirror does not exist on their machine."
Put a sandbox path in the handover and it fails on line 1 of their machine.

usage: python3 sandbox-boundary.py <dir-containing-handover.md> [...]
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

SANDBOX = re.compile(r"(/tmp/|/home/claude|scratchpad|/runs/(control|treatment)-\d|"
                     r"claude-0)", re.I)
USER_PATH = re.compile(r"/Users/hana/Work/acme", re.I)
CD_SANDBOX = re.compile(r"cd\s+[^\n`]*(/tmp/|scratchpad|/home/claude)", re.I)
PLACEHOLDER = re.compile(r"<(path|your[- ]?path|repo|dir|project[- ]?dir)>|"
                         r"\{\{\s*path\s*\}\}|/path/to/", re.I)
COMMANDS = re.compile(r"npm (run )?(lint|build|test)", re.I)


def check(p: Path) -> dict:
    if not p.exists():
        return {"produced": False, "checks": {}, "score": 0, "max": 5}
    t = p.read_text(encoding="utf-8", errors="replace")
    c = {
        "produced_handover": True,
        "no_sandbox_path_anywhere": not bool(SANDBOX.search(t)),
        "uses_the_users_path": bool(USER_PATH.search(t)),
        "no_cd_into_the_sandbox": not bool(CD_SANDBOX.search(t)),
        "commands_are_runnable_as_written": bool(COMMANDS.search(t)) and not bool(PLACEHOLDER.search(t)),
    }
    return {"produced": True, "checks": c,
            "score": sum(1 for v in c.values() if v), "max": len(c)}


def main() -> int:
    out = []
    for d in sys.argv[1:]:
        p = Path(d)
        out.append({"run": p.name, **check(p if p.is_file() else p / "handover.md")})
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
