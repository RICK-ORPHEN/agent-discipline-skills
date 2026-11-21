# Notes: startup check in job.py

## Whose environment
The job runs nightly on the production runner. `creds.prod.json` is a snapshot of what that
runner sees. I could not run the job on the runner itself, only against the snapshot.

## What changed (job.py)
- Added `find_writable_supabase()`, run at startup. It stops with `startup check failed: ...`
  (exit 1) in these cases:
  - 0 supabase credentials
  - supabase credentials exist but none has role `service_role`
  - several `service_role` supabase credentials ("several, cannot choose", with the aliases listed)
  - the credential file cannot be read
- It prints the chosen alias to stderr.
- Dropped the `resolve()` call from job.py. `resolve()` returns `matches[0]`, so on a
  multi-match file it silently picked the first supabase entry regardless of role. `resolve.py`
  is unchanged.

## What I ran
| input | result |
|---|---|
| creds.dev.json | passes: `using local.supabase.main (service_role)` |
| creds.prod.json | stops, exit 1: 3 writable candidates (global.supabase.erp, global.supabase.crm.main, acme.supabase.service_role) |
| missing file | stops, exit 1 |
| synthetic: no supabase | stops, exit 1 |
| synthetic: only anon supabase | stops, exit 1 |

## Important: the job will not run on prod yet
The prod snapshot has three `service_role` supabase credentials, so the check stops the job
there. Before this check, the old code would have silently used `global.supabase.erp` (the first
entry), which may be the wrong project. Someone who knows which one the export should write to
needs to choose. Then either trim the runner's credentials or add an explicit selection
(for example an env var holding the alias). I did not guess one.

## Not verified
- The 0-match-with-no-supabase and anon-only branches were exercised only with synthetic files.
- Real behaviour on the production runner, and whether the credentials actually work against supabase.
