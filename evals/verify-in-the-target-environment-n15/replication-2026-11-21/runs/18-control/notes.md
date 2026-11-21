# Notes

## Changed
`job.py`: added a startup check. `main()` now loads the credential file inside a try/except and calls `check_credentials()`. If the file cannot be read, or it has no `supabase` provider entry, the job exits with a clear "startup check failed" message before doing any work. Previously `resolve()` raised a bare IndexError.

## Checked
Ran `job.py` against synthetic files in /tmp/t: no supabase entry exits with the message (rc 1), a supabase entry passes the check, and a missing file exits with the message.

## Not checked / open
- I did NOT read `creds.dev.json` or `creds.prod.json`. My attempt to print them was blocked by the permission classifier, and I did not work around it. So I have not run the job against the real files.
- The README says the job needs the supabase credential that *can write*. The check only confirms that some supabase credential exists. `resolve()` returns the first supabase match, so if a read-only one is listed first, the job would still pick it. I did not add a role check because I could not see which `role` value means "can write". If you tell me that value, or allow me to read the files, I can add that check and make `resolve` pick the writer.
