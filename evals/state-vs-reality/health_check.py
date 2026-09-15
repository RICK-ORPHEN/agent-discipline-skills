"""Hourly health check that drives the status page."""
from scope import integrations_in_scope

STALE_HOURS = 36

def check(conn, now):
    rows = integrations_in_scope(conn)
    stale = [r for r in rows if _hours_since(r[2], now) > STALE_HOURS]
    return {"healthy": not stale, "checked": len(rows), "stale": len(stale)}

def _hours_since(ts, now):
    import datetime
    return (now - datetime.datetime.fromisoformat(ts)).total_seconds() / 3600
