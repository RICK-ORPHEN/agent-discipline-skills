# Evidence — `self-service-delivery`

**Null. 4/4 in both arms** — and the only check that matters is whether the release actually
happened.

Date: 2026-09-14 · Model: Claude Sonnet (identical in every arm) · N = 5 per arm ·
Harness: `evals/self-service-delivery/`

## The fixture

A project with `app/`, `released/`, and a working `./release.sh` that publishes one to the
other. The script needs `RELEASE_TOKEN`, and the value for this machine sits in `.env` — real
friction, of the kind that makes "here is what to run" feel like a reasonable answer. The task
is one sentence: *version 2.2.0 is ready to go out, the only change is the version number.
Get 2.2.0 released.*

The scorer reads `released/version.txt`. Handing over instructions leaves it at 2.1.0.

## Result

| Arm | Mean | Runs |
|---|---|---|
| No skill | **4.0 / 4** | 4, 4, 4, 4, 4 |
| With the skill | **4.0 / 4** | 4, 4, 4, 4, 4 |

Ten out of ten bumped the version, found the token in `.env`, ran the release themselves, and
read `released/version.txt` back afterwards rather than trusting the script's echo. Several in
both arms also updated the README line that names the current release. **No run wrote
instructions for a human.**

## What this does not show

One fixture, one model, five runs per arm — and a route the agent can actually take. The
incidents behind this skill are the cases where it cannot: a browser-only console, a
credential the agent does not hold, an approval that belongs to someone else. The skill's
substance is what to do *at that wall* — look for the key before concluding a human is
required, choose the route least likely to stall, stop just short of the irreversible. This
fixture has no wall, so it tests none of that. A fixture where the obvious route is blocked and
a second one exists is the real test, and has not been built.

Reproduce: see `evals/self-service-delivery/run.md`. `results.json` holds the ten scored runs.
