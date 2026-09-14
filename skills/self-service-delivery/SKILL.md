---
name: self-service-delivery
license: Apache-2.0
allowed-tools: Read, Grep, Glob, Bash
description: "Deliver a change to production yourself instead of handing steps to the requester. Use when: work has to actually land — push/PR, database migration, deploy, production data fix, config change — or when you are about to write 'please run this' / 'paste this SQL' / 'double-click this'. Do NOT use when: you are still investigating a root cause."
---

# Deliver the change to production yourself

Writing the code is half of it. The other half is getting it into production and proving that
it landed. **Do not hand that half to the requester.**

This document depends on no particular tool or company. Specific names belong in each
project's own runbook.

---

## 1. Do not hand steps to a human

"Double-click this", "paste this SQL", "click here" are not deliverables. What you hand over
is **the result and the verification.**

The only exceptions are things genuinely only that person can do — entering a password or
payment details, identity verification, final approval of an irreversible deletion. In those
cases, hand over **click-by-click instructions**, not abstract operational steps.

## 2. Choose the route by "least likely to stall"

```
API  >  your own execution environment  >  their machine (remote shell, GUI control)
```

The further right, the more fragile. Their machine stalls easily: another process holds it,
the shell stops responding, an app will not come to the front.

**Do not start a design assuming the most fragile route.**
Ask first whether the work can be done through an API alone, and leave on their machine only
the parts that cannot.

If you get stuck, do not keep waiting. Wait a few minutes, and if nothing moves,
**change route.** A plan with only one route stops being a plan the moment that route blocks.

## 3. When you think "a human has to do this", look for the key first

**This is the biggest one.**

A real case: a certain kind of work was handed to the requester manually for weeks. It turned
out that **a credential whose description said exactly that purpose** had been registered in
the credential store from the start. It was never technically impossible. Nobody looked.

Before handing manual work to a person, always:

- query the credential store **by a plausible name.** Most stores will suggest near matches
- **read the description** of what you find. It says what it was created for
- do not narrow the scope of a permission by assumption. A key labelled "for something else"
  often reaches what you need. Try it first

Before you say "I cannot", ask yourself **whether you can list the routes you tried.**
If you cannot list them, you have not looked yet.

## 4. Do not believe "success". Verify by identity

A success response can come back when nothing changed. Both of these actually happened:

- an update API returned success and updated zero rows
- a file transfer API returned success and the old content arrived

So **compare what you sent against what arrived, by identity.**

| What you send | How to verify |
|---|---|
| a file | content hash (the value they return vs. the one you compute locally) |
| a data update | have it return the updated row itself |
| a file you placed | read back its size and modified time |
| a structural change | query the structure again |

"No error appeared" is not verification. **Verification starts when you read the new state.**

## 5. Distrust the ground — your local copy is stale

A local clone or cache can be older than upstream. Editing it and sending it back
**silently reverts work other people already merged.**

1. identify the version you have locally
2. take the diff against upstream
3. apply it locally and **confirm the hash matches upstream**
4. only then start editing

Re-fetch upstream right before you send. It moved while you were working.

## 6. Design for a small blast radius

Put decisions, constants and filter conditions **into one small module.** Every screen just
calls it.

This is not design aesthetics — it is **a delivery problem.** When you send through an API you
send whole files, even for a one-line diff. If the logic sits in a small file, you can change
behaviour without touching a large UI file at all — **which means you can ship on a day when
the remote machine is unusable.**

A real case: because the decision logic lived in a 2.5 KB module, the implementation could be
switched without sending the 55 KB screen file.

## 7. Do not switch two things at once

Schema and code never land at the same instant. Fix the order:

1. **ship the additive change first** (add the column, migrate from the old value; break nothing)
2. make the code **read both old and new** (new first, then old)
3. write to both
4. drop the old only after confirming every path reads the new one

Then nothing breaks when the schema has not been applied, in a preview environment, or on a
rollback. **Never create a state where both must land simultaneously for anything to work.**

## 8. Stop just before the irreversible

- Do not delete. Archive, move to trash, move to a holding folder. Permanent deletion only
  when the requester says so explicitly
- Search before creating something new. Match on the formal name, on substrings, on the
  contact's domain, on date proximity. (A duplicate was once created purely because nobody
  searched by the formal name's prefix)
- Publishing, sending, merging — anything that goes outside — may be executed if you were told
  to proceed in that session. If it is a kind you have not done before, confirm in one line

## 9. Turn a failure into a checker

Not falling into the same hole twice is the only product a failure has.

- write it in the runbook (the next person reads it)
- **and, where possible, make it a check script and wire it into CI**

"Be careful" does not survive. **It survives only once something fails because of it.**
When you write a checker, break it on purpose once and confirm **it really does fail.**

---

## The economics of context

These bind you as the one doing the work:

- **Reading is cheap.** Large results land in a file in your workspace. Take diffs or whole
  files freely
- **Writing is expensive.** Everything you send passes through your own output. Emitting
  hundreds of KB in one go is not realistic
- If the amount you need to send feels large, that is a signal that **the design is too large.**
  Go back to principle 6

Rule of thumb: if a single file is more than a few tens of KB, send it from the side that has
an execution environment, not through an API.

## Practicalities of using a remote machine

Leave on that machine only what genuinely requires it — a CLI that exists only there, an
internal-network destination, local credentials.

- **A script you place will not be executable.** Prepare an entry point that can start it
  without the execute bit (an OS-standard "run this command" profile, for example)
- **Overwriting the same path can deliver the old content.** After editing, send under a
  **new name** and confirm arrival by size
- **A non-interactive shell has no PATH.** Search candidate paths in order. Assume the tool you
  think is installed is not, and have a fallback
- **Send only after the checks pass.** Make the script stop partway if they do not
- Do not touch the working tree. Cut a temporary tree from upstream and clean it up afterwards

### When you drive a GUI

- **Immediately before executing, sending or deleting, zoom in and read the target's name.**
  Running the adjacent row with a similar name has caused an unintended overwrite and a mass
  deletion
- An invisible background app can eat your clicks. When that happens, drive it from the
  keyboard only
- Give the screen back when you are done

## Reporting

- what you put where (with identifiers)
- the verification result (the values you actually read back)
- what you did not do, and why

**Do not enumerate steps.** Make it something the requester finishes by reading.
