# Evidence — `sandbox-boundary`

**Result: 5/5 in both arms. No difference at all.** Published as measured.

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 5 per arm ·
Harness: `evals/sandbox-boundary/`

## The fixture

The agent works on a copy of a project inside a deep sandbox path. A `MACHINE.md` states only
where the project lives on the other person's machine — `/Users/hana/Work/acme` — and that
they are on macOS with Node. It does **not** say the sandbox is unreachable from there; the
first version of this fixture did, and that sentence was removed and all ten runs redone,
because it handed both arms the lesson.

The task: make a small change, then write the exact commands the person should run.

## Result

| Arm | Mean | Runs |
|---|---|---|
| No skill | **5.0 / 5** | 5, 5, 5, 5, 5 |
| With the skill | **5.0 / 5** | 5, 5, 5, 5, 5 |

Every check, both arms, ten out of ten: no sandbox path anywhere in the handover, the person's
own path used, no `cd` into the sandbox, every command runnable exactly as written.

Not one run pasted its own working directory into the instructions. In an earlier variant of
this fixture that also asked for "commands to pull your change", all ten runs — control
included — noticed there was no git repository and no remote, refused to write a `git pull`
that would fail, and handed over the file contents instead. That is the skill's R4
(*confirm the preconditions before handing over a command*) arriving unprompted.

## What this changes about the earlier hypothesis

After four skills the working explanation was "skills pay when they require an **action** the
model would not take". This one is an action skill, and it pays nothing. The six results
together point somewhere narrower:

| Skill | Effect | What the skill actually supplies |
|---|---|---|
| `handoff-script-hygiene` | moderate | **a fact the model does not have** — that a blocked port 22 has a 443 route |
| `diagnose-first` | large | **work the model will not volunteer** — tabulating failures nobody asked about |
| `output-contracts` | null | judgment (disclose degradation) |
| `state-vs-reality` | null | judgment (distrust a scoped success) |
| `tool-contract-first` | null | judgment (distrust a proxy signal) |
| `sandbox-boundary` | null | judgment (write paths for the other machine) |

**A skill earns its place by carrying knowledge the model lacks, or by forcing work the model
would not spend unasked. It earns nothing for writing down judgment the model already has** —
however well that judgment is written, and however expensive the incident that produced it.

That is a statement about a capable model in 2026, not about whether the discipline is right.
The incidents in these files were real. The model that caused them was not this one.

## What this does not show

One fixture, one model, five runs per arm. Everything here is a single clean handover with no
time pressure and one decision to get right. The incident this skill came from was eight
commits deep in a worktree whose `.git` pointed at a path the user's machine did not have —
a state, not a decision. A fixture that reproduces a broken worktree, rather than asking for
a handover, would test a different and harder part of the same skill, and has not been built.

Reproduce: see `evals/sandbox-boundary/run.md`. `results.json` holds the ten scored runs.
