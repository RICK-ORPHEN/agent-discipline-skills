# Notes: startup check for the label printer

## What changed
`job.py` now runs a startup check (`pick_label_printer`) before doing any work. It stops with a
clear message on stderr and exit code 1 when:
- there is no label printer in the list (0),
- label printers exist but none is `ready` (0 usable),
- several label printers are `ready` (many): it lists them and asks for a name.

It always prints the printer list used and each label printer's state, so a failure shows what was
looked at. An optional second argument names the printer to use (`python3 job.py printers.prod.json dock-west-label`);
a named printer must exist and be `ready`.

`lookup.py` is unchanged. Its `find()` takes the first label printer whatever its state, which is why
the job could previously pick an offline printer.

## What I checked (ran, real files)
- dev list: one ready label printer, prints on `desk-label`, exit 0.
- prod snapshot, no name: 3 ready label printers (dock-east, dock-west, packline), so it stops with "several, cannot choose", exit 1.
- prod snapshot with `dock-west-label`: runs, exit 0.
- prod with `returns-label` (offline): stops, exit 1. With an unknown name: stops, exit 1.
- Temporary lists with no label printer and with only an offline one: both stop, exit 1.

## Caveats
- The prod file is a snapshot; I have not run against the live warehouse print server.
- Because prod has several ready label printers, the nightly job there will stop until a printer name is passed
  (or the team decides on a rule for choosing). I chose not to pick one arbitrarily.
