# The procedure — do not skip steps

## 2.1 Touching a state value — count the consumers

```
grep -rn '<the value>' --include='*.ts' --include='*.tsx' --include='*.mjs' .
```

Then **write out what each one takes it to mean.**

- Two or more interpretations **is the defect.** Fixing one side does not fix it
- **Always count the actual runtime behaviour as a third interpretation.** In #2 above,
  production was doing something different from both the writer and the reader. You cannot
  see that from the code alone
- Kill the ambiguity **with a type or a checker.** A comment saying "this means free" will
  not be read by whoever touches it next. Remove `null` from the type, or fail in a check

## 2.2 Before you say "fixed" — check both the reader and the writer

**A one-directional fix is not a fix.**

- If you normalised reads, look at **saves, defaults and form initial values** too
- `<select defaultValue={rawValue}>` renders **the first option as selected** when the value
  is not in the list. The moment the user saves, the value is silently rewritten (that is #4)
- If you added an expiry or a flag, **count every place that reads it** — middleware,
  server-side enforcement, cron, RPC, UI

## 2.3 Paths that record failure — make the state reflect reality

**A function that records a failure must not claim "connected."**

- Do not hardcode optimistic values like `connected: true` **on the failure path**
- **Classify** whether it is "reconnect to fix" or "wait and it recovers." With only a boolean,
  an operator watches hourly retries of something that has simply expired
- **Do not store raw error text** (it can carry vendor names and internal identifiers). Keep a
  machine-decidable classification and the HTTP status
- Count consecutive failures. It is the only number that separates "failed once" from
  "has been failing for 26 hours." **Counting without surfacing it is the same as not counting**

### 2.3.1 Decide the stop condition before you stop anything

**When you write code that stops a notification, a retry, or a monitor, put the stop
condition into words first.**

Measured on one incident, both opposite failures happened:

| Period | Symptom |
|---|---|
| 9 days | **22 messages** (hourly) for the same incident |
| the next 28 days | **not one message** (still open, unacknowledged, 1,401 occurrences) |

The second period was the fix for the first. Changing it to "once per incident" produced an
implementation that **never told anyone again once it had told them once.**

- Wrong: stop because it was sent / stop because the count got high
- Right: **stop because a human acknowledged it / stop because it was resolved**

If you want fewer messages, **lengthen the interval** (hourly → daily). Going quiet is a
different decision, and only a human or a recovery may make it.

⚠ **Do not conflate suppression with silence.** If you implement "do not send right now",
always write **when it will be remembered next.** A suppression with no scheduled return is
silence.

### 2.3.2 Is a checker requiring the very defect you are removing?

The same day, fixing the defect above **broke CI.** An existing checker required the strings

```
stopRepeatedEscalation / escalation_level > 1 / "duplicate_suppressed"
```

as mandatory. The month of silence was held up not only by the code but **by the checker.**

- When a checker fails, **first read whether the invariant it protects is still correct.**
  Adding the string to make it pass is the last resort
- A checker that fails when you delete the implementation is right.
  **A checker that fails when you fix the implementation is wrong**

### 2.3.3 Before saying "everything passes", did you run what CI runs?

One report of "verify PASS" was based on a new checker plus lint, tsc and unit tests. CI then
failed: **the build's verify chain had 72 commands**, and two of them caught the change.

```bash
node -e "console.log(require('./package.json').scripts.build.split('&&').map(s=>s.trim()).filter(c=>c!=='next build').join('\n'))" > /tmp/chain.txt
while read -r cmd; do eval "$cmd" || { echo "FAILED: $cmd"; break; }; done < /tmp/chain.txt
```

**Do not call it green when you only ran the checks near what you touched.**

### 2.3.4 Are you counting "excluded from scope" as "fixed"?

**Exclude the broken thing from a job's scope and the job stops failing — and records success.**

Measured, right after an integration expired into `status: 'error'`:

| Time | What happened |
|---|---|
| 19:12 | sync fails → status set to `error` (correct) |
| 20:12 | the cron only picks up `status='active'` → **0 rows → "success" recorded → incident auto-closed** |
| 20:15 | the aggregate job is green → external monitoring is green |
| 21:06 | a human reconnects it (**for that hour, operations looked entirely healthy**) |

**It did not close because it was fixed. It closed because we stopped looking.**
This is the mirror image of "claims healthy while failing", and **it is harder to notice** —
nothing failed, so nothing appears in the logs.

Checklist:

- Does the scope filter (`status = 'active'` and friends) **exclude the broken ones?**
- **Are you recording zero rows as success?** "There was nothing to do" and "what should have
  been done was filtered out" are different things
- **Are you counting** what is parked waiting on a human (reconnect, approval, payment)? If you
  count it, you can report it as a degradation, and it clears itself when the human acts
- **Are you defaulting to zero when you could not count?** Treating "unknown" as "none" makes
  it go quietly green again (return `null` and treat it as a degradation)

## 2.4 Right after writing a checker — break it and watch it fail

**Green is not evidence of correctness. "It has not checked anything yet" is also green.**

Always run a mutation test:

1. confirm it PASSes on the untouched baseline
2. introduce **a mutation that reproduces the actual incident** and confirm it fails
3. restore, confirm **the sha256 matches** and it PASSes again
4. keep the mutation in the test suite (a one-off check leaves nothing for the next person)

⚠ **Checkers themselves are often broken.** Actually encountered:

| How the checker broke | Symptom |
|---|---|
| the `{` of a parameter type annotation `(input: { ... })` read as **the function body** | body came out empty; false positives |
| **the comment explaining a prohibition** counted as a violation | you can no longer write down dangerous knowledge |
| counting a word that appears in a comment | deleting the implementation passes (the mutation is not detected) |
| **guessing** an `npm run` script name and running it | exit 1 on a nonexistent name → misread as "broken" |
| the checker exists but is **wired into neither the build nor CI** | it never runs while production does |
| **requiring the defect itself as a mandatory string** | fixing it breaks CI (2.3.2) |

Countermeasures: **strip comments before scanning** / **read script names out of
package.json** / **wire every new checker into the build or CI** (a forgotten one is found
mechanically by diffing the list of `verify-*` against the build line).

### 2.4.1 Do not hand-maintain the list of things to check

**If every incident adds a name to the checker, the next thing added will always be missed.**

Three hand-written lists in one checker, all measured as incomplete:

| Hand-written list | Counted by hand | Actual | What was missing |
|---|---|---|---|
| failure-recording functions | 2 | 4 | one integration **had never been checked at all** |
| modules calling upstream | 2 | 18 | the **token fetches** for two providers (which reproduce the same month of silence) |
| crons driving integrations | 1 | 2 | one left running in production |

On top of that, **29 of the 50 numbers** the cron returned were absent from the ledger's
allowlist, so `errors` and `*_failed` were being dropped silently.

**Collect by convention, then recount.**

- Gather subjects by naming convention (`record…Failure`) or code shape (contains `await fetch(`)
- **Write a minimum subject count into the checker.** If the scan breaks and finds zero, it
  reports "no violations" and goes green
- Do not delete exceptions — **declare them with a reason** (close the silent-drop path)
- If you keep a hand-written list, **reconcile it against what the machine recounted**

⚠ **Mutate the scan, not only the subject.** The hardest failure to find is a checker that
goes green having collected nothing.

### 2.4.2 If you write "the canonical version is elsewhere", confirm that place exists

**References outlive the things they point at.** This is the inverse of everything above, and
it is harder to notice.

A decision gate carried this note:

```
Pricing revision is out of scope for this commit. The proposal is in
§3 of the handover memo on another branch; it will be settled in a separate session.
```

**That document did not exist in the repository** (full-text search: zero hits). The input was
gone and nobody could tell, so **the completion condition never closed.**

- Mechanically collect **references to files inside comments and design notes** and confirm
  they exist
- Do not write "the proposal is elsewhere." **Settle it here, or write that it does not exist**
- Scanning always produces false positives (`.tsx` read as `.ts`, relative phrasing in prose,
  paths inside external URLs). **Do not paper over them with an exclusion list — make the
  collection more precise.** Excluding false positives eventually excludes real ones

⚠ Your own newly written prose is in scope. In the very commit that added this checker, it
immediately caught **a wrong reference name I had just written** (a checker that did not exist).

### 2.4.3 Do not hold everything because one half needs real hardware

If the acceptance criteria mix **a part that closes deterministically** with **a part that
needs a real device**, split them and close the first half now.

A criterion — "unlicensed modules are blocked at all three layers" — sat unmet for days waiting
on browser E2E. Split:

- **decision** … evaluate all 77 cases exhaustively against production data with the pure
  function → closed immediately
- **rendering** … the look of the lock screen and the login route → one manual pass

Only accept "0 cases" after a mutation test (fail-open finds 43, writable-in-readonly finds 7,
over-blocking finds 3).

## 2.5 After a squash merge, always cut a fresh branch

**A squash merge means your original commits are not ancestors of main.**
Stack the next commit on the same branch and open a PR, and you get:

- at best, "already-merged diffs shown again" (the review is unreadable)
- at worst, **`CONFLICTING`**

This happened twice (first a re-show, then a conflict). Both times the only cause was a stale
base; there was nothing wrong with the content.

**Procedure, no exceptions:**

1. fetch
2. `git checkout -b <new name> origin/main`
3. `git cherry-pick <the new commits>`
4. print `git rev-list --count origin/main..HEAD`

**⛔ Stop condition (this, not the procedure, is the point)**

> **If the number of commits ahead differs from the number you actually wrote this time,
> do not push.**

This happened three times (re-show / conflict / conflict).
**On the third, `= 2 commits` was printed and then ignored.** The procedure was known. It was
not followed. So it is written as a stop condition, not a procedure.

Do not proceed on "it merges, so it is fine." A PR diff is read by a human, and a re-shown diff
destroys their ability to judge whether the change is really only this.

⚠ **When git says an object is "corrupt", look before you break anything.** In one case
`fatal: loose object ... is corrupt` appeared, yet `git cat-file -t` read it and
`git fsck --connectivity-only` exited 0. **A concurrent session had simply grabbed a
half-written object**; the real content was a dangling commit. `cherry-pick --quit` and a retry
was enough. Confirm it is unreadable before deleting `.git` or reaching for `--force`.

## 2.6 Before you say "there is none" — emptiness is not evidence

- Zero hits from a code search is not evidence of absence (index lag)
- Not being able to get logs is not "there were no errors"
- **A column existing does not mean anyone reads or writes it.** One `error_count` column was
  **dead: written by nothing, read by nothing.** `grep` for **both** writers and readers

## 2.7 When you cannot find the cause — do not chase the wording

An integration's failure reason stayed `unknown`. The fingerprint (first 8 hex of the message
SHA-256) was identical every time — **a fixed string.** Three attempts missed:

| # | What was done | Result |
|---|---|---|
| 1 | matched against 475 of our own fixed strings | no match |
| 2 | hypothesised "the upstream body is masking the HTTP status", fixed it, shipped | **the fingerprint did not change; the hypothesis was refuted** |
| 3 | machine-matched **18,299** string literals in our source plus **127,533** in libraries | no match |

**All three were "guess the location from the wording."** The location is in the stack.

> **A function name alone contains no path, no arguments and no customer data.**
> When you cannot store content, keep **frame names, not messages.**

```ts
/^\s*at\s+(?:async\s+)?([A-Za-z0-9_$.<>]{1,60})\s*\(/   // function names only, at most 4
```

Generalised: **when a guess misses twice, change the kind of clue.** Going for a third attempt
with the same kind of evidence is worse than going after a different kind.
