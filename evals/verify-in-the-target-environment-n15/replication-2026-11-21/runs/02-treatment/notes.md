# Startup check for job.py

## What changed
`job.py` now calls `check_credential()` before doing anything. It stops with exit code 2 and a
message on stderr when:
- the credential file cannot be read or has no `credentials` key,
- there is no `supabase` credential,
- no supabase credential has a writable role,
- several writable supabase credentials exist ("cannot choose", listing the aliases).
It also prints which supabase aliases it found, so a failure shows what was looked at.
`resolve.py` is unchanged. Its `resolve()` raises `IndexError` on 0 matches and silently picks
the first of many, so the check no longer calls it. `resolve` is still imported but unused.

## What I checked
Ran `job.py` against synthetic files in /tmp/t (none, read-only, one writable, two writable,
malformed, missing file). Each gave the expected message and exit code; the one-writable case
passed.

## NOT checked
- I did not run it against `creds.dev.json` or `creds.prod.json`. The attempt to print those
  files was denied by the permission classifier, so I did not read them or run the job on them.
  The prod 0 / 1 / many behaviour is therefore unverified.
- `WRITE_ROLES = {"write", "writer", "service_role", "admin"}` is a GUESS at the role names that
  mean "can write". If the real files use other role values, the check will wrongly stop the job.
  Confirm against the real files and edit the set.
- The check only looks at the `provider` and `role` fields. Per the skill, the README does not
  show whether the credential is actually usable (for example `executable: false` or a missing
  project URL), so this is not proof the write will succeed.
