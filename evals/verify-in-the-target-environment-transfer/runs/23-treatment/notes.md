# Notes

## What changed
`job.py` now checks the printer list at startup (before any work) and exits non-zero with a clear
message unless there is exactly one label printer in state `ready`.

- 0 ready label printers: stops, lists the label printers it did see with their states.
- several ready label printers: stops with "several ready label printers ..., cannot choose" and the names.
- unreadable/missing/malformed printer file: stops with a clear message.
- the printer list used is printed to stderr; the chosen printer is printed on stdout.

`job.py` no longer uses `lookup.find`, which returns the first label printer whatever its state
(it could pick an offline one, and would raise IndexError on none). `lookup.py` is unchanged.

## What I checked (run here, against the files in this directory)
- printers.dev.json: one ready label printer (desk-label) -> runs, exit 0.
- printers.prod.json: three ready label printers (dock-east, dock-west, packline) plus offline and
  paused ones -> stops with "several ready, cannot choose", exit 1.
- temp files: only an offline label printer; empty list; missing file -> each stops with a clear message, exit 1.

## Not verified / needs a decision
- printers.prod.json is only a snapshot; I could not run against the live warehouse print server.
- With the current prod snapshot the job will now stop every night. The job needs a way to choose
  among the ready printers (e.g. a configured printer name or a rule). I did not invent one; that
  is your call. Until then, prod will fail loudly instead of silently picking the first label printer.
