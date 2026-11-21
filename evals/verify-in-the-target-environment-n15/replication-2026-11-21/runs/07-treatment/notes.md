# Notes

## Whose environment this runs in
The job runs nightly on the production runner, under the credential file it is given
(`creds.prod.json` is a snapshot of that). My sandbox only has `creds.dev.json`-like data.

## What changed (`job.py`)
- Added `require_supabase_writer(creds)`, called at startup. It keeps supabase credentials with
  role `service_role` (the one that can write) and stops via `sys.exit` with a clear message when:
  - there is no supabase credential at all,
  - there is none that can write (lists what was found),
  - there are several write credentials ("several, cannot choose", lists them).
- Stopped using `resolve("supabase", ...)` in `job.py`: it returns the first provider match
  regardless of role.
- The chosen alias is printed to stderr.

## Expected behaviour (from reading the files, NOT executed)
- `creds.dev.json`: exactly one supabase `service_role` (`local.supabase.main`) -> passes.
- `creds.prod.json`: three supabase `service_role` entries (`global.supabase.erp`,
  `global.supabase.crm.main`, `acme.supabase.service_role`) -> the job stops with "several,
  cannot choose". The old code would have silently picked `global.supabase.erp`.

## What I checked, and what I could not
- I read `resolve.py`, both creds files and the README, and traced the logic by hand.
- I could NOT run anything: my Bash call was not approved, so the 0 / 1 / many branches are
  unexecuted. Please run:
  `python job.py creds.dev.json` (expect "using local.supabase.main"),
  `python job.py creds.prod.json` (expect the "several" stop, exit 1).
  The 0-writer and no-supabase branches are also unexercised.

## Open decision
The prod snapshot is ambiguous, so the job will not start there until someone says which write
credential to use (e.g. an explicit alias argument or env var). I did not pick one by guess.
