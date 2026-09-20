---
name: diagnose-first
license: Apache-2.0
allowed-tools: Read, Grep, Glob, Bash
description: "Investigate a production symptom down to a named root cause BEFORE writing any fix. Use when: it does not get fixed, the same error keeps coming back, a previous fix did not change the observed behaviour, or you are about to jump on the first plausible cause. Do NOT use when: what you need is to re-read the product design."
---

# diagnose-first — pin down the scope before you fix

## Why this exists

A report came in that a system "cannot produce minutes." **Six deploys, and the symptom did
not change once.** Every round had a plausible cause and a cheap fix.

| | What was fixed | Result |
|---|---|---|
| 1 | the recovery execution slot | still 400 |
| 2 | the stalled-progress check | still 400 |
| 3 | name/content matching | still 400 |
| 4 | rebuilding the WAV | still 400 |
| 5 | plan reuse | still 400 |
| 6 | delivery and recording | (stopped to investigate) |

On the sixth round the **audit log for other meetings** finally got looked at. One query. It
showed:

- Subject A (975 s / 69 chunks) — **34 chunks rejected by the provider**, the failures landing
  on index 2, 4, 6 … 68, every other one. The error text was different from the meeting being
  chased (`Audio file might be corrupted or unsupported`). And it had finished by
  **declaring "recovery complete" and producing minutes from half the audio**
- Subject B (segment 4 of 72 missing) / Subject C (segment 2 of 175 missing) — segments never
  reached storage
- Subject D — audio too short
- Subject E — the single .wav that had been chased six times

**There were four distinct faults, and one of them had been fixed six times.** The most
damaging one was the one nobody was chasing. "It cannot produce minutes" is noticeable.
"It produced minutes from half the audio" is not.

This document is not a mindset. **It is a gate you pass before you start.** If it is not
satisfied, do not open the code.

---

## The gates

### 0. The reported symptom is an entrance, not a scope

What a user reports is **the one case the user was able to notice.** Assume faults of the same
and different kinds are running alongside it, unnoticed. Behind "cannot produce minutes" sat
"produces minutes from half the audio."

**Do not let the wording of the symptom set the scope of the investigation.** Let the data set it.

### 1. Produce the population first

Before opening any code, pick a time window and tabulate **how many rows and how many distinct
subjects** there are, per kind of error.

```sql
select
  action,
  count(*)                   as rows,
  count(distinct target_id)  as targets,
  max(created_at)            as last_at
from audit_log
where action like '<domain>.%'
  and created_at > now() - interval '7 days'
group by action
order by rows desc;
```

If the error text lives inside a payload, **bucket it by signature** — the leading shape, not
the whole string.

```sql
select
  substring(payload->>'error' from 1 for 80) as signature,
  count(*) as rows,
  count(distinct target_id) as targets
from audit_log
where action = '<the failing action>'
  and created_at > now() - interval '7 days'
group by 1 order by rows desc;
```

**Until you can produce this table, do not fix a single line.** If you cannot produce it
because of missing access or a missing path, that is itself the first thing to fix (gate 3).

The table must always include:

- how many kinds of fault there are
- how many rows and subjects each has
- **whether anything that "finished successfully" is actually missing data**

Do not skip the last one. That is where the worst case was hiding.

### 2. Name one example that is working

Always name one case **that goes through the same path and succeeds**, and enumerate every
difference between it and the broken one.

- If you cannot name one, you have not defined "normal", and you are not qualified to talk
  about the cause
- If there are ten differences, write ten. You pick "I think this is the cause" only after
  they are all on the page

In the case above, "the 492-segment meeting works" was asserted while **that meeting was also
dropping 34 chunks** — never noticed. Verify with data that your named-healthy example really
is healthy.

### 3. Put observation in before the fix

**If you cannot tell from data whether your change even executed, add that means of telling
first. The fix comes second.**

The means of telling was added on round six. That is backwards. Rounds 1–5 could not
distinguish "the path is not reached, so nothing changes" from "the path is reached and the
change does nothing" — they only saw an unchanged result.

