# Notes

## Changed
`job.py`: added `require_label_printer()`, called at startup in `main()`. It keeps only
`kind == "label"` printers whose `state == "ready"`. If none exist, the job exits with status 1 and
a message naming the printer file and either the label printers found with their states
(e.g. `returns-label (offline)`) or "no label printer in the list".
Before, `find()` returned the first label printer whatever its state (so an offline one could be
picked), and raised a bare IndexError when there was none. `lookup.py` is unchanged.

## Checked
- `python3 job.py` (dev): prints on desk-label (ready).
- `python3 job.py printers.prod.json`: prints on dock-east-label (ready).
- Temp files in /tmp: only offline/paused labels -> clear error, exit 1; only a document printer ->
  clear error, exit 1; first label offline and second ready -> picks the ready one, exit 0.

## Not checked
- Behaviour against the real print server; only the two JSON snapshots and synthetic files were used.
- prod.json is a snapshot, so a printer ready now may not be ready at run time.
