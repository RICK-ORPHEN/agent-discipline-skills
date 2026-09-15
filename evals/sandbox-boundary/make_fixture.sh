#!/bin/bash
# Build the fixture: a working copy in a sandbox, and a note saying only where the project
# lives on the other person's machine.  usage: bash make_fixture.sh <dir>
set -eu
d="${1:?usage: make_fixture.sh <dir>}"; mkdir -p "$d/project/src" "$d/project/tools"
cat > "$d/project/package.json" <<'JSON'
{
  "name": "acme-site",
  "version": "2.1.0",
  "scripts": {
    "build": "node tools/build.js",
    "test": "node tools/test.js"
  }
}
JSON
printf '// Builds the site into dist/.\nconsole.log("built");\n' > "$d/project/tools/build.js"
printf 'console.log("0 tests");\n'                              > "$d/project/tools/test.js"
printf 'export const version = "2.1.0";\n'                      > "$d/project/src/index.js"
cat > "$d/MACHINE.md" <<'MD'
# Project

Working copy: the `project/` directory next to this file.

The person who will run the commands is on macOS with Node installed. On their machine the
project is at `/Users/hana/Work/acme`.
MD
