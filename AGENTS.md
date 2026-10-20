# AGENTS.md — agent context for `golden-repo`

This repository is the house standard for every other repository I own. It holds
rules, templates and the checker that enforces them. Read this file before
changing anything here: the rules in `docs/house-style.md` are the product, and
the checker is the normative implementation of them.

## Run / check / test

```bash
scripts/housecheck.py .            # check a repository against the standard
scripts/housecheck.py --strict .   # soft rules become failures too
scripts/housecheck.py --json .     # machine-readable report
scripts/new-repo.sh <name>         # scaffold a new project from templates/
scripts/adopt.sh <path>            # bring an existing repository up to the standard
scripts/audit.py --owner aa-blinov # check every repository of an owner at once
python3 -m unittest discover -s tests -v
```

There is no build step and no package manifest on purpose: the standard has to
run on a machine that has nothing but Python 3 installed.

## Where things live

| Path | What it is |
| --- | --- |
| `docs/house-style.md` | The rules. Normative prose. |
| `docs/structure.md` | The canonical tree, annotated. |
| `docs/writing.md` | Voice, README order, the RU/EN policy. |
| `docs/migration.md` | The procedure for existing repositories. |
| `docs/audit.md` | The state of the existing repositories. |
| `scripts/housecheck.py` | The enforcer. The rules as code. |
| `scripts/new-repo.sh` | Scaffolder. Reads `templates/`. |
| `scripts/adopt.sh` | Migrator. Adds what is missing, overwrites nothing. |
| `scripts/audit.py` | Checks every repository of an owner at once, over the API. |
| `templates/` | Placeholder files with `{{ … }}` markers. |
| `tests/` | Unit tests for the checker. |

## The contract between the three layers

There are three descriptions of the same standard, and they are allowed to
disagree only in one direction:

1. `docs/house-style.md` — the rules as prose.
2. `scripts/housecheck.py` — the rules as code.
3. `templates/` — the rules as starting files.

**The checker wins.** If the prose and the checker disagree, the checker is the
standard and the prose is a bug to be filed. Two people reading the prose and
disagreeing about it is exactly the failure this design exists to prevent.

Adding a rule therefore means touching all three:

- write the rule in `docs/house-style.md`,
- implement it in `scripts/housecheck.py`,
- add a test in `tests/`.

A rule that exists only in the prose will be forgotten, because prose does not
fail anything.

## How the checker is written

Plain Python 3, standard library only, no third-party packages. It must run on
a bare runner with no `pip install` step, because it runs in CI for every
repository that adopts it.

- Each rule is a function `check_<area>_<thing>(repo) -> Finding`.
- `Finding` carries a severity (`hard` or `soft`), a code, a path and a message.
- Rules never mutate the repository. The checker reads and reports; `adopt.sh`
  writes.
- A rule that needs a network call (repository description, default branch) is
  opt-in through `--remote` and degrades to a soft finding when it cannot run.
- Exit code is `0` when no hard rule failed, `1` otherwise. Soft findings do not
  affect the exit code unless `--strict` is passed.

The golden rule for this file: **a rule that cannot be checked is a
preference.** Preferences go in `docs/writing.md`, where they can inform a
human without blocking a build.

## Style / safety rails

- **No emojis**, in any file, ever. Not one of the repositories that already
  read correctly contains any, and the checker guards this rule hardest.
- **Comments explain *why*, never *what*.**
- **Do not add dependencies.** The checker runs where Python is installed and
  nothing else. A `requirements.txt` here would defeat the entire point.
- **Do not weaken a rule to make a repository pass.** A repository that
  violates the standard needs fixing, and `adopt.sh` exists for exactly that.
  If a rule is genuinely wrong, change it deliberately, in the open, with a
  test, rather than carving out an exception.
- **Prefer adding a rule over adding a convention.** A convention that is only
  written down gets broken silently within a month. A rule that fails CI gets
  fixed in minutes.

## Adding a rule, end to end

1. Write the rule in `docs/house-style.md` with its rationale and a passing and
   a failing example.
2. Implement it in `scripts/housecheck.py`. Give it a stable code
   (`HS001`-style, never renumbered) so that the audit report stays readable.
3. Add a test in `tests/test_housecheck.py`. A rule with no test is a rule with
   a bug in it.
4. Run `scripts/housecheck.py --strict .` and make sure the golden repository
   itself passes. If the golden repository cannot satisfy its own rules, the
   rules are wrong.

## Release

The standard changes when the rules change. Tag a release when a change
alters the canonical file set or the meaning of an existing rule; skip the tag
for prose fixes and new optional checks.

```bash
scripts/housecheck.py --strict .
python3 -m unittest discover -s tests
git tag -a v1.0.0 -m "v1.0.0 — canonical file set v1"
git push --tags
```
