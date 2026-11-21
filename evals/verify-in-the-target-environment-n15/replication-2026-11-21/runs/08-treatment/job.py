"""Nightly export job."""
import os
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
WRITER_ROLE = "service_role"


def stop(msg):
    print(f"STARTUP CHECK FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def pick_supabase_writer(creds, wanted=None):
    """Return the one supabase credential that can write, or stop with a clear message."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    if not supa:
        stop(f"no supabase credential in {CREDS}")
    writers = [c for c in supa if c.get("role") == WRITER_ROLE]
    if not writers:
        have = ", ".join(f"{c['alias']} ({c.get('role')})" for c in supa)
        stop(f"supabase credential(s) found but none can write (need role {WRITER_ROLE}): {have}")
    if wanted:
        chosen = [c for c in writers if c["alias"] == wanted]
        if len(chosen) != 1:
            stop(f"SUPABASE_ALIAS={wanted} is not a writable supabase credential; "
                 f"choices: {', '.join(c['alias'] for c in writers)}")
        return chosen[0]
    if len(writers) > 1:
        stop("several writable supabase credentials, cannot choose: "
             + ", ".join(c["alias"] for c in writers)
             + ". Set SUPABASE_ALIAS to one of them.")
    return writers[0]


def main():
    creds = load(CREDS)
    cred = pick_supabase_writer(creds, os.environ.get("SUPABASE_ALIAS"))
    print(f"using {cred['alias']} ({cred['role']})", file=sys.stderr)
    # ... the job runs here


if __name__ == "__main__":
    main()
