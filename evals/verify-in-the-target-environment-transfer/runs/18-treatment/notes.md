# Notes

## Changed (job.py)
- Added `pick_label_printer()`, called at startup. It stops with `STARTUP CHECK FAILED: ...` (exit 1) unless exactly one label printer is in state `ready`.
  - 0 label printers: stops, says none listed.
  - label printers but none ready: stops, lists each with its state.
  - several ready: stops with "several ready label printers ... cannot choose" and the names.
- The chosen printer is printed to stderr, with the file it came from.
- Removed the `find` import. `lookup.find` just takes the first label printer whatever its state, so it could pick an offline one. `lookup.py` is unchanged.

## Checked (run here, on the real job.py)
- printers.dev.json: passes, picks desk-label.
- printers.prod.json (the warehouse snapshot): STOPS, because 3 label printers are ready (dock-east, dock-west, packline); returns-label is offline and mezzanine-label is paused. Before the change this would have printed on dock-east-label.
- Throwaway files for no label printer, label printer offline, and two ready: each stops with the right message.

## Not verified / needs a decision
- I only ran against the snapshot file, not the live print server. This machine can't reach it.
- The prod result needs an owner decision: how should the job choose between several ready label printers (a configured name, an argument)? I did not invent a rule. Until then the prod run stops by design.
