#!/usr/bin/env python3
"""adopt_bot — open a pull request that brings a repository to the standard.

    scripts/adopt_bot.py <repository> [--owner aa-blinov] [--dry-run]

One repository per run, so that a matrix of workflows can fan it out and a
failure is one repository rather than eighty. The script:

1. clones the repository shallowly,
2. runs the migrator, which adds what is missing and overwrites nothing,
3. opens a pull request with the result.

The pull request is the point. The migration is mechanical, and a mechanical
change is worth reading as a diff rather than merging straight onto main.
Nobody has to review eighty files one by one: the diff is the same in every
repository, and the first one is read carefully.

The token needs write access to the repository. In CI that is a personal
access token with the `repo` scope, stored as the GH_TOKEN secret of the
standard repository. Locally, the gh CLI's own authentication is used.
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
STANDARD_OWNER = "aa-blinov"
STANDARD_NAME = "golden-repo"


def run(args, cwd=None, check=True, env=None):
    result = subprocess.run(
        args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False, env=env,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            "%s: %s" % (" ".join(args[:3]), result.stderr.decode("utf-8", "replace").strip())
        )
    return result.stdout.decode("utf-8", "replace")


def gh(args, check=True):
    return run(["gh"] + args, check=check)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="adopt_bot")
    parser.add_argument("repository", help="the repository to bring to the standard")
    parser.add_argument("--owner", default=STANDARD_OWNER)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--branch-prefix", default="standard/adopt-the-house-standard",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="adopt even a repository the exclusion list names",
    )
    args = parser.parse_args(argv)


    name = args.repository

    # The exclusion list is not a formality. A repository on it holds
    # somebody else's work, and the house style does not apply to it.
    exclusions_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "adoption-targets.json",
    )
    if not args.force and os.path.exists(exclusions_path):
        with open(exclusions_path) as handle:
            excluded = json.load(handle).get("excluded", {})
        if name in excluded:
            print("adopt: %s is excluded: %s" % (name, excluded[name]))
            return 0

    work = tempfile.mkdtemp(prefix="adopt-%s-" % name)
    # The clone directory is named after the repository, so the scaffolder
    # does not take "repo" for the project's name.
    target = os.path.join(work, name)
    branch = "%s-%s" % (args.branch_prefix, name)

    try:
        run([
            "git", "clone", "--depth=1", "--quiet",
            "https://github.com/%s/%s.git" % (args.owner, name), target,
        ])
        base = run(
            ["git", "-C", target, "symbolic-ref", "--short", "HEAD"]
        ).strip() or "main"
        code, output = run(
            ["gh", "api", "repos/%s/%s" % (args.owner, name), "--jq", ".default_branch"],
            check=False,
        )
        default = output.strip()
        if default:
            base = default

        # The migrator adds what is missing and overwrites nothing.
        run(["bash", os.path.join(HERE, "adopt.sh"), target], check=True)  # noqa: E501

        changes = run(["git", "-C", target, "status", "--porcelain", "-uall"])
        if not changes.strip():
            print("adopt: %s already follows the standard" % name)
            return 0

        added = [
            line[3:] for line in changes.split("\n")
            if line[:2] in ("??", " A", "AM")
        ]

        if args.dry_run:
            print("adopt: %s would gain %d file(s):" % (name, len(added)))
            for path in added:
                print("  + %s" % path)
            return 0

        # A branch, a commit, and a pull request.
        run(["git", "-C", target, "checkout", "-q", "-b", branch])
        run(["git", "-C", target, "add", "-A"])
        message = (
            "Adopt the house standard\n\n"
            "Adds the files every repository in this collection carries, and "
            "nothing else. No file that already existed was changed.\n\n"
            "Files added:\n%s\n\n"
            "## The house-style check is red until the stubs are written\n\n"
            "`PRODUCT.md`, `DESIGN.md`, `AGENTS.md` and the two files in "
            "`docs/` arrive as starting points, not as finished documents. The "
            "check fails on them, and that is the standard working: the "
            "product truth cannot be defaulted, and a file that has not been "
            "written yet should not pass for one that has.\n\n"
            "Fill in the stubs, delete the `house-style: template` line from "
            "each, and the check goes green. The rules are in "
            "[docs/house-style.md]"
            "(https://github.com/aa-blinov/golden-repo/blob/main/docs/house-style.md).\n"
            % "\n".join("  %s" % p for p in sorted(added))
        )
        run(["git", "-C", target, "commit", "-q", "-m", message])

        # The token that pushes the branch. In CI it is the secret, and it has
        # to travel in the remote URL, because the runner has no credential
        # helper configured. Locally the gh CLI's own authentication is used.
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        env = dict(os.environ)
        if token:
            remote = "https://x-access-token:%s@github.com/%s/%s.git" % (
                token, args.owner, name,
            )
        else:
            remote = "https://github.com/%s/%s.git" % (args.owner, name)

        # The branch belongs to the bot, and a fresh clone produces a commit
        # with a different hash, so the push has to replace it.
        run(["git", "-C", target, "push", "-q", "--force",
             remote, "HEAD:refs/heads/%s" % branch], env=env)

        # Reuse an open pull request for this branch, if there is one.
        existing = gh([
            "pr", "list", "--repo", "%s/%s" % (args.owner, name),
            "--head", branch, "--state", "open", "--json", "number",
        ])
        try:
            numbers = [p["number"] for p in json.loads(existing)]
        except ValueError:
            numbers = []

        if numbers:
            gh([
                "api", "-X", "PATCH",
                "repos/%s/%s/pulls/%d" % (args.owner, name, numbers[0]),
                "-f", "title=Adopt the house standard",
                "-f", "body=%s" % message,
            ])
            print("adopt: %s — updated pull request #%d" % (name, numbers[0]))
        else:
            created = gh([
                "pr", "create", "--repo", "%s/%s" % (args.owner, name),
                "--head", branch, "--base", base,
                "--title", "Adopt the house standard",
                "--body", message,
            ])
            number = ""
            for token_part in created.split():
                if token_part.startswith("https://") and "/pull/" in token_part:
                    number = token_part.rstrip("/").split("/")[-1]
            print("adopt: %s — pull request %s" % (name, number or "opened"))
        return 0
    except Exception as error:  # noqa: BLE001 — one repository is not fatal
        sys.stderr.write("adopt: %s failed: %s\n" % (name, error))
        return 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
