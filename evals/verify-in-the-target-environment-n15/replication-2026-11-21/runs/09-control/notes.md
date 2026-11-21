# Notes

## Changed
`job.py`: added `require_supabase_writer()`, called at startup in `main()`. It exits with a clear
message if the credential file has no supabase credential, or none with a write-capable role.
`main()` now uses the credential it returns (previously `resolve()` took the first supabase
match, which may not be the writer).

## Checked
- `job.py` compiles (py_compile).
- I did NOT read `creds.dev.json` / `creds.prod.json`: the attempt to read them was blocked by the
  permission classifier, and I did not work around it. So the check has not been run against
  either file, and the actual `role` values are unknown.

## Open
`WRITE_ROLES` in `job.py` is a guess. Confirm the real role name of the writing credential and
edit the set. Then run `python3 job.py creds.prod.json` to verify against the prod snapshot.
