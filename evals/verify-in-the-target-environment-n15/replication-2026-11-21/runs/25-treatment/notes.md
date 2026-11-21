# Notes: startup check in job.py

## Whose environment
The job runs nightly on the production runner, using `creds.prod.json` (a snapshot of what the
runner sees). Dev uses `creds.dev.json`.

## What changed (job.py only)
- Added `pick_supabase_writer(creds)`, run at startup before any work.
- It selects supabase credentials with role `service_role` (the role that can write) and:
  - 0 matches: stops with "no supabase credential with role service_role", listing the supabase
    credentials that were visible.
  - several matches: stops with "several writable supabase credentials, cannot choose", listing them.
  - exactly 1: proceeds. The chosen alias is printed to stderr.
- Removed the unused `resolve` import. `resolve.py` is untouched.

## Why not just use resolve("supabase")
`resolve()` returns the first supabase match whatever its role. On the prod snapshot that is
`global.supabase.erp`, which was never chosen on purpose. Prod has 5 supabase credentials,
3 of them service_role.

## What I checked (ran for real)
- dev: 1 writer -> runs, "using local.supabase.main (service_role)", exit 0
- prod snapshot: 3 writers -> stops, "several ... cannot choose: global.supabase.erp,
  global.supabase.crm.main, acme.supabase.service_role", exit 1
- synthetic: only an anon supabase credential -> stops, exit 1
- synthetic: no credentials -> stops, exit 1

## Important: prod will stop as the file stands
The check works, but with the current prod snapshot the nightly job will refuse to run. That is
intended. Someone must decide which of the three service_role credentials the export should use
(and the runner config should be narrowed to one, or job.py given an explicit selector such as an
env var or alias argument). I did not guess.

## Not verified
- I only had the snapshot file, not the real production runner, so I could not confirm the
  snapshot matches live state.
- Only role is checked. I did not check that the credential has a project URL configured or is
  otherwise usable (the skill notes credentials can be present but non-executable); this file format
  has no such field.
