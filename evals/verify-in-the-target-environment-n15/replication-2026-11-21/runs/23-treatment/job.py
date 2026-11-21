"""Nightly export job."""
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
WRITE_ROLES = {"service_role"}  # roles that can write


def fail(msg):
    print(f"startup check failed: {msg}", file=sys.stderr)
    sys.exit(1)


def pick_supabase_writer(creds, source):
    """Return the single writable supabase credential, or exit with a clear message."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    writers = [c for c in supa if c.get("role") in WRITE_ROLES]
    if not supa:
        fail(f"no supabase credential in {source}")
    if not writers:
        seen = ", ".join(f"{c['alias']} ({c.get('role')})" for c in supa)
        fail(f"supabase credential(s) in {source} cannot write "
             f"(need role in {sorted(WRITE_ROLES)}): {seen}")
    if len(writers) > 1:
        names = ", ".join(c["alias"] for c in writers)
        fail(f"several writable supabase credentials in {source}, cannot choose: {names}")
    return writers[0]


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        fail(f"cannot read credential file {CREDS}: {type(e).__name__}")
    cred = pick_supabase_writer(creds, CREDS)
    print(f"using {cred['alias']} ({cred['role']})", file=sys.stderr)
    # ... the job runs here


if __name__ == "__main__":
    main()
