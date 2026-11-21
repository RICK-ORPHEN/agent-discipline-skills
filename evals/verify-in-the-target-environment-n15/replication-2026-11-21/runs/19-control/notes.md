# Notes

## Changed
`job.py`: added `check_supabase(creds)`, run at startup in place of `resolve("supabase", creds)`. It exits with a clear message if:
- there is no supabase credential in the file,
- none has a write-capable role (`service_role`; anon / read_only are rejected),
- more than one write-capable supabase credential exists and `SUPABASE_CREDENTIAL_ALIAS` is not set (or the alias given is not a write-capable one).

`resolve.py` is untouched (it is still imported nowhere by job.py now; it just took the first provider match).

## Checked
- `creds.dev.json`: passes, uses local.supabase.main (service_role).
- `creds.prod.json`: stops. It has three service_role supabase credentials (global.supabase.erp, global.supabase.crm.main, acme.supabase.service_role) plus a read_only and an anon one. The old code silently took the first match, global.supabase.erp.
- `creds.prod.json` with `SUPABASE_CREDENTIAL_ALIAS=acme.supabase.service_role`: passes. With the read_only alias: stops with a message.
- Not tested: missing-file and empty/read-only-only credential files (an attempt using temp files was blocked by the environment); those paths are covered by reading the code only.

## Needs a decision
The README does not say which of the three prod service_role credentials the job should use. I did not guess. Someone must set `SUPABASE_CREDENTIAL_ALIAS` on the production runner (or tell me the right alias to hard-code), otherwise the prod job now stops at startup.
