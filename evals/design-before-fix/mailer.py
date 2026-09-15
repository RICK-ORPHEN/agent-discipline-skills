"""Render and write outgoing mail."""
from pathlib import Path

OUTBOX = Path(__file__).parent / "outbox"

TEMPLATE = "Hello {name},\n\nWelcome to Acme.\n"


def send(job):
    OUTBOX.mkdir(exist_ok=True)
    body = TEMPLATE.format(name=job["payload"]["name"])
    (OUTBOX / f"{job['payload']['email']}.txt").write_text(body)
