# Notes

## What changed
`job.py`: after loading the printer list, `main()` now checks that at least one label printer
is in state `ready`. If not, the job exits with status 1 and a message naming the file and the
label printers it saw with their states (e.g. `ERROR: no ready label printer in X. Label printers: a (paused)`).
It then picks the printer from the ready label printers only.

Reason: `lookup.find()` returns the first printer of the kind regardless of state, so an
offline/paused printer listed first would have been chosen and the job would fail later.
`lookup.py` was left unchanged.

## What was checked
- `python3 job.py` (dev): prints on desk-label (ready).
- `python3 job.py printers.prod.json`: prints on dock-east-label (ready).
- Temp files (not kept): offline label listed before a ready one -> uses the ready one;
  only a paused label printer -> exit 1 with message; no label printer at all -> exit 1, "none listed".

## Not checked
- No real printer or print server was contacted; "available" is judged only from the `state`
  field in the JSON list. prod.json is a snapshot, so the live server may differ.
