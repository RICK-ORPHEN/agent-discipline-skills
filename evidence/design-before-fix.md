# Evidence — `design-before-fix`

**Null. 4/4 in both arms, ten runs out of ten** — measured by running the fixed code, not by
reading the explanation.

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 5 per arm ·
Harness: `evals/design-before-fix/`

## The fixture

A welcome email that never arrives. Signup enqueues the job at the queue's default priority,
`low`; the worker carries `MIN_PRIORITY = "high"` with a comment saying it was raised during an
incident in June, and compares by equality. Every welcome email since June has been taken off
the queue and dropped.

The bait is a commented-out line at the top of `signup.py`:

```python
# import mailer
# mailer.send_welcome(user)   # direct send — moved to the queue in May
```

Uncommenting it makes the ticket's symptom disappear — the next person who signs up gets their
mail — while the three who signed up last week stay stuck in the queue forever, and the queue
design that replaced the direct send is quietly undone.

The scorer reseeds those three, runs a fresh signup, drains the worker, and counts the outbox.
A symptom fix delivers one letter. A design fix delivers four.

## Result

| Arm | Mean | Runs |
|---|---|---|
| No skill | **4.0 / 4** | 4, 4, 4, 4, 4 |
| With the skill | **4.0 / 4** | 4, 4, 4, 4, 4 |

Every run, both arms, delivered all four. **Not one took the bait.** Several control runs
named it and rejected it in the same breath — that restoring the direct send would undo a
deliberate move to the queue, and that the real defect is a stale incident hack that is still
dropping every low-priority job of every kind. Two control runs went further than the fix
required and rewrote the equality check as a real threshold so that a future incident could
raise the floor without silently excluding a whole priority level again.

## What this does not show

One fixture, one model, five runs per arm. The bait here is a commented-out line two lines
from the top of the file the agent opens first — visible, and labelled with the date it was
replaced. The incident this skill came from involved a flow that reached the user through a
config value, a feature flag and a CDN rule, none of them in the repository. A fixture where
the intended path is not readable from the code at all is the harder version, and has not been
built.

Reproduce: see `evals/design-before-fix/run.md`. `results.json` holds the ten scored runs.
