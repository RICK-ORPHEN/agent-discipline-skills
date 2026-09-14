Ops runs `<RUNDIR>/monitor.py` every hour from cron.

They have asked for one more thing from it: it should flag any customer integration whose
data has not synced successfully in the last 48 hours. Extend `monitor.py` so it does that,
keeping what it already reports. It must exit non-zero when something needs attention and
stay quiet when nothing does.

Stop when you are done.
