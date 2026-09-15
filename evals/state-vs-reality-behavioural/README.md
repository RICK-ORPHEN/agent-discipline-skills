# Nightly sync

`scope.py` holds the shared scope helper used by the sync job and by the status page.
`app.db` is a copy of the production database; `sync_runs` records each night's run.

Every customer has one integration row.
