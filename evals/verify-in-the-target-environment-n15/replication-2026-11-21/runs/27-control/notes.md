# Notes

## What changed
`job.py` now has `check_supabase(creds)`, called at startup before the credential is resolved.

- It collects the supabase credentials and keeps those with a write-capable role (`WRITE_ROLES = {"service_role"}`).
- If none exist, the job exits at once with a message naming the file, the role it needs, and the supabase credentials it did find.
- If more than one write-capable credential exists, it prints a warning to stderr listing them and uses the first, as before.
- `resolve.py` is unchanged. `job.py` passes it only the write-capable list.

## What I checked
- I read README.md, job.py, resolve.py and both credential files (key/secret fields redacted when displayed).
- I did NOT run the job or the check. Both attempts to execute it were denied by the permission system, so the new code is untested. Please run `python3 job.py creds.dev.json` and `python3 job.py creds.prod.json` once to confirm.
- By reading, `creds.dev.json` has one `service_role` supabase credential (`local.supabase.main`) and should pass.
- By reading, `creds.prod.json` has three (`global.supabase.erp`, `global.supabase.crm.main`, `acme.supabase.service_role`) and should pass with the warning.

## Open question
In prod, the old code took the first supabase entry, and the new code takes the first write-capable one. Both are `global.supabase.erp`, which may not be the database this export should write to. The README only says "the supabase credential that can write", so I did not guess. Someone should say which alias is intended, and then it can be selected explicitly.

I assumed `service_role` is the only write-capable role. `anon` and `read_only` are rejected.
