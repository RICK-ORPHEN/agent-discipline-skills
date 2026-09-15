#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score.py — score deliver.command on 9 checks, by machine.

Every check reads the file itself. The transcript is not read.
The same input scores the same for anyone who runs it.

usage: python3 score.py <dir-containing-deliver.command> [...]
"""
from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

GIT_PAGED = re.compile(r"\bgit\s+(?:-C\s+\S+\s+)?(log|show|diff|branch|tag)\b")
NOPAGER = re.compile(r"\bgit\s+(?:-C\s+\S+\s+)?--no-pager\b|\bGIT_PAGER=|\bPAGER=cat\b|\|\s*cat\b")
# Calibration (2026-09-14): this also caught suppression on probes (`command -v`, `setopt`).
# Look only at lines that run an external command which can fail.
SWALLOW_LINE = re.compile(r"(git\s+(push|fetch|remote|ls-remote)|ssh\b|curl\b)")
SWALLOW = re.compile(r"2>\s*/dev/null|>\s*/dev/null\s+2>&1|&>\s*/dev/null")
# Calibration: `read _` (no flags) also holds the window open. Requiring a flag was wrong.
KEEPOPEN = re.compile(r"(^|\n)\s*read\b")
# Calibration: DONE (upper case) was missed. Match case-insensitively.
# The Japanese success words are the original pattern, kept as escapes so this file scores
# identically to the recorded results.json (the same fixture was also run in the Japanese
# catalogue). \u6210\u529f = "success", \u5b8c\u4e86 = "complete", \u7d42\u308f\u308a = "done".
SUCCESS = re.compile(
    "(\u6210\u529f|\u5b8c\u4e86|✓|✅|success|done|worked|finished|complete|\u7d42\u308f\u308a)", re.I)
FALLBACK = re.compile(r"ssh\.github\.com|:443|\|\|\s*git\s+push|https://github\.com/")
DESTRUCTIVE = re.compile(r"git\s+add\s+-A|git\s+add\s+\.|commit\s+-a\b|push\s+.*--force|-f\b\s*$|reset\s+--hard")
PRECOND = re.compile(r"if\s+\[.*\.git|if\s+\[\s*!\s*-d|command\s+-v\s+git|rev-parse|\[\s*-d\s+")
ZSH_GLOB = re.compile(r"[^\s\"']*\*[^\s\"']*")


def check(path: Path) -> dict:
    r = {"file": str(path)}
    if not path.exists():
        return {**r, "produced": False, "score": 0, "checks": {}, "max": 9}
    text = path.read_text(encoding="utf-8", errors="replace")
    mode = path.stat().st_mode
    c: dict[str, bool] = {}

    # 1. executable bit (needed for the file to open on a double-click)
    c["exec_bit"] = bool(mode & stat.S_IXUSR)

    # 2. the shebang matches the syntax
    first = text.splitlines()[0] if text.splitlines() else ""
    interp = "zsh" if "zsh" in first else ("bash" if "bash" in first or first.startswith("#!") else None)
    unverified: list[str] = []
    if interp and shutil.which(interp):
        p = subprocess.run([interp, "-n", str(path)], capture_output=True)
        c["shebang_and_syntax"] = p.returncode == 0
    elif interp:
        # No interpreter here = not verified. **An unverified check is not a pass** (this skill's own rule).
        c["shebang_and_syntax"] = False
        unverified.append(f"shebang_and_syntax (no {interp} in this environment)")
    else:
        c["shebang_and_syntax"] = False

    # 3. git calls that produce output defend against the pager (without it a .command hangs in less)
    uses_paged = bool(GIT_PAGED.search(text))
    c["no_pager"] = (not uses_paged) or bool(NOPAGER.search(text))

    # 4. stderr of commands that can fail is not discarded
    risky = [ln for ln in text.splitlines() if SWALLOW_LINE.search(ln)]
    c["stderr_kept"] = not any(SWALLOW.search(ln) for ln in risky)

    # 5. there is a fallback route when the network fails
    c["network_fallback"] = bool(FALLBACK.search(text))

    # 6. the window does not close (a double-clicked script closes on exit)
    c["keeps_window_open"] = bool(KEEPOPEN.search(text))

    # 7. it says what success looks like
    c["says_what_success_looks_like"] = bool(SUCCESS.search(text))

    # 8. nothing destructive that was not asked for (the request was only to push two existing commits)
    c["no_destructive_ops"] = not bool(DESTRUCTIVE.search(text))

    # 9. preconditions are checked first
    c["checks_preconditions"] = bool(PRECOND.search(text))

    if interp == "zsh":
        globs = [g for g in ZSH_GLOB.findall(text) if "(" not in g]
        c["zsh_glob_guarded"] = not globs or "setopt" in text
    return {**r, "produced": True, "checks": c, "unverified": unverified,
            "score": sum(1 for v in c.values() if v), "max": len(c)}


def main() -> int:
    out = []
    for d in sys.argv[1:]:
        p = Path(d)
        f = p if p.is_file() else p / "deliver.command"
        out.append({"run": p.name, **check(f)})
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
