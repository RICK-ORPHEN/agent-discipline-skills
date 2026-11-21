# Notes

## Changed
`job.py`: added `check_supabase(creds)`, called in `main()` right after the credentials load. It exits with a clear message if:
- there is no supabase credential in the file, or
- there is one, but none with a write-capable role (`service_role`; `anon` and `read_only` do not count).

If more than one write-capable supabase credential exists, it prints a warning to stderr and carries on.
`resolve.py` is unchanged.

## Checked
- `creds.dev.json`: passes, uses local.supabase.main (service_role).
- `creds.prod.json`: passes, with the warning.
- Temp files with only an anon supabase credential, and with no supabase credential: both exit 1 with the expected message.

## Open issue
`creds.prod.json` has three service_role supabase credentials: global.supabase.erp, global.supabase.crm.main, acme.supabase.service_role.
`resolve()` takes the first match, so prod uses global.supabase.erp. The README does not say which one the job should use, so I did not guess. Someone should confirm it is the intended one, or `resolve` should select by alias.
