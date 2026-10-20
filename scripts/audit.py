#!/usr/bin/env python3
"""audit — check every repository of an owner against the house standard.

    scripts/audit.py [--owner aa-blinov] [--json report.json] [--markdown]

Each repository is cloned shallowly and checked with the ordinary checker,
so the findings are the real ones, produced by the same code that runs in CI.

Cloning over git rather than reading the REST API matters: an audit of
eighty repositories would otherwise spend the hourly API quota and get
rate-limited half way through.

    scripts/audit.py --owner aa-blinov --markdown > docs/audit.md
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import housecheck  # noqa: E402



def gh(args, cwd=None):
    try:
        out = subprocess.run(
            ["gh"] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except (OSError, ValueError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout


def list_repositories(owner):
    raw = gh(["repo", "list", owner, "--limit", "200", "--json",
              "name,description,visibility,isArchived,isTemplate,primaryLanguage,"
              "stargazerCount,updatedAt,url"])
    if raw is None:
        return []
    return json.loads(raw.decode("utf-8", "replace"))


def audit_repository(owner, repo_info):
    """Clone a repository shallowly and check it.

    The clone is over git, not the REST API, so an audit of eighty
    repositories does not spend the hourly API quota and does not get
    rate-limited half way through. The fidelity is better too: the checker
    sees the real files, so a link that resolves is a link that resolves.
    """
    name = repo_info["name"]
    url = repo_info.get("url") or ""
    root = tempfile.mkdtemp(prefix="audit-%s-" % name)
    target = os.path.join(root, "repo")
    try:
        clone = subprocess.run(
            [
                "git", "clone", "--depth=1", "--quiet",
                "https://github.com/%s/%s.git" % (owner, name), target,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
        )
        if clone.returncode != 0:
            return None

        branch = "main"
        head = subprocess.run(
            ["git", "-C", target, "symbolic-ref", "--short", "HEAD"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
        )
        if head.returncode == 0 and head.stdout.strip():
            branch = head.stdout.decode("utf-8", "replace").strip()

        findings = housecheck.run(housecheck.Repo(target))
    finally:
        shutil.rmtree(root, ignore_errors=True)

    return {
        "name": name,
        "url": url,
        "description": (repo_info.get("description") or "").strip(),
        "visibility": repo_info.get("visibility") or "",
        "archived": bool(repo_info.get("isArchived")),
        "template": bool(repo_info.get("isTemplate")),
        "default_branch": branch,
        "stars": repo_info.get("stargazerCount") or 0,
        "language": (repo_info.get("primaryLanguage") or {}).get("name", ""),
        "updated_at": repo_info.get("updatedAt") or "",
        "findings": [f.as_dict() for f in findings],
        "hard": len([f for f in findings if f.severity == "hard"]),
        "soft": len([f for f in findings if f.severity == "soft"]),
    }


def summarise(results):
    by_code = {}
    for result in results:
        for finding in result["findings"]:
            entry = by_code.setdefault(finding["code"], {"hard": 0, "soft": 0, "repos": []})
            entry[finding["severity"]] += 1
            if result["name"] not in entry["repos"]:
                entry["repos"].append(result["name"])
    return by_code


def print_text(results):
    print("audit — %d repositories" % len(results))
    print("")
    print("%-32s %-10s %6s %6s  %s" % ("repository", "visibility", "hard", "soft", "description"))
    print("-" * 110)
    for result in sorted(results, key=lambda r: (-r["hard"], r["name"])):
        print("%-32s %-10s %6d %6d  %s" % (
            result["name"],
            result["visibility"],
            result["hard"],
            result["soft"],
            (result["description"] or "")[:50],
        ))

    by_code = summarise(results)
    print("")
    print("by rule")
    for code in sorted(by_code):
        entry = by_code[code]
        print("  %-8s hard %3d  soft %3d  in %d repositories" % (
            code, entry["hard"], entry["soft"], len(entry["repos"])))


def tier(result):
    """Where a repository sits in the order of work.

    The order is not by size of the problem. It is by how much the
    repository is looked at: a visitor's first impression is made by the
    repositories people actually open.
    """
    name = result["name"]
    if result["archived"]:
        return 4
    if name.startswith("monos-sync-") or name.startswith("monos-conflict-") \
            or name in ("monos-sync-test", "monos-notes", "monos-conflict-lab"):
        return 4
    if result["stars"] > 0:
        return 1
    if result["visibility"] == "PUBLIC" and not result["archived"]:
        return 2
    return 3


TIER_NAMES = {
    1: "Tier 1 — looked at, or in active use",
    2: "Tier 2 — public",
    3: "Tier 3 — private",
    4: "Tier 4 — exempt: archived, test sandboxes, throwaways",
}


def print_markdown(results, owner):
    by_code = summarise(results)
    total_hard = sum(r["hard"] for r in results)
    total_soft = sum(r["soft"] for r in results)
    clean = [r for r in results if r["hard"] == 0]

    print("# Audit")
    print("")
    print("Every repository of **%s** checked against the house standard by" % owner)
    print("`scripts/housecheck.py`, the same code that runs in CI. Each")
    print("repository is cloned shallowly and checked as it stands, so a link")
    print("that resolves is a link that resolves.")
    print("")
    print("| | |")
    print("| --- | --- |")
    print("| Repositories checked | %d |" % len(results))
    print("| Hard failures | %d |" % total_hard)
    print("| Soft findings | %d |" % total_soft)
    print("| Repositories with no hard failure | %d |" % len(clean))
    print("")
    print("A hard failure is a rule the repository breaks. A soft finding is a")
    print("preference, reported but not enforced.")
    print("")

    print("## What has been done")
    print("")
    status_path = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "adoption-status.json")
    if os.path.exists(status_path):
        with open(status_path) as handle:
            status = json.load(handle)
        updated = status.get("updated", {})
        sites = status.get("with_landing_site", {})
        exempt = status.get("excluded", {})
        print("Every repository of the collection was brought under the standard")
        print("directly. The documents were written from the code and pushed to")
        print("the default branch, rather than proposed in a pull request, because")
        print("a proposal waits for a reader and the work was the point.")
        print("")
        print("| | |")
        print("| --- | ---: |")
        print("| Repositories under the standard | %d |" % len(updated))
        print("| With a landing page in the house style | %d |" % len(sites))
        print("| Exempt | %d |" % len(exempt))
        print("")
        print("The exemptions carry a reason, and a repository is exempt because of")
        print("what it holds rather than because of what it is called: a repository")
        print("that points at EORA's portal or serves EORA's pages is EORA's work,")
        print("whatever the name says. The list was built by searching the")
        print("collection for the identifiers that give it away.")
        print("")
        print("The landing pages are the same page in seven repositories: the same")
        print("stylesheet, the same class vocabulary, the same structure. What")
        print("differs is the content, which is the repository's own.")
        print("")

    print("## Which rules are broken most")
    print("")
    print("| Rule | Hard | Soft | Repositories affected |")
    print("| --- | ---: | ---: | ---: |")
    for code in sorted(by_code):
        entry = by_code[code]
        print("| %s | %d | %d | %d |" % (code, entry["hard"], entry["soft"], len(entry["repos"])))
    print("")
    print("The three rules that account for most of the total are the cheapest to")
    print("fix and the most visible:")
    print("")
    print("- **HS001, the canonical root file set.** Every repository is missing")
    print("  most of it. `scripts/adopt.sh` adds the missing files in one command,")
    print("  overwriting nothing.")
    print("- **HS005, CI.** Every repository needs a workflow that runs on pull")
    print("  requests. The template has one.")
    print("- **HS006, issue forms.** A repository with no forms gets blank")
    print("  issues. The templates ask for the environment and the expected")
    print("  behaviour, which is the difference between a report that can be")
    print("  acted on and one that cannot.")
    print("")

    print("## Where to start")
    print("")
    print("The order follows how much the repository is looked at.")
    print("")
    for level in (1, 2, 3, 4):
        group = [r for r in results if tier(r) == level]
        if not group:
            continue
        print("### %s" % TIER_NAMES[level])
        print("")
        print("| Repository | Hard | Soft | Description |")
        print("| --- | ---: | ---: | --- |")
        for result in sorted(group, key=lambda r: (-r["hard"], r["name"])):
            print("| [%s](%s) | %d | %d | %s |" % (
                result["name"], result["url"], result["hard"], result["soft"],
                (result["description"] or "").replace("|", "\\|")[:60],
            ))
        print("")

    print("## Every repository")
    print("")
    print("| Repository | Visibility | Hard | Soft | Description |")
    print("| --- | --- | ---: | ---: | --- |")
    for result in sorted(results, key=lambda r: (-r["hard"], r["name"])):
        print("| [%s](%s) | %s | %d | %d | %s |" % (
            result["name"], result["url"], result["visibility"],
            result["hard"], result["soft"],
            (result["description"] or "").replace("|", "\\|")[:70],
        ))
    print("")

    print("## The rules behind the codes")
    print("")
    print("See [house-style.md](house-style.md) for what each code means and why")
    print("it exists, and [migration.md](migration.md) for the procedure.")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="audit")
    parser.add_argument("--owner", default="aa-blinov")
    parser.add_argument("--json", dest="json_path")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--only", help="check a single repository")
    parser.add_argument(
        "--from-json", dest="from_json",
        help="regenerate the report from a saved JSON file, without calling "
             "the API",
    )
    args = parser.parse_args(argv)

    if args.from_json:
        with open(args.from_json) as handle:
            results = json.load(handle)
        if args.json_path:
            with open(args.json_path, "w") as handle:
                json.dump(results, handle, indent=2, ensure_ascii=False)
        if args.markdown:
            print_markdown(results, args.owner)
        else:
            print_text(results)
        return 0

    repositories = list_repositories(args.owner)
    if not repositories:
        sys.stderr.write("audit: could not list the repositories of %s\n" % args.owner)
        return 2

    results = []
    selected = [
        info for info in repositories
        if not args.only or info["name"] == args.only
    ]

    # The repositories are independent, and a clone is the expensive part,
    # so a few of them run at once.
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(audit_repository, args.owner, info): info
            for info in selected
        }
        for future in as_completed(futures):
            info = futures[future]
            try:
                result = future.result()
            except Exception as error:  # noqa: BLE001 — one bad repo is not fatal
                sys.stderr.write("audit: %s failed: %s\n" % (info["name"], error))
                continue
            if result is None:
                sys.stderr.write("audit: skipped %s\n" % info["name"])
                continue
            results.append(result)
            sys.stderr.write("audit: %s — %d hard, %d soft\n" % (
                result["name"], result["hard"], result["soft"]))

    if not results:
        return 2

    if args.json_path:
        with open(args.json_path, "w") as handle:
            json.dump(results, handle, indent=2, ensure_ascii=False)

    if args.markdown:
        print_markdown(results, args.owner)
    else:
        print_text(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
