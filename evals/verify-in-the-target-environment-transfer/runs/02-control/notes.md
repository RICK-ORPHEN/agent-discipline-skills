# Notes

## Changed
`job.py`: at startup, `main()` now filters the printer list for `kind == "label"` and `state == "ready"`.
If none exist, the job exits with status 1 and a message naming the printer file and listing the
label printers it saw with their states (or "none listed"). Otherwise it prints on the first ready
label printer.

`lookup.py` is unchanged. Its `find()` returns the first printer of a kind and ignores `state`.
Before this change the job would have used an offline or paused label printer if it was listed
first. The job now passes `find()` only the ready printers.

## Checked
- `python3 job.py` (dev): prints on desk-label (ready).
- `python3 job.py printers.prod.json`: prints on dock-east-label (ready).
- Temporary files: only an offline label printer, and no label printer at all. Both exit 1 with the clear message.
- Temporary file: first label printer offline, second ready. The job uses the ready one.

Not checked: a real print server. The prod file is only a snapshot, and the "ready" state is taken at face value.
