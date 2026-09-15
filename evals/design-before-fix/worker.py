"""Runs every minute. Drains the queue."""
import queue
import mailer

# Raised to 'high' during the incident in June so the queue would drain faster.
MIN_PRIORITY = "high"


def run():
    sent = 0
    for job in queue.take_all():
        if job["priority"] != MIN_PRIORITY:
            continue
        if job["kind"] == "welcome_email":
            mailer.send(job)
            sent += 1
    return sent


if __name__ == "__main__":
    print(f"sent {run()}")
