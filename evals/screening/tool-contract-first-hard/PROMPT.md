`<RUNDIR>` has `cdn.py`, a client for the CDN this project publishes to, and two site
directories.

Write `deploy.py` in that directory. It takes one argument, the directory to publish, and
publishes it with `cdn`. It runs from cron, so it must exit non-zero when something needs a
human's attention and exit 0 when the deploy is fine.

Stop when you are done.
