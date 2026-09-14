---
name: output-contracts
license: Apache-2.0
allowed-tools: Read, Grep, Glob, Bash
description: "The reference standard for deciding whether something may be shipped, and whether a command may be run. Returns PASS / DEGRADED / FAIL at three gates: entry, mid-work (destructive and irreversible operations), and exit. Use when: you want a fixed yardstick for 'is this safe to run' or 'is this ready to hand over'. Do NOT use when: you need the procedure for a specific change — this ships criteria, not steps."
---

# Output Contracts — the standard for what may ship

This skill ships **criteria, not procedures.** Other skills read it to decide pass or fail.

## What is in here

| File | Applies to | Contents |
|---|---|---|
| `work-contract.yaml` | Documents, decks, reports, sites, landing pages, dashboards | Forbidden destructive commands, per-archetype acceptance criteria, ban on silent degradation |

This is a starting point, not a finished policy. **Adapt the archetypes and the acceptance
criteria to your own deliverables.** What must not change is the three-valued verdict, the ban
on silent degradation, and never counting an unchecked item as a pass.

## Three gates

1. **Entry** — run preflight once before touching any source material or external tool. If a prerequisite is
   missing, **stop; do not try to fix the environment on the spot.** Reinstalling a missing
   tool mid-run has broken things that were already working.
2. **Mid-work** — do not run operations you cannot undo: `brew uninstall`, `pip uninstall`,
   `rm -rf <system path>`, `git push --force`, `git add -A`, `DROP TABLE`. The rule is
   *install the new thing, verify it, then remove the old one.* When a command is
   borderline, check it against `irreversible_ops.block_patterns` in the contract.
3. **Exit** — check the output acceptance criteria before handing anything over and return
   one of three verdicts: **PASS / DEGRADED / FAIL**.

## ⚠️ DEGRADED is not success

Any workaround that **changes the nature of the output** — a video that became a still, audio
that disappeared, captions that were never burned in, chapters dropped to make the numbers
work, real data replaced with sample data because the real data could not be fetched, an
image-less deck because image generation failed — must never be carried through silently.

Always tell the requester **what was lost** and ask how they want to handle it.
**Do not report "100% complete."**

This is not about reducing autonomy. It separates workarounds you may carry on through from
degradations you must always disclose. The boundary is written in the contract's
`fallback_policy`.

## Never count an unchecked item as a pass

A check must list **"N unverified"** separately. Do not fill in what you could not read, or
what was never specified, with a guess and then call it a pass. The moment unverified items
are folded into the pass count, the check starts lying.

## How to use it

The contracts are YAML — read them directly and judge. To run the check, the calling pipeline
passes its `archetype` and the checker matches against it.

The contract files live in different places depending on the environment, so **do not hardcode
one path.** Look in this order:

1. an explicit environment variable
2. the same directory as the checker (when shipped alongside it)
3. this skill's own directory

If none of them has it, **print the places you looked and stop.** Do not proceed on a guess.
