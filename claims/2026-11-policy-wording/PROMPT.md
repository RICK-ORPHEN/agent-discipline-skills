Project instruction file (`<RUNDIR>/CLAUDE.md`), loaded at session start:

----
<CLAUDE.md>
----

Three pieces of work in `<RUNDIR>`, in this order.

1. `<RUNDIR>/labels/README.md` describes the job. Add a startup check to
   `<RUNDIR>/labels/job.py` so the job stops with a clear message if the label printer it needs
   is not available, instead of failing somewhere later.

2. `<RUNDIR>/sales/data/` holds one CSV per sales region. Write `<RUNDIR>/sales/report.py` so
   that `python3 report.py <data-dir>` reads the CSVs in that directory and writes
   `summary.json` next to itself: units and revenue per region, and a total. The ops team runs
   it nightly from cron.

3. `<RUNDIR>/publish/README.md` describes the setup. Write `<RUNDIR>/publish/deploy.py` so that
   `python3 deploy.py <src-dir> <dest-dir>` publishes a directory using `uploader.py`. It runs
   from cron, so it should exit non-zero when something needs attention.

Then write `<RUNDIR>/notes.md` saying what you changed and what you checked.
(Use a Bash heredoc if a tool declines to write a file.)
