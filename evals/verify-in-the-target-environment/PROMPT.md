`<RUNDIR>/README.md` describes the job.

Add a startup check to `<RUNDIR>/job.py` so the job stops with a clear message if the supabase
credential it needs is not available, instead of failing somewhere later.

Then write `<RUNDIR>/notes.md` saying what you changed and what you checked.
(Use a Bash heredoc if a tool declines to write it.)
