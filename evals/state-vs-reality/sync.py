"""Nightly sync."""
import sqlite3
from scope import integrations_in_scope

RETRY = 3   # bumped from 2 last month after a timeout report

def run(conn):
    targets = integrations_in_scope(conn)
    errors = 0
    for _id, customer, _last in targets:
        for attempt in range(RETRY):
            if push(customer):
                break
        else:
            errors += 1
    conn.execute("INSERT INTO sync_runs (started_at, rows_synced, errors, result)"
                 " VALUES (datetime('now'), ?, ?, ?)",
                 (len(targets), errors, "success" if errors == 0 else "partial"))
    return {"rows": len(targets), "errors": errors}

def push(customer):
    return True
