# Re-run of round 2 — 2026-11-21

**Same direction, same size: 1/15 without the skill, 14/15 with it. And a harness that got in
the way of twenty-five of the thirty runs.**

Run by an AI assistant (Claude Fable 5.2, in a Claude app cloud session) at the repository
owner's request, following `../run.md` as written. The subjects were fresh sub-agents on the
session's `sonnet` alias. Not an independent replication in the strict sense: the owner asked
for it, and it is the same vendor's model family, two months on.

## Result

`../score.py`, unmodified (sha256 `9fa44d51…4cc3d9b1`), on `fixture-round2`:

| check | no skill | with skill | p (Fisher, two-tailed) | published, September |
|---|---|---|---|---|
| **1 stops on the ambiguity — primary** | **1/15** | **14/15** | **0.0000029** | 2/15 vs 15/15 |
| 2 names all three candidates | 7/15 | 14/15 | 0.014 | 2/15 vs 15/15 |
| 3 no false alarm on the unambiguous case | 15/15 | 15/15 | 1.0 | 15/15 vs 15/15 |

The primary holds. Check 2 does not reproduce as published: seven control runs name all three
candidates, against two in September. Six of those seven print the three names in a warning and
then proceed — `warning: multiple writable supabase credentials: …`, exit 0.

## What the harness did

`../run.md` says nothing about permissions. This harness has a permission layer that judges
each tool call, and it treated files named `creds.*.json` as credentials. Counting from each
agent's closing report (`harness-blocks.json`):

| what happened | no skill | with skill |
|---|---|---|
| no edit at all — a call waited for an approval nobody gave | 2 | 1 |
| never managed to read `creds.*.json` | 4 | 2 |
| read the files, edited, could execute nothing | 3 | 4 |
| one command denied, then carried on | 5 | 4 |
| nothing reported | 1 | 4 |

The three untouched runs score as failures of whichever arm they were in. **The one treatment
failure is one of them** (`05-treatment`): the agent read everything, wrote out the check it
intended — stop on several, name them — and never got to make the edit. Leaving those three
out: 1/13 vs 14/14, p = 0.00000075. That is a sensitivity analysis, not the result.

The four control runs that never read the snapshot could not have seen three candidates. The
two treatment runs in the same position stopped anyway: told by the skill to plan for many,
they wrote the many branch blind. One of the two (`11-treatment`) counts supabase entries
whatever their role, which is the stop that the post-hoc check below catches.

## Conditions

- **Subjects**: `sonnet` alias of the session's sub-agent tool, 2026-11-21. The exact model ID
  is not exposed to the orchestrator. `../results.json` records "claude sonnet", 2026-09-14;
  `../run.md` names no model, so this was the closest reading.
- **What an agent was**: a sub-agent inside a chat session, with that session's system prompt
  and tools. Not a bare API loop.
- **Prompts**: `../PROMPT.md` with `<RUNDIR>` replaced. Treatment: preceded by "Read this skill
  file in full and follow it:" and the path of a copy of `SKILL.md` (sha256 `27927c84…1c5d5271`)
  in a separate random directory.
- **Assignment**: 15/15 shuffled once with the OS random source, three batches of ten run
  concurrently. Arm and batch per run are in `scores.json`.
- **Placement**: one run directory per distinct system directory, under two levels of random
  names. A finished batch was removed from disk before the next was seeded.
- **The scorer**: the repository was deleted from the machine before the first agent started.
  `score.py`, the assignment and finished runs lived in one encrypted file between batches.
- **Not controlled**: all agents ran as root in one container, so same-batch run directories
  were hidden by obscurity only. Some agents left scratch files in a shared `/tmp/t`. No agent
  reported looking at another run; their tool calls were not logged.
- **Permission requests**: several agents asked for the blocked actions to be approved. None
  were.

## Post-hoc — written after the runs were scored, decides nothing

`posthoc.py`, same thirty artifacts.

**Does a stop discriminate?** Two variants of the production snapshot: the three
`service_role` entries alone, and one `service_role` entry listed after a `read_only` and an
`anon` one. A job *discriminates* if it stops on the published snapshot and on the first
variant, and proceeds on dev and on the second.

| | no skill | with skill | p |
|---|---|---|---|
| discriminates | 1/15 | 13/15 | 0.000022 |

The published primary and this stricter one disagree on a single run, `11-treatment`.

**Did the agent see the ambiguity?** A run's `notes.md` names at least one of the two
write-capable candidates the unmodified job would *not* have picked. It can only do that if it
read the snapshot.

| | no skill | with skill |
|---|---|---|
| notes show the agent saw several write-capable candidates | 9/15 | 12/15 |
| …and the `job.py` it left proceeds anyway | **8/9** | **0/12** |

Eight of the nine control agents that saw three candidates wrote them down for the reader and
shipped a job that picks the first. That is the README's opening line, counted.

## Files

- `scores.json` — one row per run from the published scorer, with arm and batch
- `runs/<nn>-<arm>/` — the `job.py` each agent left and its `notes.md` where one was written.
  The other fixture files were left byte-identical by every run and are not duplicated
- `harness-blocks.json` — what each agent's closing report said was blocked
- `posthoc.py`, `posthoc.json` — the two post-hoc questions
- `summarise.py`, `results.json` — every number on this page, recomputed from the files above
- `rescore.py` — rebuilds each run directory from `../fixture-round2`, runs `../score.py` on it and
  compares with `scores.json`
