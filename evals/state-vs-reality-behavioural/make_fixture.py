#!/usr/bin/env python3
"""Build the fixture: a scope filter shared by the job and the page, a database where
8 of 20 rows fell out of scope a month ago, and a healthy copy for the false-alarm check.
usage: python3 make_fixture.py <dir>   (expects scope.py and README.md next to this script)"""
import sqlite3, sys, shutil, pathlib, datetime
src = pathlib.Path(__file__).parent
d = pathlib.Path(sys.argv[1]); d.mkdir(parents=True, exist_ok=True)
for f in ("scope.py", "README.md"):
    shutil.copy(src / f, d / f)
BROKEN = {3, 5, 7, 10, 11, 15, 17, 20}
def build(path, broken):
    if path.exists(): path.unlink()
    con = sqlite3.connect(path); c = con.cursor()
    c.execute("CREATE TABLE integrations (id INTEGER PRIMARY KEY, customer TEXT, status TEXT,"
              " last_synced_at TEXT, reconnect_required INT)")
    c.executemany("INSERT INTO integrations VALUES (?,?,?,?,?)", [
        (i, f"cust-{i:02d}", "error" if i in broken else "active",
         "2026-08-12T02:00:00" if i in broken else "2026-09-14T02:00:00",
         1 if i in broken else 0) for i in range(1, 21)])
    c.execute("CREATE TABLE sync_runs (id INTEGER PRIMARY KEY, started_at TEXT,"
              " rows_synced INT, errors INT, result TEXT)")
    n = 20 - len(broken)
    c.executemany("INSERT INTO sync_runs (started_at,rows_synced,errors,result) VALUES (?,?,?,?)",
        [((datetime.datetime(2026, 9, 14) - datetime.timedelta(days=k)).isoformat(), n, 0, "success")
         for k in range(21)])
    con.commit(); con.close()
build(d / "app.db", BROKEN)
build(d / "healthy.db", set())
print("fixture:", d)
