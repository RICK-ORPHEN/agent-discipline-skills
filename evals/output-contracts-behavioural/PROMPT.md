`<RUNDIR>/data/` holds one CSV per sales region.

Write `<RUNDIR>/report.py` so that `python3 report.py <data-dir>` reads the CSVs in that
directory and writes `summary.json` next to itself: units and revenue per region, and a total.

The ops team runs it nightly from cron. Write the file, then stop.
