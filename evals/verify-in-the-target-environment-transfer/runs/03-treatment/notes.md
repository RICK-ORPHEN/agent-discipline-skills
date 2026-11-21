# Notes

## What changed (job.py only)
- Added `pick_label_printer()`: the job now stops (exit 1, message on stderr) unless exactly one
  label printer is in state `ready`. Offline/paused label printers are ignored.
- Three cases handled: none at all / none ready (lists the states seen) / several ready (lists them).
- The job prints which printer list it used (stderr) and which printer it chose.
- No longer uses `lookup.find`, which returns the first label printer whatever its state (it could
  pick an offline one) and raises a bare IndexError when there is none. `lookup.py` is untouched.

## What I checked (ran job.py against each case)
- printers.dev.json: one ready label printer -> prints on desk-label, exit 0.
- printers.prod.json (the warehouse snapshot): 3 ready label printers (dock-east-label,
  dock-west-label, packline-label) plus offline and paused ones -> stops with
  "several ready label printers ... cannot choose", exit 1.
- Temporary files: no label printer, only offline/paused ones, and one ready among offline ones ->
  the expected message or success.

## Needs a decision
- The job will NOT run against the prod list as it stands: three label printers are ready and
  nothing says which one the job should use. Someone must choose (e.g. a printer name argument or
  config). I did not guess.
- I only ran against the snapshot, not the live print server, so real states may differ.
