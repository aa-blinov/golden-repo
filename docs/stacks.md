# Working with a stack

The standard fixes what a repository looks like. It does not fix the language
it is written in: a Python project and a Go project share the root file set,
not their tooling. What follows is the narrow part the standard can still say,
because the alternative is sixty repositories each rediscovering the same
trap.

Each section names three things: what the repository has to have wired, the
one failure the ecosystem does not catch by itself, and the commands CI has to
run. The rules behind the checkable half live in `scripts/housecheck.py` as
`HS210` to `HS215`, and each one fails the build. Every rule was introduced
soft, the collection was fixed, and only then did it start blocking.

**What this document is not.** It is not how to write Python or Go. The
formatter, the linter and the type checker already say that, and a document
that restates them goes stale faster than the tools do.

## Python

Wire: `pyproject.toml` with the tool configuration (`ruff`, `pytest`, and the
type checker if the project has one). A `requirements.txt` is enough for a
project that has not moved yet.

The trap: a request that cannot fail its certificate check. `verify=False` and
`urllib3.disable_warnings(InsecureRequestWarning)` turn a private certificate
into no certificate, silently, and the call reads like every other call.
`HS212`.

The other trap: the notebook. A cell run once and committed carries whatever
key it used, and a notebook is the one file nobody greps. `HS213` covers
`.ipynb` beside the build configs.

CI must run: the formatter in check mode, the linter, the tests. A repository
where these run only on someone's laptop is a repository where they do not
run.

## Node and TypeScript

Wire: `package.json` with `engines.node`, a committed lockfile, and the
`packageManager` field when the project uses pnpm. `HS210` for the runtime,
`HS211` for the lockfile.

The trap: the runtime the dependency tree needs is not the runtime CI
installs. One repository here died inside `undici` because the workflow
installed Node 20 and a transitive package declared 22.19. `engines.node` is
where that minimum belongs, and the workflow should read it rather than
restate it.

The second trap: peers. A major bump of one package moves a peer range that
another package has not caught up with, and the install fails on a machine
that resolved a different tree. The lockfile is the contract; a dependency
added by hand without one is a different tree.

CI must run: install from the lockfile (`--frozen-lockfile`), the type check,
the linter, the tests, the build.

## Go

Wire: `go.mod` with the version the code was written against, and the same
version in the workflow. `HS214` compares them.

The trap: `govulncheck` fails the build when the standard library behind it
predates a fix, and the fix ships in a patch release. A module that says
`go 1.27.3` while CI installs `1.27.2` is a build that fails on a Tuesday for
a reason nobody changed.

CI must run: `go vet`, the tests with the race detector where they are cheap
enough, `govulncheck`, and the build.

## Swift

Wire: `.swiftformat` and `.swiftlint.yml` if the project uses them, and a CI
step that installs **that** version of the tool. `HS215` reports a formatter
installed without a version.

The trap: the formatter changes its rules between minor releases. SwiftFormat
0.63 and 0.64 disagree about indentation, and a repository here went red
because the runner had the older one while the code was formatted with the
newer. Pinning the version is not caution, it is the only way a formatting
rule means anything.

CI must run: the formatter in lint mode, the linter, the tests, the build.

## Everything else

A repository that is a shell script, a static page or a collection of small
tools has no stack section, and that is fine. The root file set, the README
order and the checker still apply.
