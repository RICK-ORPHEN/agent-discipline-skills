"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
# Roles treated as able to write. Assumption: confirm against the real role values.
WRITE_ROLES = {"write", "writer", "read-write", "readwrite", "service_role", "admin"}


def require_supabase_writer(creds, path):
    """Startup check: exit with a clear message if no write-capable supabase credential exists."""
    found = [c for c in creds if c.get("provider") == "supabase"]
    if not found:
        sys.exit(f"ERROR: no supabase credential in {path}. The job needs one that can write.")
    writers = [c for c in found if str(c.get("role", "")).lower() in WRITE_ROLES]
    if not writers:
        have = ", ".join(f"{c.get('alias', '?')} ({c.get('role', '?')})" for c in found)
        sys.exit(f"ERROR: supabase credential(s) in {path} cannot write: {have}. "
                 "The job needs a write-capable one.")
    return writers[0]


def main():
    creds = load(CREDS)
    cred = require_supabase_writer(creds, CREDS)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