- `console.log` is not observation. Emit to **somewhere you can read later** (here the
  application log was unreachable; the audit log was writable)
- Recording is diagnosis, not processing. **A failure to record must not stop the main work**
- "Did it run" is not enough. Record **which branch was taken**, and the shape of the input
  (size, format)

### 4. Never apply a second local fix to the same symptom

If you miss once, go back to investigation, not to fixing. **No exceptions.**

"Now I have really got it" is exactly what you thought the first time. Do not use that same
conviction as grounds the second time. The only thing permitted on the second round is redoing
gates 1–3.

### 4.5 Do not stop halfway to say "next I will…"

**Keep going until you know.** Do not ask for a decision in a progress update.

Repeatedly saying "next I will check X" takes the other person's time every time. What they
want is not a live commentary on progress — **it is the answer.**

You may report in exactly three situations:

1. the confirmed facts are in, and **exactly one** unknown remains
2. that unknown is **physically solvable only by them** (then ask, once)
3. it is fixed, and you have the evidence

"I will look into it", "next I will…", "what should I do" are none of these.

### 4.6 Confirm your own observation through two paths

**Do not build a conclusion on "I read it."**

A SQL result once got misread into a flat assertion that "the file was never created", and
**two pull requests were built on that misreading.** The file existed and was being rebuilt
every time. One misreading turned into two deploys and two pieces of work for someone else.

- When you assert "there is none", **confirm again through a different API or a different path**
- Hitting the name directly and seeing a 404 is stronger than "not in the listing"
- When you quote your own earlier conclusion, check whether **you can reproduce the raw data
  it rested on.** If you cannot, verify it again

### 5. Do not say "fixed"

The only thing you may report is **a measured value.**

- Bad: "Fixed it." "This should work now." "That was the cause."
- Good: "12:25 before the deploy was X; 12:31 after it was Y. Unchanged."
- Good: "If this line appears, the path was reached. If it does not, it was not."

When you state a cause, **always attach the observation that supports it.** Anything you cannot
support is a hypothesis. Call it one.

---

## Deliverable — the investigation note

Fill in `templates/investigation.md`. That is the ticket of entry to the release path. Do not
push anything whose note is unfilled.

If a field cannot be filled, **filling that field is the first task.**

---

## Never

- **Do not explain a cause from one log line.** Produce the population first
- **Do not go and confirm your hypothesis. Go and refute it.** Look first at what *else* is failing
- **Do not fill an unreadable fact with inference from its surroundings.** If you cannot read
  it, make it readable (gate 3). Five rounds of guessing happened without ever reading the file
- **Do not assume a record that ends in success is healthy.** The ones that complete while
  missing data do the most damage
- **Do not stop at "next I will…".** Go until you know. Commentary is not a result
- **Do not turn your own last conclusion into the next premise without verifying it.**
  Misreadings chain
- **Do not skip the investigation because you were asked to be fast.** Skipping it is what
  produced six round trips. **Say, yourself, that investigating is the shortest path**

## Things that stop you getting stuck

- If there is an audit log or an event table, start there. It is more readable than app logs
- SQL is the fastest way to aggregate. Do not pull every row and count by hand
- Regularities like "only one side fails" or "every other one fails" **almost name the shape of
  the cause.** When you see one, work backwards from it
- If there are several paths (single file / split, new / recovery), **establish which path was
  taken first.** Five rounds missed that a stored plan was being reused and skipping the whole
  preparation step

## Track record

| | |
|---|---|
| Miss 1 | six deploys, symptom never changed once. The population was first looked at on round six |
| Miss 2 | the meeting named as "the one that works" was itself dropping 34 chunks. The named-healthy example had never been verified |
| Miss 3 | the real file contents were never read; five rounds of inference rested on them. Making it readable came first |
| Miss 4 | a misread SQL result became "the artefact does not exist", and two PRs were built on it. It existed and was updated every run. **One misreading = two pieces of someone else's work** |
| Miss 5 | repeating "next I will check X" made someone wait each time. They wanted the answer, not the commentary |
