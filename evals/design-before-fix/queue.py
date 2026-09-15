"""In-memory job queue backed by a file."""
import json
from pathlib import Path

QUEUE = Path(__file__).parent / "queue.json"


def enqueue(kind, payload, priority="low"):
    jobs = json.loads(QUEUE.read_text()) if QUEUE.exists() else []
    jobs.append({"kind": kind, "payload": payload, "priority": priority})
    QUEUE.write_text(json.dumps(jobs, indent=1))


def take_all():
    jobs = json.loads(QUEUE.read_text()) if QUEUE.exists() else []
    QUEUE.write_text("[]")
    return jobs
