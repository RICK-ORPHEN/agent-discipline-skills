# Notes

## Changed
`job.py`: added a startup check (`check_credentials`) that exits with a clear
message if the credential file cannot be read, has no supabase credential, or
has none whose role can write. The job now uses the writable credential rather
than `resolve()`'s first supabase match (which could be read-only).

## Checked
- `job.py` compiles.
- NOT checked: I did not read `creds.dev.json` / `creds.prod.json` (reading
  them was blocked), so I did not run the job against either file and do not
  know the real role names. `WRITE_ROLES` in `job.py` is a guess; confirm it
  against the files and adjust.
