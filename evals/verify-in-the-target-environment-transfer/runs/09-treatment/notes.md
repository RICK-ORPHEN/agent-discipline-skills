# Notes: startup check for the label printer

## What changed
`job.py` now has `pick_label_printer()`, called at startup. It stops (exit 1, message starting
"STARTUP CHECK FAILED") unless exactly one label printer is in state `ready`:
- no label printer at all -> stop
- label printers exist but none ready -> stop, listing each name=state
- several ready -> stop, "several ready label printers ... cannot choose", listing them
- exactly one ready -> continue

It also prints which printer list file was used (stderr). The unused `find` import was removed;
`lookup.py` is unchanged. Note `lookup.find` ignores `state` and takes the first label printer,
which is why the check filters on state itself.

## What I checked (run, not just read)
- `printers.dev.json`: passes, prints on desk-label (ready).
- `printers.prod.json`: STOPS with "several ready ... cannot choose: dock-east-label,
  dock-west-label, packline-label".
- Temporary files (in /tmp/t): one offline label printer -> stop; no label printer -> stop;
  one ready -> passes.

## Needs a decision
Against the prod snapshot the job now refuses to start, because three label printers are ready.
Before, it silently used the first label printer (dock-east-label), and would have used an
offline one if it were listed first. I did not choose a rule for picking among several (e.g. a
printer name setting); that is your call. Also, I only tested against the prod snapshot file, not
the live warehouse print server, so printer states there may differ.
