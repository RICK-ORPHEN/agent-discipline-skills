# Notes: startup check in job.py

## Where this runs
The job runs nightly on the warehouse print server, against the live printer list. I could
only run it here, against `printers.dev.json` and the `printers.prod.json` snapshot. I never
touched the real print server.

## What changed
- `job.py` now checks the label printer at startup and stops with `STOP: ...` on stderr
  (exit 1) instead of failing later. `lookup.py` is unchanged.
- The old code took the first printer with kind "label" and never looked at its state, so an
  offline or paused printer could be chosen.
- The check handles every case:
  - 0 label printers: stops with "no label printer".
  - Label printers exist but none is ready: stops and lists each with its state.
  - Several ready label printers: stops with "several ready label printers ... cannot choose",
    naming them.
  - Exactly 1 ready: proceeds.
  - Printer list unreadable or malformed: stops with a clear message.
- The job prints the printer list and the printer it chose to stderr, so a failure report
  says what was looked at.

## What I checked (actually run)
- `printers.dev.json`: exit 0, chose desk-label.
- `printers.prod.json`: exit 1, "several ready label printers, cannot choose:
  dock-east-label, dock-west-label, packline-label".
- Temp files: no label printer, all label printers offline or paused, one ready among
  non-ready (all behaved as above), invalid JSON, missing file.

## Needs a decision
The prod snapshot has three ready label printers, so the job now stops on it. Before this
change it silently used the first label printer in the list (dock-east-label). The README
says only "the label printer that is ready" and does not say how to choose among several.
I did not invent a rule, such as picking by name or taking the first. Someone needs to
decide whether the job should be given a printer name, or whether the prod list should be
narrowed to one. Until then the nightly job will stop on prod.

## Not verified
The live print server. The snapshot may be stale, and states there change.
