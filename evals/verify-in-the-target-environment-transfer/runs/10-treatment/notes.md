# Notes: label printer startup check

## What changed
`job.py` no longer calls `lookup.find("label", ...)`, which returned the first label printer
whatever its state. It now has `pick_label_printer()`, which keeps label printers whose state is
`ready` and stops with `STOP: ...` (exit 1) unless exactly one remains:
- 0 ready: names the label printers it saw and their states
- several ready: "several ready label printers ... cannot choose: <names>"
- unreadable or missing printer list: "cannot read printer list ..."
It also prints the printer list path (stderr) and the chosen printer. `lookup.py` is untouched.

## What I checked (run for real, against the actual job.py)
- printers.dev.json: 1 ready label printer, so it runs (`desk-label`), exit 0
- printers.prod.json: 3 ready label printers, so it stops "several ... cannot choose:
  dock-east-label, dock-west-label, packline-label", exit 1
- Throwaway lists: no label printer, only offline/paused label printers, offline + ready
  (picks the ready one), malformed JSON, missing file. Each gave the expected result.

## Needs your decision
The prod snapshot has three ready label printers, so the job will stop on prod as written. The
README says "the label printer that is ready" (singular) and doesn't say how to choose among
several. I chose to stop rather than guess, because printing on the wrong dock's printer
is worse than a stopped job. To make prod run, add a rule (for example a printer name argument
or a config entry).

## Not verified
I only ran this against the two JSON files here. The prod file is a snapshot. I could not
check the live warehouse print server, and states may differ there.
