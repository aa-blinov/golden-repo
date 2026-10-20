# golden-repo

Canonical shape for every repository I own. One file tree, one README order, one
voice — so that `koloda`, `puuush`, `petzy` and whatever comes next read as the
work of one author, not of four strangers.

This repository is three things at once: the **standard** itself (the rules live
in [`docs/house-style.md`](docs/house-style.md)), a **worked example** (every
file here is a filled-in copy of the template), and a **toolchain** that applies
the standard to other repositories and proves they still follow it.

[![House style](https://github.com/aa-blinov/golden-repo/actions/workflows/house-style.yml/badge.svg)](https://github.com/aa-blinov/golden-repo/actions/workflows/house-style.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Quick start

```bash
git clone https://github.com/aa-blinov/golden-repo.git
cd golden-repo
python3 scripts/housecheck.py --strict .
```

That is the whole installation. The checker is plain Python 3 with no
dependencies, so it runs anywhere Python does — a fresh laptop, a CI
container, a macOS runner.

Three commands, one contract:

| Command | What it does |
| --- | --- |
| `scripts/new-repo.sh <name>` | Scaffolds a new project from `templates/` with every standard file in place. |
| `scripts/adopt.sh <path>` | Brings an **existing** repository up to the standard without touching its code. |
| `scripts/housecheck.py <path>` | Verifies that a repository follows the standard. Exit code 0 means it does. |

And one that looks at all of them at once:

| Command | What it does |
| --- | --- |
| `scripts/audit.py --owner aa-blinov` | Checks every repository of an owner against the standard, one shallow clone at a time. |

### Start a new project

```bash
gh repo create aa-blinov/<name> --template aa-blinov/golden-repo --public
cd <name>
../golden-repo/scripts/new-repo.sh .          # or: scripts/new-repo.sh <name>
```

`new-repo.sh` copies `templates/`, substitutes the `{{ … }}` tokens, and leaves
you a repository whose only remaining findings are the ones that ask you to
fill it in. Fill in `PRODUCT.md` first — everything else depends on it.

### Bring an existing project to the standard

```bash
../golden-repo/scripts/adopt.sh ~/code/some-project
```

`adopt.sh` is deliberately conservative. It **adds** the files that are missing
and never overwrites a file that already exists, because a repository that has
been running for a year has opinions its owner did not write down. What it
cannot add safely — `PRODUCT.md`, `DESIGN.md` — it creates as a stub with the
questions to answer marked inline.

Afterwards, run the checker to see what is left:

```bash
scripts/housecheck.py ~/code/some-project
```

### Check a repository

```bash
scripts/housecheck.py                # checks the current directory
scripts/housecheck.py --strict       # warnings become failures
scripts/housecheck.py --json         # machine-readable, for CI
```

The exit code is `0` when every hard rule passes, `1` otherwise. CI runs it on
every push and pull request.

## What it does

The standard is three things at once: the **rules** themselves
([`docs/house-style.md`](docs/house-style.md)), a **worked example** (every
file in this repository is a filled-in copy of the template), and a
**toolchain** that applies the standard to other repositories and proves they
still follow it.

The checker is the point. A written standard decays the moment it is only prose;
a checker fails the build instead, and the build fails before the standard does.

## The standard in one screen

Every repository carries the same root. Nothing here is optional unless the
rule says so.

```
<repo>/
├── README.md            # The front door. H1 = product name, then a pitch.
├── AGENTS.md            # Commands, layout, traps, rails. For humans and agents alike.
├── PRODUCT.md           # Durable product truth. impeccable:product-schema 1.
├── DESIGN.md            # Visual system. YAML frontmatter + 8 canonical sections.
├── CHANGELOG.md         # Keep a Changelog. Newest first.
├── CONTRIBUTING.md      # How to propose a change.
├── CODE_OF_CONDUCT.md   # How to behave.
├── SECURITY.md          # How to report a vulnerability.
├── LICENSE              # MIT, © Alexander Blinov.
├── .editorconfig        # Indentation, charset, final newline.
├── .gitignore
├── .impeccable/         # design.json sidecar + config.json
├── .github/
│   ├── ISSUE_TEMPLATE/  # bug_report.md, feature_request.md, config.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml
│   └── workflows/       # ci.yml, release.yml
├── docs/                # Guides, architecture, screenshots.
├── scripts/             # bootstrap, build, release helpers.
├── src/                 # Code.
└── tests/               # Tests.
```

Three rules explain most of the rest:

1. **The README is ordered.** Quick start, then what it does, then screens, then
   configuration, then how it works, then development, then license. A visitor
   should never have to hunt for how to run the thing.
2. **Facts over adjectives.** Sizes, versions and error paths are named
   precisely. "Faster" is not a fact; "97,469,540 B" is.
3. **No emojis.** Anywhere, in any file. They render inconsistently in
   terminals, diffs and issue trackers, and they make a repository look like a
   brochure.

The full list, with the reasoning behind each rule, is in
[`docs/house-style.md`](docs/house-style.md).

## What the checker enforces

Hard rules — the build fails without them:

- The root file set exists, and `LICENSE` names a real license and a real holder.
- `README.md` opens with a single H1 and contains the required sections.
- `PRODUCT.md` carries the `impeccable:product-schema` marker and its sections.
- `DESIGN.md` has YAML frontmatter and its eight canonical sections in order.
- Every relative link and image in every Markdown file resolves.
- No emoji in any tracked text file.
- No heading level is skipped, no trailing whitespace, every file ends in a newline.
- No file larger than 50 MB is committed, and nothing above 100 MB at all.

Soft rules — reported, not enforced:

- `README.md` and `AGENTS.md` are non-trivial, i.e. they are not stubs.
- The repository description is set and is not the repository name.
- A `docs/` index exists and links to the other guides.
- The default branch is `main`.

The list of rules and the rationale for each is in
[`docs/house-style.md`](docs/house-style.md). The checker is the normative
implementation — if the two disagree, the checker is the standard and the
document is the bug.

## Documentation

| Guide | What it covers |
| --- | --- |
| [`docs/house-style.md`](docs/house-style.md) | Every rule, why it exists, and how to satisfy it. |
| [`docs/structure.md`](docs/structure.md) | The canonical tree, file by file, with the contract for each. |
| [`docs/writing.md`](docs/writing.md) | Voice, README section order, the Russian/English policy. |
| [`docs/migration.md`](docs/migration.md) | Bringing an existing repository to the standard, safely. |
| [`docs/audit.md`](docs/audit.md) | Where the existing repositories stand today. |

## Development

```bash
scripts/housecheck.py .            # the standard, applied to itself
scripts/housecheck.py --strict .   # including soft rules
python3 -m unittest discover -s tests -v
```

The checker is tested in `tests/`, and the tests are what keep the rules
honest.

## License

MIT — © Alexander Blinov. See [LICENSE](LICENSE).
