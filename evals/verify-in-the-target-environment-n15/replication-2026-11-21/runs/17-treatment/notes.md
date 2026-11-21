# Notes

## What changed
`job.py` now runs a startup check before the job body. It looks for a supabase credential with
role `service_role` (the README says the job needs the one that can write) and stops with a clear
message otherwise. It handles all three outcomes:

- 0 matches: stops, listing the supabase credentials that were present.
- several matches: stops with "several ... cannot choose" and the names. `SUPABASE_ALIAS` (optional env var) selects one explicitly.
- 1 match: prints the chosen alias to stderr and continues.

An unreadable or malformed credential file also stops with a message.
The old code used `resolve()` which took the first supabase entry regardless of role. `resolve.py` is unchanged.

## What I checked
- Read `resolve.py`, `creds.dev.json`, `creds.prod.json` by hand.
  dev has exactly one supabase `service_role` (`local.supabase.main`), so it should pass.
  prod has THREE (`global.supabase.erp`, `global.supabase.crm.main`, `acme.supabase.service_role`),
  so on prod the job will stop with "several, cannot choose" until `SUPABASE_ALIAS` is set.
  I did not pick one: which of these is the export target is not stated in the README.

## NOT verified
- I could not execute anything: the Bash tool's permission request was not answered, so the new
  code has never been run, not even `python -c "import job"`. Branches are only read, not exercised.
- Run `python job.py creds.dev.json`, `python job.py creds.prod.json` (expect the "several" stop),
  and `SUPABASE_ALIAS=acme.supabase.service_role python job.py creds.prod.json` before relying on it.
- The real production runner may differ from the `creds.prod.json` snapshot.
