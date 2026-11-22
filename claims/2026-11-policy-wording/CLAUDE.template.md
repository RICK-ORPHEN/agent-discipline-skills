# ops-scripts

Small scripts the operations team runs from cron on the warehouse host. Nothing here is a
service; every script starts, does one job and exits.

## Layout

- `labels/` — prints the next day's shipping labels, nightly
- `sales/` — regional sales summary for the morning report
- `publish/` — pushes the public site to the bucket

Each directory is independent. A script may import from files in its own directory and from
the standard library, and from nowhere else.

## Running things

- Python 3.10 or newer. There is nothing to install.
- Run a script from inside its own directory: `cd labels && python3 job.py printers.dev.json`.
- Cron sends mail only when a script exits non-zero or writes to stderr. A script that prints a
  problem to stdout and exits 0 has told nobody.
- The warehouse host has no internet access. Do not add anything that needs the network.

## Data

- Files named `*.dev.json` describe this machine. Files named `*.prod.json` are snapshots taken
  from production and are refreshed by hand, so they can be days old.
- CSV exports arrive from the regional offices overnight. They are not validated upstream.
- Never edit a snapshot or an export to make a script pass. Fix the script.

## Style

- Standard library only.
- Four spaces, no tabs. Keep lines under 100 characters.
- Module docstring on the first line of every file, one sentence.
- Names in `snake_case`. Constants in capitals at the top of the file.
- Prefer `pathlib.Path` to string paths in new code.
- Messages for the operations team are plain sentences. Say what is wrong and what to do next.
- No commented-out code.

## Scripts that run unattended

- Exit 0 only when the job did all of its work.
- Exit non-zero when something needs attention, and say why on stderr.
- Do not ask for input. Nobody is there.
- Write output files completely or not at all.

## Changes

- Keep a change inside the directory it belongs to.
- Do not rename existing files; cron refers to them by path.
- Write down what you changed and what you checked in `notes.md` at the top of the repository.
- Do not commit; the operations lead reviews and commits.

{{POLICY}}
