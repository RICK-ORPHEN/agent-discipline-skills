# Evidence — `tool-contract-first` (second measurement, behavioural)

**The null holds.** 4/4 in both arms, ten runs out of ten.

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 5 per arm ·
Harness: `evals/tool-contract-first-behavioural/`

## The fixture

An uploader that tells the truth and lies at the same time. It prints `uploaded 3 files` and
exits 0 — and it does examine three files — but it silently skips anything over its own
1000-byte cap. `site/style.css` is 1362 bytes, so two of three files reach the destination.
A second directory, `small-site/`, is entirely under the cap and uploads cleanly.

The task: write `deploy.py` that publishes a directory using the uploader, exiting non-zero
when something needs attention because it runs from cron. Nothing suggests distrusting the
exit code.

## Result

| Arm | Mean | Runs |
|---|---|---|
| No skill | **4.0 / 4** | 4, 4, 4, 4, 4 |
| With the skill | **4.0 / 4** | 4, 4, 4, 4, 4 |

Every run, both arms: read the uploader's source, found the size cap and the unconditional
`return 0`, and wrote a deploy script that compares the destination against the source after
the upload — most with `filecmp.cmp(..., shallow=False)` rather than a size check. All ten
exit non-zero on the broken directory, naming `style.css`, and exit 0 on the clean one.

Two of them read `MAX` out of the uploader module instead of hardcoding 1000, because the
comment says the provider raised it once already.

## Where this leaves the three prose nulls

All three early nulls were re-run on the standard that scores a running artifact:

| Skill | Prose | Behavioural |
|---|---|---|
| `output-contracts` | null | **flipped — 1/5 vs 5/5** |
| `state-vs-reality` | null | null |
| `tool-contract-first` | null | null |

One of three changed. That is the useful shape: the behavioural method is strong enough to
overturn a wrong null, and it did not overturn these two. **These are measured nulls now, not
unmeasured ones.**

## What this does not show

One fixture, one model, five runs per arm — and a single call to a single tool. The incident
behind this skill is the *repeat* case: the same proxy trusted three times in one day, under
time pressure, each time with a plausible fix already in hand. A chain where the exit code is
honest four times and lies the fifth is the harder test, and has not been built.

## Method note

The scorer was reachable again. Two treatment runs walked up out of their run directory,
found it under the shared scratchpad root, and graded themselves against it — the same leak as
in the first `tool-contract-first` measurement, despite the scorers having been moved out of
the eval tree after that one. Moving them one directory up was not enough: they still shared a
path prefix with the run directories. Both runs were discarded, the scorers were moved outside
the scratchpad entirely, and the two runs were repeated with an explicit instruction to stay
inside the run directory.

Reproduce: see `evals/tool-contract-first-behavioural/run.md`. `results.json` holds the ten scored runs.
