"""Nightly export job."""
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"

# Roles that are allowed to write. The job writes, so read_only / anon do not count.
WRITE_ROLES = {"service_role"}


def stop(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def find_write_credential(creds, source):
    """Startup check: exactly one write-capable supabase credential must exist."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    writers = [c for c in supa if c.get("role") in WRITE_ROLES]
    if not supa:
        stop(f"no supabase credential in {source}. Cannot run.")
    if not writers:
        seen = ", ".join(f"{c['alias']} ({c.get('role')})" for c in supa)
        stop(f"supabase credentials in {source} exist but none can write "
             f"(need role in {sorted(WRITE_ROLES)}). Found: {seen}")
    if len(writers) > 1:
        names = ", ".join(c["alias"] for c in writers)
        stop(f"several write-capable supabase credentials in {source}, "
             f"cannot choose: {names}. Make the credential file contain only one.")
    return writers[0]


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        stop(f"cannot read credential file {CREDS}: {e}")
    cred = find_write_credential(creds, CREDS)
    print(f"credential file: {CREDS}", file=sys.stderr)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
