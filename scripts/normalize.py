#!/usr/bin/env python3
"""normalize — the mechanical part of the house style.

    scripts/normalize.py <path> [--check]

Three fixes, and nothing else:

- every text file ends with a newline,
- no line ends with a space or a tab,
- no Markdown line is indented with a tab.

They are mechanical, they are what the house style's hygiene rules ask for,
and they are the kind of change nobody wants to review line by line. So they
are made here, once, rather than by hand in sixty-five repositories.

The checker reports these as HS042, HS043 and HS044. This script is what
clears them.

With --check the script reports what it would change and changes nothing.
"""

import argparse
import os
import sys

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "out", "target", "vendor",
    ".venv", "venv", "__pycache__", ".next", ".nuxt", ".output", "coverage",
    "site-packages", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".gradle", ".idea", ".cache", "third_party", "third-party",
}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".icns", ".svg",
    ".pdf", ".zip", ".gz", ".bz2", ".xz", ".7z", ".woff", ".woff2", ".ttf",
    ".otf", ".eot", ".mp3", ".mp4", ".mov", ".wav", ".ogg", ".webm",
    ".pyc", ".so", ".dylib", ".dll", ".exe", ".bin", ".db", ".sqlite",
}


def is_text(path):
    if os.path.splitext(path)[1].lower() in BINARY_EXTENSIONS:
        return False
    try:
        with open(path, "rb") as handle:
            chunk = handle.read(8192)
    except (IOError, OSError):
        return False
    return b"\x00" not in chunk


def fix_text(content, is_markdown):
    """Return the fixed content, and whether anything changed."""
    original = content
    lines = content.split("\n")

    fixed = []
    for line in lines:
        if is_markdown and line.startswith("\t"):
            # A tab indents a code block by four columns in a Markdown
            # renderer and by eight in a terminal, so it is never what the
            # author meant.
            line = "    " + line[1:]
        fixed.append(line.rstrip(" \t"))

    content = "\n".join(fixed)
    if content and not content.endswith("\n"):
        content += "\n"
    # A file that ended with several newlines keeps one.
    while content.endswith("\n\n"):
        content = content[:-1]
    return content, content != original


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            yield path, os.path.relpath(path, root)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="normalize")
    parser.add_argument("path")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.path)
    if os.path.isfile(root):
        root = os.path.dirname(root)

    changed = []
    for path, rel in walk(root):
        if not is_text(path):
            continue
        try:
            with open(path, "r", errors="replace") as handle:
                content = handle.read()
        except (IOError, OSError):
            continue
        fixed, did_change = fix_text(content, path.endswith(".md"))
        if not did_change:
            continue
        changed.append(rel)
        if not args.check:
            with open(path, "w") as handle:
                handle.write(fixed)

    for rel in changed:
        print("%s %s" % ("would fix" if args.check else "fixed", rel))
    print("normalize: %d file(s)" % len(changed))
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
