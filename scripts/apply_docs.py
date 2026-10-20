#!/usr/bin/env python3
"""apply_docs — put the generated documents into a repository and push them.

    scripts/apply_docs.py <repository> --docs <dir> [--owner aa-blinov] [--push]

The documents are written by hand, from the facts in the repository, and this
script is what puts them in. It checks the result before it commits, because a
document that breaks the house style is not worth pushing.

The previous version of every file stays in the history, so a change that
turned out to be wrong is one `git revert` away.

What it does:

1. clones the repository,
2. copies the generated files over the ones they replace,
3. runs the house-style checker and the humanizer's linter on the result,
4. commits, and pushes when asked to.
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

# What the checker and the linter are run against.
DOCUMENTS = ["README.md", "AGENTS.md", "PRODUCT.md", "DESIGN.md",
              "CHANGELOG.md", "LICENSE"]


def run(args, cwd=None, check=True, env=None):
    result = subprocess.run(
        args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        check=False, env=env,
    )
    output = result.stdout.decode("utf-8", "replace")
    if check and result.returncode != 0:
        raise RuntimeError("%s failed:\n%s" % (" ".join(args[:3]), output))
    return result.returncode, output


def copy_documents(docs_dir, target):
    """Copy the generated files over the ones they replace.

    Every file under the collection directory is copied, at the path it
    has there: a document in docs/ lands in docs/, not in the root. The
    site folder is left alone, because it has its own rule.
    """
    changed = []
    # The site stays where the repository already keeps it. This is worked
    # out before anything is copied, because copying a document into docs/
    # creates that folder, and the repository did not necessarily have one.
    folders = [
        folder for folder in ("docs", "site", "website", "web", "landing")
        if os.path.isdir(os.path.join(target, folder))
    ]
    # A repository can have several of these folders. The landing page is
    # the one whose index.html is a document, with a doctype and a <html>
    # element. The index of a documentation folder is a Markdown-ish file
    # that happens to be called index.html, and the site does not go there.
    landing = None
    for folder in folders:
        index = os.path.join(target, folder, "index.html")
        if not os.path.exists(index):
            continue
        with open(index, "r", errors="replace") as handle:
            head = handle.read(400).lower()
        if "<!doctype html" in head or "<html" in head:
            landing = folder
            break
    if landing:
        folders = [landing]
    for root, dirs, files in os.walk(docs_dir):
        dirs[:] = sorted(d for d in dirs if d != "site")
        for name in sorted(files):
            source = os.path.join(root, name)
            relative = os.path.relpath(source, docs_dir)
            destination = os.path.join(target, relative)
            with open(source, "r", errors="replace") as handle:
                content = handle.read()
            previous = ""
            if os.path.exists(destination):
                with open(destination, "r", errors="replace") as handle:
                    previous = handle.read()
            if content == previous:
                continue
            directory = os.path.dirname(destination)
            if directory and not os.path.isdir(directory):
                os.makedirs(directory)
            with open(destination, "w") as handle:
                handle.write(content)
            changed.append(relative.replace(os.sep, "/"))

    # The landing site, when the repository has one and a new one was made.
    # The site stays where it is: docs/, site/, website/, web/ or landing/.
    # Moving it would break the link that publishes it.
    site_source = os.path.join(docs_dir, "site")
    if os.path.isdir(site_source) and folders:
        for name in sorted(os.listdir(site_source)):
            source = os.path.join(site_source, name)
            if not os.path.isfile(source):
                continue
            with open(source, "r", errors="replace") as handle:
                content = handle.read()
            for folder in folders:
                destination = os.path.join(target, folder, name)
                if os.path.exists(destination):
                    with open(destination, "r", errors="replace") as handle:
                        previous = handle.read()
                    if previous == content:
                        break
                with open(destination, "w") as handle:
                    handle.write(content)
                changed.append("%s/%s" % (folder, name))
                break
    return changed


def is_excluded(repository):
    """Whether the standard must not touch this repository.

    The exclusion list is the owner's decision, and it is a decision about
    content, not about a name: a repository that holds EORA's work is not
    the owner's personal project, whatever it is called. The applier
    refuses them, rather than trusting the caller to remember.
    """
    path = os.path.join(ROOT, "adoption-targets.json")
    if not os.path.exists(path):
        return False
    try:
        with open(path) as handle:
            targets = json.load(handle)
    except (IOError, ValueError):
        return False
    return repository in targets.get("excluded", {})


def main(argv=None):
    parser = argparse.ArgumentParser(prog="apply_docs")
    parser.add_argument("repository")
    parser.add_argument("--docs", required=True, help="the directory with the generated files")
    parser.add_argument("--owner", default="aa-blinov")
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--message")
    parser.add_argument("--skip-checks", action="store_true")
    parser.add_argument("--skip-normalize", action="store_true")
    args = parser.parse_args(argv)

    if is_excluded(args.repository):
        print("apply_docs: %s is excluded from the standard" % args.repository)
        print("           The reason is in adoption-targets.json.")
        return 2

    docs_dir = os.path.abspath(args.docs)
    if not os.path.isdir(docs_dir):
        sys.stderr.write("apply_docs: no such directory: %s\n" % docs_dir)
        return 2

    work = tempfile.mkdtemp(prefix="apply-")
    # The clone directory is named after the repository. It used to be called
    # "repo", and the scaffolder took the repository's name from it, so every
    # adopted repository said "Thanks for looking at repo".
    target = os.path.join(work, args.repository)
    try:
        run(["git", "clone", "--depth=1", "--quiet",
             "https://github.com/%s/%s.git" % (args.owner, args.repository), target])

        # The default branch is not always main. Two thirds of these
        # repositories are on master, and one is on prod.
        code, output = run(
            ["gh", "api", "repos/%s/%s" % (args.owner, args.repository),
             "--jq", ".default_branch"],
            check=False,
        )
        branch = output.strip() or "main"

        # The standard's files first, so that the generated documents land on
        # top of a repository that already carries the rest of the standard.
        run([sys.executable, os.path.join(ROOT, "scripts", "scaffold.py"),
             "adopt", target, "--slug", args.repository], check=False)

        changed = copy_documents(docs_dir, target)
        if not changed:
            print("apply_docs: %s is already up to date" % args.repository)
            return 0

        # The mechanical part of the standard: final newlines, trailing
        # whitespace, tabs in Markdown. Nobody reviews that by hand.
        if not args.skip_normalize:
            run([sys.executable, os.path.join(ROOT, "scripts", "normalize.py"), "."],
                cwd=target, check=False)

        if not args.skip_checks:
            # Only the files this run touched decide whether it passes. The
            # repository may have other problems, and fixing them is a
            # separate job with its own commit.
            code, output = run(
                [sys.executable, os.path.join(ROOT, "scripts", "housecheck.py"),
                 "--json", "."],
                cwd=target, check=False,
            )
            try:
                findings = json.loads(output).get("findings", [])
            except ValueError:
                findings = []
            # An exact path. A loose suffix match would catch
            # docs/qa/README.md when README.md is the file that changed.
            mine = [f for f in findings
                    if f["severity"] == "hard" and f["path"] in changed]
            if mine:
                for finding in mine:
                    print("%s  %s  %s: %s" % (
                        finding["severity"], finding["code"],
                        finding["path"], finding["message"],
                    ))
                sys.stderr.write(
                    "apply_docs: the files this run changed fail the house "
                    "style; not committing\n"
                )
                return 1

            prose = [os.path.join(".", name) for name in changed if name.endswith(".md")]
            if prose:
                code, output = run(
                    [sys.executable, os.path.join(ROOT, "scripts", "anti_ai.py")] + prose,
                    cwd=target, check=False,
                )
                if code != 0:
                    print(output)
                    sys.stderr.write(
                        "apply_docs: %s has AI writing patterns; not committing\n"
                        % args.repository
                    )
                    return 1

        message = args.message or (
            "Bring the documentation to the house standard\n\n"
            "The documents are written from the code: the commands are the ones "
            "the project has, the dependencies are the ones it uses, and the "
            "file tree is the tree. The previous version stays in the history, "
            "so this is one revert away if it turns out to be wrong.\n\n"
            "Files changed:\n%s\n" % "\n".join("  %s" % name for name in changed)
        )

        run(["git", "-C", target, "add", "-A"])
        run(["git", "-C", target, "commit", "-q", "-m", message])

        if args.push:
            token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
            if token:
                remote = "https://x-access-token:%s@github.com/%s/%s.git" % (
                    token, args.owner, args.repository,
                )
            else:
                remote = "https://github.com/%s/%s.git" % (args.owner, args.repository)
            run(["git", "-C", target, "push", "-q", remote,
                 "HEAD:refs/heads/%s" % branch])

        # The adoption pull request, if there is one, is now redundant: the
        # documents went to the default branch. Leaving it open would invite
        # a merge that undoes this work.
        if args.push:
            code, existing = run([
                "gh", "pr", "list", "--repo",
                "%s/%s" % (args.owner, args.repository),
                "--state", "open", "--json", "number,title",
            ], check=False)
            try:
                for pull in json.loads(existing):
                    if pull["title"] == "Adopt the house standard":
                        run([
                            "gh", "pr", "close", str(pull["number"]),
                            "--repo", "%s/%s" % (args.owner, args.repository),
                            "--comment",
                            "Closing: the house standard was applied directly "
                            "to this branch, and the documents were rewritten "
                            "from the code. This pull request would undo that.",
                            "--delete-branch",
                        ], check=False)
            except ValueError:
                pass

        print("apply_docs: %s — %d file(s) %s" % (
            args.repository, len(changed), "pushed" if args.push else "committed",
        ))
        return 0
    except Exception as error:  # noqa: BLE001 — one repository is not fatal
        sys.stderr.write("apply_docs: %s failed: %s\n" % (args.repository, error))
        return 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
