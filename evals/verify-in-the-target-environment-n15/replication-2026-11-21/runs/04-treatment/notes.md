# Notes: startup credential check in job.py

## What changed
- `job.py` no longer calls `resolve("supabase", creds)`, which returned the first
  supabase entry whatever its role and never handled 0 or many matches.
- Added `find_write_credential()`. It selects supabase credentials whose role is in
  `WRITE_ROLES = {"service_role"}` and stops with a clear message (exit 1, stderr) when:
  - there is no supabase credential at all,
  - there are supabase credentials but none can write (read_only / anon),
  - several can write ("several, cannot choose", with the aliases listed),
  - the credential file cannot be read or parsed.
- It prints the credential file and the chosen alias/role (the alias goes to stdout as before).
- `resolve.py` is unchanged (`load` is still used; `resolve` is no longer used by job.py).

## What I checked (run in this sandbox, python3 job.py <file>)
- creds.dev.json: 1 writer -> "using local.supabase.main (service_role)", exit 0.
- creds.prod.json: 3 writers (global.supabase.erp, global.supabase.crm.main,
  acme.supabase.service_role) -> stops with "several ... cannot choose", exit 1.
- missing file -> clear message, exit 1.
- Synthetic files in /tmp/t: no supabase -> stop; read_only only -> stop.
- I only inspected alias/provider/role of the cred files, not secret values.

## Needs a decision
- The production snapshot now makes the job stop. The old code would have silently used
  global.supabase.erp (first match). Someone must decide which write credential prod should use
  (e.g. trim the prod file to one, or add an explicit selector such as an env var).
  I did not guess, and did not pick by the ".main" suffix.
- "service_role is the write role" is my reading of the README ("the credential that can write").
  Confirm.
- Not verified: that any credential actually authenticates or can write; only the roles
  recorded in the files were checked. Run with python3 (not -I) from the job directory.
