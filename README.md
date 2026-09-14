# Agent Discipline Skills

Ten skills for AI coding agents. Not "how to build X" — **how not to ship something broken
while you build it.**

Every one of them was written after an incident, and every one carries the numbers from that
incident. They depend on no vendor, no product and no company. Drop them into any agent that
reads `SKILL.md` files.

## Why these exist

Most agent skills describe a capability or a domain: make a deck, write SQL, design a UI.
Almost none describe **the ways an agent fails while doing that** — and those failures are
where the real cost is.

A sample of what is written down here, with its measurements:

- six deploys in a row that never changed the symptom once, because the population of failures
  was never queried (`diagnose-first`)
- a "one alert per incident" fix that produced **28 days of silence** on an open, unacknowledged
  incident, right after 22 alerts an hour for the same one (`state-vs-reality`)
- a job that recorded **success** because the broken rows had been filtered out of its scope,
  which auto-closed the incident and turned monitoring green (`state-vs-reality`)
- the same push handed to a human **five times**, every failure catchable before handing it
  over (`handoff-script-hygiene`)
- a gate wired into the build to prevent an outage, which **could not succeed in any
  environment** and so could never detect that outage (`verify-in-the-target-environment`)
- eight commits reported as "entirely done", sitting in a worktree from which not one command
  worked on the user's machine (`sandbox-boundary`)

## The ten

| Skill | What it stops |
|---|---|
| `diagnose-first` | fixing a symptom before you have the population of failures |
| `design-before-fix` | a correct fix that is the wrong change, because you never read how the feature reaches the user |
| `state-vs-reality` | the value says one thing, the system does another, and nobody reconciles them |
| `tool-contract-first` | judging by a proxy signal (exit codes, counts, etags) you never calibrated |
| `output-contracts` | shipping a degraded deliverable as a success |
| `self-service-delivery` | handing steps to the requester instead of delivering the change |
| `handoff-script-hygiene` | making someone run the same thing five times |
| `verify-in-the-target-environment` | "it passed on my machine" as evidence about their machine |
| `sandbox-boundary` | work that only exists in a path the user's machine does not have |
| `independent-verifier` | a review that silently downgrades to a weaker model and calls it verified |

## Install

Copy the directories under `skills/` into wherever your agent reads skills from — for example:

```bash
git clone https://github.com/<owner>/<repo>.git
cp -R <repo>/skills/* ~/.claude/skills/
```

They are plain Markdown with YAML frontmatter. Nothing is executed at install time.
The only script in the set (`sandbox-boundary/scripts/check_worktree_paths.py`) is read-only
and you run it yourself.

## Portability

The format is `SKILL.md` with `name`, `description` and `allowed-tools` frontmatter, which many
agent platforms read. Where a skill needs something platform-specific it says so in the body,
and it stops loudly rather than pretending.

Three of them talk about a sandbox that is separate from the user's machine
(`sandbox-boundary`, `verify-in-the-target-environment`, `self-service-delivery`). If your agent
runs directly on the user's machine, those sections simply do not apply — the rest still does.

`independent-verifier` needs a host that can launch a sub-agent on a named model. If yours
cannot, that skill will tell you and stop instead of substituting one.

## What is deliberately not here

- No "make it better" advice. Every rule is a gate you can fail
- No vendor names, no product names, no customer names
- No telemetry. Nothing phones home

## Contributing

The most useful contribution is **a measured incident**: what was declared, what actually
happened, how much it cost, and the check that would have caught it. Rules without a number
behind them tend not to survive contact with a real system.

## Licence

Apache-2.0. See `LICENSE`.
