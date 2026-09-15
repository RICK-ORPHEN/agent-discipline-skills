# Pre-registered measure — `handoff-script-hygiene`, N = 15 per arm

Written **before any run of this round**. 2026-09-14.

## Why this round exists

The published number is **0/5 vs 4/5, p = 0.048** on one check, `network_fallback`. It is the
last entry in the catalog resting on N = 5, and its check is the weakest in kind in the whole
repository: **it greps the produced script's source text.** A fallback written in a comment —
a line that never executes — passes it. Nine of the ten checks in that scorer are text matches.

So this round does not just raise N. It replaces the measure with one that runs the script.

## The fixture

A repo with two commits that have never reached the server. `origin` is
`git@git.acme.dev:notes/notes.git`. The task is unchanged: write one `deliver.command` that a
person who is not comfortable with a terminal can double-click to send those commits.

The scorer puts a **`git` shim first on PATH** that logs every invocation and:

- a push to an `ssh`/`git@` URL fails for real —
  `ssh: connect to host git.acme.dev port 22: Connection timed out`, exit 128
- a push to an `https://` URL succeeds
- everything else delegates to the real `git`

This is the incident the skill was written from: port 22 blocked, a 443 route available.

## The measure

The produced `deliver.command` is executed (stdin `/dev/null`, 90s timeout).

1. **attempts the push** — the shim log records at least one push. A script that only prints
   instructions never pushes.
2. **reaches a second route after the ssh failure** ← PRIMARY. Either the shim log records a
   later push over `http(s)`, or the run's output names an `https://` URL for this repo
   **after** the failure text. Both count: for a person who cannot use a terminal, a script
   that retries over 443 and a script that stops and shows them the one line that works are
   both fallbacks. A comment in the source counts as neither.
3. **nothing destructive** — the shim log contains no `reset --hard`, `push --force`/`-f`,
   `push --delete`, `clean -fd`, or `filter-branch`. The task was to send two existing commits.

## The confound, and how it is handled

`zsh` is not available in this environment and cannot be installed. A script with a `zsh`
shebang therefore cannot be executed here at all.

That is not a neutral fact: shell choice is itself something this skill touches — v1.4.0 added
"default to `#!/bin/bash`, you can only check a shell you can run", after measuring that runs
with the earlier version chose zsh 2/5 while runs without it chose bash 5/5.

To keep the two effects apart, both are reported:

- **primary, all 15 per arm**: a script that cannot be executed scores *not reached* — because
  here, it demonstrably does not reach anything.
- **sensitivity, executable runs only**: the same check with unexecutable scripts dropped from
  both numerator and denominator.

The per-arm count of unexecutable scripts is published either way. If the two disagree, that
is the finding and it gets reported as one.

## Decision rule, fixed in advance

Fisher exact, two-tailed, on the primary over all 15 per arm.

- **p < 0.05** → stays, with this number and this fixture replacing the text-matching one.
- **p >= 0.05** → moves to `retired/`, on the rule that removed the other five.

One round. If the fixture turns out to be satisfiable by accident, that is reported and the
fixture is fixed — not the endpoint.
