# Notes

## Changed
`job.py`: `main()` now checks at startup for a label printer whose state is `ready`.
If there is none, it exits (status 1) with a message naming the printer file and the
label printers it saw with their states. Otherwise it selects from the ready ones only.
`lookup.py` is unchanged. Note that `find()` ignores state, so before this change the job
would have picked the first label printer even if it was offline or paused.

## Checked
- `printers.dev.json`: prints on desk-label (ready).
- `printers.prod.json`: prints on dock-east-label (ready).
- Temp copies of the prod file (not kept): all label printers offline, and no label printer at all,
  both exit 1 with the clear message; first label printer paused picks the next ready one (dock-west-label).
- Not tested against a real print server; only the JSON snapshots.
