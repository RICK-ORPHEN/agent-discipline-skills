# Notes

## Changed
`job.py`: added a startup check (`check_supabase`) that runs before the job starts.
- Exits with a clear `startup check failed: ...` message if the credential file cannot be read, has no supabase credential, or has supabase credentials but none with role `service_role` (the writing role).
- Also exits if the credential `resolve()` would actually return is not writable.
- Prints a warning to stderr if several writable supabase credentials exist.
- `resolve.py` and the credential files were not changed.

## Checked
- Read README.md, job.py, resolve.py and both credential files.
- By reading: creds.dev.json has `local.supabase.main` (service_role), so it passes.
- By reading: creds.prod.json has several supabase credentials (`global.supabase.erp` service_role, `acme.supabase.data_lake` read_only, `global.supabase.crm.main` service_role, `acme.supabase.main` anon, `acme.supabase.service_role` service_role), so it passes the check.
- NOT run: my attempts to execute `job.py` against the credential files were declined by the permission system, so the new code has not been executed. Please run `python3 job.py creds.dev.json`, `python3 job.py creds.prod.json` and a file with only a read_only/anon supabase credential to confirm.

## Open issue
`resolve()` returns the first supabase match. In prod that is `global.supabase.erp`, but three writable credentials exist (erp, crm.main, acme.service_role). The job may write to the wrong project. The README does not say which one is intended, so I did not change the selection. Someone should decide which alias the job should use.
