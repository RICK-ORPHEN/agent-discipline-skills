---
name: design-before-fix
license: Apache-2.0
allowed-tools: Read, Grep, Glob
description: "Before fixing a symptom, read end to end how the feature is designed to reach the user, and pin that down. Use when: the change touches product boundaries, credentials, permissions, distribution or billing — or when you are about to conclude 'this cannot work in this environment'. Do NOT use when: you are investigating the root cause of a live symptom; that is a different discipline."
---

# Design Before Fix — read how it is meant to reach the user

## What this discipline is for

Sometimes **the symptom is real, the fix is technically correct, and the change is still
wrong.** That happens when you close the inconsistency in front of you without reading how
the feature was designed to reach the user. Locally it all adds up, so **you cannot catch it
from the inside.**

## When it triggers

If any of these is true, run this procedure before changing a single line.

- The change touches a product boundary — **who may use it, how it is billed, what they receive**
- **Credentials, permissions or connections** to an external service are involved
- You are changing distribution, publication, contracts or entitlements
- **You are about to conclude "this does not work here", "the customer does not have that",
  "this cannot be used"** — the moment just before a flat assertion is the moment you have
  read the design least

## Procedure

### 1. Read until you can write the intended flow in one paragraph

What does the user already have, where are they authenticated, which path executes, whose
credentials are used, what gets billed. **If you cannot write it, you are not yet qualified
to fix it.**

⚠️ Do not assume one file holds the answer. A boundary is implemented across
**entry (routing) → decision (authorization) → resolution (credentials) → execution**, and
**reading only the entry gives you the opposite conclusion.** Above all, check whether the
call is **intercepted onto a different path partway through**. If it is, every inference you
drew from the code before that point is wrong.

### 2. Write down the evidence, quoted

Do not proceed on "it is probably like this." **Quote the actual line that makes the
decision.** Where you cannot quote one, write "not determinable from the code."

### 3. Fill the rest by measurement — config and data are not in the code

A correct design still does nothing **if that row is not in production.** The reverse also
happens: something that looks unimplemented may be switched on in data. Every question left
after reading the code must be closed with a production value.

### 4. Compare the intended flow before and after your change

Check that your change does not **break** the design intent. A symptom disappearing and the
design being honoured are two different things.

### 5. If the answer is "no change needed", report that as the result

**"I decided not to fix it" is a legitimate conclusion.** Judge by whether it fits the
design, not by how much you typed.

## Fouls

- ❌ symptom → search for an existing rule → match → fix, in one straight line.
  **You never checked whether that rule applies to the current design**
- ❌ applying outside common sense because "this is how it is usually done."
  **The product's own design is the authority**
- ❌ inferring meaning from the shape of a name (a `global.` prefix must mean personal, and
  so on). **Names do not tell you the design. Read where it is resolved**
- ❌ arguing when someone says "it is supposed to be designed that way" without checking.
  Agreeing without checking is the same foul

## A real incident

A fixed identifier was found written into a customer-facing skill. It **matched an existing
rule** — "names differ per environment, so resolve them at runtime" — so the identifier was
replaced with a placeholder across several skills, and a "please connect your provider"
message was added.

**The design was the opposite.** That identifier was a fixed platform-side name, and
execution ran on the operator's supply credentials. Users did not need an account with that
service at all, and the platform **was already showing them that name.** The hardcoded value
was correct, and the change had turned something that worked into something that did not.

The shape of the miss:

- the call was **intercepted onto another path before the decision point**, and that branch
  was never read
- an assumption — "users do not hold their own key" — **was treated as a premise**
- matching an existing rule had become the reason not to read the design

Only on re-reading did **a different, genuine gap** surface: some providers really were not in
the supply pool, and those alone needed the user's own credentials. **Reading the design
changes what you should fix.**
