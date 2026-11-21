# Notes

## Changed
`job.py`: `main()` now checks at startup that a label printer in the `ready` state exists. If not, the job
exits with status 1 and a message naming the printer list file and every label printer with its state
(or "none"). Otherwise it picks a printer from the ready ones.

Why: `lookup.find("label", ...)` returns the first label printer whatever its state. It would have returned
an offline or paused one, and the job would have failed later. `lookup.py` is unchanged.

## Checked
- `printers.dev.json`: prints on desk-label, exit 0.
- `printers.prod.json`: prints on dock-east-label, exit 0.
- Temporary copies of the prod list (in /tmp, not kept):
  - no label printer ready: clear message, exit 1.
  - no label printer at all: clear message, exit 1.
  - first label printer offline: skips it and uses dock-west-label, exit 0.
- Not checked: real printer connectivity. The job only reads the JSON snapshot, so "ready" means the
  snapshot says ready. The prod file is a snapshot, not a live view of the print server.
