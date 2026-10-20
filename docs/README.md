# Documentation

The house standard, in four documents and a checker.

| Document | What it covers |
| --- | --- |
| [`house-style.md`](house-style.md) | Every rule, with its code, its rationale, and its severity. The normative document. |
| [`structure.md`](structure.md) | The canonical tree, file by file, and what each file is for. |
| [`writing.md`](writing.md) | Voice, README section order, the Russian/English policy. Preferences, not rules. |
| [`migration.md`](migration.md) | Bringing an existing repository to the standard, safely, and in what order. |
| [`audit.md`](audit.md) | Where the existing repositories stand today, and which are worth the effort. |

## The toolchain

| Command | What it does |
| --- | --- |
| `scripts/housecheck.py` | Checks a repository against the standard. Exit code 0 means it passes. |
| `scripts/new-repo.sh` | Scaffolds a new project from `templates/`. |
| `scripts/adopt.sh` | Brings an existing repository up to the standard, overwriting nothing. |
| `scripts/audit.py` | Checks every repository of an owner at once, without cloning any of them. |

## The three layers

The standard is described three times, and they may disagree in one direction
only:

1. [`house-style.md`](house-style.md) — the rules as prose.
2. `scripts/housecheck.py` — the rules as code.
3. `templates/` — the rules as starting files.

**The checker wins.** If the prose and the checker disagree, the checker is the
standard and the prose is a bug.

## Reading order

New project: [`structure.md`](structure.md), then
[`writing.md`](writing.md), then copy `templates/`.

Existing project: [`migration.md`](migration.md), then
[`audit.md`](audit.md) to see where the repository stands.

Changing the standard: [`house-style.md`](house-style.md), and read
[`../AGENTS.md`](../AGENTS.md) first — it describes the contract between the
three layers.
