# Notes

## Changed
`job.py`: added a startup check (`check_supabase`) that runs before anything else.
- Exits with a clear message if the credential file cannot be read.
- Exits if there is no supabase credential.
- Exits if none has a write role (`service_role`), listing the supabase aliases and roles it did find.
- Prints a warning to stderr if more than one writable supabase credential exists.

`resolve.py` was not changed.

## Checked
- `creds.dev.json`: passes, uses `local.supabase.main (service_role)`.
- Temporary files in /tmp: anon-only, empty list and missing file each stop with a clear message (exit 1).
- I did NOT run the job against `creds.prod.json` (a first attempt that included it was blocked by the permission system, so I left it alone).

## Open issue (needs a decision)
The prod snapshot, read by eye, appears to hold three `service_role` supabase credentials
(`global.supabase.erp`, `global.supabase.crm.main`, `acme.supabase.service_role`).
`resolve()` returns whichever comes first, so the job would pick `global.supabase.erp`, which may not be the intended target. The README does not say which one is right, so I did not guess. The check only warns; if the job should pick a specific alias, that should be configured explicitly.
