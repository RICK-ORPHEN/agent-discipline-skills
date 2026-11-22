# Pre-registered measure — does the wording of a rule change how often it is followed?

Fixed 2026-11-22, 22:51 JST, before any counted run. Two mechanics pilots had run by then and are
described under "Conditions"; nothing else had.

Written by an AI assistant (Claude, in a Claude app cloud session) at the repository owner's
request. The assistant chose the claim, built the task and the checker, and will launch and
score the runs.

## The claim

Tsuchida, Fan, Matsumoto, Shimari and Kula, *Do Coding Agents Follow AGENTS.md? The Effect of
Policy Wording on Instruction Compliance*, arXiv:2611.04367v1 (3 November 2026). One rule was
appended to a repository's instruction file in four wordings, and agents then did 86
SWE-bench-style tasks. On Claude Code 2.1.227 with claude-sonnet-5 the rule was followed in:

| wording | compliance |
|---|---|
| prescriptive | 71.6% |
| explanatory | 49.4% |
| conditional | 35.6% |
| prohibitive | 17.3% |

On claude-opus-5 the spread was much smaller (78.0 / 77.2 / 64.2 / 70.7). The authors advise
against conditional phrasing and say a style tuned for one agent should not be assumed to work
for another.

The Sonnet row travelled further than the paper: a Japanese summary of it on X on 5 November
2026 had about 120,000 views when this was written, with the advice "rewrite *if …* and
*never …* as plain statements". That advice is what is tested here, on a model that is current
today.

## What is the same as the paper and what is not

The same: the rule, and its four wordings, taken from the paper's Table 1 (`policies.json`).
The rule is appended as the last line of the instruction file after a blank line. A session
complies only when every Python function it added or modified carries the marker.

Not the same, and each of these limits what a result here can say:

- **The subject is not Claude Code.** It is a sub-agent of a Claude app session. Claude Code
  loads `CLAUDE.md` itself; here the file's text is placed at the top of the prompt under the
  line "Project instruction file (…/CLAUDE.md), loaded at session start", and the same file is
  also in the workspace. The sub-agent carries the session's own system context besides.
- **The model is not claude-sonnet-5.** It is whatever the `sonnet` alias of the sub-agent tool
  resolves to on the day. The exact ID is not exposed to the orchestrator.
- **The task is not SWE-bench.** It is three small scripts in one session (`PROMPT.md`), built
  from fixtures already in this repository. A session is minutes, not tens of minutes.
- **The instruction file is 54 lines written for this test** (`CLAUDE.template.md`), not a real
  project's file. The paper's files were whatever the ten repositories already had.
- **N is 15 sessions per wording**, against roughly 240 in the paper.

A short session with a short instruction file makes a rule easier to keep. If all four wordings
come out near the ceiling, that says the difference did not show at this length; it does not
say the paper is wrong about long sessions.

## The measure

`check.py <baseline> <run-dir>`. It parses every `.py` file in the run directory and never
imports or executes one.

- A function is a **target** when it is new, or when its source differs from the function of the
  same qualified name in the seeded workspace. Marker-only lines are ignored in that comparison.
- **strict**: the physical line directly below the end of the def header is exactly
  `# @tracked`. The paper does not say how its checker treats a signature spread over several
  lines; here the line below the closing `):` counts.
- A session **complies** when it has at least one target and every target is strict.

**Primary endpoint: `complies`, per wording.**

Reported beside it and not tested: `complies_lenient` (marker on the def line, directly above
it, or between the header and the first statement), and the share of targets carrying the
marker anywhere.

Sessions that touch no Python function are excluded, as in the paper, and counted. A session
that leaves a file that does not parse is counted as not complying.

`calibration/check.py` runs nineteen hand-written cases through the checker and exits non-zero
on a mismatch. It passes at the commit that fixes this document.

## Conditions, fixed in advance

- **Subjects**: the `sonnet` alias of the session's sub-agent tool, one fresh agent per session,
  no access to this conversation.
- **N**: 15 per wording, 60 sessions. Order shuffled once with the OS random source. Batches of
  ten, concurrent within a batch.
- **Placement**: each run directory is `<system dir>/<8 random chars>/<6 random chars>/`.
- **The checker is not hidden.** The rule states exactly what is checked, so there is nothing in
  `check.py` an agent could use that the rule does not already say.
- **Pilots**: two sessions, one conditional and one prohibitive, run before this document was
  fixed, only to see that an agent can write into the run directory and finish. They are not
  counted. Both finished in under a minute and both complied: 9 of 9 and 8 of 8 touched
  functions carried the marker. So the ceiling warned about above is likely. The task and the
  instruction file were written before the pilots and are **not** changed because of them:
  lengthening the session until a difference appears would be choosing the result. If the
  formal runs sit at the ceiling, that is the finding, and a longer session is a separate
  pre-registration.
- **Harness blocks**: every session is scored as it was left. No session is replaced or
  repeated. Sessions whose own report says a tool call was refused are counted and named.

## Decision rule, fixed in advance

The largest gap the paper reports is prescriptive against prohibitive, 71.6% against 17.3%.
Fisher exact, two-tailed, on `complies` for those two wordings.

- **p < 0.05, prescriptive higher** → "the wording effect showed here too".
- **p < 0.05, prohibitive higher** → "the opposite showed here".
- **anything else** → "no difference showed at this length, on this model".

With 15 per arm this test finds a gap of the reported size (71.6% against 17.3%) with
probability 0.78. A 40-point gap (80% against 40%, or 70% against 30%) is found less than half
the time. So "no difference showed" here means "no gap as large as the paper's", and the
write-up says so.

The other four cells are published as a table. Prescriptive against conditional — the
comparison the authors themselves rest their advice on — is reported with its own Fisher p and
carries no verdict; it is a second look at the same sessions.

No third option and no re-running for a better number.

## What is published

The seeded fixture, the prompt, the checker, the calibration set, one JSON line per session
(wording, targets, strict, lenient, missed functions) and every agent's `notes.md`. The agents'
Python files are published too; they are theirs and the fixture is this repository's.
