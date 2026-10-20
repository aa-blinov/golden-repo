#!/usr/bin/env bash
# new-repo.sh — scaffold a new project from the house standard.
#
#   scripts/new-repo.sh <directory> [--name <display name>] [--description <text>]
#
# Copies templates/ into the target, substitutes the tokens, and leaves a
# repository that already passes the checker. Fill in PRODUCT.md first: the
# rest of the repository is derived from it.
#
# It refuses to overwrite anything. If the target is not empty, it stops.

set -euo pipefail

STANDARD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES_DIR="$STANDARD_DIR/templates"

TARGET=""
DISPLAY_NAME=""
DESCRIPTION=""
LICENSE_HOLDER="Alexander Blinov"
YEAR="$(date +%Y)"
OWNER="aa-blinov"

usage() {
  sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 2
}

while [ $# -gt 0 ]; do
  case "$1" in
    --name)        DISPLAY_NAME="$2"; shift 2 ;;
    --description) DESCRIPTION="$2"; shift 2 ;;
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

if [ -z "$DISPLAY_NAME" ]; then
  DISPLAY_NAME="$(basename "$TARGET_DIR")"
fi

if [ -z "$DESCRIPTION" ]; then
  DESCRIPTION="One line that says what this does and who it is for."
fi

SLUG="$(basename "$TARGET_DIR")"

if [ ! -d "$TEMPLATES_DIR" ]; then
  echo "new-repo: templates not found at $TEMPLATES_DIR" >&2
  exit 1
fi

echo "new-repo: creating $TARGET_DIR"

mkdir -p "$TARGET_DIR"

# Copy the templates, preserving the directory structure.
( cd "$TEMPLATES_DIR" && find . -type f -print ) | while read -r rel; do
  clean="${rel#./}"
  mkdir -p "$TARGET_DIR/$(dirname "$clean")"
  cp "$TEMPLATES_DIR/$clean" "$TARGET_DIR/$clean"
done

# Substitute the tokens. One pass with sed, so that a value containing a
# slash does not break the expression.
while read -r rel; do
  clean="${rel#./}"
  target="$TARGET_DIR/$clean"
  [ -f "$target" ] || continue
  sed -i.bak \
    -e "s|{{PROJECT_NAME}}|$DISPLAY_NAME|g" \
    -e "s|{{PROJECT_SLUG}}|$SLUG|g" \
    -e "s|{{PROJECT_DESCRIPTION}}|$DESCRIPTION|g" \
    -e "s|{{PROJECT_TAGLINE}}|One line that says what this does.|g" \
    -e "s|{{LICENSE_HOLDER}}|$LICENSE_HOLDER|g" \
    -e "s|{{PROJECT_YEAR}}|$YEAR|g" \
    -e "s|{{REPO_OWNER}}|$OWNER|g" \
    -e "s|{{REPO_URL}}|https://github.com/$OWNER/$SLUG|g" \
    -e "s|{{INSTALL_COMMAND}}|echo 'replace with the install command'|g" \
    -e "s|{{TEST_COMMAND}}|echo 'replace with the test command'|g" \
    -e "s|{{BUILD_COMMAND}}|echo 'replace with the build command'|g" \
    -e "s|{{SURFACE_ONE}}|the network interface, and the files it reads|g" \
    -e "s|{{SURFACE_TWO}}|the dependency tree|g" \
    "$target"
  rm -f "$target.bak"
done < <( cd "$TEMPLATES_DIR" && find . -type f -print )

# The directories the standard requires, whether or not a template filled them.
mkdir -p "$TARGET_DIR/.github/workflows" \
         "$TARGET_DIR/.github/ISSUE_TEMPLATE" \
         "$TARGET_DIR/.impeccable" \
         "$TARGET_DIR/docs/screenshots" \
         "$TARGET_DIR/scripts" \
         "$TARGET_DIR/src" \
         "$TARGET_DIR/tests"

# Empty directories are not tracked by git. A .gitkeep keeps the shape.
for dir in src tests docs/screenshots; do
  [ -z "$(ls -A "$TARGET_DIR/$dir" 2>/dev/null)" ] && touch "$TARGET_DIR/$dir/.gitkeep"
done

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
