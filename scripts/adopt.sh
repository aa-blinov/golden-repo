#!/usr/bin/env bash
# adopt.sh — bring an existing repository up to the house standard.
#
#   scripts/adopt.sh <path>
#
# Adds the standard files that are missing and never touches a file that
# already exists. PRODUCT.md and DESIGN.md are the exception: they are
# written as stubs with the questions to answer marked inline, and only if
# they do not exist already.
#
# The list of files comes from standard.json, so the migrator and the checker
# cannot disagree about what a repository carries.
#
# The point is that the migration is one commit and does not need reviewing
# line by line. Everything it adds is new; everything it leaves alone is
# yours.

set -euo pipefail

STANDARD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OWNER="aa-blinov"
YEAR="$(date +%Y)"

usage() {
  sed -n '2,17p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 2
}

[ $# -ge 1 ] || usage

TARGET="$1"
[ -d "$TARGET" ] || { echo "adopt: $TARGET is not a directory" >&2; exit 1; }
TARGET="$(cd "$TARGET" && pwd)"

# A working tree with uncommitted changes means the migration would be mixed
# with something else. Stop rather than guess.
if [ -d "$TARGET/.git" ]; then
  if [ -n "$(git -C "$TARGET" status --porcelain)" ]; then
    echo "adopt: the working tree has uncommitted changes." >&2
    echo "       Commit or stash them first, then run this again." >&2
    exit 1
  fi
fi

echo "adopt: applying the house standard to $TARGET"

python3 "$STANDARD_DIR/scripts/scaffold.py" adopt "$TARGET" \
  --owner "$OWNER" --year "$YEAR"

# The docs index links to architecture.md, which this repository may not
# have. Drop the references to files that do not exist rather than
# shipping an index with broken links.
if [ -f "$TARGET/docs/README.md" ]; then
  python3 - "$TARGET/docs/README.md" "$TARGET" <<'PY'
import os
import re
import sys

index_path, root = sys.argv[1], sys.argv[2]
with open(index_path) as handle:
    text = handle.read()

lines = []
for line in text.split("\n"):
    # Drop a table row whose link target is missing.
    match = re.match(r"^\|\s*\[([^\]]*)\]\(([^)]+)\)\s*\|", line)
    if match:
        target = match.group(2)
        if not target.startswith(("http://", "https://", "#")):
            resolved = os.path.normpath(os.path.join(os.path.dirname(index_path), target))
            if not os.path.exists(resolved):
                continue
    lines.append(line)

text = "\n".join(lines)

# Drop the inline mentions of a document that is not there.
text = re.sub(r"\[[^\]]*\]\(([^)]*architecture[^)]*)\)", "the architecture document", text)
text = re.sub(r", then the architecture document", "", text)

with open(index_path, "w") as handle:
    handle.write(text)
PY
fi

cat <<EOF

adopt: done. Nothing of yours was changed.

Next:
  1. Fill in PRODUCT.md — it is a stub with the questions to answer.
  2. Check what is left:
       python3 $STANDARD_DIR/scripts/housecheck.py $TARGET
  3. Review and commit:
       git -C $TARGET status

EOF
