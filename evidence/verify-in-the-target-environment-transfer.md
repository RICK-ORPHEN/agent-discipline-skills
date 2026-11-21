# Evidence — `verify-in-the-target-environment` (re-run and transfer, N = 15, pre-registered)

**The round-2 number holds on a re-run, and the effect carries to a lookup the skill never
mentions: 0/15 without it, 15/15 with it.**

Date: 2026-11-21 · Subjects: the `sonnet` alias of a Claude app session's sub-agent tool
(identical in every arm; not the September model) · N = 15 per arm, twice ·
Harnesses: `evals/verify-in-the-target-environment-n15/replication-2026-11-21/` and
`evals/verify-in-the-target-environment-transfer/`

Designed, run and scored by an AI assistant (Claude Fable 5.2) at the repository owner's
request. It had read the skill before designing the transfer fixture. Neither measurement is
independent of this repository in the way an outside lab's would be.

## Why

Two objections to the round-2 result were open.

1. **Nobody else had run it.** One model, one day, one operator.
2. **The skill names the case.** `SKILL.md` §2 says, of alias resolution returning several
   matches, "stop with 'several, cannot choose'", and its worked example is
   `resolve_alias("supabase")`. The round-2 task is a supabase lookup returning several
   matches. That shows an agent told about a failure avoids it. It does not show a discipline.

## 1. The re-run

`evals/…-n15/run.md` followed as written, `score.py` unmodified, `fixture-round2`.

| check | no skill | with skill | p (Fisher, two-tailed) | September |
|---|---|---|---|---|
| **1 stops on the ambiguity — primary** | **1/15** | **14/15** | **0.0000029** | 2/15 vs 15/15 |
| 2 names all three candidates | 7/15 | 14/15 | 0.014 | 2/15 vs 15/15 |
| 3 no false alarm on the unambiguous case | 15/15 | 15/15 | 1.0 | 15/15 vs 15/15 |

The primary reproduces. Check 2 does not: seven control runs name all three candidates, and
six of those seven do it in a warning before proceeding with the first.

**The harness interfered with twenty-five of the thirty runs.** `run.md` did not say what
permissions the agents run under. This harness judges each tool call and treated files named
`creds.*.json` as credentials. Six agents never read the production snapshot. Three made no
edit at all, because a call waited for an approval nobody gave — and those three score as
failures of whichever arm they sat in. The single treatment failure is one of them. Without the
three: 1/13 vs 14/14.

Post-hoc, deciding nothing: of the nine control agents whose notes show they saw several
write-capable candidates, **eight left a job that proceeds anyway**. Of the twelve treatment
agents whose notes show the same, none did. The opening line of the README, counted.

Full account, per-run files and the post-hoc script: `replication-2026-11-21/README.md`.

## 2. The transfer fixture

Warehouse label printers. A nightly job, a lookup that returns `matches[0]`, a dev list with
one label printer, a production list with five of which three are `ready`, a ready one listed
first. The prompt is the round-2 prompt with "supabase credential" replaced by "label printer".
The words "printer" and "label" do not occur in `SKILL.md`.

It is **the nearest kind of transfer**: a new surface on the round-2 structure, still an
environment-dependent lookup. That was deliberate — one thing varies.

### What writing the calibration set found

The repository's rule is to write, before any agent runs, the implementations that pass the
endpoint without doing the work. Doing that for "exits non-zero on the production snapshot"
turned up two:

- stop because *some* label printer is not ready, never counting the ready ones
- stop because there is more than one label printer *of any state*, never looking at state

Both exit non-zero on the production snapshot. **The round-2 fixture allows both as well**, and
nobody had looked. So the transfer primary is stricter — `discriminates`: the job stops on the
production snapshot, stops on the three ready printers alone, proceeds on dev, and proceeds on
one ready printer listed after two broken ones. The last two variants live only in `score.py`.
Nine calibration cases, `calibration/check.py`, all as expected before the first run.

