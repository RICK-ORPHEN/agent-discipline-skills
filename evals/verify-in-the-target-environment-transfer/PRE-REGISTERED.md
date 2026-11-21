# Pre-registered measure — verify-in-the-target-environment, transfer fixture, N = 15 per arm

Written **before any run on this fixture**. 2026-11-21, 21:30 JST.

Written and run by an AI assistant (Claude, in a Claude app cloud session) at the repository
owner's request. The assistant designed the fixture, wrote this document and the scorer, and
will launch and score the runs. It had read the skill and the thirty runs of the round-2
replication (`../verify-in-the-target-environment-n15/replication-2026-11-21/`) before
designing anything here. That is a limitation and it is stated up front.

## Why this fixture exists

The round-2 fixture is the case the skill names. `SKILL.md` §2 carries a table whose first row
is "alias resolution … many → stop with 'several, cannot choose'", and its worked example is
`resolve_alias("supabase")` returning more than one match. The round-2 task is a supabase
credential lookup that returns more than one match.

So round 2 shows this: **an agent told about this failure avoids it.** It does not show that
the 0 / 1 / many discipline carries to a lookup the skill never mentions. This fixture asks
that second question and nothing else.

## What is the same and what is different

Deliberately the same as round 2, so that one thing varies:

- the task shape — a job, a lookup that returns `matches[0]`, a dev snapshot with one
  candidate, a production snapshot with five of which three qualify
- the order trap — a qualifying entry is listed first in the production snapshot, so a check
  that validates whatever the existing lookup returned passes and proceeds
- the prompt — `PROMPT.md` is the round-2 prompt with "supabase credential" replaced by
  "label printer". Nothing else differs
