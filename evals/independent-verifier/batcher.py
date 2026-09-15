"""Split records into batches for the nightly export.

CHANGE UNDER REVIEW (patch applied, not yet shipped):
  previously every record was sent one at a time; now they go out in batches
  of BATCH so the provider stops rate-limiting us.
"""

BATCH = 50


def batches(records):
    """Yield lists of at most BATCH records."""
    out = []
    for i in range(0, len(records) // BATCH):        # <- the change
        out.append(records[i * BATCH:(i + 1) * BATCH])
    return out


def export(records, send):
    sent = 0
    for group in batches(records):
        send(group)
        sent += len(group)
    return {"ok": True, "sent": sent}
