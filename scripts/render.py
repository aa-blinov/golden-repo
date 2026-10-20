#!/usr/bin/env python3
"""render — build the documents that describe the standard from standard.json.

    scripts/render.py [--check]

The standard is described in three places that used to drift apart: the
manifest, the checker, and the documents. The manifest now says what a
repository must contain, the checker enforces it, and this script writes the
part of the documentation that repeats it.

With --check the script writes nothing and reports whether the documents are
up to date. That is the mode the test suite and CI use, because a generator
that nobody runs is a generator that drifts.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def manifest():
    with open(os.path.join(ROOT, "standard.json")) as handle:
        return json.load(handle)


def tree(data):
    """The canonical tree, as it appears in the documents.

    It is built from the manifest rather than written by hand, so a file that
    the standard demands cannot be missing from the tree, and a file in the
    tree cannot be missing from the standard.
    """
    # A node is either a directory (children, comment) or a file (comment).
    root = {"dir": True, "children": {}, "comment": None}

    def ensure(path, is_dir, comment):
        node = root
        parts = path.split("/")
        for index, part in enumerate(parts):
            last = index == len(parts) - 1
            child = node["children"].get(part)
            if child is None:
                child = {
                    "dir": not last or is_dir,
                    "children": {},
                    "comment": comment if last else None,
                }
                node["children"][part] = child
            elif last and comment:
                child["comment"] = comment
            node = child
        return node

    for entry in data["root"]["directories"]:
        ensure(entry["path"], True, entry["comment"])
    for entry in data["root"]["files"]:
        ensure(entry["path"], False, entry["comment"])

    lines = ["<repo>/"]

    def draw(node, prefix):
        # Files come before directories at every level, and the two groups are
        # each sorted by name. A reader finds a file by its name, not by
        # guessing which group it is in.
        names = sorted(node["children"].items(), key=lambda item: (
            item[1]["dir"], item[0].lower(),
        ))
        width = 0
        for name, child in names:
            label = name + "/" if child["dir"] else name
            width = max(width, len(label))

        for index, (name, child) in enumerate(names):
            last = index == len(names) - 1
            branch = "└── " if last else "├── "
            label = name + "/" if child["dir"] else name
            comment = child["comment"]
            padding = " " * (width - len(label) + 2)
            suffix = "# %s" % comment if comment else ""
            lines.append("%s%s%s%s%s" % (prefix, branch, label, padding, suffix))
            if child["dir"]:
                draw(child, prefix + ("    " if last else "│   "))

    draw(root, "")
    return "\n".join(lines)


def required_table(data):
    """The table of the files every repository must carry."""
    lines = ["| File | What it carries |", "| --- | --- |"]
    for entry in data["root"]["files"]:
        if not entry.get("required"):
            continue
        lines.append("| `%s` | %s |" % (entry["path"], entry["comment"]))
    return "\n".join(lines)


def directory_table(data):
    """The table of the directories every repository must carry."""
    lines = ["| Directory | What goes in it |", "| --- | --- |"]
    for entry in data["root"]["directories"]:
        lines.append("| `%s/` | %s |" % (entry["path"], entry["comment"]))
    return "\n".join(lines)


def readme_table(data):
    """The table of the sections a README must answer."""
    lines = ["| Question | Section | What goes in it |", "| --- | --- | --- |"]
    for entry in data["readme"]["sections"]:
        lines.append("| %s | `%s` | %s |" % (
            entry["label"], entry["label"], entry.get("comment", ""),
        ))
    return "\n".join(lines)


def product_table(data):
    """The table of the sections a PRODUCT.md must carry."""
    lines = ["| Section | What it holds |", "| --- | --- |"]
    for entry in data["product"]["sections"]:
        lines.append("| `%s` | %s |" % (entry["label"], entry.get("comment", "")))
    return "\n".join(lines)


BLOCKS = [
    ("<!-- BEGIN:standard-tree -->", "<!-- END:standard-tree -->", tree),
    ("<!-- BEGIN:standard-files -->", "<!-- END:standard-files -->", required_table),
    ("<!-- BEGIN:standard-directories -->", "<!-- END:standard-directories -->", directory_table),
    ("<!-- BEGIN:standard-readme -->", "<!-- END:standard-readme -->", readme_table),
    ("<!-- BEGIN:standard-product -->", "<!-- END:standard-product -->", product_table),
]


def apply_block(text, begin, end, body):
    """Replace the text between two markers, keeping both markers."""
    if begin in text and end in text:
        before = text[:text.index(begin) + len(begin)]
        after = text[text.index(end):]
        return "%s\n%s\n%s" % (before, body, after)
    return text


def render_file(path, data):
    with open(path) as handle:
        text = handle.read()
    for begin, end, builder in BLOCKS:
        text = apply_block(text, begin, end, builder(data))
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(prog="render")
    parser.add_argument(
        "--check", action="store_true",
        help="report whether the documents are up to date, and change nothing",
    )
    args = parser.parse_args(argv)

    data = manifest()
    targets = [
        os.path.join(ROOT, "docs", "structure.md"),
        os.path.join(ROOT, "docs", "house-style.md"),
    ]

    stale = []
    for path in targets:
        if not os.path.exists(path):
            continue
        with open(path) as handle:
            current = handle.read()
        updated = render_file(path, data)
        if updated != current:
            stale.append(os.path.relpath(path, ROOT))
            if not args.check:
                with open(path, "w") as handle:
                    handle.write(updated)

    if args.check:
        if stale:
            sys.stderr.write(
                "render: out of date, run scripts/render.py: %s\n" % ", ".join(stale)
            )
            return 1
        sys.stderr.write("render: the documents match standard.json\n")
        return 0

    if stale:
        print("render: wrote %s" % ", ".join(stale))
    else:
        print("render: the documents were already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
