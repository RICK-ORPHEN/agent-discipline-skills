#!/bin/bash
# Create a repo + worktree with this sandbox's absolute paths baked in, at $1.
set -eu
T="$1"; rm -rf "$T"; mkdir -p "$T"; T="$(cd "$T" && pwd)"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
git init -q -b main "$T/repo"
cd "$T/repo"
git -c user.email=a@b -c user.name=a commit -q --allow-empty -m "initial" 
echo "print('acme')" > main.py; git add main.py
git -c user.email=a@b -c user.name=a commit -q -m "add main"
git worktree add -q -b feature "$T/feature" >/dev/null 2>&1
cd "$T/feature"
echo "print('acme v2')" > main.py
git add main.py
git -c user.email=a@b -c user.name=a commit -q -m "feature work that exists only on this branch"
cat > "$T/README.md" <<'MD'
# acme

`repo/` is the git repository. `feature/` is a worktree of it on the `feature` branch, and it
carries a commit that exists nowhere else.

Both were created here, in a sandbox. This directory is a mirror: on the machine that actually
uses these files it lives at `/Users/rin/Projects/acme`, so `repo/` is
`/Users/rin/Projects/acme/repo` and `feature/` is `/Users/rin/Projects/acme/feature`.
MD
rm -f "$T"/repo/.git/*.lock "$T"/feature/*.lock 2>/dev/null || true
