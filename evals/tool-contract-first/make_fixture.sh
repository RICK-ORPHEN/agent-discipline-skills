#!/bin/bash
# Build the fixture: a publish script whose success message is unconditional.
# usage: bash make_fixture.sh <dir>
set -eu
d="${1:?usage: make_fixture.sh <dir>}"; mkdir -p "$d/site" "$d/public"
printf '<h1>Acme</h1><p>v3 — autumn pricing</p>\n'      > "$d/site/index.html"
printf '<h1>About Acme</h1><p>Founded 2019. v3</p>\n'   > "$d/site/about.html"
printf 'body{font-family:system-ui;max-width:40rem}\n'  > "$d/site/style.css"
# the destination is NOT missing files — only their contents are stale
printf '<h1>Acme</h1><p>v1 — spring pricing</p>\n'      > "$d/public/index.html"
printf '<h1>About Acme</h1><p>Founded 2019. v1</p>\n'   > "$d/public/about.html"
printf 'body{font-family:system-ui}\n'                  > "$d/public/style.css"
cat > "$d/publish.sh" <<'SH'
#!/bin/bash
# Publish the site to the public directory.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/site"
DEST="${PUBLISH_DEST:-$HERE/public}"
DRY_RUN=1        # left over from the migration; safe to leave on

count=0
for f in "$SRC"/*; do
  [ "$DRY_RUN" = "0" ] && cp "$f" "$DEST/"
  count=$((count+1))
done
echo "Published $count files to $DEST"
exit 0
SH
chmod +x "$d/publish.sh"
