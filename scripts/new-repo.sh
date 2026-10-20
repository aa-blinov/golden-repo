#!/usr/bin/env bash
# new-repo.sh — scaffold a new project from the house standard.
#
#   scripts/new-repo.sh <directory> [--name <display name>]
#
# The list of files comes from standard.json and the content comes from
# templates/, so the scaffolder and the checker cannot disagree about what a
# repository carries.
#
# It refuses to overwrite anything. If the target is not empty, it stops.

set -euo pipefail

STANDARD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

TARGET=""
DISPLAY_NAME=""
OWNER="aa-blinov"
YEAR="$(date +%Y)"

usage() {
  sed -n '2,11p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 2
}

while [ $# -gt 0 ]; do
  case "$1" in
    --name)        DISPLAY_NAME="$2"; shift 2 ;;
    --owner)       OWNER="$2"; shift 2 ;;
    --year)        YEAR="$2"; shift 2 ;;
    -h|--help)     usage ;;
    *)             TARGET="$1"; shift ;;
  esac
done

[ -n "$TARGET" ] || usage

TARGET_DIR="$(cd "$(dirname "$TARGET")" 2>/dev/null && pwd)/$(basename "$TARGET")" || TARGET_DIR="$TARGET"

if [ -e "$TARGET_DIR" ] && [ -n "$(ls -A "$TARGET_DIR" 2>/dev/null)" ]; then
  echo "new-repo: $TARGET_DIR is not empty; refusing to overwrite." >&2
  echo "           Use scripts/adopt.sh for an existing repository." >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

echo "new-repo: creating $TARGET_DIR"

python3 "$STANDARD_DIR/scripts/scaffold.py" new "$TARGET_DIR" \
  --name "${DISPLAY_NAME:-$(basename "$TARGET_DIR")}" \
  --owner "$OWNER" --year "$YEAR"

if [ -d "$TARGET_DIR/.git" ]; then
  echo "new-repo: the target is already a git repository; leaving git alone."
else
  git -C "$TARGET_DIR" init -q -b main 2>/dev/null || git -C "$TARGET_DIR" init -q
fi

cat <<EOF

new-repo: done.

  $TARGET_DIR

Next:
  1. Fill in PRODUCT.md — the product truth everything else is derived from.
  2. Fill in DESIGN.md, or delete it if the project has no visual system.
  3. Write the README: quick start, what it does, development, license.
  4. Run the checker:
       python3 $STANDARD_DIR/scripts/housecheck.py $TARGET_DIR

EOF
