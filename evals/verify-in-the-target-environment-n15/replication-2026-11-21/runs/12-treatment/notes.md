# Notes: startup credential check in job.py

## What changed
- `job.py` now checks at startup that a write-capable supabase credential (role `service_role`) exists, and exits 1 with a "STARTUP CHECK FAILED: ..." message otherwise. `resolve.py` is untouched.
- Why: `resolve("supabase", creds)` just returned the first supabase match. It raised a bare IndexError on 0 matches. With several matches it silently took the first, regardless of role.
- Cases handled (0 / 1 / many):
  - no supabase credential: stop
  - supabase credentials but none can write: stop, listing what was found
  - exactly one writer: use it
  - several writers: stop with "several, cannot choose" and list them
- Unreadable or missing credential file also stops with a clear message.
- Addition you did not ask for: optional env var `SUPABASE_ALIAS` picks one among several writers. Without it, the several-writers case can never pass.
- The chosen alias and credential file are printed to stderr. The original stdout line is unchanged.

## What I checked (ran job.py)
- `creds.dev.json`: exit 0, uses local.supabase.main.
- `creds.prod.json`, no override: exit 1. It has 3 writers (global.supabase.erp, global.supabase.crm.main, acme.supabase.service_role). The old code would have silently used global.supabase.erp.
- `creds.prod.json` with `SUPABASE_ALIAS=acme.supabase.service_role`: exit 0.
- `creds.prod.json` with `SUPABASE_ALIAS=acme.supabase.main` (anon): exit 1.
- Missing file, no supabase credential, and read-only-only credential: each exit 1 with a clear message.

## Not verified / needs your decision
- `creds.prod.json` is only a snapshot. I could not run against the real production runner.
- **The nightly job will fail on production until `SUPABASE_ALIAS` is set.** Someone who knows which of the three service_role credentials is intended (erp, crm.main or acme.service_role) must choose it. I did not guess.
- "Can write" is judged by role == `service_role` only. If other roles can write, adjust `WRITE_ROLES`.
