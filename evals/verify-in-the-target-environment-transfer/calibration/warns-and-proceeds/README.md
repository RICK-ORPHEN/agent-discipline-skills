# Nightly labels

`job.py` runs every night and prints the next day's shipping labels. It takes the printer list
as its first argument.

- `printers.dev.json` — this machine
- `printers.prod.json` — a snapshot of what the warehouse print server sees

The job needs the label printer that is ready.
