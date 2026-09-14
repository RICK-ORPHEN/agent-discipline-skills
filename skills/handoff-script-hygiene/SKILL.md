---
name: handoff-script-hygiene
license: Apache-2.0
allowed-tools: Read, Grep, Glob, Bash
description: "The discipline for writing a script someone else will run, and for the moment you are about to ask them to run it again. A ledger of 19 incidents from making one person redo the same work five times, plus the checks that kill each one mechanically. Use when: you are about to borrow someone's hands. Do NOT use when: you can finish it yourself."
---

# Hygiene for tools you hand to a human — a record of saying "run it again" five times

> "You are making too many mistakes. Record all of it and turn it into a skill." — the owner

Over one evening and the following morning, **the same single push required five runs of a
handed-over script, and the diagnostic script was run three more times** (two more followed).
Not one was technically hard. Every one could have been caught before handing it over. The
whole thing is in the ledger below, and the prevention is written as procedure.

## 0. The 60-second check before handing anything over

```
[ ] **default to `#!/bin/bash`.** Use zsh only when something actually needs it. Half the
    rules in this list exist because of zsh's differences, and you can only check a shell
    you can run — `bash -n` exists nearly everywhere, `zsh -n` does not
[ ] chmod +x run **after the last edit** (sed -i and file writes drop the bit)
[ ] shebang and syntax agree: #!/bin/bash → `bash -n`; #!/bin/zsh → `zsh -n`
[ ] zsh only: (N) on globs; no command lines stored in "$VAR" (use a function or ${=VAR})
[ ] --no-pager on git output commands (log / show / diff / branch)
[ ] stdin provided for anything that prompts (rm confirmation, login, read)
[ ] stderr of fallible external commands is shown on screen (not >/dev/null 2>&1)
[ ] a fallback route for network failure (ssh 22 → ssh.<host>:443)
[ ] ALL the checks CI runs were run locally (not one rule in isolation)
[ ] one line written afterwards saying what "success" looks like on screen
```

## 1. The incident ledger — 19 entries, in order

| # | What happened | The real cause | The rule from now on |
|---|---|---|---|
| 1 | the script stopped on a `:` screen during `git show` | a pager (less) opened | always `git --no-pager` for output commands |
| 2 | "cannot be executed because you do not have the right permission" | `sed -i` had dropped the +x bit | run `chmod +x` **after the last edit**. Check `-rwx` with `ls -l` right before handing over |
| 3 | died on line 1 with `no matches found: ~/<dir>/bin` | zsh exits on a non-matching glob | add `(N)` to globs in zsh, or `setopt +o nomatch` |
| 4 | `command not found: npx -y <pkg>@latest` | zsh does not word-split `$SB` (written with bash habits) | keep command lines in a function — `sb() { npx -y <pkg>@latest "$@"; }` — or `${=SB}` |
| 5 | misdiagnosed as "cannot even write a test key → permission or login problem" | the probe's stderr was thrown away with `>/dev/null 2>&1`. It was really a 415 `invalid_mime_type` | always show stderr of commands that can fail. Do not classify the cause yourself (permission / login / MIME) — print the error text as-is |
| 6 | the probe failed with 415 | the CLI's auto-detect sent `text/plain; charset=utf-8`, which was not in the bucket's exact-match `allowed_mime_types` | give the probe the same `--content-type` as production. Read the bucket's allowed MIME list from the management API first |
| 7 | `storage rm` stopped on a Yes/No prompt | the CLI added a confirmation in a newer version | pipe stdin: `printf 'y\n' \|`. Do not use `< /dev/null` |
| 8 | CI drift check red (1st time) | a public skill's body contained a path that is not part of the distribution | do not write **paths to directories that are not shipped** in a public skill body. Reference by basename |
| 9 | CI drift check red (2nd time) | a heading contained `scripts/routing-policy.yaml`, read as a relative path reference → "a file that is not carried" | do not write a nonexistent relative path in the body. If you write it, actually ship it |
| 10 | hit red twice in two separate rounds | called it green after running only `--rule X`. CI runs all rules plus six sub-checks | run **the whole CI drift check** (all rules + sub-checks) before pushing. If it is slow, run it under nohup and wait |
| 11 | push over ssh port 22 failed | network (VPN / Wi-Fi switch) | include `\|\| git push ssh://git@ssh.<host>:443/...` from the start |
| 12 | asked three times for the same push | could not close #8–#10 in one round | for each re-run you ask for, **pass every gate locally first** |
| 13 | wasted time failing to open a script through background file-manager control | a background double-click triggers rename, not open. Opening needs display-scope control | write it expecting a human to run it. If you will open it via computer control, take display-scope permission from the start |
| 14 | restored a copy of a page that another source of truth had deliberately redirected away | read only one of the two canonical documents, and missed the other's intent | when two canonical sources point opposite ways, **follow neither — ask the owner** |
| 15 | this very ledger skill went red in CI | the local drift check scans **only git-tracked files**. A new file not yet in the index is out of scope, so it looks green locally | add new files to the index (a temporary index is fine) before checking. Do not write a "python3 + relative path" command in a body |
| 16 | a handed-over `git checkout -b` stopped with "Your local changes would be overwritten" | the previous PR had been committed **through a temporary index**, so the same content remained uncommitted in the working tree. HEAD and the working tree disagreed and `git status` was never checked before handing over | after committing through a temporary index, assume **the working tree is still dirty**. Never make a handed-over script do checkout / add / commit — **make the commit yourself and hand over only the push**. Always look at `git status -sb` first |
| 17 | a merge left the working tree behind, so `git diff` showed a **reverting** diff ("deleted", "15 → 14 files") | with `git merge` unavailable in the sandbox, the tree was assembled in a temporary index and `update-ref`'d. That creates HEAD and a commit but **does not write one byte of the working tree.** The published procedure follows the same step with a `git checkout` to bring the tree along and then verifies — and that route was bypassed by merging by hand | after merging through a temporary index, **always bring the working tree along and verify.** Do not bypass the published route. Run a checker that compares the working tree against HEAD after committing (it stops on a revert) |
| 18 | `update-index --add` straight after `read-tree HEAD` picked up **the blob from HEAD**, not the working tree, and committed it | a commit was created with stale content. `write-tree` succeeds and the filenames line up as expected, so **nothing looks wrong** | after `write-tree`, compare `git rev-parse <tree>:<path>` with `git hash-object <path>`. If they differ, use `hash-object -w` + `update-index --cacheinfo` to pin the hash |
| 19 | `update-ref` failed with `cannot lock ref` three times in a row, so the second commit's **parent stayed at the previous one** and the history forked | the sandbox cannot unlink under `.git`, so every ref operation leaves a `.lock` residue that the next one hits | sweep stale locks **immediately before every ref-moving operation.** When stacking commits, confirm the parent with `git log --oneline -1` after each one |

## 2. The rules, extracted

### 2.1 Writing

- Shebang `#!/bin/zsh`. **Do not bring bash habits** (word splitting, ignoring non-matching globs)
- Keep command lines in functions. `for d in ...(N)`. With `set -e`, keep `|| true` as narrow as possible
- `git --no-pager`. Kill prompts with `printf 'y\n' |`. Show stderr
- Assume port 22 is blocked and write the 443 fallback

### 2.2 Before handing over

- `chmod +x` → `ls -l` → `zsh -n`, **immediately before handing over**
- Look at `git status -sb`. If the working tree is dirty, do not make the script do checkout /
  add / commit — make the commit yourself and hand over only the push
- Run every gate CI runs. Do not call it green from one rule
- Measure an external tool's contract (MIME, overwrite semantics, prompts) **on something
  disposable**, and read the stderr

### 2.3 When you hand it over

- Three lines: what it will do, what appears on screen on success, what to paste back on failure
- When you hand over the same tool a second time, say in one line **what is different from
  last time**

## 3. Related

- *tool-contract-first* (read the contract; do not judge by a proxy)
- *verify-in-the-target-environment* (passing here is not passing there)
- *sandbox boundaries* (paths differ)
- *design before fix*
