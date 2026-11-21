#!/usr/bin/env python3
"""Recompute every number quoted in README.md from scores.json, posthoc.json and
harness-blocks.json, and write results.json. Nothing here is typed in by hand."""
import json
from math import comb
from pathlib import Path

here = Path(__file__).resolve().parent
scores = json.loads((here / "scores.json").read_text())
posthoc = {r["run"]: r for r in json.loads((here / "posthoc.json").read_text())}
blocks = {k: v for k, v in json.loads((here / "harness-blocks.json").read_text()).items() if not k.startswith("_")}


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
touched = [r for r in scores if r["job_py_changed"]]
cats = {}
for run, b in blocks.items():
    a = run.split("-")[1]
    cats.setdefault(b["category"], {"control": 0, "treatment": 0})[a] += 1
saw = lambda r: posthoc[r["run"]]["notes_name_a_candidate_not_picked"]
res = {
    "fixture": "fixture-round2", "scorer": "../score.py, unmodified", "n_per_arm": 15,
    "date": "2026-11-21", "subjects": "the `sonnet` alias of a Claude app session's sub-agent tool",
    "pre_registered_checks": {
        "stops_on_ambiguity": line("stops_on_ambiguity"),
        "names_all_three": line("names_all_three"),
        "no_false_alarm": line("no_false_alarm"),
    },
    "mean_score": {a: round(sum(r["score"] for r in arm(a)) / 15, 2) for a in ("control", "treatment")},
    "sensitivity_excluding_untouched_job_py": {"stops_on_ambiguity": line("stops_on_ambiguity", touched)},
    "harness_blocks_by_category": cats,
    "post_hoc": {
        "discriminates": line(None, get=lambda r: posthoc[r["run"]]["discriminates"]),
        "notes_show_the_agent_saw_the_ambiguity": line(None, get=saw),
        "saw_it_and_the_job_still_proceeds": line(None, [r for r in scores if saw(r)],
                                                   get=lambda r: not r["stops_on_ambiguity"]),
    },
    "test": "Fisher exact, two-tailed",
}
(here / "results.json").write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res, indent=1))
