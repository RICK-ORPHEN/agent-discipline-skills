# Notes

## What changed
`job.py` now runs a startup check before doing any work. It exits with a non-zero status and a one-line
message ("startup check failed: ...") if:
- the printer list cannot be read or parsed,
- the list contains no label printer, or
- label printers exist but none is in state `ready` (the message lists each one's state).

It also now passes only `ready` printers to `find()`. `lookup.find()` returns the first printer of a kind
regardless of state, so before this change an offline or paused label printer listed first would have been
chosen. `lookup.py` is unchanged.

## What I checked
Run with `python3 job.py <file>`:
- `printers.dev.json`: prints on desk-label, exit 0.
- `printers.prod.json`: prints on dock-east-label, exit 0. Four of its five label printers are not ready or
  not first, so this snapshot only worked before by luck of ordering.
- Temporary files in /tmp: an offline label printer listed before a ready one picks the ready one; only a
  paused label printer, only a document printer, and a missing file each stop with a clear message and exit 1.

Not checked: real printer connectivity. The job only sees the state recorded in the JSON list, so a printer
that is listed `ready` but unreachable would not be caught.
