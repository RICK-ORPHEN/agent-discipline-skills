"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


WRITE_ROLE = "service_role"


def check_credentials(creds):
    """Stop early unless a write-capable supabase credential is available."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    writers = [c for c in supa if c.get("role") == WRITE_ROLE]
    if not supa:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    if not writers:
        roles = ", ".join(f"{c['alias']} ({c.get('role')})" for c in supa)
        sys.exit(f"startup check failed: no supabase credential with role "
                 f"{WRITE_ROLE!r} in {CREDS}; found: {roles}")
    if len(writers) > 1:
        names = ", ".join(c["alias"] for c in writers)
        print(f"warning: {len(writers)} writable supabase credentials ({names}); "
              f"resolve() will pick the first", file=sys.stderr)


def main():
    creds = load(CREDS)
    check_credentials(creds)
    cred = resolve("supabase", creds)
    if cred.get("role") != WRITE_ROLE:
        sys.exit(f"startup check failed: resolve() chose {cred['alias']} "
                 f"(role {cred.get('role')}), which cannot write")
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
