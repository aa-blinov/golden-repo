#!/usr/bin/env python3
"""bump — open a pull request that bumps the standard's pin in a repository.

    scripts/bump.py [--owner aa-blinov] [--dry-run]

The standard is a dependency. A repository that adopts it references the
checker at a version:

    uses: aa-blinov/golden-repo/.github/actions/house-style@v1.0.0

This script finds the repositories that reference it, compares the version
they pin with the latest tag, and opens a pull request that moves the pin.

Why this exists rather than relying on Dependabot: Dependabot does read the
reference as a dependency, and it does fetch the standard's tags, but it does
not propose a bump for a standard that is published as a release in the same
repository as its own tooling. The observed behaviour is in the commit that
introduced this script. A scheduled workflow that does the job itself is a
hundred lines and behaves the same way every time.

The script needs a token that can write to the repositories it touches. In CI
that is a personal access token with the `repo` scope, stored as the
GH_TOKEN secret of this repository. Locally, the `gh` CLI's own
authentication is used.
"""

import argparse
import json
import os
import re
import subprocess
import sys

# The reference to look for. A repository pins the standard in its workflow
# files, and the pin is the tag after the @.
REFERENCE_RE = re.compile(
    r"uses:\s*([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_./-]+)?)@([^\s#'\"]+)"
    r"(?:\s*#\s*(v[0-9.]+))?",
)

# The standard lives in this repository. A reference to it is a dependency on
# the standard; a reference to anything else is not.
STANDARD_OWNER = "aa-blinov"
STANDARD_NAME = "golden-repo"


