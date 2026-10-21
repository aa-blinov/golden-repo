# Documentation

The house standard, in six documents and a checker.

| Document | What it covers |
| --- | --- |
| [`house-style.md`](house-style.md) | Every rule, with its code, its rationale, and its severity. The normative document. |
| [`structure.md`](structure.md) | The canonical tree, file by file, and what each file is for. |
| [`writing.md`](writing.md) | Voice, README section order, the Russian/English policy. Preferences, not rules. |
| [`new-repo.md`](new-repo.md) | Creating a repository from the scaffolder, and the traps that cost time. |
| [`migration.md`](migration.md) | Bringing an existing repository to the standard, safely, and in what order. |
| [`audit.md`](audit.md) | Where the existing repositories stand today, and which are worth the effort. |

## The toolchain

| Command | What it does |
| --- | --- |
| `scripts/housecheck.py` | Checks a repository against the standard. Exit code 0 means it passes. |
| `scripts/new-repo.sh` | Scaffolds a new project from `templates/`. |
| `scripts/adopt.sh` | Brings an existing repository up to the standard, overwriting nothing. |
| `scripts/audit.py` | Checks every repository of an owner at once, one shallow clone at a time. |

## The three layers

The standard is described three times, and they may disagree in one direction
only:

1. [`house-style.md`](house-style.md) — the rules as prose.
2. `scripts/housecheck.py` — the rules as code.
3. `templates/` — the rules as starting files.

**The checker wins.** If the prose and the checker disagree, the checker is the
standard and the prose is a bug.

## Reading order

New project: [`new-repo.md`](new-repo.md) for the steps, then
[`structure.md`](structure.md) and [`writing.md`](writing.md) for what goes
in each file.

Existing project: [`migration.md`](migration.md), then
[`audit.md`](audit.md) to see where the repository stands.

Changing the standard: read [`../AGENTS.md`](../AGENTS.md) first, since it
describes the contract between the three layers, then
[`house-style.md`](house-style.md).
