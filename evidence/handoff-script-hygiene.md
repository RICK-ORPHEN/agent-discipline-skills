# Evidence — `handoff-script-hygiene`

> **Superseded.** N = 5, and the measure grepped the produced script's *source* — a
> fallback written in a comment passed it. Re-measured by executing the script against a
> `git` that fails port 22 for real: `handoff-script-hygiene-n15.md`. Kept unedited.

**Does the skill change what the agent produces?** Measured, not asserted.

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 5 per arm ·
Harness: `evals/handoff-script-hygiene/`

## The task (identical in every arm)

> A person who is not comfortable with a terminal, on macOS, will double-click a file in
> Finder. A git repository has two local commits that never reached GitHub. Write one
> `deliver.command` that this person can double-click to send those commits. Do not push
> it yourself.

Nothing in the task mentions shells, pagers, stderr, ports or preconditions. The failure
modes have to occur to the agent on its own — or come from the skill.

## Scoring

`score.py` reads **the file the agent left behind** — never the transcript — and returns a
pass/fail on nine mechanical checks drawn from the skill's own 60-second list: executable
bit, shebang/syntax agreement, `--no-pager` on git output commands, stderr of fallible
commands not discarded, a fallback route when the network blocks port 22, the window
staying open, a line saying what success looks like, no destructive or out-of-scope git
operations, and preconditions checked before acting. Same input, same score, any machine.

## Result

| Arm | Mean | Runs |
|---|---|---|
| No skill | **7.6 / 9** | 7, 7, 8, 8, 8 |
| Skill v1 | **8.4 / 9** | 8, 8, 8, 9, 9 |
| Skill v2 (after the fix below) | **8.4 / 9** | 7, 8, 9, 9, 9 |

Per check, out of 5 runs:

| Check | No skill | v1 | v2 |
|---|---|---|---|
| network fallback (port 22 blocked → 443) | **0** | **4** | **4** |
| checks preconditions first | 3 | 5 | 3 |
| shebang and syntax verifiable | 5 | **3** | 5 |
| the other six checks | 5 | 5 | 5 |

**The skill's contribution is concentrated in one line: the fallback route.** Without the
skill, five runs out of five shipped a script that simply fails for anyone whose network
blocks port 22 — and that failure looks, to the person double-clicking it, exactly like
"it is broken." No run invented that fallback on its own. Six of the nine checks were
already satisfied without the skill; a capable model does not need to be told to add a
shebang.

## A defect the measurement found, and the fix

In v1, **two of five runs chose `#!/bin/zsh`** while five of five no-skill runs chose bash.
The skill's checklist named zsh first and spent two of its nine lines on zsh-only pitfalls,
which reads as a recommendation. It steered the agent into the shell whose traps the skill
itself was written to warn about — and `zsh -n` is not installed everywhere, so those
scripts could not even be syntax-checked.

v2 adds one line: default to bash, use zsh only when something needs it. Five of five v2
runs chose bash and all were syntax-checked clean. `checks_preconditions` moved the other
way (5 → 3) with no change to the text covering it; at N = 5 that is inside the noise, and
it is the next thing to measure, not something to claim.

## What this does not show

One task, one model, five runs per arm. It shows that the skill adds the checks the model
does not already make, and that a nine-point rubric mostly saturates without it. It does
not show a difference in real-world outcome, or that the effect holds on another model.

Reproduce: `evals/handoff-script-hygiene/` — the harness, the prompt and the scorer are all
in that directory, and `results.json` holds the fifteen scored runs.

## The scorer was wrong first

Three of the checks misfired on the first pass and were calibrated against the actual files
before any number above was reported: `stderr_kept` flagged `2>/dev/null` on harmless
`command -v` probes; `keeps_window_open` required a flag on `read` and so missed a bare
`read _`; `says_what_success_looks_like` did not match `DONE` in capitals. Uncalibrated
proxies produced two "regressions" that did not exist. Recorded here because the skill next
to this one (`tool-contract-first`) exists to prevent exactly that, and it caught us.
