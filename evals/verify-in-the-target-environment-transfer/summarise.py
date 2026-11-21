#!/usr/bin/env python3
"""Recompute every number quoted in RESULTS.md from scores.json, posthoc.json, tripwire.json
and harness-blocks.json, and write results.json. Nothing here is typed in by hand."""
import json
from math import comb
from pathlib import Path

here = Path(__file__).resolve().parent
scores = json.loads((here / "scores.json").read_text())
posthoc = {r["run"]: r for r in json.loads((here / "posthoc.json").read_text())}
blocks = {k: v for k, v in json.loads((here / "harness-blocks.json").read_text()).items() if not k.startswith("_")}
tripwire = json.loads((here / "tripwire.json").read_text())["batches"]


def fisher(a, na, b, nb):
    """Two-tailed Fisher exact for a/na vs b/nb."""
    n, k = na + nb, a + b
    p = lambda x: comb(na, x) * comb(nb, k - x) / comb(n, k)
    obs = p(a)
    return sum(p(x) for x in range(max(0, k - nb), min(na, k) + 1) if p(x) <= obs * (1 + 1e-9))


def arm(name, rows=scores):
    return [r for r in rows if r["arm"] == name]


def line(key, rows=scores, get=None):
    get = get or (lambda r: r[key])
    c, t = arm("control", rows), arm("treatment", rows)
    a, b = sum(bool(get(r)) for r in c), sum(bool(get(r)) for r in t)
    return {"control": f"{a}/{len(c)}", "treatment": f"{b}/{len(t)}", "p": float(f"{fisher(a, len(c), b, len(t)):.3g}")}


assert len(scores) == 30 and len(arm("control")) == 15 and len(arm("treatment")) == 15
assert set(blocks) == {r["run"] for r in scores} == set(posthoc)
said = lambda r: posthoc[r["run"]]["notes_say_several_are_ready"]
cats = {}
for run, b in blocks.items():
    cats.setdefault(b["category"], {"control": 0, "treatment": 0})[run.split("-")[1]] += 1
primary = line("discriminates")
res = {
    "fixture": "fixture/ (label printers)", "scorer": "score.py as committed in 93fb071", "n_per_arm": 15,
    "date": "2026-11-21", "subjects": "the `sonnet` alias of a Claude app session's sub-agent tool",
    "primary": {"discriminates": primary},
    "round_2_form": {
        "stops_on_ambiguity": line("stops_on_ambiguity"),
        "names_all_three": line("names_all_three"),
        "no_false_alarm": line("no_false_alarm"),
    },
    "variant_checks": {
        "stops_without_bystanders": line("stops_without_bystanders"),
        "proceeds_on_one_ready": line("proceeds_on_one_ready"),
    },
    "mean_score": {a: round(sum(r["score"] for r in arm(a)) / 15, 2) for a in ("control", "treatment")},
    "integrity": {
        "job_py_left_untouched": sum(not r["job_py_changed"] for r in scores),
        "notes_md_missing": sum(not r["notes_md_written"] for r in scores),
        "snapshots_edited": sum(r["snapshots_edited"] for r in scores),
        "traceback_on_prod": sum(r["traceback_on_prod"] for r in scores),
        "harness_blocks_by_category": cats,
        "tripwire_paths_read_per_batch": [len(b["paths_read"]) for b in tripwire],
    },
    "post_hoc": {
        "notes_say_several_are_ready": line(None, get=said),
        "said_it_and_the_job_still_proceeds": line(None, [r for r in scores if said(r)],
                                                   get=lambda r: not r["stops_on_ambiguity"]),
    },
    "verdict": ("primary passed: p < 0.05 with treatment higher"
                if primary["p"] < 0.05 and int(primary["treatment"].split("/")[0]) > int(primary["control"].split("/")[0])
                else "primary did not pass"),
    "test": "Fisher exact, two-tailed",
}
(here / "results.json").write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res, indent=1))
