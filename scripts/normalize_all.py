"""Run the mechanical part of the house style across a collection.

    scripts/normalize_all.py [--owner aa-blinov] [--dry-run]

Three fixes per file, and nothing else: a final newline, no trailing
whitespace, no tab indentation in Markdown. They are what HS042, HS043 and
HS044 ask for, and nobody reviews them by hand.
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="aa-blinov")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    targets = json.load(open(os.path.join(ROOT, "adoption-targets.json")))
    names = [n for n in (targets["tier1"] + targets["tier2"] + targets["tier3"])
             if n not in targets.get("excluded", {})]

    total = 0
    for name in names:
        work = tempfile.mkdtemp(prefix="norm-")
        target = os.path.join(work, name)
        try:
            result = subprocess.run(
                ["git", "clone", "--depth=1", "--quiet",
                 "https://github.com/%s/%s.git" % (args.owner, name), target],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                print("%-24s не клонирован" % name)
                continue
            before = subprocess.run(
                [sys.executable, os.path.join(HERE, "normalize.py"), target, "--check"],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            if b"normalize: 0 file(s)" in before.stdout:
                continue
            subprocess.run(
                [sys.executable, os.path.join(HERE, "normalize.py"), target],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            count = int(before.stdout.decode().strip().split()[-2])
            total += count
            print("%-24s файлов: %d" % (name, count))
            if args.dry_run:
                continue
            subprocess.run(["git", "-C", target, "add", "-A"], check=True)
            subprocess.run(
                ["git", "-C", target, "commit", "-q", "-m",
                 "The mechanical part of the house style\\n\\n"
                 "A final newline, no trailing whitespace, no tab indentation "
                 "in Markdown. These are HS042, HS043 and HS044, and nobody "
                 "reads them by hand."], check=True)
            subprocess.run(
                ["git", "-C", target, "push", "-q", "origin",
                 "HEAD:refs/heads/%s" % branch_of(target)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print("\\nвсего файлов: %d" % total)


def branch_of(target):
    result = subprocess.run(
        ["git", "-C", target, "rev-parse", "--abbrev-ref", "HEAD"],
        stdout=subprocess.PIPE)
    return result.stdout.decode().strip()


if __name__ == "__main__":
    main()
