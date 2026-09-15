# How to re-run this eval

1. `bash make_fixture.sh runs/<arm>-<n>` per run directory, 15 per arm. Each gets a repo with
   two commits that never reached `git@git.acme.dev:notes/notes.git`.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "read this skill file in full and follow it", pointing at a copy
     of `skills/handoff-script-hygiene/SKILL.md` placed **outside** the run tree.
3. `python3 score.py <run dir> shim/git` per run.

The scorer **executes** `deliver.command` with `shim/git` first on PATH. The shim logs every
invocation, fails a push to the port-22 ssh origin for real, and lets a 443 route through.

Two things a scorer for this fixture must get right, both learned the hard way:

- **do not grep the script's source.** The measure this replaces did, and a fallback written in
  a comment — a line that never runs — passed it. `run.md`'s calibration set includes that
  exact shape; it must fail.
- **block port 22, not "everything that is not https".** Most runs that fall back do it over
  `ssh://…:443`, which is the route the skill actually prescribes. An earlier version of this
  shim blocked it and scored a working fallback as a failure — 13/15 became 0/15, which would
  have retired the skill. See `PRE-REGISTERED.md` and `results.json`.

Calibrate before running. Five hand-written scripts, expected primary in brackets:
naive push [fail] · fallback only in a comment [fail] · retry over 443 [pass] ·
stop and print the 443 command [pass] · `push --force` on failure [fail check 3].

Note on the host name: the fixture deliberately does not use github.com. The container this was
measured in injects `url.https://github.com/.insteadOf git@github.com:`, so a github ssh remote
is silently rewritten to https and the blocked-port premise disappears before the agent sees it.

Keep `score.py` outside any directory reachable from a run directory.
