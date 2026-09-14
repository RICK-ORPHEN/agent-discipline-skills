"""Ops dashboard summary. Rendered on the internal status page every 5 minutes."""
from .queries import active_integrations, rows_synced_last_night


def summary(conn):
    integrations = active_integrations(conn)
    return {
        "integrations": len(integrations),
        "rows_last_night": sum(rows_synced_last_night(conn, i["id"]) for i in integrations),
    }
