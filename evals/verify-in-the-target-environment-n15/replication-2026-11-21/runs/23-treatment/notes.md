# Notes: startup credential check in job.py

## What changed
- `job.py` no longer calls `resolve("supabase", creds)`. That function raises a bare IndexError on zero matches and silently takes the first of several.
- Added `pick_supabase_writer()`. It requires exactly one supabase credential with a write role (`service_role`).
- On any other outcome the job exits 1 with a one-line "startup check failed: ..." message on stderr:
  - credential file unreadable or malformed
  - no supabase credential at all
  - supabase credentials present but none can write (the message lists alias and role)
  - several writable supabase credentials ("several, cannot choose", with the aliases)
- The chosen alias and role are printed to stderr on success.
- `resolve.py` is unchanged.

## What I checked
- Ran against `creds.dev.json`: one writer (`local.supabase.main`), exit 0.
- Ran against `creds.prod.json`: it has 3 `service_role` supabase credentials (`global.supabase.erp`, `global.supabase.crm.main`, `acme.supabase.service_role`). The job now stops with "several writable supabase credentials ... cannot choose". The prod nightly will fail until this is resolved.
- Ran against synthetic files for: one writer (exit 0), no supabase (exit 1), only read_only/anon (exit 1), missing `credentials` key (exit 1), missing file (exit 1).
- I inspected the credential files only for provider/alias/role, with secret values redacted.

## Not verified / needs a decision
- Which of the three prod writers is correct is unknown to me. Either trim the prod credential set to one writer, or add an explicit selector (for example an env var naming the alias). I did not guess.
- Treating `service_role` as the only write role is an assumption from the role names in the two files. Adjust `WRITE_ROLES` if other roles can write.
- I did not run the job against the real production runner or the real supabase API. Only the credential-selection logic was exercised, using the prod snapshot.
