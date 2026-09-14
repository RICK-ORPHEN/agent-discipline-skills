---
name: sandbox-boundary
license: Apache-2.0
allowed-tools: Read, Grep, Glob, Bash
description: "Your execution sandbox and the user's machine are two different filesystems, and the same file has a different absolute path in each. Catch, mechanically, everything that breaks when an operation crosses that boundary — including when you add a new working directory. Use when: paths or file locations might disagree between environments. Do NOT use when: the question is how to test in their environment, or how to write the script you hand over."
---

# sandbox-boundary — working across two filesystems

## 0. Why this exists — the damage

`git worktree add` was run from the sandbox. Git bakes **the absolute path it can see at that
moment** into two files.

```
<worktree>/.git
  → gitdir: /sessions/<session>/mnt/<folder>/<repo>/.git/worktrees/…

<repo>/.git/worktrees/<worktree>/gitdir
  → /sessions/<session>/mnt/<folder>/<worktree>/.git
```

`/sessions/...` **does not exist on the user's machine.** Running git there gives:

```
fatal: not a git repository: /sessions/…/worktrees/<worktree>
```

Eight commits and 63 files were stacked there, every check went green, and the report said
**"the code side is entirely done."** In reality it sat in a place from which not one command
worked on the user's machine.

The real damage came after. The inability to push was misdiagnosed as "no SSH key", the
clipboard was rewritten four times, and several round trips passed before anyone noticed the
terminal had no window open. **The cause was a worktree created by me, from the very start,
and I kept suspecting the environment instead of my own output.**

---

## 1. Absolute rules

### R1 — Never `git worktree add` from the sandbox

Branch inside the existing working tree instead. If you genuinely need a worktree, fix the
paths per §2 and **pass the check in §3 before doing anything else.**

The same applies to `git clone`, `git submodule`, absolute paths in `ln -s`, handed-over
scripts, and paths inside `*.json` configuration.

### R2 — Write paths in the shape of the machine that will use them

| Purpose | Path to write |
|---|---|
| Something a human runs (commands, scripts, config) | a path under `$HOME` |
| Something entirely inside the sandbox | the sandbox absolute path |
| Something used from both | **a relative path** — but read §2 first |

### R3 — Never write a command into chat in a form that cannot be run

An abbreviated `cd <path to>/<worktree>` written for explanation gets pasted verbatim. That happened
(`cd: no such file or directory`).

**Every command you put in chat must be runnable exactly as written.**
If you want to abbreviate, do not write it as a command — describe it in prose.

### R4 — Before handing over a command, confirm its preconditions hold

Check all of these immediately before. If even one is unconfirmed, do not hand it over.

- [ ] does that directory exist **at the user's path**
- [ ] is it recognised as a git repository **from their machine** (the §3 check)
- [ ] are the required config files (`.env.local` and friends) actually there
- [ ] **does the terminal have a window open** (confirm by screenshot — an app can be running
      with zero windows, and then there is nowhere to paste)

### R5 — Before saying "it cannot be done", suspect your own output first

Before suspecting the environment (no key, no permission, wrong architecture), check whether
**the thing you just created** is broken. That is where the cause was.

---

## 2. Fixing a worktree's paths

For one you already created, or one you find that the user's machine cannot use.

```bash
W=<the worktree's sandbox path>
A=<parent repo>/.git/worktrees/<worktree name>

# .git becomes relative → resolvable from both machines
#   (requires the parent directory layout to be identical in both)
#   Compute it instead of hand-writing it, so it is correct wherever the worktree sits
REL=$(python3 -c 'import os,sys;print(os.path.relpath(sys.argv[1],sys.argv[2]))' "$A" "$W")
echo "gitdir: $REL" > "$W/.git"

# gitdir becomes the absolute path of the machine that actually uses it
#   Making it relative causes `git worktree list` to mark it prunable, and prune deletes it
echo "$HOME/<path to>/<worktree name>/.git" > "$A/gitdir"
```

⚠ **Never make `gitdir` relative.** Measured: it becomes `prunable`, and a
`git worktree prune` removes the worktree's bookkeeping entirely.

⚠ With this configuration, **the sandbox will report the worktree as prunable.** That is
normal. Never run `git worktree prune` from the sandbox.

### When you cannot make it relative — switch temporarily, and always switch back

Sometimes `.git` points at **the user's absolute path**: fine from their machine, but every git
operation fails in the sandbox. Making it relative works for both, but **when you do not want
to risk breaking the side they use**, flip it to the sandbox form for the duration of the work
and **always flip it back before handing over.**

