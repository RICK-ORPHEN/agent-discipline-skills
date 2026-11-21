"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


def check_supabase_credential(creds, source):
    """Stop early unless exactly one writable supabase credential is available."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    writable = [c for c in supa if c.get("role") == "service_role"]
    print(f"  credential file: {source}", file=sys.stderr)
    print(
        "  supabase entries: "
        + (", ".join(f"{c['alias']} ({c.get('role')})" for c in supa) or "(none)"),
        file=sys.stderr,
    )
    if not writable:
        sys.exit(
            f"ERROR: no writable supabase credential (role service_role) in {source}. "
            "The job needs one; add it before running."
        )
    if len(writable) > 1:
        sys.exit(
            f"ERROR: several writable supabase credentials in {source}, cannot choose: "
            + ", ".join(c["alias"] for c in writable)
            + ". Leave exactly one service_role supabase credential."
        )
    return writable[0]


def main():
    creds = load(CREDS)
    cred = check_supabase_credential(creds, CREDS)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
