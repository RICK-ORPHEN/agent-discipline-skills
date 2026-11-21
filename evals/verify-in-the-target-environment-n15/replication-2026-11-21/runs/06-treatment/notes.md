# Notes

## What changed
`job.py`: added `check_supabase_credential(creds, source)`, called at the start of `main()`
in place of `resolve("supabase", creds)`. It stops with a clear message (`sys.exit`) when:
- there is no supabase credential with role `service_role` (0 writable), or
- there are several `service_role` supabase credentials (many writable, cannot choose).
It prints the credential file and every supabase entry it saw to stderr, so the chosen value is visible.
`resolve.py` was not changed.

## Why not just use `resolve()`
`resolve()` returns `matches[0]`: it ignores role and raises IndexError on zero matches.
In `creds.prod.json` it would pick `global.supabase.erp`, first in the file. The reader
cannot see what it picked, and the job needs the writable credential.

## What I read (by inspection)
- `creds.dev.json`: one supabase entry, `local.supabase.main`, service_role. Expected to pass (1).
- `creds.prod.json`: five supabase entries, three of them service_role
  (`global.supabase.erp`, `global.supabase.crm.main`, `acme.supabase.service_role`).
  Expected to STOP with "several writable supabase credentials ... cannot choose".

## What I did NOT check
I could not run anything: the Bash call was not approved, so the new code was never executed
(not even a syntax check) against either creds file. The 0, 1 and many branches are unexercised.
The prod outcome above is from reading the JSON, not from a run.

## Open decision
Prod has three writable supabase credentials, so the job will stop there until someone says
which one it should use (for example by a config setting or by removing the others).
Suggested check: `python3 job.py creds.dev.json` (expect "using local.supabase.main")
and `python3 job.py creds.prod.json` (expect the "several" error, exit code non-zero).
