#!/usr/bin/env python3
"""Check that paths baked into a git worktree (or a symlink) resolve on the machine that uses it.

The incident this exists for:
  `git worktree add` was run from a sandbox, so `/sessions/<session>/mnt/...` was written into
  `.git` and into the admin `gitdir`. That path does not exist on the user's machine, so git
  there returns `fatal: not a git repository`. Eight commits were stacked in that worktree and
  reported as "entirely done".

This check exists to fail before that report is made.

Usage:
    python3 check_worktree_paths.py <worktree path> [--host-home /Users/<user>]

exit 0 = resolvable from the host / exit 1 = not resolvable (prints what to fix)
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Sandbox-side mount prefixes. If one of these is baked in, the host cannot resolve it.
SANDBOX_PREFIXES = ("/sessions/", "/home/claude/", "/tmp/")


def fail(problems: list[str], message: str) -> None:
    problems.append(message)


def check_worktree(worktree: Path, host_home: str, problems: list[str]) -> None:
    dotgit = worktree / ".git"
    if not dotgit.exists():
        fail(problems, f"{dotgit} is missing (not a worktree, or it is broken)")
        return

    if dotgit.is_dir():
        print(f"  {worktree.name}: ordinary repository (.git is a directory) — not applicable")
        return

    raw = dotgit.read_text(encoding="utf-8").strip()
    if not raw.startswith("gitdir:"):
        fail(problems, f"unexpected format in {dotgit}: {raw[:80]!r}")
        return

    gitdir_value = raw[len("gitdir:"):].strip()
    print(f"  .git      -> {gitdir_value}")

    if gitdir_value.startswith(SANDBOX_PREFIXES):
        fail(
            problems,
            f"{dotgit} has a sandbox absolute path baked in.\n"
            f"      now: {gitdir_value}\n"
            f"      fix: rewrite as a relative path "
            f"(a path relative to this worktree, pointing up into "
            f"<parent repo dir>/.git/worktrees/<worktree name>)",
        )
        return

    if not gitdir_value.startswith("/"):
        resolved = (worktree / gitdir_value).resolve()
        if not resolved.exists():
            fail(problems, f"relative gitdir does not resolve: {gitdir_value} -> {resolved}")
            return
        admin = resolved
    else:
        # A host absolute path cannot be existence-checked from the sandbox.
        # Only its shape can be validated.
        if not gitdir_value.startswith(host_home):
            fail(problems,
                 f"gitdir is neither a host path nor sandbox-relative: {gitdir_value}")
            return
        print("      (host absolute path; shape checked only — cannot verify existence here)")
        return

    admin_gitdir = admin / "gitdir"
    if not admin_gitdir.exists():
        fail(problems, f"{admin_gitdir} is missing")
        return

    back = admin_gitdir.read_text(encoding="utf-8").strip()
    print(f"  gitdir    -> {back}")

    if back.startswith(SANDBOX_PREFIXES):
        fail(
            problems,
            f"{admin_gitdir} has a sandbox absolute path baked in.\n"
            f"      now: {back}\n"
            f"      fix: rewrite as the host absolute path ({host_home}/...)\n"
            f"      WARNING: never make this one relative. `git worktree list` marks it\n"
            f"        prunable and a prune deletes the worktree bookkeeping (measured)",
        )
        return

    if not back.startswith("/"):
        fail(
            problems,
            f"{admin_gitdir} is a relative path: {back}\n"
            f"      -> git will mark it prunable. Use the host absolute path",
        )
        return

    if not back.startswith(host_home):
        fail(problems, f"{admin_gitdir} is not a host path: {back}")


def check_symlinks(worktree: Path, problems: list[str]) -> None:
    """Detect absolute symlinks (node_modules and friends). Relative ones work in both."""
    for entry in sorted(worktree.iterdir()):
        if not entry.is_symlink():
            continue
        target = os.readlink(entry)
        if target.startswith(SANDBOX_PREFIXES):
            fail(
                problems,
                f"symlink {entry.name} points at a sandbox absolute path: {target}\n"
                f"      -> relink it as a relative path",
            )
        else:
            print(f"  symlink   {entry.name} -> {target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("worktree", help="path of the worktree to check")
    parser.add_argument("--host-home", default=str(Path.home()),
                        help="home prefix on the machine a human uses (default: $HOME here)")
    args = parser.parse_args()

    worktree = Path(args.worktree).resolve()
    if not worktree.is_dir():
        print(f"x no such directory: {worktree}", file=sys.stderr)
        return 1

    print(f"# worktree path check: {worktree}")
    problems: list[str] = []
    check_worktree(worktree, args.host_home, problems)
    check_symlinks(worktree, problems)

    if not problems:
        print("\nOK resolvable from the host machine")
        return 0

    print(f"\nx {len(problems)} problem(s)", file=sys.stderr)
    for problem in problems:
        print(f"  - {problem}", file=sys.stderr)
    print(
        "\nHanding a command to the user in this state produces "
        "`fatal: not a git repository`.\nFix it before handing it over.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
