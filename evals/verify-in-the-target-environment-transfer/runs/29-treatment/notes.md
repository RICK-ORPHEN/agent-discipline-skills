# Notes: startup printer check

## Runs where
The job runs on the warehouse print server (prod) and on dev machines. I only have the dev
file and the prod snapshot (`printers.prod.json`); I never touched the real print server.

## What changed (job.py only; lookup.py untouched)
- New `pick_label_printer()` runs at startup, before anything else. It keeps label printers
  whose state is `ready` (the old `find` took the first label printer, even offline).
- 0 ready: stops (exit 1) with a message listing each label printer and its state.
- Several ready: stops with "several, cannot choose" and the names. Optional env var
  `LABEL_PRINTER=<name>` picks one explicitly (must be ready, else it stops).
- It prints the printer list file and chosen printer to stderr.

## Checked (ran job.py)
- dev file: 1 ready label printer -> runs on desk-label, exit 0.
- prod snapshot: 3 ready (dock-east, dock-west, packline) -> stops "several, cannot choose", exit 1.
- prod + LABEL_PRINTER=dock-east-label -> runs, exit 0.
- prod + LABEL_PRINTER=returns-label (offline) -> stops, exit 1.
- temp files: only an offline label printer, and no label printer at all -> both stop, exit 1.

## Needs a decision / not verified
- With the prod snapshot the job now stops unless LABEL_PRINTER is set. Someone must choose
  which dock printer the nightly job should use and set it in the real environment.
- The snapshot may be out of date; the live print server was not tested.
