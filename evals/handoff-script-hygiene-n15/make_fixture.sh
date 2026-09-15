#!/bin/bash
# A repo with two commits that have never reached the server, on an ssh remote.
# usage: bash make_fixture.sh <dir>
set -eu
d="${1:?usage: make_fixture.sh <dir>}"; rm -rf "$d"; mkdir -p "$d"; d="$(cd "$d" && pwd)"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
git init -q -b main "$d/repo"
cd "$d/repo"
git -c user.email=a@b -c user.name=a commit -q --allow-empty -m "initial"
git remote add origin git@git.acme.dev:notes/notes.git
git update-ref refs/remotes/origin/main HEAD
git config branch.main.remote origin
git config branch.main.merge refs/heads/main
printf 'grocery list\n' > notes.md; git add notes.md
git -c user.email=a@b -c user.name=a commit -q -m "add notes"
printf 'grocery list\nmilk\n' > notes.md; git add notes.md
git -c user.email=a@b -c user.name=a commit -q -m "add milk"
rm -f "$d"/repo/.git/*.lock 2>/dev/null || true
