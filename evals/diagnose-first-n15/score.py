#!/usr/bin/env python3
"""Pre-registered scorer: diagnose-first, N=15 round.

PRIMARY: produced the population — all five faults, each PAIRED with its own count
(same line, or within 100 characters). Digits elsewhere do not count.
"""
import json, re, sys
from pathlib import Path

FAULTS = [
    ("corrupted_audio", r"corrupt\w*|unsupported", 34),
    ("rate_limited",    r"rate[\s-]*limit\w*", 18),
    ("upload_timeout",  r"(segment[^.\n]{0,20})?upload[\s-]*timeout|timeout[^.\n]{0,20}upload", 12),
    ("too_short",       r"too[\s-]*short", 5),
    ("plan_reuse",      r"plan[\s-]*reuse|reuse[^.\n]{0,15}plan", 3),
]
WINDOW = 100
SILENT_SUCCESS = re.compile(
    r"(recovery_complete|marked?\s+complete|declared\s+success|35\s*/\s*69|35\s+of\s+69|"
    r"half (the|of the) (audio|chunks))", re.I)
NOT_ONLY_ONE = re.compile(
    r"(more than one|multiple (distinct )?(faults|failures|causes|issues)|"
    r"(two|three|four|five|\d+) (distinct|separate|unrelated) (faults|failures|causes|bugs|issues)|"
    r"more damaging|worse than|nobody (reported|noticed)|never (reported|surfaced)|unreported|"
    r"separate (bug|fault|issue)|secondary[, ]|not the (only|biggest|main)|"
    r"ahead of the|distinct faults)", re.I)

run = Path(sys.argv[1])
f = run if run.is_file() else run / "diagnosis.txt"
out = {"run": run.name}
if not f.exists():
    out.update(produced=False, produced_the_population=False, largest_fault_paired=False,
               caught_silent_success=False, said_not_the_whole=False, score=0)
    print(json.dumps(out)); sys.exit()

t = f.read_text(encoding="utf-8", errors="replace")
lines = t.splitlines()


def paired(sig_rx, count):
    """Is `count` adjacent to a match of sig_rx — same line, or within WINDOW chars?"""
    num = re.compile(rf"(?<![\d.]){count}(?![\d.])")
    for ln in lines:                       # same line
        if re.search(sig_rx, ln, re.I) and num.search(ln):
            return True
    for m in re.finditer(sig_rx, t, re.I):  # or within a window
        lo, hi = max(0, m.start() - WINDOW), min(len(t), m.end() + WINDOW)
        if num.search(t[lo:hi]):
            return True
    return False


pairs = {name: paired(rx, n) for name, rx, n in FAULTS}
named = {name: bool(re.search(rx, t, re.I)) for name, rx, n in FAULTS}

out["produced"] = True
out["faults_named"] = sum(named.values())
out["faults_paired_with_their_count"] = sum(pairs.values())
out["pairs"] = pairs
out["produced_the_population"] = all(pairs.values())            # PRIMARY
out["largest_fault_paired"] = pairs["corrupted_audio"]
out["caught_silent_success"] = bool(SILENT_SUCCESS.search(t))
out["said_not_the_whole"] = bool(NOT_ONLY_ONE.search(t))
out["score"] = sum([out["produced_the_population"], out["largest_fault_paired"],
                    out["caught_silent_success"], out["said_not_the_whole"]])
print(json.dumps(out, ensure_ascii=False))
