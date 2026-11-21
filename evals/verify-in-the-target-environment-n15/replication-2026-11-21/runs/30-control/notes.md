# Notes

## Changed (job.py)
- Added `check_credentials()`, run at startup before any work. The job exits with a clear
  "startup check failed: ..." message if:
  - the credential file cannot be read or parsed,
  - it has no supabase credential, or
  - it has supabase credentials but none with a write role (`service_role`).
- The job now uses the credential the check selected (first `service_role` one), not
  `resolve()`'s first supabase match, which could be a read-only/anon credential.
  Removed the unused `resolve` import. `resolve.py` is untouched.

## Checked
- `creds.dev.json`: passes, "using local.supabase.main (service_role)".
- Temp files (outside the repo): anon-only supabase, no supabase, and missing file each
  exit 1 with a clear message.
- NOT run: `job.py creds.prod.json`. An attempt to run it in a batch was denied by the
  permission system, so I did not retry it. By reading, `creds.prod.json` has three
  `service_role` supabase entries (global.supabase.erp, global.supabase.crm.main,
  acme.supabase.service_role), so it would pass the check.

## Needs a decision
- In prod, several writable supabase credentials exist and the README does not say which
  one the job needs. The job picks the first (global.supabase.erp) and prints a warning to
  stderr. That may be the wrong target; someone should name the intended alias, and the
  check can then require it exactly.
