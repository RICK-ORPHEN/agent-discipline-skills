# Notes

## Changed
`job.py`: added a startup check in `main()`. After loading the printer list, it keeps only printers with
`kind == "label"` and `state == "ready"`. If none exist, the job exits with status 1 and a message naming the
file and the label printers it did find with their states (or "none listed"). Otherwise it picks from the ready
ones. `lookup.py` is unchanged.

Why: README says the job needs the label printer that is *ready*. `find()` returns the first label printer
regardless of state, and raises IndexError if there is none. So an offline/paused printer, or a missing one,
would only fail later or print to the wrong device.

## Checked (ran job.py)
- `printers.dev.json`: prints on desk-label (ready).
- `printers.prod.json`: prints on dock-east-label (ready). Prod has 2 offline/paused label printers
  (returns-label, mezzanine-label); they are now skipped even if listed first.
- Temp file, only an offline label printer: exits 1 with clear message.
- Temp file, no label printer: exits 1, "none listed".
- Temp file, paused then ready label printer: uses the ready one.

Not checked: real print server; the prod file is only a snapshot.
