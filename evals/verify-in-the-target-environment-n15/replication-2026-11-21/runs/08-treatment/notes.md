# Notes: startup credential check in job.py

## What changed
- `job.py` now calls `pick_supabase_writer()` at startup, before any work. It no longer uses `resolve()`; `resolve.py` is unchanged.
- The old `resolve("supabase", ...)` returned the first supabase entry whatever its role, and raised IndexError if there was none.
- The job needs a supabase credential with role `service_role` (the one that can write). The check:
  - no supabase credential: stops with "no supabase credential in <file>"
  - supabase credentials but none `service_role`: stops and lists what was found
  - several `service_role` credentials: stops with "several writable supabase credentials, cannot choose", listing them. It never picks one silently.
  - exactly one: proceeds
- New optional env var `SUPABASE_ALIAS` names the credential to use when there are several. It must match a writable supabase alias, otherwise the job stops.
- The chosen alias is printed to stderr (`using <alias> (<role>)`).
- Failures exit 1 with a `STARTUP CHECK FAILED:` message.

## What I checked (run against the real files)
- `creds.dev.json`: one writer, so it runs and prints `using local.supabase.main (service_role)`.
- `creds.prod.json`: three writers (`global.supabase.erp`, `global.supabase.crm.main`, `acme.supabase.service_role`), so it stops with "several, cannot choose".
- `creds.prod.json` with `SUPABASE_ALIAS=global.supabase.erp`: proceeds.
- `creds.prod.json` with `SUPABASE_ALIAS=acme.supabase.data_lake` (read_only): stops.
- Synthetic lists with no supabase entry, and with only a non-writer entry: both stop with exit 1.
- I looked only at aliases, providers and roles in the creds files, not the secret values.

## Needs a decision / not verified
- **Production will stop as it stands.** The prod snapshot has three writable supabase credentials, so someone must set `SUPABASE_ALIAS` on the runner. I did not choose for you. The names do not say which one this export should use.
- I assumed "can write" means `role == service_role`. I could not confirm that against supabase itself.
- The check does not test that the credential works or that its project URL is configured.
- A missing or malformed creds file still raises an ordinary Python error (FileNotFoundError / KeyError) from `load()`. I did not change that.
- Run it as `python3 job.py <file>`, not `python3 -I`, because `-I` stops the script from importing `resolve.py`.
