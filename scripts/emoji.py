"""Deal with the emoji that are left in a repository's own documents.

Two kinds, and they are not the same thing.

A **decoration** is an emoji that carries no meaning: a logo in a heading,
an icon before a warning, a person's emoji in a changelog entry. It goes,
and where the prose needs a word in its place, the word is given.

A **vocabulary** is an emoji the document defines: a legend, a column in a
table, a flag in a report. The document says what the glyph means, and
removing it would take the meaning with it. Such a file says so, in the
open, with the house marker, and the checker leaves it alone.

The decision is made by reading the file, not by a pattern, so it is
written down in a decisions file rather than guessed at here.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import housecheck  # noqa: E402

MARKER = "<!-- house-style: emoji-ok -->"
NOTE = ("<!-- The emoji in this file are a vocabulary the document defines:\n"
        "     a legend, a column in a table, a flag in a report. Removing them\n"
        "     would take the meaning with them. See docs/house-style.md. -->\n")


def apply_decisions(per_repo, data):
    """The changed paths for one repository."""
    changed = []
    for rel, decision in sorted(per_repo.items()):
        full = os.path.join(data["target"], rel)
        if not os.path.exists(full):
            continue
        with open(full, encoding="utf-8") as handle:
            text = handle.read()
        head = "\n".join(text.split("\n")[:3])
        if housecheck.EMOJI_OPT_OUT in head:
            continue
        if decision == "mark":
            if text.startswith(MARKER):
                continue
            with open(full, "w", encoding="utf-8") as handle:
                handle.write(MARKER + "\n" + NOTE + text)
            changed.append(rel)
            continue
        # remove: every emoji in the file goes, and the words that replace
        # them are given.
        out = []
        for char in text:
            if housecheck.has_emoji(char) is not None:
                continue
            out.append(char)
        stripped = "".join(out)
        for old, new in (decision.get("replace") or {}).items():
            stripped = stripped.replace(old, new)
        if stripped != text:
            with open(full, "w", encoding="utf-8") as handle:
                handle.write(stripped)
            changed.append(rel)
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="aa-blinov")
    parser.add_argument("--decisions", default=os.path.join(HERE, "emoji-decisions.json"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    decisions = json.load(open(args.decisions, encoding="utf-8"))
    for name, per_repo in decisions.items():
        if name.startswith("_"):
            continue
        work = tempfile.mkdtemp(prefix="emoji-")
        target = os.path.join(work, name)
        try:
            result = subprocess.run(
                ["git", "clone", "--depth=1", "--quiet",
                 "https://github.com/%s/%s.git" % (args.owner, name), target],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                print("%-24s не клонирован" % name)
                continue
            changed = apply_decisions(per_repo, {"target": target})
            if not changed:
                continue
            print("%-24s изменено: %s" % (name, ", ".join(changed)))
            if args.dry_run:
                continue
            subprocess.run(["git", "-C", target, "add", "-A"], check=True)
            subprocess.run(
                ["git", "-C", target, "commit", "-q", "-m",
                 "The emoji that meant nothing are gone\n\n"
                 "An emoji that carries no meaning: a logo in a heading, an icon\n"
                 "before a warning, a person's emoji in a changelog. The house\n"
                 "style does not have them in a document.\n\n"
                 "The emoji that are a vocabulary the document defines are left\n"
                 "alone, in the files that say so."], check=True)
            branch = subprocess.run(
                ["git", "-C", target, "rev-parse", "--abbrev-ref", "HEAD"],
                stdout=subprocess.PIPE).stdout.decode().strip()
            subprocess.run(
                ["git", "-C", target, "push", "-q", "origin",
                 "HEAD:refs/heads/%s" % branch],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        finally:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
