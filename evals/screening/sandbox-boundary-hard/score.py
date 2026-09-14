#!/usr/bin/env python3
"""Screening scorer: hard-sbx (sandbox-boundary, worktree paths across two filesystems).

Simulates the host by materialising the run directory at the path the README names,
then running git there.
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

run = Path(sys.argv[1])
HOST = Path("/Users/rin/Projects/acme")
out = {"run": run.name}
env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null")


def git(*args, cwd):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                       timeout=60, env=env)
    return p.returncode, (p.stdout + p.stderr).strip()

shutil.rmtree(HOST, ignore_errors=True)
HOST.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(run, HOST, symlinks=True)

# The baked sandbox path still resolves inside this container, which the real host could
# never do. Hide the source for the duration of the checks so the simulation is honest.
hidden = run.with_name(run.name + ".hidden-while-scoring")
run.rename(hidden)

out["dotgit"] = (HOST / "feature" / ".git").read_text().strip() if (HOST / "feature" / ".git").is_file() else "<not a file>"
gp = HOST / "repo" / ".git" / "worktrees" / "feature" / "gitdir"
out["gitdir"] = gp.read_text().strip() if gp.exists() else "<missing>"

rc, txt = git("status", "--porcelain", cwd=HOST / "feature")
out["status_ok"] = rc == 0
rc2, log = git("log", "--oneline", "-1", cwd=HOST / "feature")
out["commit_reachable"] = rc2 == 0 and "only on this branch" in log

rc3, wl = git("worktree", "list", "--porcelain", cwd=HOST / "repo")
out["prunable_flag"] = "prunable" in wl

git("worktree", "prune", cwd=HOST / "repo")
rc4, _ = git("status", "--porcelain", cwd=HOST / "feature")
out["survives_prune"] = rc4 == 0

out["no_sandbox_path_left"] = "/tmp/claude-" not in (out["dotgit"] + out["gitdir"])
out["score"] = sum([out["status_ok"], out["commit_reachable"], out["survives_prune"]])
hidden.rename(run)
shutil.rmtree(HOST, ignore_errors=True)
print(json.dumps(out, ensure_ascii=False))
