# Notes

## What changed (job.py only; lookup.py untouched)
- Startup check `pick_label_printer`: keeps label printers whose state is "ready" and stops (exit 1, message on stderr) if there are none, or if several are ready ("cannot choose", listing them).
- Optional 2nd argument names the printer to use (needed for several-ready case). It must exist and be ready, else the job stops.
- Prints the printer list and the chosen printer to stderr.
- Why not `find()`: it returns the first "label" printer regardless of state, so an offline/paused one could be picked.

## What I checked (run against the real job.py)
- dev list: 1 ready label printer -> runs, exit 0.
- prod snapshot, no name: 3 ready label printers -> stops "several ready label printers, cannot choose" (exit 1). The prod job therefore needs the printer name as 2nd argument.
- prod + dock-west-label -> runs. prod + returns-label (offline) -> stops. unknown name -> stops.
- test files with no label printer, and only an offline one -> stop with clear messages.

## Not verified
- Only the JSON snapshots were used; not run against the live warehouse print server. States other than ready/offline/paused are treated as not ready.
- Which printer prod should use is a decision for you; I did not pick one.
