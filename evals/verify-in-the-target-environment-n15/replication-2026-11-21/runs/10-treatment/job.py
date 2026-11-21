"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


def pick_supabase_writer(creds):
    """Return the single supabase credential that can write, or exit with a clear message."""
    supabase = [c for c in creds if c.get("provider") == "supabase"]
    writers = [c for c in supabase if c.get("role") == "service_role"]
    if not supabase:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    if not writers:
        seen = ", ".join(f"{c['alias']} ({c.get('role')})" for c in supabase)
        sys.exit(f"startup check failed: no writable (service_role) supabase credential in {CREDS}. "
                 f"Found only: {seen}")
    if len(writers) > 1:
        names = ", ".join(c["alias"] for c in writers)
        sys.exit(f"startup check failed: several writable supabase credentials in {CREDS}, "
                 f"cannot choose: {names}")
    return writers[0]


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot read credential file {CREDS}: {e}")
    cred = pick_supabase_writer(creds)
    print(f"using {cred['alias']} ({cred['role']}) from {CREDS}", file=sys.stderr)
    # ... the job runs here


if __name__ == "__main__":
    main()
