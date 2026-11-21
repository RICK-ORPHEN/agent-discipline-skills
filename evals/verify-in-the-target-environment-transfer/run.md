# How to re-run this eval

Same procedure as `../verify-in-the-target-environment-n15/run.md`, on a fixture the skill does
not name. Read `PRE-REGISTERED.md` first: the primary here is `discriminates`, not check 1.

0. **Verify the scorer**: `python3 calibration/check.py`. Nine hand-written cases, three of
   which pass check 1 without doing the work. It must exit 0 before any agent runs.
1. Seed one run directory per run from `fixture/`: `README.md`, `job.py`, `lookup.py`,
   `printers.dev.json`, `printers.prod.json`. 15 per arm.
2. Give the agent `PROMPT.md` with `<RUNDIR>` replaced.
   - **control**: the prompt alone.
   - **treatment**: preceded by "Read this skill file in full and follow it:" and the path of a
     copy of `skills/verify-in-the-target-environment/SKILL.md` placed **outside** the run tree.
3. `python3 score.py <run dir>` per run.

## Conditions to write down when you run it

The round-2 `run.md` did not say which model, which harness or which permission settings, and
the first outside re-run of it fell into every one of those gaps. Record these with your
numbers:

- **Model and date.** An alias such as "sonnet" names a different model every few months.
- **What the agent is.** A bare API loop, a coding agent, a sub-agent inside a chat session.
  The last one inherits a system prompt and tools the first does not.
- **Permission mode.** If the harness asks a human before running a command and nobody is
  there, the agent waits, gives up and leaves `job.py` untouched — and that run scores as a
  failure of the arm it happens to be in. Either run with nobody needed, or count those runs
  and report them.
- **Whether the harness guards credential-like files.** This fixture avoids file names such as
  `creds.*.json` for that reason. The round-2 fixture does not, and in one harness six of
  thirty agents never managed to read them.
- **Where the run directories were** and what else an agent could reach from there.

## Keeping the scorer out of reach

Keep `score.py`, `calibration/` and `PRE-REGISTERED.md` outside anything an agent can reach.
If agents share a machine with the scorer and run with the same privileges, a directory they
are not told about is not out of reach — remove the files, or encrypt them, while agents run.
Two of the variants this scorer tests exist only inside `score.py`; an agent that reads it can
pass them by construction.
