# Notes: startup check in job.py

## What changed
- `job.py`: added `require_label_printer(printers)`, called at the start of `main()` in place of the bare `find("label", ...)`.
  - Keeps only label printers whose state is `ready`.
  - 0 ready: exits with `ERROR: no ready label printer in <file>. Label printers seen: name (state), ...`.
  - More than 1 ready: exits with `ERROR: several ready label printers in <file>, cannot choose: ...` (it does not silently take the first one).
  - Exactly 1: returns it and the job continues.
  - Prints the printer list file it used to stderr.
- `lookup.py` is unchanged. `find()` ignores state and takes the first match, so the old job could pick an offline printer.

## What I checked (python3 job.py <file>)
- `printers.dev.json`: exit 0, "printing on desk-label (ready)".
- `printers.prod.json`: exit 1, "several ready label printers ... cannot choose: dock-east-label, dock-west-label, packline-label".
- Synthetic lists: only an offline label printer, and no label printer at all: both exit 1 with the clear message.

## Needs a decision
- The prod snapshot has 3 ready label printers, so with this check the job stops in prod until it is told which one to use (for example a config value or a second argument). I did not choose one for you. The README says only "the label printer that is ready", which does not settle it.

## Not verified
- I ran this only against the two JSON files here. I could not run it against the live warehouse print server. The prod file is a snapshot, so real states may differ.
- Printer states other than ready/offline/paused are treated as not ready.
