# Agent Discipline Skills

**A capable model notices the problem. The code it writes does not.**

That is not a slogan — it is the result every rubric in this repository had to be rebuilt to
see, and the reason half the catalog is gone.

- Asked to *describe* a hazard, a current model describes it correctly. Every prose rubric we
  wrote saturated at 10/10 across both arms. Those rubrics measured nothing.
- Asked to *write the nightly report script*, **4 of 5** runs produce one that drops unreadable
  rows, logs a warning to stderr, and emits a `summary.json` a machine cannot tell apart from a
  clean night.
- Asked to *write the startup check*, **13 of 15** runs produce one that silently selects one of
  three write-capable credentials. Several of them state in their own write-up that the choice
  is ambiguous and order-dependent — and ship it anyway.

The disclosure a model performs in its own voice does not survive being turned into code. These
five skills are what carries it across.

Not "how to build X" — **how not to ship something broken while you build it.** Every one was
written after an incident, carries an A/B number against a current model, and ships with the
harness that produced it. Ten were written. Five are here. **The other five were removed by the
same measurement**, and the record of that is below.

They depend on no vendor, no product and no company. Drop them into any agent that reads
`SKILL.md` files.

## The incidents behind them

Most agent skills describe a capability or a domain: make a deck, write SQL, design a UI.
Almost none describe **the ways an agent fails while doing that** — and those failures are
where the real cost is.


- six deploys in a row that never changed the symptom once, because the population of failures
  was never queried (`diagnose-first`)
- a nightly job that reported success on data it had silently dropped, because the loss went to
  stderr and cron's mail is where warnings go to die (`output-contracts`)
- the same push handed to a human **five times**, every failure catchable before handing it
  over (`handoff-script-hygiene`)
- a gate wired into the build to prevent an outage, which **could not succeed in any
  environment** and so could never detect that outage (`verify-in-the-target-environment`)
- a review that quietly ran on a weaker model than the one it was asked for, and was reported
  as an independent second opinion (`independent-verifier`)

## Does it change anything?

Ten skills were measured. Same task, same model, five runs with the skill and five without,
scored off what the agent leaves behind — and, wherever the deliverable runs, by **running it**
against the hard case.

**Five changed something. Five did not. The five that did not are not in this repository.**

| Skill | Effect | The measured difference |
|---|---|---|
| `diagnose-first` | **large** | **0/5 produced the population without it, 5/5 with.** No overlap between the arms (p = 0.008) |
| `output-contracts` | **large** | **5/15 without it emit a loss a machine can see, 15/15 with** (p = 0.0002). Scored on prose first: null. That null was wrong |
| `verify-in-the-target-environment` | **large** | Both arms describe the problem. **2/15 without it then write a check that silently picks one of three write-capable credentials; 15/15 with it stop** (p = 0.000002) |
| `handoff-script-hygiene` | moderate | **0/5 added a fallback for a blocked port, 4/5 with.** (p = 0.048.) Six of nine checks were already satisfied without it |
| `independent-verifier` | one axis only | Both arms found the bug. **0/5 disclosed that the "independent" review was its own; 5/5 with it did** (p = 0.008, measured post-hoc) |

### What the five that work have in common

Each carries something **the task cannot imply**:

- a fact the model does not have — a blocked port 22 has a 443 route
- work it will not volunteer — tabulate the failures nobody asked about
- a rule that must survive being turned into code — put the loss in the output, not in stderr
- a decision at an ambiguous point — three candidates, stop rather than pick
- an obligation to report on its own process — say the second opinion was not second

## The five that were removed

`design-before-fix`, `state-vs-reality`, `tool-contract-first`, `sandbox-boundary` and
`self-service-delivery` each measured **null** — no difference between the arms, on a fixture
built to catch exactly the failure the skill describes.

A null on one fixture is weak evidence, so each of the five got a second fixture, built
specifically to attack the limitation its own evidence file had already admitted: the bait
moved out of the file the agent opens first, the scope filter buried in a shared package, the
verification reader made to lie too, a real git worktree with sandbox paths baked into both
link files. Then the **control arm alone** was run, to answer the only question that matters
before rewriting anything:

> Can this model, with no skill at all, still be made to fail here?

**No.** All five harder fixtures: control at ceiling, 5/5, every check. Not one failing run.

There is nothing for a rewrite to close. So they came out.

The one apparent exception proves the rule. `self-service-delivery` was the only skill for
which a failing control could be produced — a release whose normal route was blocked and whose
second route was a credential sitting in the repo. Control scored 0/5. But all five runs found
that second route, understood it, and **refused it on principle**: publishing around a token
the ops team deliberately keeps off the machine is not the agent's call. Two flagged the
checked-in key as a security problem. Making control "pass" that fixture would mean writing a
skill that teaches an agent to get past an access control with a key it found lying around.
Rebuilt with the second route explicitly sanctioned, control scored 5/5.