def gh(args, check=True):
    """Run the gh CLI and return its stdout."""
    result = subprocess.run(
        ["gh"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip())
    return result.stdout.decode("utf-8", "replace")


def gh_json(args, payload):
    """Run the gh CLI with a JSON body and return the parsed response."""
    result = subprocess.run(
        ["gh"] + args + ["--input", "-"],
        input=json.dumps(payload).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip())
    return json.loads(result.stdout.decode("utf-8", "replace"))


def latest_tag(owner, name):
    """The highest version tag of a repository, by semver."""
    raw = gh(["api", "repos/%s/%s/tags" % (owner, name)])
    tags = []
    for entry in json.loads(raw):
        tag = entry.get("name", "")
        match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", tag)
        if match:
            tags.append((tuple(int(p) for p in match.groups()), tag))
    if not tags:
        return None
    return max(tags)[1]


def version_tuple(tag):
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", tag or "")
    if not match:
        return None
    return tuple(int(p) for p in match.groups())


def workflow_files(owner, name):
    """The workflow files of a repository, with their content."""
    raw = gh(["api", "repos/%s/%s/contents/.github/workflows" % (owner, name)])
    try:
        entries = json.loads(raw)
    except ValueError:
        return []
    if not isinstance(entries, list):
        return []

    files = []
    for entry in entries:
        path = entry.get("path", "")
        if not path.endswith((".yml", ".yaml")):
            continue
        content = gh(["api", "repos/%s/%s/contents/%s" % (owner, name, path)])
        try:
            body = json.loads(content).get("content", "")
        except ValueError:
            continue
        import base64
        try:
            files.append((path, base64.b64decode(body).decode("utf-8", "replace")))
        except Exception:
            continue
    return files


def find_pins(owner, name):
    """Every pin of the standard in a repository: (path, current version)."""
    pins = []
    for path, content in workflow_files(owner, name):
        for match in REFERENCE_RE.finditer(content):
            dependency = match.group(1)
            # A reference pinned by commit carries the version in the comment
            # beside it; a reference pinned by tag carries it in the ref.
            version = match.group(3) or match.group(2)
            parts = dependency.split("/")
            if len(parts) < 2:
                continue
            if parts[0] != STANDARD_OWNER or parts[1] != STANDARD_NAME:
                continue
            pins.append((path, version))
    return pins


def tag_commit(owner, tag):
    """The commit a tag points at, peeling an annotated tag."""
    try:
        data = json.loads(gh(["api", "repos/%s/%s/git/ref/tags/%s" % (
            owner, STANDARD_NAME, tag)]))
    except Exception:  # noqa: BLE001 — a missing tag is the caller's problem
        return None
    obj = data.get("object") or {}
    if obj.get("type") == "tag":
        try:
            annotated = json.loads(gh(["api", "repos/%s/%s/git/tags/%s" % (
                owner, STANDARD_NAME, obj.get("sha"))]))
        except Exception:  # noqa: BLE001
            return None
        return (annotated.get("object") or {}).get("sha")
    return obj.get("sha")


def bump_pull_request(owner, name, latest, dry_run=False):
    """Open, or update, the pull request that moves the pin."""
    pins = find_pins(owner, name)
    if not pins:
        return None, None

    current = pins[0][1]
    current_version = version_tuple(current)
    latest_version = version_tuple(latest)
    if current_version is None or latest_version is None:
        return None, None
    if latest_version <= current_version:
        return current, None
    if dry_run:
        # The flag exists so that a run can be inspected before it writes to
        # sixty-four repositories. It returned nothing for a while, which is
        # how a "dry" run opened every pull request it was meant to describe.
        return current, -1

    branch = "standard/bump-to-%s" % latest
    # Delete a branch left over from a previous attempt.
    subprocess.run(
        ["gh", "api", "-X", "DELETE",
         "repos/%s/%s/git/refs/heads/%s" % (owner, name, branch)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )

    base = gh(["api", "repos/%s/%s" % (owner, name), "--jq", ".default_branch"]).strip()
    base = base or "main"

    body = []
    for path, version in pins:
        body.append("%s: %s -> %s" % (path, version, latest))
    # Conventional, because a repository that lints its commits lints this
    # one too, and a bump that fails the lint is a bump nobody merges.
    message = "chore: bump the house standard to %s\n\n%s\n" % (latest, "\n".join(body))

    # Build the commit with the GitHub API, so that no local clone is needed.
    base_sha = gh([
        "api", "repos/%s/%s/git/ref/heads/%s" % (owner, name, base),
        "--jq", ".object.sha",
    ]).strip()
    tree = gh([
        "api", "repos/%s/%s/git/trees/%s?recursive=1" % (owner, name, base_sha),
    ])
    tree_sha = json.loads(tree).get("sha")

    commit = tag_commit(owner, latest)
    changed = []
    for path, content in workflow_files(owner, name):
        updated = re.sub(
            r"(uses:\s*%s/%s(?:/[A-Za-z0-9_./-]+)?)@([^\s#'\"]+)(?:\s*#\s*v[0-9.]+)?" % (
                STANDARD_OWNER, STANDARD_NAME,
            ),
            # Pinned by commit, with the version beside it. A tag is a moving
            # target: anyone with write access to the standard can repoint it,
            # and a security scanner is right to say so.
            lambda m: "%s@%s # %s" % (m.group(1), commit or latest, latest),
            content,
        )
        if updated != content:
            changed.append((path, updated))

    if not changed:
        return current, None

    # One blob per changed file, then a tree, then a commit, then the ref.
    # The payloads go through --input, because a form-encoded field cannot
    # carry a multi-line file or a JSON array.
    blob_entries = []
    for path, content in changed:
        blob = gh_json(
            ["api", "-X", "POST", "repos/%s/%s/git/blobs" % (owner, name)],
            {"content": content, "encoding": "utf-8"},
        )["sha"]
        blob_entries.append({
            "path": path,
            "mode": "100644",
            "type": "blob",
            "sha": blob,
        })

    new_tree = gh_json(
        ["api", "-X", "POST", "repos/%s/%s/git/trees" % (owner, name)],
        {"base_tree": tree_sha, "tree": blob_entries},
    )["sha"]

    commit = gh_json(
        ["api", "-X", "POST", "repos/%s/%s/git/commits" % (owner, name)],
        {"message": message, "tree": new_tree, "parents": [base_sha]},
    )["sha"]

    gh_json(
        ["api", "-X", "POST", "repos/%s/%s/git/refs" % (owner, name)],
        {"ref": "refs/heads/%s" % branch, "sha": commit},
    )

    # Reuse an open pull request for this branch, if there is one.
    existing = gh([
        "pr", "list", "--repo", "%s/%s" % (owner, name),
        "--head", branch, "--state", "open", "--json", "number",
    ])
    try:
        numbers = [p["number"] for p in json.loads(existing)]
    except ValueError:
        numbers = []

    if numbers:
        gh([
            "api", "-X", "PATCH", "repos/%s/%s/pulls/%d" % (owner, name, numbers[0]),
            "-f", "title=chore: bump the house standard to %s" % latest,
            "-f", "body=%s" % message,
        ])
        return current, numbers[0]

    created = gh([
        "pr", "create", "--repo", "%s/%s" % (owner, name),
        "--head", branch, "--base", base,
        "--title", "chore: bump the house standard to %s" % latest,
        "--body", message,
    ])
    number = None
    match = re.search(r"/pull/(\d+)", created)
    if match:
        number = int(match.group(1))
    return current, number


def main(argv=None):
    parser = argparse.ArgumentParser(prog="bump")
    parser.add_argument("--owner", default=STANDARD_OWNER)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--only", action="append", default=[],
        help="check only this repository; may be repeated",
    )
    args = parser.parse_args(argv)

    latest = latest_tag(args.owner, STANDARD_NAME)
    if not latest:
        sys.stderr.write("bump: %s/%s has no version tag\n" % (args.owner, STANDARD_NAME))
        return 2
    sys.stderr.write("bump: the latest standard is %s\n" % latest)

    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "adopters.json")
    if not os.path.exists(path):
        sys.stderr.write("bump: no adopters.json at %s\n" % path)
        return 2
    with open(path) as handle:
        adopters = json.load(handle)

    names = args.only or adopters.get("repositories", [])
    failures = 0
    for name in names:
        try:
            current, number = bump_pull_request(args.owner, name, latest, args.dry_run)
        except Exception as error:  # noqa: BLE001 — one repository is not fatal
            sys.stderr.write("bump: %s failed: %s\n" % (name, error))
            failures += 1
            continue
        if number is None:
            sys.stderr.write("bump: %s is on %s, nothing to do\n" % (name, current))
        elif number == -1:
            sys.stderr.write("bump: %s %s -> %s, would open a pull request\n" % (
                name, current, latest,
            ))
        else:
            sys.stderr.write("bump: %s %s -> %s, pull request #%d\n" % (
                name, current, latest, number,
            ))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