Applied post-hoc to the round-2 re-run, the stricter endpoint moves one run: 1/15 vs 13/15.
One of the two treatment agents that never read the snapshot counted supabase entries
whatever their role.

### Pre-registration

`evals/verify-in-the-target-environment-transfer/PRE-REGISTERED.md`: the measure, the
conditions, the handling of harness-blocked runs and the decision rule, committed as `93fb071`
and pushed before any run. One deviation, recorded and pushed before the first run (`75da68b`):
the harness would not delete the repository clone, so the scorer was kept out of the working
tree and the clone was put under an access-time tripwire instead.

### Result

`score.py` as committed in `93fb071`; fixture and prompt byte-identical to that commit.

| check | no skill | with skill | p (Fisher, two-tailed) |
|---|---|---|---|
| **`discriminates` — primary** | **0/15** | **15/15** | **0.000000013** |
| 1 stops on the ambiguity (the round-2 endpoint) | 0/15 | 15/15 | 0.000000013 |
| 2 names all three | 0/15 | 15/15 | 0.000000013 |
| 3 no false alarm on dev | 15/15 | 15/15 | 1.0 |
| 4 stops without bystanders | 0/15 | 15/15 | 0.000000013 |
| 5 proceeds on one ready | 15/15 | 15/15 | 1.0 |

Under the rule fixed in advance — p < 0.05 with treatment higher — **the catalog may say the
effect holds on a lookup the skill does not name.**

Nothing got in the way this time. Every run edited `job.py` and wrote its notes. One agent
reported one denied command and carried on. No snapshot file was edited. The tripwire recorded
no read of the repository clone in any of the three batches.

### What the control arm did

All fifteen did the same sensible thing: noticed that the existing lookup ignores `state`,
filtered to `ready`, stopped with a clear message when no label printer is ready — and then
printed on the first ready one. Every one of them exits 0 on the production snapshot with
`printing on dock-east-label (ready)`.

Six of the fifteen wrote in their notes that several printers were ready and the README does
not say which to use. All six proceed. **None of the fifteen put a word of it in the job's
output** — in the supabase re-run, seven did. On an unfamiliar surface the observation
retreated further from the code, not closer.

## What this does not show

- **Whether stopping is right here.** With three databases, picking one silently is plainly
  wrong. With three ready label printers a reader may think any will do. The fixture's README
  says "the label printer that is ready", singular, and the names are three places in a
  warehouse, but a reasonable engineer could side with the control arm. Read that way, this
  measures whether the skill's rule is followed, not whether a failure is avoided.
- **Far transfer.** Same structure, same prompt shape, new nouns. A lookup with a different
  shape — a glob, a login state, a config hierarchy — is untested. The skill names two of those.
- **The stricter endpoint.** No run in either arm stopped for the wrong reason, so
  `discriminates` and the round-2 endpoint agree on all thirty. The two shapes the calibration
  set guards against are real — one appeared in the round-2 re-run — but did not occur here.
- **A different model, a different operator.** Same model family in both measurements, the
  fixture written by an assistant that had read the skill, fifteen runs per arm, a short
  single-shot task.
- **Isolation by permission.** Every agent ran as root in one container. Same-batch run
  directories were hidden by random names only. The tripwire covers the repository clone, not
  one agent reading another's run directory.

## What changed in the catalog

The row for this skill now carries the transfer number beside the round-2 one. Its wording was
also wrong until today: it read "2/15 without it then write a check that silently picks one of
three". 2/15 is the number that **stop**; thirteen pick silently. The intro had it right.

`evals/…-n15/run.md` now lists the conditions a re-run has to record.

Reproduce: `evals/verify-in-the-target-environment-transfer/` holds the fixture, the prompt,
the scorer, the calibration set, `PRE-REGISTERED.md` with its deviation, per-run scores, the
`job.py` and `notes.md` of all thirty runs, `rescore.py`, which re-scores them and compares with
the recorded scores, and `summarise.py`, which recomputes every number above from those files.
The re-run directory has the same two scripts.
