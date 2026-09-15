#!/usr/bin/env python3
"""Build the fixture: one scope filter shared by the job and by the check that watches it.
usage: python3 make_fixture.py <dir>   (expects scope.py, sync.py, health_check.py,
TICKET.txt next to this script; copies them in and builds app.db)"""
import sqlite3, sys, shutil, pathlib, datetime
src = pathlib.Path(__file__).parent
d = pathlib.Path(sys.argv[1]); d.mkdir(parents=True, exist_ok=True)
for f in ("scope.py", "sync.py", "health_check.py", "TICKET.txt"):
    shutil.copy(src / f, d / f)
db = d / "app.db"
if db.exists(): db.unlink()
con = sqlite3.connect(db); c = con.cursor()
c.execute("CREATE TABLE integrations (id INTEGER PRIMARY KEY, customer TEXT, status TEXT,"
          " last_synced_at TEXT, reconnect_required INT)")
BROKEN = {3, 5, 7, 10, 11, 15, 17, 20}          # 8 of 20 -> 12 remain in scope
c.executemany("INSERT INTO integrations VALUES (?,?,?,?,?)", [
    (i, f"cust-{i:02d}", "error" if i in BROKEN else "active",
     "2026-08-12T02:00:00" if i in BROKEN else "2026-09-14T02:00:00",
     1 if i in BROKEN else 0) for i in range(1, 21)])
c.execute("CREATE TABLE sync_runs (id INTEGER PRIMARY KEY, started_at TEXT,"
          " rows_synced INT, errors INT, result TEXT)")
c.executemany("INSERT INTO sync_runs (started_at,rows_synced,errors,result) VALUES (?,?,?,?)",
    [((datetime.datetime(2026, 9, 14) - datetime.timedelta(days=k)).isoformat(), 12, 0, "success")
     for k in range(21)])
con.commit(); con.close()
print("fixture:", d)
