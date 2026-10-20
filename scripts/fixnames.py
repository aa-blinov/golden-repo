"""Fix the project name in the files the standard hands over.

The migrator used to clone a repository into a directory called "repo" and
take the project's name from that directory. Every repository the standard
touched therefore said "Thanks for looking at repo" in its CONTRIBUTING.md,
"All notable changes to repo" in its CHANGELOG.md, and pointed its issue
template at github.com/aa-blinov/repo.

This script repairs the files it can prove it did not write. A file is
replaced only when it matches the template exactly, rendered with the old
wrong name. A file the owner has edited does not match, and is left alone.
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

import scaffold  # noqa: E402

WRONG_SLUG = "repo"


def render(data, path, template, slug):
    """The file the standard would write for a project called `slug`."""
    values = scaffold.values_for(
        os.path.join(os.path.dirname(os.path.dirname(path)), slug),
        {"slug": slug},
    )
    if template is None:
        return ""
    with open(template, encoding="utf-8") as handle:
        return scaffold.substitute(handle.read(), values)


def repair(target, name, data):
    """Replace every standard file that still carries the wrong name."""
    repaired = []
    for path, template in scaffold.file_plan(data):
        if template is None:
            continue
        full = os.path.join(target, path)
        if not os.path.exists(full):
            continue
        with open(full, encoding="utf-8") as handle:
            current = handle.read()
        if WRONG_SLUG not in current:
            continue
        if current != render(data, path, template, WRONG_SLUG):
            # The owner edited this file. It is theirs now.
            continue
        with open(full, "w", encoding="utf-8") as handle:
            handle.write(render(data, path, template, name))
        repaired.append(path)
    return repaired


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="aa-blinov")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    data = scaffold.manifest()
    targets = json.load(open(os.path.join(ROOT, "adoption-targets.json")))
    names = [n for n in (targets["tier1"] + targets["tier2"] + targets["tier3"])
             if n not in targets.get("excluded", {})]

    total = 0
    for name in names:
        work = tempfile.mkdtemp(prefix="fixname-")
        target = os.path.join(work, name)
        try:
            result = subprocess.run(
                ["git", "clone", "--depth=1", "--quiet",
                 "https://github.com/%s/%s.git" % (args.owner, name), target],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print("%-24s не клонирован" % name)
                continue
            repaired = repair(target, name, data)
            if not repaired:
                continue
            total += len(repaired)
            print("%-24s исправлено файлов: %d  (%s)" %
                  (name, len(repaired), ", ".join(repaired)))
            if args.dry_run:
                continue
            subprocess.run(["git", "-C", target, "add", "-A"], check=True)
            subprocess.run(
                ["git", "-C", target, "commit", "-q", "-m",
                 "The name of the project was wrong in these files\n\n"
                 "The migrator took the project's name from the directory it\n"
                 "cloned into, and that directory was called \"repo\". Every\n"
                 "repository the standard touched therefore said \"Thanks for\n"
                 "looking at repo\".\n\n"
                 "These files are the standard's own, byte for byte, so they\n"
                 "are safe to regenerate. Anything a file said that the\n"
                 "template does not is left alone."], check=True)
            push = subprocess.run(
                ["git", "-C", target, "push", "origin",
                 "HEAD:refs/heads/%s" % branch_of(target)],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if push.returncode != 0:
                print("   не запушено: %s" % push.stdout.decode()[:200])
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print("\nвсего исправлено файлов: %d" % total)


def branch_of(target):
    result = subprocess.run(
        ["git", "-C", target, "rev-parse", "--abbrev-ref", "HEAD"],
        stdout=subprocess.PIPE)
    return result.stdout.decode().strip()


if __name__ == "__main__":
    main()
