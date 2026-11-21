# Notes

## What changed
`job.py` now has a startup check in `main()`. After loading the printer list it
keeps only printers with kind "label" and state "ready". If there are none, the
job exits with status 1 and a message naming the file and every label printer
with its state, for example:
`ERROR: no ready label printer in X. Label printers: a (paused). Not starting.`

The job also now prints on a ready label printer. Before, `find("label", ...)`
returned the first label printer whatever its state, so an offline or paused
printer listed first would have been picked. `lookup.py` is unchanged; I pass
`find` only the ready printers.

## What I checked
- `printers.dev.json`: runs, prints on desk-label (ready).
- `printers.prod.json`: runs, prints on dock-east-label (ready). Its first label
  printer is ready, but returns-label (offline) and mezzanine-label (paused) are
  also listed, so the old code only worked because of the ordering.
- Synthetic lists in /tmp: offline label printer listed before a ready one, so
  the ready one is chosen (exit 0). Only a paused label printer gives the clear
  error (exit 1). No label printer at all gives the error with "none listed"
  (exit 1).

## Not checked
The job body after the print line is a placeholder, and I did not test against a
real print server. The prod file is a snapshot, so a live state could differ.