```bash
# 0. preserve (secure the way back first)
cp "$W/.git"    /tmp/dotgit.host.bak
cp "$A/gitdir"  /tmp/gitdir.host.bak

# 1. switch to the sandbox form
printf 'gitdir: %s\n' "$A" > "$W/.git"
printf '%s\n' "$W/.git"    > "$A/gitdir"

# …work, up to the commit…

# 2. always switch back
cp /tmp/dotgit.host.bak "$W/.git"
cp /tmp/gitdir.host.bak "$A/gitdir"
```

**Confirm the restore by measurement** (handing over on "I think I restored it" means they hit it):

```bash
cat "$W/.git"                       # must start with $HOME
(cd "$W" && git status 2>&1 | head -1)
# → "fatal: not a git repository ..." is the correct result here.
#   Losing sandbox access is the evidence that the host form is back.
```

⚠ On a mounted filesystem you often **cannot unlink files**, so preserve with `mv`.
Overwriting with `cp` works. Move `*.lock` and `tmp_obj_*` aside before and after
(a commit leaves many; git ignores them, but a leftover lock stalls the next operation).

### ⚠ Your local `origin/main` goes stale on every merge — fix it yourself, do not ask

**Confirm `origin/main` is current every time** before `git checkout -b <new> origin/main`.
The sandbox cannot fetch, so **the moment your PR is merged, your local copy is stale.**
Branching from a stale base means **already-merged diffs are re-shown in your PR.**

This led to asking a human to `git fetch` **three times in one day**, and to being told the
asking itself was a waste. **Asking was the design error.**

**The permanent fix: a script that does fetch and push only**, which the agent can launch
itself through the file manager.

Principles when you write it:

- **Do not include add or commit.** Commits can be made from the sandbox. If it is not in the
  script, a `git add -A` accident is structurally impossible
- **Explicitly refuse pushes to the protected branch**
- **Never write `--force` or `reset --hard`**
- **Tee the output to a log** (once the window closes, the screen is unreadable)
- **Move a leftover `index.lock` aside rather than deleting it**, and do not touch it while a
  git process is running

⚠ **Strip comment lines when you check for these.** A grep once matched **the sentence
explaining "never write `git add -A`"** and reported a false positive.

**If the same round trip happens twice in another repository, build the same script without
waiting for a third time.**

---

## 3. The check

```bash
python3 scripts/check_worktree_paths.py <path to the worktree>
```

- reads the contents of `.git` and `gitdir` and decides **whether the host can resolve them**
- **exit 1** if a sandbox absolute path is baked in
- detects absolute symlink targets the same way

**Run it right after creating a worktree, and before handing any command to a human.**

---

## 4. Choosing a push route

Decide in this order. **Try from the top and stop at the first that works.**

### 4-1. An HTTP API route that needs no human

If you have an API credential for the forge, check the repository's permissions first, and use
it for pull requests, branch checks, CI status and small file operations.

⚠ **Do not use it to push many files.** Carrying blobs through tool arguments corrupts them
(measured: a 51 KB TypeScript file was mangled from line 549 onwards).
Rule of thumb: **up to 5 files and 50 KB total** via the API; beyond that, 4-2.

### 4-2. `git push` on the user's machine

There is no SSH key in the sandbox. **That is an environment constraint you cannot fix.**
Hand over one line — after passing **every item in R4**, especially the worktree paths and
whether a terminal window exists.

### 4-3. You can still *look* at the terminal

Screen control can usually read a terminal's state even when it cannot type into it, and
menus can be driven by clicking (open a window via Shell → New Window if there is none).

Injecting keystrokes is blocked structurally. Do not work around it. What you can do is
**identify what is stuck and get it to a state where one paste finishes the job.**

---

## 5. Things that only run on real hardware — settle this first

A sandbox is often a different CPU architecture from the user's machine.

| Check | Runs in the sandbox? | Reason |
|---|---|---|
| browser-based quality checks | ❌ | the browser downloads an x86-64 build → `Exec format error`; no arm64 package, no root |
| runtime smoke tests needing that browser | ❌ | same |
| authenticated end-to-end matrices | ❌ | needs an environment variable pointing at a real tenant |
| generation steps needing a provider key | ❌ | but a hand-written supplement file is usually provided for sessions that cannot run it |
| everything else (type check, lint, unit) | ✅ | |

**Before reporting "this only runs on the real machine", actually try it** unless the reason is
already in this table. The browser case was settled by *trying it and finding an x86-64
binary.* Do not assert it from a guess.

---

## 6. Never

- `git worktree add` / `clone` / `submodule add` from the sandbox
- make the `gitdir` file a relative path
- `git worktree prune` in the sandbox
- write an abbreviated path as a command in chat
- hand a command to a human without confirming the preconditions
- push 63 files one at a time through an API
- suspect the environment before suspecting your own output
