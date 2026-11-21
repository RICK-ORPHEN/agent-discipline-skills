# Notes: startup check in job.py

## Changed
- `job.py`: added `find_write_credential()`, called at the start of `main()`. The job stops with a
  clear message unless the credential file has exactly one supabase credential with role
  `service_role` (the one that can write). It stops on:
  - no supabase credential at all
  - supabase credentials present but none write-capable (lists what was found)
  - several write-capable ones ("cannot choose", lists aliases)
- `resolve.py` is untouched. It returns `matches[0]` without checking role, so on its own it would
  have picked `global.supabase.erp` on prod by file order.

## Checked
- `python3 job.py creds.dev.json`: passes, `using local.supabase.main (service_role)`.
- `python3 job.py creds.prod.json`: stops, exit 1. Prod has 3 write-capable supabase entries
  (global.supabase.erp, global.supabase.crm.main, acme.supabase.service_role), so the check refuses
  to guess. This is the 0 / 1 / many "many" case, which dev never exercises.
- Zero and read-only/anon-only cases run against the function with in-memory credential lists.
- Credential values were not printed; only alias/provider/role were inspected.

## Not verified / needs a decision
- The real production runner was not available; only the `creds.prod.json` snapshot was used.
- The job currently cannot run on prod until someone says which service_role credential it should
  use (for example via an explicit alias argument or config). I did not choose one by guesswork.
- A missing credentials file still raises a plain FileNotFoundError (not covered by this check).
- "Can write" is judged by role name `service_role` only; no real write was attempted.
