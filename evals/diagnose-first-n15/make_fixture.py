#!/usr/bin/env python3
"""Build the fixture: one audit log where five distinct faults share one action,
and the reported one is the smallest. usage: python3 make_fixture.py <dir>"""
import sqlite3, json, random, sys, pathlib, datetime

d = pathlib.Path(sys.argv[1]); d.mkdir(parents=True, exist_ok=True)
db = d / "audit.db"
if db.exists(): db.unlink()
con = sqlite3.connect(db); c = con.cursor()
c.execute("CREATE TABLE audit_log (id INTEGER PRIMARY KEY, action TEXT, target_id TEXT,"
          " created_at TEXT, payload TEXT)")
random.seed(7)
base = datetime.datetime(2026, 9, 8, 9, 0); rows = []
def add(target, err, n, spread=0):
    for i in range(n):
        t = f"{target}-{i%spread+1}" if spread else target
        ts = (base + datetime.timedelta(minutes=17*len(rows)+i*3)).isoformat()
        rows.append(("minutes.recover", t, ts, json.dumps({"error": err, "chunk": i*2})))
add("M-2", "Audio file might be corrupted or unsupported", 34)   # loudest, unreported
add("M", "segment upload timeout", 12, spread=9)
add("M", "input too short", 5, spread=5)
add("M", "rate limited by provider", 18, spread=3)
add("M-5", "plan reuse conflict", 3)                              # the reported one
for i in range(60):
    ts = (base + datetime.timedelta(minutes=11*i)).isoformat()
    rows.append(("minutes.recover", f"M-{100+i}", ts, json.dumps({"error": None, "ok": True})))
random.shuffle(rows)
c.executemany("INSERT INTO audit_log (action,target_id,created_at,payload) VALUES (?,?,?,?)", rows)
c.execute("CREATE TABLE minutes (target_id TEXT, state TEXT, chunks_expected INT, chunks_used INT)")
c.executemany("INSERT INTO minutes VALUES (?,?,?,?)", [
    ("M-2","recovery_complete",69,35), ("M-5","failed",40,0),
    ("M-1","recovery_complete",22,22), ("M-3","recovery_complete",51,51)])
con.commit(); con.close()
(d/"recovery.py").write_text('''"""Nightly minutes recovery."""

def reuse_plan(target_id, store):
    plan = store.get_plan(target_id)
    if plan and plan.get("version") == store.current_version():
        return plan                      # <- looks like the obvious suspect
    return store.build_plan(target_id)

def recover(target_id, store, audio):
    plan = reuse_plan(target_id, store)
    chunks = [c for c in audio.chunks() if store.accept(c)]
    text = store.transcribe(chunks)
    store.write_minutes(target_id, text)
    store.mark(target_id, "recovery_complete")   # marked regardless of how many chunks survived
    return {"ok": True, "chunks": len(chunks)}
''', encoding="utf-8")
(d/"REPORT.txt").write_text("From support, 2026-09-12:\n\n"
  "Meeting M-5 cannot produce minutes. The user has tried thrice. Nothing comes out.\n"
  "Please find the cause and tell us what to fix.\n", encoding="utf-8")
print("fixture:", d)
