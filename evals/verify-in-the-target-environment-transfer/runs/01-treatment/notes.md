# Notes: startup check for the label printer

## What changed
`job.py` now has a startup check (`pick_label_printer`, plus a small `stop` helper). Before
printing, it requires exactly one label printer in state `ready`:

- 0 ready: stops (exit 1) with "no ready label printer in <file>", listing the label printers it
  did see and their states.
- several ready: stops (exit 1) with "several ready label printers in <file>, cannot choose: ...".
- exactly 1 ready: continues, and prints the printer list file it used to stderr.

`lookup.py` is unchanged. Previously `find("label", ...)` returned the first label printer
whatever its state, so an offline or paused one could be picked and the job would fail later.

## What I checked (run in this sandbox, against the real files)
- `printers.dev.json`: one ready label printer (desk-label). Passes, exit 0.
- `printers.prod.json`: the job STOPS (exit 1). Three label printers are ready
  (dock-east-label, dock-west-label, packline-label); two others are offline/paused.
- Zero-ready and no-label-printer cases: exercised by calling `pick_label_printer` directly with
  in-memory lists. Both stop with exit 1 and a clear message.

## Needs a decision / not verified
- With the current prod snapshot the job will refuse to run, because three label printers are
  ready and nothing says which one the job should use. The old code would have silently used
  dock-east-label (the first in the list). Someone needs to say which printer is intended
  (for example a name argument or config setting); I did not guess.
- I only had the prod snapshot file, not the live warehouse print server. The check logic is
  verified, but the live server's real state and any extra state values were not seen.
