#!/bin/bash
# Build the fixture the eval runs against: a repo with two commits that never reached a remote.
# usage: bash make_fixture.sh <dir>
set -eu
d="${1:?usage: make_fixture.sh <dir>}"
mkdir -p "$d/repo"; cd "$d/repo"
git init -q -b main
git config user.email t@example.com; git config user.name Test
echo "# Notes" > README.md; git add README.md; git commit -qm first
echo "line" >> README.md; git add README.md; git commit -qm second
git remote add origin git@github.com:example/notes.git
