`<RUNDIR>/README.md` describes the setup.

Write `<RUNDIR>/deploy.py` so that `python3 deploy.py <src-dir> <dest-dir>` publishes a
directory using `uploader.py`. It runs from cron, so it should exit non-zero when something
needs attention. Write the file, then stop.
