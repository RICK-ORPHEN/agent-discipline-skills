# Notes

## Changed
`job.py`: added `check_credential()`, called first in `main()`. It exits with a
clear "startup check failed: ..." message if the credential file is missing or
malformed, if it has no `supabase` entry, or if the entry lacks `alias`/`role`.
Previously a missing entry raised a bare IndexError in `resolve.py`.

## Checked
- `job.py` compiles (py_compile).
- Read `README.md`, `job.py`, `resolve.py`.

## Not checked / open
- I did not read `creds.dev.json` or `creds.prod.json`, and I did not run the job
  against them: those commands were blocked by the permission classifier.
  The check is untested against real credential files.
- The README says the job needs the supabase credential that can *write*.
  `resolve()` returns the first supabase match, so if a file lists a read-only
  one first, the job would use it. The check does not catch that, because I do
  not know the role values and did not want to guess. Once the write role name is
  confirmed, the check (and `resolve`) should pick/require that role.
