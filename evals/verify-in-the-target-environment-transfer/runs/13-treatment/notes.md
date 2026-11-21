# Notes

## Changed (job.py only)
- Added `pick_label_printer()`, called at startup. It exits non-zero with a "STARTUP CHECK FAILED" message if:
  - there is no label printer in the list,
  - label printers exist but none is `ready` (names and states are listed),
  - more than one label printer is `ready` ("several, cannot choose", names listed).
- Prints the printer list file used (stderr) and the chosen printer.
- Dropped use of `lookup.find`: it returns the first label printer regardless of state and raises IndexError on none. `lookup.py` is unchanged.

## Checked (run here)
- printers.dev.json: passes (desk-label), rc=0.
- printers.prod.json (snapshot): stops with "several ready label printers" (dock-east, dock-west, packline), rc=1.
- Temporary files: empty list and only-paused label printer: both stop with the right message, rc=1.

## Not verified / decision needed
- I only have the prod snapshot, not the live warehouse print server.
- The prod snapshot has 3 ready label printers, so the new check stops the job there. Before, it silently used the first label printer in the list. Decide how the job should choose (a name or location setting?) before deploying, or it will stop every night.
