# Notes

## What changed
`job.py` now runs a startup check before doing any work. It exits with a clear
"startup check failed: ..." message if:
- the credential file cannot be loaded,
- it has no supabase credential,
- it has supabase credentials but none with a write role (`service_role`), or
- the credential `resolve()` picks (the first supabase match) cannot write.

`WRITE_ROLES = {"service_role"}` is my assumption for "can write", based on the
role names present in the files (`service_role`, `anon`, `read_only`).

## What I checked
- Ran `job.py` against throwaway files in /tmp: read-only only (fails), no
  supabase (fails), missing file (fails), writable (passes).
- Ran against `creds.dev.json`: passes, uses `local.supabase.main`.
- Looked only at provider/alias/role of the creds files (they hold no secret
  values). I did not run the job against `creds.prod.json`.

## Open issue
`creds.prod.json` has three writable supabase credentials (`global.supabase.erp`,
`global.supabase.crm.main`, `acme.supabase.service_role`). `resolve()` returns the
first one (`global.supabase.erp`). The README does not say which is intended, so
the check cannot tell if that is the right one. Someone should confirm.
