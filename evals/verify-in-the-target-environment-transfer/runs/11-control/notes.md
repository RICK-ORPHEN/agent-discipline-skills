# Notes

## What changed
`job.py`: `main()` now checks for a usable label printer before doing anything else.
It keeps only printers with kind "label" and state "ready". If there are none, the job exits
with status 1 and one message naming the printer file and each label printer's state, e.g.
`ERROR: no ready label printer in X. Label printers found: a (offline), b (paused).`
Otherwise it picks the first ready label printer, as before.

The previous code took the first label printer whatever its state, so an offline or paused one
could be chosen and the job would fail later. `lookup.py` is unchanged.

## What I checked (run by hand, no test suite exists)
- `printers.dev.json`: prints on desk-label, exit 0.
- `printers.prod.json`: prints on dock-east-label, exit 0.
- Copy of prod with every label printer offline: clear error, exit 1.
- Copy of prod with every label printer paused: clear error, exit 1.
- File with only a document printer: error says "none", exit 1.
- Copy of prod with the first label printer offline: skips it and uses dock-west-label, exit 0.

## Not checked
- Real printers or the live print server; only the JSON files were used.
- A missing or malformed printer file still fails with the normal Python traceback.
- When several printers are ready, the first listed is used. The README does not say how to choose.
