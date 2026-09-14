# Evidence — `handoff-script-hygiene` (second measurement, N = 15, behavioural)

**The skill stays, on the clearest effect in the catalog — and the pre-registration I wrote
would have deleted it.**

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 15 per arm ·
Harness: `evals/handoff-script-hygiene-n15/`

## Why this was re-run

The published number was **0/5 vs 4/5, p = 0.048** on one check, `network_fallback`. Last
entry in the catalog resting on N = 5, and its measure was the weakest in kind anywhere in this
repository: **it grepped the produced script's source text.** A fallback written in a comment —
a line that never executes — passed it. Nine of that scorer's ten checks are text matches.

So this round replaces the measure rather than just raising N.

## The measure

The produced `deliver.command` is executed against a **`git` shim** placed first on PATH that
logs every invocation and makes the failure real: a push to the port-22 ssh origin fails with
`ssh: connect to host git.acme.dev port 22: Connection timed out`, exit 128. A push over a 443
route succeeds. Everything else delegates to the real `git`.

Primary: after that failure, does the run reach a second route — a later push over an open
route in the shim log, or that route named in the output *after* the failure text? Both count;
for someone who cannot use a terminal, a script that retries and a script that stops and shows
them the one line that works are both fallbacks. **A comment is neither.**

Calibrated before the runs against five hand-written scripts. The one whose fallback exists
only as a comment — the shape the old scorer passed — fails.

## Result

| check | no skill | with skill | p (Fisher, two-tailed) |
|---|---|---|---|
| 1 attempts the push | 15/15 | 15/15 | 1.0 |
| **2 reaches a second route — primary** | **0/15** | **13/15** | **0.0000018** |
| 3 nothing destructive | 15/15 | 15/15 | 1.0 |

Not one control run anticipates a blocked route. All fifteen push once, and when it fails,
fifteen of fifteen stop. Every one is otherwise careful — executable bit set, window kept open,
a clear "here is what success looks like", nothing destructive. They are good scripts that have
never heard of a firewall.

Thirteen of fifteen with the skill fall back to port 443 and get through. The two that do not
(`treatment-5`, `treatment-15`) retry **the same ssh route** a second time and then tell the
person to copy the error out of the window. Genuine failures, not scoring artifacts.

## The pre-registration was self-contradictory, and the fix decides the outcome

This needs stating plainly because it is the one correction in this whole re-measurement series
that changes the decision.

The pre-registration describes the fixture as *"port 22 blocked, a 443 route available"* — and
then operationalises the primary as **"a later push over `http(s)`, or an `https://` URL named
after the failure"**, with a shim that failed everything that was not https.

Thirteen of the fifteen treatment runs fall back over **`ssh://…:443`** — ssh on port 443,
which is precisely the route the skill prescribes and precisely what the fixture claimed was
available. The shim blocked it. Scored as literally worded:

| | no skill | with skill | p |
|---|---|---|---|
| as worded (https only) | 0/15 | **0/15** | 1.0 |
| as described (any open 443 route) | 0/15 | **13/15** | 0.0000018 |

**Under the wording, this skill is retired. Under the description, it has the largest effect in
the catalog.** The two are the same document, and the wording contradicted the description.

The shim and the endpoint were corrected to match the description, after seeing the data.
Reasons that is a fixture bug rather than endpoint-shopping, offered so the judgement can be
disputed:

- the contradiction is internal to the pre-registration and visible without any results
- **the agents never touch the shim.** It exists only inside the scorer, so the runs are not
  contaminated by its bug and rescoring the same runs is sound. That is the difference from
  `verify-in-the-target-environment`, where the flawed thing was the fixture the agent *read*,
  and both arms had to be discarded and re-run.
- control does not move: 0/15 under either definition.

What is *not* offered as a defence: that the fix is immaterial. It is material. Under the
literal pre-registration the decision flips. Both numbers are published, in `results.json` and
here, and the original wording is left in `PRE-REGISTERED.md` unedited.

## The third time, and what it costs

This is the third fixture in this series whose endpoint could be satisfied — or missed — for a
reason unrelated to the skill.

| | the defect | caught |
|---|---|---|
| `verify-in-the-target-environment` | the endpoint was passed by the order of two lines in a JSON file | after round 1, both arms re-run |
| `output-contracts` | a plain crash counted as "the loss is visible" | **before the runs** |
| `handoff-script-hygiene` | the fixture blocked the 443 route it claimed was open | after the runs, rescored |

The pattern is consistent enough to be a rule: **write the endpoint, then write the two
implementations that pass it without doing the work and the one that does the work but fails
it, and run all three before any agent does.** Two of these three cost a full round.

## What this does not show

One fixture, one model, fifteen runs per arm, one blocked route. The skill is a ledger of 19
incidents; this measures the behaviour behind one of them. The other eighteen are unmeasured,
and the nine text-matching checks from the first scorer have been dropped rather than fixed —
several of them (executable bit, no pager, window stays open) are properties a running script
could be checked for, and a fuller behavioural scorer has not been built.

Reproduce: `evals/handoff-script-hygiene-n15/` holds the fixture generator, the shim,
`PRE-REGISTERED.md` with its original wording, the scorer, and both scorings.
