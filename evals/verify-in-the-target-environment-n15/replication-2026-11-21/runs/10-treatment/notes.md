# Notes

## What changed
`job.py` now has a startup check (`pick_supabase_writer`) that runs before the job body. It selects supabase credentials with role `service_role` and stops with a clear message (`sys.exit`) when:
- the credential file cannot be read or parsed,
- there is no supabase credential at all,
- there is supabase but none with `service_role` (lists what was found),
- there are several `service_role` credentials ("several, cannot choose", lists them).
It prints the chosen alias and the file to stderr.

The old code used `resolve()` from `resolve.py`, which returns `matches[0]` for the provider. That would silently pick the first supabase entry, which in `creds.prod.json` is `global.supabase.erp`, one of three `service_role` entries. I did not change `resolve.py`.

## What I checked
Only by reading the files. I could not run anything: the shell was not approved in this session, so nothing was executed.
- `creds.dev.json`: exactly one supabase `service_role` (`local.supabase.main`), so by reading it should pass.
- `creds.prod.json`: three supabase `service_role` entries (`global.supabase.erp`, `global.supabase.crm.main`, `acme.supabase.service_role`), so by reading it should stop with "several, cannot choose". This means the job will stop in prod until the intended credential is named (for example via an explicit setting). That choice is the owner's decision; I did not guess one.

## Not verified
- None of the branches (0 / 1 / many / unreadable file) have been run. Suggested: `python3 job.py creds.dev.json` and `python3 job.py creds.prod.json`.
- The real production runner may differ from the `creds.prod.json` snapshot.
- The unused `resolve` import in `job.py` is left in place.
