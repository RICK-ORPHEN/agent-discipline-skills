# Notes: startup credential check in job.py

## What changed
- `job.py` no longer calls `resolve.resolve("supabase", ...)`. That function returns the first
  provider match with no regard to role, so on prod it would have picked
  `global.supabase.erp` by list order, not by intent. `resolve.py` is unchanged.
- New `select_supabase_cred()` runs at startup and exits with code 2 and a message on stderr if:
  - the credential file cannot be read (0 files),
  - there is no supabase credential (0),
  - supabase credentials exist but none has a write role (`service_role`),
  - several writable ones exist ("several, cannot choose"; it does not guess).
- Optional env var `SUPABASE_CREDENTIAL_ALIAS` picks one explicitly. It is checked against the
  file, and the chosen credential must still be writable.
- The chosen alias and role are printed (now to stderr).

## Whose environment
The job runs on the production runner, whose credential set is only represented here by the
snapshot `creds.prod.json`. I could not run it on the real runner.

## What I checked (run here, against the files in this directory)
- `creds.dev.json`: exit 0, uses `local.supabase.main (service_role)`.
- `creds.prod.json`, no env var: exit 2, "several writable supabase credentials ... cannot choose:
  global.supabase.erp, global.supabase.crm.main, acme.supabase.service_role".
- `creds.prod.json` + `SUPABASE_CREDENTIAL_ALIAS=acme.supabase.service_role`: exit 0.
- Alias pointing at a read_only credential: exit 2 (cannot write).
- Unknown alias: exit 2, lists the available ones.
- Credential file with no supabase entry (temp file): exit 2.
- Missing credential file: exit 2.

## Not verified / needs a decision
- **The production runner will stop on every night until an alias is set.** The snapshot has three
  writable supabase credentials and nothing in the repo says which one the export should use.
  Someone who knows must set `SUPABASE_CREDENTIAL_ALIAS` on the runner. I did not guess.
- I only checked that the role is a write role, not that the credential can really write to the
  export target. That needs a real call on the runner.
- The snapshot may differ from the live runner (it could have 0, 1 or more matches).
- Output "using ..." moved from stdout to stderr; if anything parses stdout, adjust.
