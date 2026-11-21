# Notes

## What I changed
Only `job.py`. `main()` now checks at startup that a ready label printer exists:

- It keeps only printers whose `state` is `ready`, then looks for a `label` printer among them.
- If none exists, it exits with status 1 and a message naming the file, the label printers
  it did find with their states, and "Nothing was printed."
- An unreadable or malformed printer list also exits with a clear message.
- Before, `find("label", ...)` took the first label printer whatever its state, so an
  offline or paused one could be chosen and the job would fail later.

`lookup.py` is unchanged.

## What I checked
Ran `job.py` against:
- `printers.dev.json`: prints on desk-label, exit 0.
- `printers.prod.json`: prints on dock-east-label (ready), exit 0.
- prod with dock-east-label removed: skips the offline returns-label and picks dock-west-label.
- Label printers only offline/paused: clear error, exit 1.
- No label printer at all: clear error, exit 1.
- Missing file: clear error, exit 1.

## Caveats
- Prod has several ready label printers; the job takes the first ready one in list order.
  The README does not say which one it should use, so I did not add selection logic.
- `printers.prod.json` is only a snapshot; I could not check the live print server.
  The check only sees whatever list is passed in.
