# Notes: startup printer check

## Changed
`job.py`: added `require_label_printer(printers)`, called at the start of `main()`.
It keeps only printers with kind "label" and state "ready". If none exist, the job
exits with status 1 and a message naming the cause and the printer file used:
- no label printer in the list, or
- label printers found but none ready, listing each name and state.
Otherwise it passes the ready ones to `find("label", ...)`.

`lookup.py` is unchanged. Its `find()` returns the first label printer whatever its
state, so the readiness filter lives in `job.py`.

## Checked
Run from /tmp with `python3 job.py <file>`:
- printers.dev.json -> prints on desk-label, exit 0
- printers.prod.json -> prints on dock-east-label, exit 0 (it skips none here, but
  returns-label (offline) and mezzanine-label (paused) are now never eligible)
- temp file with only an offline label printer -> clear error, exit 1
- temp file with no label printer -> clear error, exit 1

## Caveats
- prod has three ready label printers; the job takes the first listed
  (dock-east-label). The README does not say which one is wanted.
- Did not run with `python3 -I`: it blocks importing `lookup` from the script dir.
- Only the printer snapshots were checked, not a live print server.
