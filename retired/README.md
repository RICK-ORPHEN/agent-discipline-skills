# Retired — measured, and taken out of the public catalog

These five were published, then removed on 2026-09-14 because measurement said they do not
change what a current model does.

| Skill | First measurement | Harder fixture, control only |
|---|---|---|
| `design-before-fix` | null, 4/4 both arms | 3/3, 5 of 5 runs |
| `state-vs-reality` | null twice (prose and behaviour) | 3/3, 5 of 5 runs |
| `tool-contract-first` | null twice (prose and behaviour) | 3/3, 5 of 5 runs |
| `sandbox-boundary` | null, 10/10 | 3/3, 5 of 5 runs |
| `self-service-delivery` | null, 4/4 both arms | 1/1, 5 of 5 runs (sanctioned variant) |

The full argument, including the one fixture where control failed and why that failure does
not count, is in `../evidence/screening-2026-09-14.md`. The fixtures and scorers are in
`../evals/screening/`.

## Why they are kept here rather than deleted

Two reasons.

The incidents behind them were real, and the text is still the best record of what happened.
Nothing in these files has been shown to be *wrong* — what has been shown is that a current
model already does these things unprompted, in a short single-shot task, with the bait in
plain sight.

And the screening tested one setting. Every run was a clean directory, one task, no prior
context, nobody waiting. The incidents these came from were long sessions, second and third
attempts at the same bug, the agent's own earlier output sitting in context as evidence. The
honest case for these five is that the behaviour may not survive that load — which is a case
nobody has tested, in either direction.

**If a fixture is built in which a current model, with no skill, walks into one of these
failures, the matching skill comes back and that fixture is the reason.** That is the bar for
re-publishing, and it is the same bar the other five had to clear.
