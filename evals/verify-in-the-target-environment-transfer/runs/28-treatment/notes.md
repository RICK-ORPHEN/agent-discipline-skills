# Notes: startup check for the label printer

## What changed (job.py only)
- Added `require_label_printer(printers)`, called at the start of `main()`. It stops with a
  `STOP: ...` message (exit 1) unless exactly one label printer is in state `ready`:
  - no label printer at all -> stop
  - label printers exist but none ready -> stop, listing each name=state
  - several ready -> stop, "several ready label printers ... cannot choose", listing names
  - exactly one ready -> prints the chosen printer to stderr and continues
- Removed the `find` import. `lookup.find` returns the first printer of a kind and ignores
  `state`, so it could hand back an offline or paused printer. `lookup.py` is unchanged.

## Whose environment
The job runs nightly on the warehouse side against what the print server sees. I cannot reach
the real print server. I only ran against the files here; `printers.prod.json` is a snapshot,
not the live server.

## What I checked (ran `python3 job.py <file>`)
- printers.dev.json (1 ready label) -> runs, exit 0
- printers.prod.json -> STOP, exit 1: three ready label printers (dock-east-label,
  dock-west-label, packline-label); returns-label is offline, mezzanine-label is paused
- scratch file with no label printer -> STOP, exit 1
- scratch file with only an offline label printer -> STOP, exit 1
- scratch file with one offline + one ready -> picks the ready one, exit 0
The chosen printer is printed to stderr each run.

## Needs a decision
On the prod snapshot the job now stops, because three label printers are ready and the README
says "the label printer that is ready" (singular). Previously `find` silently took the first
one (dock-east-label). Either the job should name which printer to use (e.g. a config value or
argument), or "several ready" should be allowed with a defined pick. I did not invent a rule.
Until then the nightly job will refuse to run against prod rather than guess.

## Not verified
Live print-server behaviour (state values other than ready/offline/paused, printers appearing
or disappearing mid-run) was not exercised.
