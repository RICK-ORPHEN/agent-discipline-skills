---
name: state-vs-reality
license: Apache-2.0
allowed-tools: Read, Grep, Glob, Bash
description: "The discipline of reconciling the value that represents state with what the system actually does. Use when: the display or the record looks right but the real thing differs, or the reverse. Do NOT use when: you are tracing the root cause of a live symptom, or the problem is a boundary between two machines."
---

# state-vs-reality — reconcile the declaration with the behaviour

## 0. One line

**Look at what the system does, not at what the value says.
Then count every reader.**

## 1. Why this exists — eight defects measured in a single day

Every one of them had the same shape: *the source of truth was correct, and nobody was
reconciling it.* Not one was technically hard. **They were all failing silently.**

| # | Declaration | Reality | Damage |
|---|---|---|---|
| 1 | three vocabularies coexisted in an `industry` field | the signup form stored free text verbatim | **6 of 8 accounts had received no industry term at all** |
| 2 | `priceMonthlyJpy: null` meant "price undecided" in one module and "declared free" in the checker | every account used it free, ungated | **matched neither declaration** |
| 3 | middleware honoured `expires_at` | **the cron did not** | expired grants kept working |
| 4 | reads were normalised by `normalizeIndustry` | **the write path (a settings dropdown) was not** | 4 accounts lost their term on a single save |
| 5 | an integration reported `status: active`, `reconnect_required: false` | **failing every hour** (86 times over 26 hours) | nothing surfaced; nobody noticed |
| 6 | "one alert per incident" should be enough | **silence for a month** (open, unacknowledged, 1,401 occurrences) | before that, 22 alerts an hour for the same incident. It swung between both extremes |
| 7 | the delivery ledger records everything | reopening reset the stage to 0 and **collided with the old row, so the record was dropped** | you could no longer tell whether a message was sent or suppressed |
| 8 | the sync job recorded "success" | it **excluded broken integrations** via a `status = 'active'` filter | 0 rows → success → incident auto-closed → monitoring green |

⚠ **#4 happened *after* #1 was "fixed."** Only the read path had been changed, and it was
called done.

## 2. The procedure

Do not skip steps.
→ `references/procedure.md`

## 3. How to report

- If you write "fixed", **count the actual damage.** One of the expiry bugs above turned out,
  when counted in production, to have affected zero rows. The honest sentence was
  "closed the hole before it opened", not "closed a hole that was leaking"
- **Never count an unchecked item as a pass.** List them as "N unverified"
- Never carry a degradation through silently

## 4. Related

- Lessons: *one value carrying two meanings* / *confirm the baseline is green before trusting
  a checker* / *verify the subject itself before reporting on it*
- Neighbouring disciplines: boundaries between two machines (a path declared vs. where the
  file is) / overturning a "cannot be done" about an execution route by measuring it
