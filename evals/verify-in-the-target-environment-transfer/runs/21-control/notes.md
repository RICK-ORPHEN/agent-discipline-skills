# Notes

## What changed
`job.py` now has a startup check, `require_label_printer()`, run before the job body.
It exits non-zero with a clear message when:
- the printer list cannot be read,
- there is no printer of kind `label`,
- there are label printers but none in state `ready` (the message lists each one's state).

It only passes a ready label printer on. `lookup.find()` matches on kind alone, so the old code
would have picked the first label printer even if it was offline or paused. `lookup.py` is unchanged.

## What I checked
- `printers.dev.json`: runs, uses desk-label.
- `printers.prod.json` (snapshot): runs, uses dock-east-label. Of 4 label printers, 3 are ready
  (dock-east, dock-west, packline), and returns-label is offline and mezzanine-label is paused.
- Temporary files (not kept): offline label printer listed first, then a ready one, picks the ready one;
  labels all paused or offline exits 1 with states shown; no label printer exits 1;
  missing file exits 1.

## Open point
When several label printers are ready (as in prod), the job takes the first ready one in file order.
If a specific printer is meant, that needs deciding. I did not change it.
