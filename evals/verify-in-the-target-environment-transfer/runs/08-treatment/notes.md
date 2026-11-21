# Notes

## Changed
`job.py`: added `check_label_printer()`, run at startup before anything prints. It needs exactly one
label printer in state `ready`:
- 0 ready: stops (exit 1) and lists the label printers with their states.
- several ready: stops (exit 1) with "several ready label printers ... cannot choose: <names>".
- 1 ready: continues, and prints the printer list file and chosen printer to stderr.

The old code took the first `kind == "label"` entry regardless of state. `lookup.py` is unchanged
(`find` is no longer used by `job.py`).

## Checked (run with `python3 job.py <file>`)
- printers.dev.json: 1 ready label printer (desk-label), exit 0.
- printers.prod.json: 3 ready label printers (dock-east-label, dock-west-label, packline-label), so the
  job now STOPS with "several, cannot choose" (exit 1). Before, it would have silently used dock-east-label.
- Temp files: only an offline label printer (stop), no label printer at all (stop), one offline plus one ready (passes).

## Not verified / needs a decision
- Prod is only a snapshot file; I did not run against the real warehouse print server.
- The job cannot run on prod as it stands: it needs a way to say which of the ready label printers to use
  (e.g. an argument or config). I did not invent a rule for choosing.
