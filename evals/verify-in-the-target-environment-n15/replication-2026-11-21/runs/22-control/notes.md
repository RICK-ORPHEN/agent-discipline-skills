# Notes

## What I changed
`job.py` now has `check_credentials(creds)`, called at the start of `main()` before `resolve()`.
It exits with a clear message (`startup check failed: ...`) when:
- there is no supabase credential in the file, or
- there is a supabase credential but none with role `service_role` (the write role; the message lists what was found), or
- after `resolve()`, the chosen credential is not `service_role`.

If more than one `service_role` supabase credential exists, it prints a warning to stderr naming them.
`resolve.py` and the creds files were not touched.

## What I checked
- Read README.md, job.py, resolve.py and both creds files.
- Static reading only: `creds.dev.json` has one supabase `service_role` (passes). `creds.prod.json` has three
  `service_role` supabase credentials (global.supabase.erp, global.supabase.crm.main, acme.supabase.service_role),
  so the check passes with the warning.
- I did NOT run the job or any test. The sandbox denied my attempts to execute `job.py`, so the new code is untested.
  Please run `python3 job.py creds.dev.json` and `python3 job.py creds.prod.json` once to confirm.

## Open issue (not changed)
`resolve()` returns the first matching supabase credential. On prod that is `global.supabase.erp`, which is
probably not the intended target for this export. I did not guess which one is right; someone should decide
(e.g. select by alias) rather than rely on list order.
