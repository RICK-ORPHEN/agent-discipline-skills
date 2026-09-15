"""Shared scope helper. The sync and the status page both use this."""

ACTIVE_ONLY = "status = 'active'"


def integrations_in_scope(conn):
    """The integrations this system operates on."""
    return conn.execute(
        f"SELECT id, customer, last_synced_at FROM integrations WHERE {ACTIVE_ONLY}"
    ).fetchall()
