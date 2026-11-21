# Notes

## What I changed
`job.py` now runs a startup check (`require_label_printer`) before doing any work. It exits with
status 1 and a clear message if:
- the printer list cannot be read,
- there is no printer of kind `label`, or
- label printers exist but none is in state `ready` (the message lists each one and its state).

It also now picks a label printer that is `ready`. `lookup.find` only matches on kind and returns
the first label printer whatever its state, so the job could have printed on an offline or paused
printer. `lookup.py` is unchanged; the job passes it only the ready label printers.

## What I checked
Ran `job.py` against:
- `printers.dev.json`: prints on desk-label.
- `printers.prod.json`: prints on dock-east-label (ready). That snapshot also has offline and paused label printers.
- Temporary lists (in /tmp, not kept): all labels offline/paused gives the "none ready" error; no label printer gives the "not found" error; an offline label listed before a ready one picks the ready one; a missing file gives the "cannot read" error. Failures exit with status 1.

## Not checked
No real print server was contacted. `printers.prod.json` is only a snapshot, so the check reflects
the state recorded in whichever file is passed in.
