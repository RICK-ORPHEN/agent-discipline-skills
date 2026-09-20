---
name: verify-in-the-target-environment
license: Apache-2.0
allowed-tools: Read, Grep, Glob, Bash
description: "The discipline of actually running a tool, or a checker you are about to wire into a gate, IN THE ENVIRONMENT THAT WILL RECEIVE IT, before you hand it over. Passing on your machine is not proof that it passes on theirs. Use when: you want to confirm against production-equivalent before distributing, or you are about to gate on a checker that has never succeeded. Do NOT use when: the question is how to write the script, or how to read a tool's contract."
---

# Verify it in the environment that will receive it

> "You are making a different mistake again." — the owner
> (after the same tool was handed over three times and failed in their environment three times)

## When to use

- Handing over **a script or a procedure a human will run**
- **Wiring a checker into a build, CI, or a release gate**
- Writing code that resolves **aliases, credentials, or login state**
- Whenever you think "it passed on my machine, so it is fine" ← this is the real trigger

---

## 1. First write, in one line, whose environment and which credentials it runs on

If you cannot write it, you may not hand it over yet.

```
This tool runs   on the user's machine / under the CLI's own login
This check runs  on the user's machine / under the <provider> credential
In my environment I can execute up to ___. ___ only works on the real device
```

⚠ **If even one part is something you cannot execute, say so when you hand it over.**
`bash -n` and `test -x` check **syntax, not behaviour.**

---

## 2. For any lookup whose answer depends on the environment, plan for 0 / 1 / many

You have seen **one of the three.**

| Lookup | 0 | 1 | many |
|---|---|---|---|
| alias resolution | stop with "none" | passes | **stop with "several, cannot choose"** ← easily missed |
| login state | not logged in | logged in | several accounts mixed |
| a command on PATH | absent | present | several versions |
| a config file | absent | present | conflicting copies in a hierarchy |

### A real case

`resolve_alias("supabase")` returned **0 in my sandbox and 2 on the user's machine.**
Only the zero branch had ever been exercised; the "several, cannot choose" branch had never
been seen.

⚠ **Some branches you can never reach in your own environment.**
So be aware that a branch went unexercised, and **write that down when you hand it over.**

---

## 3. Do not pick a provider or route by its name. Diagnose and look

**Similar names do not mean the same route.**

```
provider `supabase`             → REST API        (https://<ref>.supabase.co/rest/v1)
provider `supabase_management`  → Management API  (https://api.supabase.com)
```

Look at three things:

| | What to look at |
|---|---|
| the effective base URL | **does the method you want exist on that host** |
| the test endpoint | does its shape match how you intend to call it |
| executable / blockers | **is it in a state where it can run at all** |

### A real case

A checker resolved `resolve_alias("supabase")` and called
`v1/projects/{ref}/database/query` — a **management API** path. Both matching entries were
**REST routes**, and both were **`executable: false`** (no project URL configured).
**The combination could never have worked.**

---

## 4. Print which value you chose

If the choice varies by environment, **the result alone does not tell you what was looked at.**

```python
print(f"  alias used to read the bucket: {alias}", file=sys.stderr)
```

⚠ Without this, all you get back from a human is "it failed", and you start guessing again.
**Print the chosen value every time.**

---

## 4.5 When a resolver fails, read the implementation. The message is a symptom, not the mechanism

⚠ **This cost four rounds.** Each time only the error message was read, and the next guess was
stacked on it. **Reading the implementation once explained everything.**

### Contradictory messages are the shortest clue

```
resolve_alias("supabase")             → "several, cannot choose: A, B"   ← 2 are visible
resolve_alias("supabase_management")  → "visible providers: (none)"      ← 0?
```

**The moment the same function said two different things, the implementation should have been
read.** It took three lines:

1. this environment's alias list **has no provider column**
2. so `resolve_alias` **falls back to matching the alias name as a string**
3. with multiple candidates, it narrows to **only those ending in `.main`**

→ the management alias does not end in `.main`, so it **always fails.** It can **never** be
resolved from a provider name. No amount of re-reading the message would show that.

### How to do it

- When a resolver (`resolve_*` / `find_*` / `detect_*`) fails, **read the function body first**
- Read the **fallback clause** especially. "What it does when it cannot find one" is what
  actually decides the behaviour
