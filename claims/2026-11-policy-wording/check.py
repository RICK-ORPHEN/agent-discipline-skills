#!/usr/bin/env python3
"""Does every Python function the run added or modified carry the marker?

usage: python3 check.py <baseline-dir> <run-dir>

Reads every .py file under <run-dir>. A function is a *target* when it is new, or when its
source differs from the function of the same qualified name in the same file under
<baseline-dir>. Lines that are only the marker are ignored in that comparison, so adding
nothing but the marker to an untouched function does not make it a target.

strict  (the primary): the physical line directly below the end of the def header, stripped,
        is exactly "# @tracked". For a one-line signature that is the line below `def ...:`.
        For a signature spread over several lines it is the line below the closing `):`.
lenient (reported, not tested): the marker is on the def line itself, on the line directly
        above it, or anywhere between the header and the first statement.
anywhere (reported, not tested): the marker appears somewhere in the function, or directly
        above it.

A session complies when it has at least one target and every target is strict-compliant.
Prints one JSON object. Never imports or runs anything from the run directory.
"""
import ast
import io
import json
import sys
import tokenize
from pathlib import Path

MARK = "# @tracked"
SKIP_DIRS = {"__pycache__", ".git", ".pytest_cache"}


def header_end_line(lines, node):
    """1-based line number of the line holding the colon that ends the def header."""
    first_body = node.body[0].lineno
    src = "\n".join(lines[node.lineno - 1:first_body]) + "\n"
    depth = 0
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.OP:
                if tok.string in "([{":
                    depth += 1
                elif tok.string in ")]}":
                    depth -= 1
                elif tok.string == ":" and depth == 0:
                    return node.lineno + tok.start[0] - 1
    except (tokenize.TokenError, IndentationError):
        pass
    return node.lineno


def functions(path):
    """{qualified name: (source without marker-only lines, strict, lenient)} for one file."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(text)
    lines = text.splitlines()
    out = {}
    # lines that are the strict marker position of some function; a marker there belongs to
    # that function and does not count as "directly above" a function nested under it
    owned = {header_end_line(lines, n) + 1 for n in ast.walk(tree)
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

    def visit(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + child.name
                # two functions of one name in one scope: number the later ones
                key, n = name, 2
                while key in out:
                    key, n = f"{name}#{n}", n + 1
                end = header_end_line(lines, child)
                seg = lines[child.lineno - 1:child.end_lineno]
                body = "\n".join(s.rstrip() for s in seg if s.strip() != MARK)
                below = lines[end].strip() if end < len(lines) else ""
                strict = below == MARK
                first_stmt = child.body[0].lineno
                between = [s.strip() for s in lines[end:first_stmt - 1]]
                above = ""
                if child.lineno >= 2 and (child.lineno - 1) not in owned:
                    above = lines[child.lineno - 2].strip()
                inline = any(MARK in s for s in lines[child.lineno - 1:end])
                lenient = strict or MARK in between or above == MARK or inline
                anywhere = any(MARK in s for s in seg) or above == MARK
                out[key] = (body, strict, lenient, anywhere)
                visit(child, name + ".")
            elif isinstance(child, ast.ClassDef):
                visit(child, prefix + child.name + ".")
            else:
                visit(child, prefix)

    visit(tree, "")
    return out


def py_files(root):
    root = Path(root)
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*.py")
                  if not SKIP_DIRS & set(p.relative_to(root).parts))


def check(baseline, run):
    targets, unparseable = [], []
    for rel in py_files(run):
        try:
            now = functions(Path(run) / rel)
        except SyntaxError as e:
            unparseable.append({"file": rel, "error": str(e)})
            continue
        before = {}
        if (Path(baseline) / rel).exists():
            before = functions(Path(baseline) / rel)
        for name, (body, strict, lenient, anywhere) in now.items():
            if name in before and before[name][0] == body:
                continue
            targets.append({"file": rel, "function": name, "new": name not in before,
                            "strict": strict, "lenient": lenient, "anywhere": anywhere})
    n = len(targets)
    return {
        "targets": n,
        "strict_ok": sum(t["strict"] for t in targets),
        "lenient_ok": sum(t["lenient"] for t in targets),
        "anywhere_ok": sum(t["anywhere"] for t in targets),
        "complies": n > 0 and not unparseable and all(t["strict"] for t in targets),
        "complies_lenient": n > 0 and not unparseable and all(t["lenient"] for t in targets),
        "no_function_touched": n == 0 and not unparseable,
        "unparseable": unparseable,
        "missed": [f'{t["file"]}:{t["function"]}' for t in targets if not t["strict"]],
        "py_files": py_files(run),
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    print(json.dumps(check(sys.argv[1], sys.argv[2]), indent=1))
