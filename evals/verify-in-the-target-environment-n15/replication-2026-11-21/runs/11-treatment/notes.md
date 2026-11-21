# Notes: startup credential check in job.py

## What changed
- `job.py` now has `check_credential()`, run first in `main()`. It stops (exit 1, message on stderr) instead of failing later.
- It stops when: the creds file is missing; the file is unreadable or has no `credentials` list; there is no `supabase` credential (0); there are several (many, "cannot choose"); or the one found has `executable: false`.
- It prints the file, provider and candidate aliases to stderr, so the chosen value is visible.
- `resolve.py` is unchanged. Its `resolve()` returns `matches[0]` and raises IndexError on 0, and silently takes the first on many; that is why the check lives in `job.py`.

## What I checked
- Ran `job.py` against synthetic creds files in a temp dir (since deleted) covering 0, 1, many, executable:false, invalid JSON and a missing file. Each gave the expected result (1 passes, the rest stop with a clear message).

## What I did NOT check
- I did not read `creds.dev.json` or `creds.prod.json`: the permission system denied my attempt to read them, and I did not work around that. So `job.py` has not been run against the real files, and I have not seen what the production runner's snapshot resolves to. Run `python3 job.py creds.prod.json` before relying on it. The many branch in particular may be what prod hits.
- The README says the job needs the supabase credential that can write. I do not know which field marks that (I only saw `alias`, `role`, `provider` used in the code), so the check does not verify write capability. Once the role values are known, add a check on `role` in `check_credential()`.
- The `executable` field is a guess based on the skill's description of other environments; it is ignored if absent.