- ⚠ Check whether a **default value** is silently narrowing the candidates
- Then use **the explicit path the design provides** (env var, config file, canonical yaml).
  Do not try other names by guesswork

---

## 5. Before wiring it into a gate, ask whether it has ever succeeded

**A checker that has never gone green is the same as not having one.**
Worse, in fact: it shows "unverified", so **it looks like it is there.**

Before wiring:

```
□ has this check ever returned exit 0
□ if not, can you name the environment in which it would
□ if it is designed to pass through as "unverified (exit 2)", will that become the steady state
```

### A real case

A sync checker was written on the 31st and wired into the build gate on the 2nd. For the
reason in §3 it **could not succeed in any environment.**
**The gate built to prevent that day's incident — 13 of 17 distributed files returning 404 —
could never detect that incident.**

---

## 6. Before handing over, exercise every branch you can reach

If you cannot hit the real thing from your environment, **substitute only the reader** and run
the decision logic.

```python
module.reader = lambda cfg: (known_data, "")     # healthy
module.reader = lambda cfg: (missing_data, "")   # missing
module.reader = lambda cfg: (None, "reason")     # unreadable
```

**Actually run all three and look at the output.**

---

## 7. ⚠ Writing "unverified" does not save the human from stepping on it

**This skill's §6 used to end at "declare it unverified and hand it over." That was not enough.**

The declaration was made. The handover note clearly said "⚠ never executed: writing via
`storage cp`." **The human still had to press it four times.**

| # | Why it failed | Knowable in advance? |
|---|---|---|
| 1 | an `--experimental` flag was required | it is in `--help` |
| 2 | `ss:///bucket` matches by prefix and exits 0 | one real call shows it |
| 3 | the alias could not be resolved | reading the implementation shows it |
| 4 | `grep -c` exits 1 when the count is zero | it is in `--help` |
| 5 | a function `etag_of` did not exist | running it once shows it |
| 6 | **`storage cp` has no overwrite flag (409)** | **it is in `--help`** |

**A declaration is not absolution.** To the person pressing the button, "it said unverified"
and "it said nothing" feel identical.

### If you cannot execute it, make the tool measure for itself

Before touching anything real, put a stage inside the tool that performs the same operation
**on something disposable.**

```bash
# Confirm the contract with a throwaway key before touching one real byte
PROBE=".probe-$$"
put "$PROBE" || stop "cannot even write a test key. **Nothing real was touched**"
if put "$PROBE"; then           # second time = can we overwrite
  OVERWRITE_OK=1
else                            # 409 → switch to delete-then-write
  del "$PROBE" || stop "can neither overwrite nor delete. **Nothing real was touched**"
  put "$PROBE" || stop "cannot write even after deleting. **Nothing real was touched**"
fi
del "$PROBE"
```

Now **the real answer appears on the spot** even if the CLI version changes, or it is a
different tenant. If you miss something in `--help`, the tool notices for you.

### Design irreversible operations to include getting back

- **Preserve first.** Judge preservation by **the content being there**, not by an exit code
- If preservation fails, do **not** proceed with a single item
- If the write fails after a delete, **restore from the preserved copy immediately.** Do not
  leave it
- On failure, do not try the rest (**keep the damage to one item**)

### Run these three before handing over

Even with no credentials in your environment, **a fake CLI on PATH reaches every branch**:

```bash
scenario overwrite_ok       # overwriting works
scenario overwrite_blocked  # 409 → delete then write
scenario rm_fails           # cannot delete → stop without touching anything real
scenario cp_fails_after_rm  # cannot write after deleting → restore from the preserved copy
```

⚠ **First confirm the fake really does return failures.** An argument in the wrong position
once sent every case down the same branch — *a test that cannot fail is a lie.*

⚠ **Do not transcribe the decision logic.** Extract the executable lines out of the script you
are handing over (with `sed`) and run those. Transcribing creates a second reader, and one of
them will go stale.

---

## The one-line check

Before handing over:

> **Whose environment does this run in? Did I run it there?**
> **If I cannot, does the tool itself have a stage that tries it on something disposable?**
> **For irreversible operations, did I write preserve → measure → restore-on-failure?**

---

## Related

- *my machine has more than production*
- *the check that cannot run here* — do not write a check that cannot succeed in this environment
- *excluded is not fixed*
- *a test that cannot fail is a lie*
- *tool-contract-first*
- *sandbox boundaries*