That is not a verdict on the discipline. The incidents behind those five were real and
expensive. **The model that caused them was not this one.** All five are kept in `retired/`
with the reason on each, the fixtures and scorers are in `evals/screening/`, and the full
argument is in `evidence/screening-2026-09-14.md` — so the removal can be argued with.

### On the numbers

Every p is Fisher's exact test, two-tailed, on the check named in the row.

`verify-in-the-target-environment` entered this catalog on **2/5 vs 5/5**. Tested afterwards,
that is **p = 0.44** — not distinguishable from chance — its separating measure had been added
*after* reading the runs, and the README stated the control arm wrong (2/5 where the evidence
file said 3/5). It was re-measured at N = 15 with the measure and the decision rule fixed in
advance, and **the first round of that re-measurement failed its own primary endpoint**
(12/15 vs 15/15, p = 0.22). Reading those runs showed the fixture was at fault: the check most
control runs wrote passed the endpoint because of the order of two lines in a JSON file. The
fixture was fixed, the endpoint kept, both arms re-run: **2/15 vs 15/15, p = 0.000002.**

The pre-registration, including the round that failed, is published in full at
`evals/verify-in-the-target-environment-n15/PRE-REGISTERED.md`.

`output-contracts` has since had the same treatment, and its scorer had the same class of
defect — the primary counted a plain crash as "the loss is visible", which is the opposite of
what the skill asks for. Closed before the runs. At N = 15 the effect is larger
(**p = 0.0002**) and the control arm is better than the N = 5 number implied: 5/15, not 1/5.
**The first measurement made the model look worse than it is**, which is the less comfortable
direction for an error to run.

**One entry above still rests on N = 5 at p = 0.048** — `handoff-script-hygiene`. Its check is
also the weakest in kind: it reads the produced script's *source*, so a fallback written in a
comment counts. It is queued for an N = 15 round on a fixture that runs the script against a
push that actually fails, and whatever comes back gets published, including if it sends the
skill to `retired/`.

### On the rubrics

Three skills were first scored by reading a write-up and all three looked null. Re-run by
executing the artifact, one flipped decisively and two held. **Where a skill produces something
runnable, run it against the hard case** — grepping a write-up measures whether the model can
describe the problem, which it can, every time.

Every measurement is written up in `evidence/`, including the ones that produced a null, and
several carry a "we got this wrong first" note, because we did: a prompt that stated the lesson
it was measuring, a scorer an agent found and graded itself against, and a fixture generator
that wrote two of its three files empty.

The screening harnesses — fixtures, scorers and results for the five removals — are in
`evals/screening/`. **The ten original A/B harnesses are not published yet**: their scorers are
commented in Japanese, and shipping them into an English repository before translating them
would be worse than saying so. Translating them is open work, listed below.

## The five

| Skill | What it stops |
|---|---|
| `diagnose-first` | fixing a symptom before you have the population of failures |
| `output-contracts` | shipping a degraded deliverable as a success |
| `verify-in-the-target-environment` | "it passed on my machine" as evidence about their machine |
| `handoff-script-hygiene` | making someone run the same thing five times |
| `independent-verifier` | a review that silently downgrades to a weaker model and calls it verified |

## Install

Copy the directories under `skills/` into wherever your agent reads skills from — for example:

```bash
git clone https://github.com/<owner>/<repo>.git
cp -R <repo>/skills/* ~/.claude/skills/
```

They are plain Markdown with YAML frontmatter. Nothing is executed at install time, and the
set contains no scripts at all.

## Portability

The format is `SKILL.md` with `name`, `description` and `allowed-tools` frontmatter, which many
agent platforms read. Where a skill needs something platform-specific it says so in the body,
and it stops loudly rather than pretending.

`verify-in-the-target-environment` assumes the agent's sandbox may be a different machine from
the user's. If your agent runs directly on the user's machine, that framing simply does not
apply — the rule it enforces still does.

`independent-verifier` needs a host that can launch a sub-agent on a named model. If yours
cannot, that skill will tell you and stop instead of substituting one.

## What is deliberately not here

- No "make it better" advice. Every rule is a gate you can fail
- No vendor names, no product names, no customer names
- No telemetry. Nothing phones home
- **No skill without a measured effect.** That is what took this from ten to five

## Contributing

The most useful contribution is **a measured incident**: what was declared, what actually
happened, how much it cost, and the check that would have caught it. Rules without a number
behind them tend not to survive contact with a real system.

A second useful contribution is **a fixture that makes one of the removed five fail.** If you
can build one — a setting where a current model, with no skill, walks into the failure — that
skill should come back, and the fixture is the argument for it.

Open work, in order:

1. translate the ten original A/B scorers and publish them alongside `evals/screening/`
2. a fixture that makes any of the five in `retired/` fail without a skill
3. re-measure the five that ship here against models other than the one they were measured on

## Licence

Apache-2.0. See `LICENSE`.