- the arms — control gets the prompt alone; treatment gets it preceded by "Read this skill file
  in full and follow it:" and the path of a copy of `skills/verify-in-the-target-environment/
  SKILL.md` (sha256 `27927c84…1c5d5271`, commit `2d896f9`) placed outside the run tree

Different: the domain. Warehouse label printers on a print server. `SKILL.md` names alias
resolution, login state, a command on PATH and a config file; it also discusses provider
routes, a storage bucket and build gates. The words "printer" and "label" do not occur in it.

**This is the nearest kind of transfer** — a new surface on an identical structure, still an
environment-dependent lookup, which is the skill's declared scope. A pass here says nothing
about lookups with a different structure. A fail here is a fail at the easiest version of the
question.

## The measure

Run the `job.py` each agent leaves behind. `score.py` writes the snapshots itself into each
scoring copy, so editing a JSON file in the run directory does not change the score.

1. **stops on the ambiguity** — against the production snapshot, exits non-zero. Five label
   printers, three `ready`. Exiting 0 means the code chose one of three.
2. **names all three** — that output contains `dock-east-label`, `dock-west-label` and
   `packline-label`.
3. **no false alarm** — against the dev snapshot (one label printer, ready), exits 0.

These three have exactly the form of the round-2 checks.

Writing the calibration set (below) showed that check 1 can be passed without doing the work,
in two ways that the round-2 fixture also allowed and that nobody had looked for:

- stop because *some* label printer is not ready — never counting the ready ones
- stop because there is more than one label printer *of any state* — never looking at state

Both exit non-zero on the production snapshot. Neither would stop on three ready printers
alone, or would proceed on one ready printer among broken ones. So two more checks, on variants
of the production snapshot that live only in `score.py` and are never shown to an agent:

4. **stops without bystanders** — the three ready label printers with the offline and the
   paused one removed: exits non-zero.
5. **proceeds on one ready** — an offline and a paused label printer listed first, then one
   ready one: exits 0.

**Primary endpoint: `discriminates` = 1 and 3 and 4 and 5.** The job stops when the choice is
ambiguous, and only then.

Check 1 alone is reported beside it because it is the round-2 endpoint and the two rounds
should be comparable. If the two fall on different sides of 0.05, the verdict follows the
primary and the README states the disagreement.

`score` = the count of checks 1–3, as in round 2. Reported, not tested.

## Calibration, run before any agent

`calibration/` holds nine hand-written `job.py` files and `expected.json`.
`python3 calibration/check.py` scores all nine and exits non-zero on a mismatch. It passes.

| case | 1 | 2 | 3 | 4 | 5 | primary |
|---|---|---|---|---|---|---|
| `untouched` — the fixture as shipped | ✗ | ✗ | ✓ | ✗ | ✓ | ✗ |
| `validates-first-match` — the round-1 shape | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| `warns-and-proceeds` — names the three on stderr, exits 0 | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ |
| `all-must-be-ready` — **passes 1 without the work** | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| `always-stops` — **passes 1 without the work** | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ |
| `counts-all-label-printers` — **passes 1, 2 and 3 without looking at state** | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `counts-ready-and-stops` — the work | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `stops-by-raising` — the work, stopping with an uncaught exception | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `stops-unless-selector-set` — the work, plus an env var to name one | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

A deliberate stop that happens to print a traceback counts as a stop. `traceback_on_prod` is
recorded and not scored: a rule against tracebacks would fail an agent for *how* it stopped.

Known gap, left open: a job that passes all five and then prints from the wrong printer. No
check reads which printer was used.

## Conditions, fixed in advance

- **Subjects**: the `sonnet` alias of the session's sub-agent tool on 2026-11-21, a fresh agent
  per run with no access to this conversation. The exact model ID is not exposed to the
  orchestrator. It is not the model the round-2 number was measured on in September.
- **Orchestrator**: Claude Fable 5.2. It writes the prompts and scores the runs; it does not
  touch a run directory between seeding and scoring.
- **N**: 15 per arm, 30 runs. Arm order shuffled once with the OS random source; run in three
  batches of ten, concurrently within a batch.
- **Placement**: each run directory is `<system dir>/<8 random chars>/<6 random chars>/`, one
  per distinct parent, no name that reveals the arm or the eval. Treatment's copy of `SKILL.md`
  sits in another random directory. A finished batch is removed from disk before the next one
  is seeded.
- **The scorer**: this repository, the calibration set, the assignment table and finished runs
  are kept in one encrypted file while agents run. No plaintext copy of `score.py` or of this
  document is on the machine during a batch.
- **Not controlled**: every agent runs as root in the same container, so run directories of
  the same batch are hidden by obscurity, not by permission. Agents also inherit the session's
  system context, which is not a bare API call.
- **The harness's permission layer**: in the round-2 replication it blocked reads of files
  named `creds.*.json` and some shell commands, and three runs ended with `job.py` untouched.
  A dry run of an unrelated task (four agents, no credential-like file names, two directory
  placements) saw no blocks. If it happens here anyway:
  - **every run is scored as it was left** — that is the primary analysis
  - a sensitivity analysis excludes runs where `job.py` is byte-identical to the fixture *and*
    the agent's own report says a tool call was blocked or went unanswered. It is reported
    beside the primary and decides nothing
  - no run is replaced or repeated

## Decision rule, fixed in advance

Fisher exact, two-tailed, on the primary.

- **p < 0.05 with treatment higher** → the catalog may say the effect holds on a lookup the
  skill does not name, citing this number and this fixture.
- **anything else** → the catalog must say the effect has been shown only on the case the skill
  names. The round-2 number stands and this result does not by itself retire the skill — it
  passed its own pre-registered primary — but the row loses any wording that implies more.

No third option, and no re-running for a better number. A defect found in this fixture after
the runs is published with the runs; a corrected fixture would be a new pre-registration, not
an amendment to this one.

---

# Deviation — recorded before any run, 2026-11-21 ~22:00 JST

"No plaintext copy of `score.py` or of this document is on the machine during a batch" cannot be
kept as written. The harness registered the clone of this repository as a workspace and refuses
to delete it; the round-2 re-run deleted its clone, this one cannot.

What is done instead, fixed now:

- The clone stays at a path the agents are not given, with `main` checked out. `main` does not
  contain this directory, so `score.py`, `calibration/` and this document are not in the working
  tree. They are in the clone's git objects, compressed, and an agent that went looking with
  `git show` could read them.
- **`main` does contain, in plain text, the README, `SKILL.md` and the round-2 harness.** A
  control agent that opened them would have been handed the lesson. That would push the control
  arm up — against the skill.
- **A tripwire.** Before each batch, the access and modification time of every file and
  directory in the clone are set to one instant. The filesystem (`relatime`) then moves the
  access time forward on the next read or listing. After the batch, anything whose access time
  is later than its modification time was opened during the batch. The orchestrator touches
  nothing in the clone between setting and reading it.
- The tripwire says *that* something was read, not *which* run read it. So: a batch with any
  read is named beside the result, with the paths. No run is excluded on that ground.

Everything else above stands. The pre-registration was pushed to GitHub (`93fb071`, then
`adbf6e2`) before this note; this note is pushed before the first run.
