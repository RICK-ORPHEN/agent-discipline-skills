# Notes

## What changed
`job.py`: added `require_label_printer()`, called at startup in `main()`. It keeps only printers
with `kind == "label"` and `state == "ready"` and picks the first one. If none qualifies, the job
exits with status 1 and a message naming the printer list file and the state of each label printer
(or saying that no label printer exists). `lookup.py` is unchanged.

Why: `lookup.find("label", ...)` returns the first label printer whatever its state, so an
offline or paused printer would have been chosen and the job would have failed later.

## What I checked
Ran `job.py` against:
- `printers.dev.json`: prints on desk-label (ready), exit 0.
- `printers.prod.json`: prints on dock-east-label (ready), exit 0.
- A copy of prod with all label printers offline: exits 1 listing each printer and its state.
- A copy of prod with no label printers: exits 1 with a "no label printer found" message.

Not checked: a real printer or print server. Only the JSON snapshots were used.
Behaviour note: with several ready label printers, the first in the list is used.
