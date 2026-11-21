#!/usr/bin/env python3
"""POST-HOC. Written after the thirty transfer runs were scored. Decides nothing.

Did the agent write down that several label printers were ready? The round-2 re-run asked the
same thing by looking for the names of the candidates the job would not have picked. That does
not work here: control agents name `dock-west-label` for another reason (testing that an
offline printer listed first is skipped). So this looks for the statement itself in notes.md:
a word for "more than one" within a clause of the word "ready".

It is a pattern over prose, the kind of measure this repository distrusts, and it is reported
as a description only. The matching sentences are printed so the count can be checked by eye.

Usage: python3 posthoc.py            (from this directory; writes posthoc.json)
"""
import json, re
from pathlib import Path

here = Path(__file__).resolve().parent
MANY = r"(several|multiple|three|3|more than one)"
PAT = re.compile(rf"\b{MANY}\b[^.\n]{{0,60}}\bready\b|\bready\b[^.\n]{{0,40}}\b{MANY}\b", re.I)

rows = []
for s in json.loads((here / "scores.json").read_text()):
    notes_file = here / "runs" / s["run"] / "notes.md"
    notes = notes_file.read_text() if notes_file.exists() else None
    m = PAT.search(notes) if notes else None
    line = next((l.strip() for l in notes.splitlines() if PAT.search(l)), None) if notes else None
    rows.append({"run": s["run"], "arm": s["arm"], "stops_on_ambiguity": s["stops_on_ambiguity"],
                 "notes_say_several_are_ready": None if notes is None else bool(m), "matched_line": line})
(here / "posthoc.json").write_text(json.dumps(rows, indent=1) + "\n")
for arm in ("control", "treatment"):
    a = [r for r in rows if r["arm"] == arm]
    said = [r for r in a if r["notes_say_several_are_ready"]]
    print(f"{arm:9s} n={len(a)}  notes_say_several_are_ready={len(said)}"
          f"  said_it_and_stopped={sum(r['stops_on_ambiguity'] for r in said)}"
          f"  said_it_and_proceeded={sum(not r['stops_on_ambiguity'] for r in said)}")
for r in rows:
    if r["arm"] == "control" and r["matched_line"]:
        print(" ", r["run"], "|", r["matched_line"][:150])
