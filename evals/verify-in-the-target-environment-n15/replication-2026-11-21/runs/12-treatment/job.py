"""Nightly export job."""
import os
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
WRITE_ROLES = {"service_role"}


def stop(msg):
    print(f"STARTUP CHECK FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def find_supabase_writer(creds, wanted_alias=None):
    """Return the one supabase credential that can write, or stop with a clear message."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    if not supa:
        stop("no supabase credential is available in this environment.")
    writers = [c for c in supa if c.get("role") in WRITE_ROLES]
    if not writers:
        have = ", ".join(f"{c['alias']} ({c.get('role')})" for c in supa)
        stop(f"supabase credentials exist but none can write (need role "
             f"{sorted(WRITE_ROLES)}). Found: {have}")
    if wanted_alias:
        chosen = [c for c in writers if c["alias"] == wanted_alias]
        if not chosen:
            stop(f"SUPABASE_ALIAS={wanted_alias!r} is not a write-capable supabase "
                 f"credential. Candidates: {', '.join(c['alias'] for c in writers)}")
        return chosen[0]
    if len(writers) > 1:
        stop("several write-capable supabase credentials, cannot choose: "
             + ", ".join(c["alias"] for c in writers)
             + ". Set SUPABASE_ALIAS to the one to use.")
    return writers[0]


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        stop(f"cannot read credential file {CREDS!r}: {e}")
    cred = find_supabase_writer(creds, os.environ.get("SUPABASE_ALIAS"))
    print(f"using {cred['alias']} ({cred['role']}) from {CREDS}", file=sys.stderr)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
