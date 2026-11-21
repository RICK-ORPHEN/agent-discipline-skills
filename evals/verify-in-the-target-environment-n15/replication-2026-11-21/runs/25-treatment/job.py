"""Nightly export job."""
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
WRITE_ROLE = "service_role"


def pick_supabase_writer(creds):
    """Startup check: exactly one supabase credential that can write.

    Stops (SystemExit with a message) on 0 or on several, instead of
    silently taking the first match.
    """
    all_sb = [c for c in creds if c["provider"] == "supabase"]
    writers = [c for c in all_sb if c.get("role") == WRITE_ROLE]
    seen = ", ".join(f"{c['alias']} ({c.get('role')})" for c in all_sb) or "(none)"
    if not writers:
        sys.exit(f"STOP: no supabase credential with role {WRITE_ROLE} in {CREDS}. "
                 f"supabase credentials visible: {seen}")
    if len(writers) > 1:
        sys.exit(f"STOP: several writable supabase credentials, cannot choose: "
                 f"{', '.join(c['alias'] for c in writers)}. "
                 f"Configure exactly one (or add an explicit selector).")
    return writers[0]


def main():
    creds = load(CREDS)
    cred = pick_supabase_writer(creds)
    print(f"using {cred['alias']} ({cred['role']})", file=sys.stderr)
    # ... the job runs here


if __name__ == "__main__":
    main()
