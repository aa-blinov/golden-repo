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
scripts/adopt_bot.py <repository>   # open the pull request that adopts it
scripts/audit.py --owner aa-blinov # check every repository of an owner at once
scripts/bump.py                    # move the pin in every adopting repository
scripts/render.py                  # regenerate the documents from standard.json
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
| `docs/new-repo.md` | Creating a repository from the scaffolder. The traps. |
| `docs/stacks.md` | Per-stack tooling, the traps, and what CI must run. |
| `docs/migration.md` | The procedure for existing repositories. |
| `docs/audit.md` | The state of the existing repositories. |
| `scripts/housecheck.py` | The enforcer. The rules as code. |
| `scripts/new-repo.sh` | Scaffolder. Reads `templates/`. |
| `scripts/adopt.sh` | Migrator. Adds what is missing, overwrites nothing. |
| `scripts/adopt_bot.py` | Opens the pull request that adopts a repository. |
| `scripts/audit.py` | Checks every repository of an owner at once, over the API. |
| `scripts/bump.py` | Opens the pull request that moves the pin in every adopting repository. |
| `scripts/render.py` | Writes the documents from `standard.json`. |
| `scripts/scaffold.py` | The file work behind the scaffolder and the migrator. |
| `standard.json` | The standard as data. The single source of truth. |
| `adopters.json` | The repositories that depend on the standard. |
| `adoption-targets.json` | The repositories the adoption workflow works through. |
| `templates/` | Placeholder files with `{{ … }}` markers. |
| `tests/` | Unit tests for the checker and for the standard's own layers. |

## The contract between the layers

The standard is described in four places, and they may disagree in one
direction only:

1. `standard.json` — the rules as data. The single source of truth.
2. `scripts/housecheck.py` — the rules as code. It reads the manifest.
3. `templates/` — the rules as starting files. The scaffolder builds from the
   manifest and fills these in.
4. `docs/house-style.md` — the rules as prose. The part that explains why.

**The manifest wins.** If the prose and the manifest disagree, the manifest is
the standard and the prose is a bug to be filed. The checker and the
scaffolder both read the manifest, so they cannot disagree with each other
either. The prose is the only layer that can be wrong, and a test in
`tests/test_standard.py` fails when it is.

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

1. Add it to `standard.json`. That is where the file set and the section
   lists live, and the checker reads them from there.
2. Write the rule in `docs/house-style.md` with its rationale and a passing
   and a failing example.
3. If the rule adds a file, add a template for it in `templates/`. The test
   in `tests/test_standard.py` fails otherwise.
4. Implement the check in `scripts/housecheck.py`, if it needs one. Give it a
   stable code (`HS001`-style, never renumbered) so that the audit report
   stays readable.
5. Add a test in `tests/test_housecheck.py`. A rule with no test is a rule
   with a bug in it.
6. Run `scripts/render.py` to write the documents from the manifest, then
   `scripts/housecheck.py --strict .`. The golden repository must still pass.
   If it cannot satisfy its own rules, the rules are wrong.

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
