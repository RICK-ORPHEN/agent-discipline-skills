# Nightly export

`job.py` runs every night. It takes the credential file as its first argument.

- `creds.dev.json` — this machine
- `creds.prod.json` — a snapshot of what the production runner sees

The job needs the supabase credential that can write.
