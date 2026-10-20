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
# The point is that the migration is one commit and does not need reviewing
# line by line. Everything it adds is new; everything it leaves alone is
# yours.

set -euo pipefail

STANDARD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES_DIR="$STANDARD_DIR/templates"
LICENSE_HOLDER="Alexander Blinov"
YEAR="$(date +%Y)"

usage() {
  sed -n '2,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 2
}

[ $# -ge 1 ] || usage

TARGET="$1"
[ -d "$TARGET" ] || { echo "adopt: $TARGET is not a directory" >&2; exit 1; }
TARGET="$(cd "$TARGET" && pwd)"
SLUG="$(basename "$TARGET")"

ADDED=()
SKIPPED=()

add_file() {
  # add_file <relative path> <source relative path>
  local rel="$1" src="$2"
  if [ -e "$TARGET/$rel" ]; then
    SKIPPED+=("$rel")
    return
  fi
  mkdir -p "$(dirname "$TARGET/$rel")"
  cp "$TEMPLATES_DIR/$src" "$TARGET/$rel"
  ADDED+=("$rel")
}

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

# The root file set.
add_file "README.md" "README.md"
add_file "AGENTS.md" "AGENTS.md"
add_file "CHANGELOG.md" "CHANGELOG.md"
add_file "CONTRIBUTING.md" "CONTRIBUTING.md"
add_file "CODE_OF_CONDUCT.md" "CODE_OF_CONDUCT.md"
add_file "SECURITY.md" "SECURITY.md"
add_file ".gitignore" ".gitignore"
add_file ".editorconfig" ".editorconfig"

# LICENSE only when there is none. An existing licence is the owner's choice
# and is never second-guessed.
add_file "LICENSE" "LICENSE"

# PRODUCT.md and DESIGN.md are stubs here. The migrator cannot know the
# product truth, so it writes the questions instead of inventing answers.
add_file "PRODUCT.md" "PRODUCT.md"
add_file "DESIGN.md" "DESIGN.md"

# The .github directory.
add_file ".github/PULL_REQUEST_TEMPLATE.md" ".github/PULL_REQUEST_TEMPLATE.md"
add_file ".github/dependabot.yml" ".github/dependabot.yml"
add_file ".github/ISSUE_TEMPLATE/bug_report.md" ".github/ISSUE_TEMPLATE/bug_report.md"
add_file ".github/ISSUE_TEMPLATE/feature_request.md" ".github/ISSUE_TEMPLATE/feature_request.md"
add_file ".github/ISSUE_TEMPLATE/config.yml" ".github/ISSUE_TEMPLATE/config.yml"
add_file ".github/workflows/ci.yml" ".github/workflows/ci.yml"
add_file ".github/workflows/release.yml" ".github/workflows/release.yml"

# The design sidecar and the rest of the directories.
add_file ".impeccable/config.json" ".impeccable/config.json"
add_file ".impeccable/design.json" ".impeccable/design.json"
add_file "docs/README.md" "docs/README.md"

for dir in .github/workflows .github/ISSUE_TEMPLATE .impeccable docs docs/screenshots scripts src tests; do
  mkdir -p "$TARGET/$dir"
done

for dir in src tests docs/screenshots; do
  if [ -z "$(ls -A "$TARGET/$dir" 2>/dev/null)" ]; then
    touch "$TARGET/$dir/.gitkeep"
  fi
done

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

# Substitute the tokens in the files that were just added.
for rel in "${ADDED[@]}"; do
  [ -f "$TARGET/$rel" ] || continue
  sed -i.bak \
    -e "s|{{PROJECT_NAME}}|$SLUG|g" \
    -e "s|{{PROJECT_SLUG}}|$SLUG|g" \
    -e "s|{{PROJECT_DESCRIPTION}}|One line that says what this does.|g" \
    -e "s|{{PROJECT_TAGLINE}}|One line that says what this does.|g" \
    -e "s|{{LICENSE_HOLDER}}|$LICENSE_HOLDER|g" \
    -e "s|{{PROJECT_YEAR}}|$YEAR|g" \
    -e "s|{{REPO_OWNER}}|aa-blinov|g" \
    -e "s|{{REPO_URL}}|https://github.com/aa-blinov/$SLUG|g" \
    -e "s|{{INSTALL_COMMAND}}|echo 'replace with the install command'|g" \
    -e "s|{{TEST_COMMAND}}|echo 'replace with the test command'|g" \
    -e "s|{{BUILD_COMMAND}}|echo 'replace with the build command'|g" \
    -e "s|{{SURFACE_ONE}}|the network interface, and the files it reads|g" \
    -e "s|{{SURFACE_TWO}}|the dependency tree|g" \
    "$TARGET/$rel"
  rm -f "$TARGET/$rel.bak"
done

echo
if [ ${#ADDED[@]} -gt 0 ]; then
  echo "added:"
  for rel in "${ADDED[@]}"; do
    echo "  + $rel"
  done
fi

if [ ${#SKIPPED[@]} -gt 0 ]; then
  echo
  echo "left alone (already present):"
  for rel in "${SKIPPED[@]}"; do
    echo "  = $rel"
  done
fi

echo
cat <<EOF
adopt: done. Nothing of yours was changed.

Next:
  1. Fill in PRODUCT.md — it is a stub with the questions to answer.
  2. Check what is left:
       python3 $STANDARD_DIR/scripts/housecheck.py $TARGET
  3. Review and commit:
       git -C $TARGET status

EOF
