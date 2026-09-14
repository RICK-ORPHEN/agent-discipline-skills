---
name: tool-contract-first
license: Apache-2.0
allowed-tools: Read, Grep, Glob, Bash
description: "Read the tool's contract before you use it, and again before you attempt a second fix for the same bug. Never judge by a proxy signal — exit codes, headers, counts — without first calibrating it against known-correct cases. Use when: a tool behaves differently from what you assumed. Do NOT use when: what you actually need is to re-read the product design."
---

# Read the tool's contract before you fix

> "This is what happens when you patch things on the fly. Analyse it properly, then fix and
> design." — the requester

## When to use

- Whenever you call an external tool (CLI / API / browser / git / SDK) **for the first time**
- **Before a second fix for the same bug** ← this is the real trigger
- Whenever you catch yourself thinking "it is probably this flag" / "probably this header"
- When you are writing a script a human will run

---

## 1. Before the second fix, stop adding conditions

**If the first fix missed, you did not guess wrong — you did not read the tool.**
The second attempt is not "add one more condition." It restarts at **reading the contract.**

Three things to read:

| | What to read |
|---|---|
| The tool itself | `--help`, **end to end.** Do not skip EXAMPLES or ARGUMENTS |
| Existing call sites | Is **somebody already calling this tool?** If so, their shape is the answer |
| The canonical config | Bucket names, project refs, URLs — **do not decide them yourself.** The config file is authoritative |

### A real record — the same trap three times in one day

- A storage `ls` failed. `2>/dev/null` had thrown the reason away, so all that could be
  reported was "cannot read it"
- Adding an `--experimental` flag then made `ss:///bucket` return **the bucket itself as one
  entry, by prefix match.** The help said "List objects by **path prefix**." **It had not
  been read**
- Only on the third attempt did the real answer appear: **a function that reads the bucket
  already existed** (`bucket_listing()` / `etag_of()` / `delivery_config()` in an existing
  sync checker). The same thing had been rewritten three times

---

## 2. Do not judge by a proxy signal

**Exit codes, headers, counts and etags are not the thing you are trying to decide.**
If you use a proxy, **calibrate it first against known-correct cases.**

### Proxies used, and how each betrayed us

| Proxy used | What it was meant to decide | What happened |
|---|---|---|
| `Accept: text/html` | did a human click it | `<a download>` sends no Accept header. **It never fired on the real button** |
| exit code 0 | was the listing readable | **exit 0 even with the wrong path form.** A "try two forms" branch stopped at the first |
| `etag == md5` | is the content identical | S3 returns `md5(md5(body))+"-1"`. All three files mismatched; a false alarm nearly shipped |
| count 0 | is the bucket empty | indistinguishable from **could not read it.** Fail-closed breaks |
| exit of `grep -c` | could we count the lines | **prints "0" and exits 1 when there are none.** Combined with `\|\| echo 0` it becomes `"0\n0"` and every later comparison breaks |

### The shell contracts that catch people most

```bash
N=$(grep -c . "$f" || echo 0)            # ❌ becomes "0\n0" when empty
N=$(awk 'NF{n++} END{print n+0}' "$f")   # ✅ does not depend on the exit code
```

⚠ **Before writing `|| echo <default>`, check whether that command "prints a value and still
fails."** `grep`, `diff` and `cmp` all return non-zero for "no difference / no match."

### How to do it

```
1. Write in one line what you actually want to decide
2. Write in one line the signal you are about to use
3. **Confirm on two or three known-correct cases that the proxy agrees with the real thing**
4. If it does not agree, throw the proxy away. Do not patch the expression — change evidence
```

⚠ **If everything matches, or nothing matches, suspect the ruler first.**

---

## 3. Do not create a second reader

**When two pieces of code read the same thing, one of them will go stale.**

- Look for an existing reader (`grep` for the subject, the bucket name, the table name)
- If one exists, **import it.** If not, create exactly one and have everyone use it
- Write a new script as a **thin driver**, not a reader. Let the existing checker read and
  decide; add only the execution

⚠ The existing reader is usually **more careful than yours.** In this case it was the existing
one that had distinguished "could not read" from "zero rows" from the start.

---

## 4. Do not swallow errors

```bash
OUT=$(tool ... 2>&1); RC=$?          # ✅ keep it and print it on failure
tool ... >/dev/null 2>&1             # ❌ the reason is gone → guessing begins
```

⚠ **The moment the reason disappears, every fix becomes a shot in the dark.**
Throwing away the reason on the first failure cost the requester two extra round trips.

Exception: a probe where only success matters (`--version`) **and you can state the reason in
your own words.**

---

## 5. Run it yourself before handing it to a human

`bash -n` and `test -x` check **syntax, not behaviour.**

**Exercise the decision logic against three known states:**

| State | Expected |
|---|---|
| healthy (everything present) | "nothing to do" |
| missing (one or two) | **only those names** are listed |
| unreadable (no credentials) | **stops with "unverified", not with "0"** |

When the reader only exists in production, **substitute the reader** and still exercise the
decision logic (`module.reader = lambda: known_data`). All three states are still reachable.

⚠ If some part genuinely cannot be exercised, **say "this part is unverified" when you hand
it over.**

---

## 6. Do not hardcode configuration

Do not write bucket names, project refs, URLs or file lists into a script.
**Read them from the canonical source** (yaml / json / manifest). Hardcoded values go stale
silently the moment the canonical source moves.

Check: `grep -c '<bucket>\|<ref>' script` must be **0**.

---

## The one-line check

Before you hand it over:

> **Is this decision looking at the thing itself, or at a proxy?**
> **If it is a proxy, did you calibrate it against known-correct cases?**
> **Is this reader the same as the one that already exists?**

Until you can answer all three, do not start fixing.

---

## Related

- *verify the comparison before comparing* — calibrate the matcher first
- *a click that sends no request* — you thought you pressed it; no request left the machine
- *failure must change state* — a failure that changes no state cannot be noticed
- *do not hand-maintain the check list*
