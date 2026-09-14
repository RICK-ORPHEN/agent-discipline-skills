"""Read helpers for the platform database. Used by the monitor and the ops dashboard."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "platform.db"


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _rows(conn, sql, args=()):
    return conn.execute(sql, args).fetchall()


def active_integrations(conn):
    """Integrations this monitor covers."""
    return _rows(
        conn,
        # region clause added 2026-03, when the monitor moved onto the us-east box
        "SELECT * FROM integrations WHERE status = 'active' AND region = 'us-east'"
        " ORDER BY id",
    )


def last_successful_sync(conn, integration_id):
    """ISO timestamp of the most recent successful run, or None."""
    r = _rows(
        conn,
        "SELECT MAX(ran_at) AS t FROM sync_runs"
        " WHERE integration_id = ? AND result = 'success'",
        (integration_id,),
    )
    return r[0]["t"]


def recent_failures(conn, integration_id, days=1):
    """Count of failed runs in the last `days` days."""
    r = _rows(
        conn,
        "SELECT COUNT(*) AS n FROM sync_runs WHERE integration_id = ?"
        " AND result != 'success' AND ran_at >= datetime('now', ?)",
        (integration_id, f"-{days} days"),
    )
    return r[0]["n"]


def rows_synced_last_night(conn, integration_id):
    r = _rows(
        conn,
        "SELECT rows_synced FROM sync_runs WHERE integration_id = ?"
        " ORDER BY ran_at DESC LIMIT 1",
        (integration_id,),
    )
    return r[0]["rows_synced"] if r else 0
