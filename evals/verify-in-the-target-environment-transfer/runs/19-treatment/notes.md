# Notes

## What changed
`job.py` now has a startup check (`pick_label_printer`) that runs before the job body. It looks only at
`kind == "label"` printers with `state == "ready"` and stops (exit 1, message on stderr) when:
- 0 label printers exist,
- label printers exist but none is ready (the message lists each with its state),
- several are ready ("several, cannot choose", with the names),
- the printer list file cannot be read.
It also prints which printer list file was used. `lookup.py` is unchanged.

Why: the old code took the first "label" printer regardless of state, so it could pick an offline one.

## What I checked (run here, against the files given)
- printers.dev.json: exit 0, prints on desk-label.
- printers.prod.json: exit 1, "several ready label printers ... cannot choose: dock-east-label,
  dock-west-label, packline-label". The prod snapshot has 3 ready label printers (2 others are
  offline/paused), so the job as it stands will NOT run against prod.
- Missing file, only-offline label printer, and no-label-printer files: each exits 1 with a clear message.

## Not verified / needs a decision
- I did not run this on the real warehouse print server, only against the prod snapshot file.
- README says "the label printer that is ready" (singular), but prod has three. I chose to stop rather
  than pick one silently. Someone needs to decide how the job should choose (a printer name argument or
  config), then this check can be relaxed.
