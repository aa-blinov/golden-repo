#!/usr/bin/env python3
"""scaffold — build a repository from the house standard.

    scripts/scaffold.py new <target>    # a new project, from templates/
    scripts/scaffold.py adopt <target>  # add what an existing project lacks

The list of files comes from standard.json, so the scaffolder and the
checker cannot disagree about what a repository carries. The content comes
from templates/.

The two modes differ in one rule: `new` writes the whole set, `adopt` writes
only what is missing and never overwrites a file that already exists. A
repository that has been running for a year has opinions its owner never
wrote down, and those outrank a template.
"""

import argparse
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEMPLATES = os.path.join(ROOT, "templates")

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")

TOKENS = {
    "PROJECT_NAME": "the project",
    "PROJECT_SLUG": "the project",
    "PROJECT_DESCRIPTION": "One line that says what this does.",
    "PROJECT_TAGLINE": "One line that says what this does.",
    "LICENSE_HOLDER": "Alexander Blinov",
    "PROJECT_YEAR": "2026",
    "REPO_OWNER": "aa-blinov",
    "REPO_URL": "https://github.com/aa-blinov/the project",
    "INSTALL_COMMAND": "echo 'replace with the install command'",
    "TEST_COMMAND": "echo 'replace with the test command'",
    "BUILD_COMMAND": "echo 'replace with the build command'",
    "SURFACE_ONE": "the network interface, and the files it reads",
    "SURFACE_TWO": "the dependency tree",
}


def manifest():
    with open(os.path.join(ROOT, "standard.json")) as handle:
        return json.load(handle)


def substitute(text, values):
    """Fill the placeholders in a template."""
    def replace(match):
        token = match.group(1)
        return values.get(token, match.group(0))
    return TOKEN_RE.sub(replace, text)


def values_for(target, overrides=None):
    values = dict(TOKENS)
    # The slug is the repository's name. It used to be the name of the
    # directory the clone landed in, and the clone was called "repo", so
    # every adopted repository ended up saying "Thanks for looking at repo".
    slug = (overrides or {}).get("slug") or os.path.basename(os.path.abspath(target))
    values["PROJECT_SLUG"] = slug
    values["PROJECT_NAME"] = overrides.get("name") if overrides and overrides.get("name") else slug
    values["REPO_URL"] = "https://github.com/%s/%s" % (values["REPO_OWNER"], slug)
    return values


def file_plan(data):
    """(path, template path) for every file the standard knows about.

    A file with a template comes from it. A file without one is created
    empty: the standard demands the path, and the project writes the
    content.
    """
    plan = []
    for entry in data["root"]["files"]:
        path = entry["path"]
        if "/" in path and path.split("/")[0] in ("src", "tests", "scripts"):
            # A directory of the project's own making, not a file the
            # standard hands over.
            continue
        template = os.path.join(TEMPLATES, path)
        plan.append((path, template if os.path.exists(template) else None))
    return plan


def write_file(target, path, content):
    full = os.path.join(target, path)
    directory = os.path.dirname(full)
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)
    with open(full, "w") as handle:
        handle.write(content)


def apply_plan(data, target, values, only_missing):
    """Copy the files into the target. Returns (added, skipped)."""
    added = []
    skipped = []
    for path, template in file_plan(data):
        full = os.path.join(target, path)
        if only_missing and os.path.exists(full):
            skipped.append(path)
            continue
        if template is None:
            write_file(target, path, "")
            added.append(path)
            continue
        with open(template) as handle:
            content = substitute(handle.read(), values)
        write_file(target, path, content)
        added.append(path)
    return added, skipped


def ensure_directories(data, target):
    """Create the directories the standard requires.

    A directory git cannot keep empty needs a file in it, or it disappears
    from the next clone and the checker reports it missing.
    """
    for entry in data["root"]["directories"]:
        path = os.path.join(target, entry["path"])
        if not os.path.isdir(path):
            os.makedirs(path)
        if not os.listdir(path):
            with open(os.path.join(path, ".gitkeep"), "w"):
                pass


def main(argv=None):
    parser = argparse.ArgumentParser(prog="scaffold")
    parser.add_argument("mode", choices=["new", "adopt"])
    parser.add_argument("target")
    parser.add_argument("--name", help="the display name of the project")
    parser.add_argument("--owner", default="aa-blinov")
    parser.add_argument("--slug", help="the repository's name, if it is not the target's")
    parser.add_argument("--year", default="2026")
    args = parser.parse_args(argv)

    data = manifest()
    target = os.path.abspath(args.target)
    values = values_for(target, {"name": args.name, "slug": args.slug})
    values["REPO_OWNER"] = args.owner
    values["PROJECT_YEAR"] = args.year

    if args.mode == "new":
        if os.path.isdir(target) and os.listdir(target):
            sys.stderr.write(
                "scaffold: %s is not empty; refusing to overwrite.\n" % target
            )
            return 1
        if not os.path.isdir(target):
            os.makedirs(target)
        added, skipped = apply_plan(data, target, values, only_missing=False)
    else:
        added, skipped = apply_plan(data, target, values, only_missing=True)

    ensure_directories(data, target)

    for path in added:
        print("  + %s" % path)
    for path in skipped:
        print("  = %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
