#!/bin/bash
# Build the fixture: an uploader whose exit code is honest and whose result is not.
# usage: bash make_fixture.sh <dir>   (expects uploader.py and README.md beside this script)
set -eu
d="${1:?usage: make_fixture.sh <dir>}"; here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$d/site" "$d/small-site"
printf '<h1>Acme</h1><p>autumn pricing</p>\n' > "$d/site/index.html"
printf '<h1>About</h1>\n'                     > "$d/site/about.html"
python3 -c "open('$d/site/style.css','w').write('/* theme */\n'+'.pad{margin:0}\n'*90)"
cp "$d/site/index.html" "$d/site/about.html" "$d/small-site/"
printf 'body{margin:0}\n' > "$d/small-site/style.css"
cp "$here/uploader.py" "$here/README.md" "$d/"
test "$(stat -c%s "$d/site/style.css")" -gt 1000 || { echo "fixture broken: style.css must exceed the cap"; exit 1; }
