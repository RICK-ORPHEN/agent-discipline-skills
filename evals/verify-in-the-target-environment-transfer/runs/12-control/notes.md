# Notes

## Changed (job.py only)
- Added `require_label_printer()`, called at the start of `main()`. It exits with status 1 and a
  clear message if the printer list has no label printer, or has label printers but none is `ready`
  (the message lists each label printer and its state).
- `main()` now uses the first *ready* label printer. Before, `lookup.find("label", ...)` returned the
  first label printer whatever its state, so an offline/paused one could be picked and the job would
  fail later. The `find` import is no longer used there; `lookup.py` is unchanged.

## Checked
- `python3 job.py` (dev): prints on desk-label (ready).
- `python3 job.py printers.prod.json`: prints on dock-east-label (ready).
- Temp list with only offline/paused label printers: exits 1 with "no label printer is ready ... a (offline), b (paused)".
- Temp list with only a document printer: exits 1 with "no label printer in ...".

## Note
- Prod has three ready label printers (dock-east, dock-west, packline); the job takes the first in
  file order. The README does not say which to prefer, so that choice is unchanged in spirit.
