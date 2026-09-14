"""Integration health monitor. Ops runs this hourly from cron."""
import sys

from platform_db.queries import connect, active_integrations, recent_failures


def main():
    conn = connect()
    problems = []
    for row in active_integrations(conn):
        n = recent_failures(conn, row["id"], days=1)
        if n:
            problems.append(f"{row['customer']}: {n} failed sync runs in the last day")

    if problems:
        for p in problems:
            print(p, file=sys.stderr)
        return 1
    print("all integrations healthy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
