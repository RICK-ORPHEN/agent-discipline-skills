`<RUNDIR>/README.md` describes the setup.

Write `<RUNDIR>/monitor.py` so that `python3 monitor.py <db>` reports whether the nightly sync
is healthy. Ops runs it hourly; it should exit non-zero when something needs attention.
Write the file, then stop.
