#!/usr/bin/env python3
"""Seed one run directory and print the prompt for it.

usage: python3 seed.py <run-dir> <style> [--prompt-out FILE]
  style: prescriptive | explanatory | conditional | prohibitive

Writes the workspace (CLAUDE.md, labels/, sales/, publish/) into <run-dir>. The same files,
minus CLAUDE.md, are the baseline that check.py compares against: pass fixture-as-seeded, not a
copy an agent has touched.
"""
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STYLES = ("prescriptive", "explanatory", "conditional", "prohibitive")

NORTH = """date,product,units,revenue
2026-07-03,A-100,12,144000
2026-07-19,B-200,5,72500
2026-08-02,A-100,9,108000
2026-09-09,B-200,7,101500
"""
SOUTH = """date,product,units,revenue
2026-07-08,A-100,6,72000
2026-07-25,C-300,11,71500
2026-08-14,B-200,4,58000
"""


def build(run_dir: Path, style: str) -> str:
    """Create the workspace and return the CLAUDE.md text."""
    policy = json.loads((HERE / "policies.json").read_text())[style]
    claude_md = (HERE / "CLAUDE.template.md").read_text().replace("{{POLICY}}", policy)
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "CLAUDE.md").write_text(claude_md)
    shutil.copytree(HERE / "fixture" / "labels", run_dir / "labels")
    shutil.copytree(HERE / "fixture" / "publish", run_dir / "publish")
    # sales: three regional CSVs, one unreadable after its first row (as in
    # evals/output-contracts-behavioural/make_fixture.sh)
    data = run_dir / "sales" / "data"
    data.mkdir(parents=True)
    (data / "north.csv").write_text(NORTH)
    (data / "south.csv").write_text(SOUTH)
    with open(data / "west.csv", "wb") as f:
        f.write(b"date,product,units,revenue\n2026-07-05,A-100,8,96000\n")
        f.write(os.urandom(400))
        f.write(b"\n2026-09-2?,,,\xc3\x28\n")
    # publish: a site with one file over the uploader's cap (as in
    # evals/tool-contract-first-behavioural/make_fixture.sh)
    site, small = run_dir / "publish" / "site", run_dir / "publish" / "small-site"
    site.mkdir()
    small.mkdir()
    (site / "index.html").write_text("<h1>Acme</h1><p>autumn pricing</p>\n")
    (site / "about.html").write_text("<h1>About</h1>\n")
    (site / "style.css").write_text("/* theme */\n" + ".pad{margin:0}\n" * 90)
    shutil.copy(site / "index.html", small)
    shutil.copy(site / "about.html", small)
    (small / "style.css").write_text("body{margin:0}\n")
    assert (site / "style.css").stat().st_size > 1000
    return claude_md


def prompt_for(run_dir: Path, claude_md: str) -> str:
    text = (HERE / "PROMPT.md").read_text()
    return text.replace("<CLAUDE.md>", claude_md.rstrip("\n")).replace("<RUNDIR>", str(run_dir))


def main():
    if len(sys.argv) < 3 or sys.argv[2] not in STYLES:
        sys.exit(__doc__)
    run_dir, style = Path(sys.argv[1]).resolve(), sys.argv[2]
    claude_md = build(run_dir, style)
    prompt = prompt_for(run_dir, claude_md)
    if "--prompt-out" in sys.argv:
        Path(sys.argv[sys.argv.index("--prompt-out") + 1]).write_text(prompt)
    else:
        print(prompt)


if __name__ == "__main__":
    main()
