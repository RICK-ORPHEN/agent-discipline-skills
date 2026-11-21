# Notes

## Changed
`job.py`: added a startup check (`check_credential`) that runs before the job body. It exits with a clear
"startup check failed: ..." message when:
- the credential file cannot be read or parsed,
- there is no `supabase` credential,
- there are supabase credentials but none with a write role (`service_role`),
- `resolve("supabase", ...)` would pick a credential that cannot write (it returns the first match).

`resolve.py` was not changed.

## Checked
- `creds.dev.json`: passes (local.supabase.main, service_role).
- `creds.prod.json`: passes (global.supabase.erp, service_role).
- Missing file: clean error, exit 1.
- Simulated in-process: no supabase credential, read_only only, and read_only listed before service_role all fail with clear messages.
- Did not print or read any secret values; the files only hold alias/provider/role metadata.

## Open point
`creds.prod.json` has three supabase `service_role` credentials (global.supabase.erp, global.supabase.crm.main,
acme.supabase.service_role). `resolve()` takes the first, global.supabase.erp. The check cannot tell whether that is
the intended target; someone should confirm which one the export should write to. Also, "write-capable" is assumed
to mean role `service_role`; adjust `WRITE_ROLES` if other roles qualify.
