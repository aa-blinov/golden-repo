"""Deliver the standard's files that a repository's .gitignore swallows.

A rule like `config.json` matches at every depth, so it also matches the
standard's `.impeccable/config.json`. The file is written, the checker does
not see it, and the repository never gets it. The rule was meant for the
server's config in the root, and the standard's file is somewhere else.

This script finds the standard's files that the repository ignores, adds a
negation for each, and commits the result.
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


def ignored(path, target):
    result = subprocess.run(
        ["git", "-C", target, "check-ignore", "-q", path],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="aa-blinov")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    data = scaffold.manifest()
    targets = json.load(open(os.path.join(ROOT, "adoption-targets.json")))
    names = [n for n in (targets["tier1"] + targets["tier2"] + targets["tier3"])
             if n not in targets.get("excluded", {})]

    for name in names:
        work = tempfile.mkdtemp(prefix="unignore-")
        target = os.path.join(work, name)
        try:
            result = subprocess.run(
                ["git", "clone", "--depth=1", "--quiet",
                 "https://github.com/%s/%s.git" % (args.owner, name), target],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                continue

            values = scaffold.values_for(target, {"slug": name})
            planned = []
            for path, template in scaffold.file_plan(data):
                if template is None:
                    continue
                full = os.path.join(target, path)
                if os.path.exists(full):
                    continue
                if not ignored(path, target):
                    continue
                planned.append((path, template))

            if not planned:
                shutil.rmtree(work, ignore_errors=True)
                continue

            print("%-24s игнорируются: %s" % (name, ", ".join(p for p, _ in planned)))
            if args.dry_run:
                shutil.rmtree(work, ignore_errors=True)
                continue

            # A negation for each, so the repository keeps its own rule for
            # the file it meant and gets the standard's file as well.
            gitignore = os.path.join(target, ".gitignore")
            with open(gitignore, "a", encoding="utf-8") as handle:
                handle.write("\n# The house standard's own files. The rule above\n")
                handle.write("# was meant for the repository's config, not for these.\n")
                for path, _ in planned:
                    handle.write("!%s\n" % path)

            for path, template in planned:
                with open(template, encoding="utf-8") as handle:
                    content = scaffold.substitute(handle.read(), values)
                scaffold.write_file(target, path, content)

            subprocess.run(["git", "-C", target, "add", "-A"], check=True)
            subprocess.run(
                ["git", "-C", target, "commit", "-q", "-m",
                 "The standard's files, which the .gitignore was swallowing\n\n"
                 "A rule for the repository's own config matched the standard's\n"
                 "file as well, because a rule without a slash matches at every\n"
                 "depth. The file was written, and never committed.\n\n"
                 "Files added:\n%s\n" % "".join(
                     "  %s\n" % p for p, _ in planned)], check=True)
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
