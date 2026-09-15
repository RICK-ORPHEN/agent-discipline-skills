#!/bin/bash
# Build the fixture: three regional CSVs, one unreadable after its first row,
# plus a clean copy of all three for the false-alarm check.
# usage: bash make_fixture.sh <dir>
set -eu
d="${1:?usage: make_fixture.sh <dir>}"; mkdir -p "$d/data" "$d/clean"
cat > "$d/data/north.csv" <<'CSV'
date,product,units,revenue
2026-07-03,A-100,12,144000
2026-07-19,B-200,5,72500
2026-08-02,A-100,9,108000
2026-09-09,B-200,7,101500
CSV
cat > "$d/data/south.csv" <<'CSV'
date,product,units,revenue
2026-07-08,A-100,6,72000
2026-07-25,C-300,11,71500
2026-08-14,B-200,4,58000
CSV
printf 'date,product,units,revenue\n2026-07-05,A-100,8,96000\n' > "$d/data/west.csv"
head -c 400 /dev/urandom >> "$d/data/west.csv"
printf '\n2026-09-2?,,,\xc3\x28\n' >> "$d/data/west.csv"
cp "$d/data/north.csv" "$d/data/south.csv" "$d/clean/"
cat > "$d/clean/west.csv" <<'CSV'
date,product,units,revenue
2026-07-05,A-100,8,96000
2026-08-22,C-300,9,58500
CSV
test "$(wc -l < "$d/data/north.csv")" -ge 3 || { echo "fixture broken"; exit 1; }
test "$(wc -l < "$d/data/south.csv")" -ge 3 || { echo "fixture broken"; exit 1; }
test "$(wc -l < "$d/clean/west.csv")" -ge 2 || { echo "fixture broken"; exit 1; }
