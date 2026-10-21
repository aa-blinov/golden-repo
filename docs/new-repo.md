# A new repository

Creating a repository is four steps, in this order: scaffold it, tell GitHub
what it is, get the first check green, and only then write the product. A
repository whose first commit is green stays green, because every later
commit is measured against the standard that was there from the start.

## The short version

```bash
cd ~/Documents/pet
../golden-repo/scripts/new-repo.sh my-project --name "My Project"
cd my-project
git add -A
git commit -m "Start from the house standard"
```

Then create the repository on GitHub, push, and wait for `house style` to pass
before you write anything else.

## Use the scaffolder, not the template button

`golden-repo` is marked as a template on GitHub, so its page carries a green
"Use this template" button. That button copies **the standard itself**: the
rules, the audit, the findings, the checker. It gives you a second copy of the
documentation about the rules, not a repository that follows them.

`scripts/new-repo.sh` is the entry point. It reads the file list from
`standard.json` and the content from `templates/`, replaces the placeholders,
inits git on `main`, and prints what to do next. The checker and the
scaffolder read the same manifest, so the repository it builds is by
construction the set the checker will accept.

It refuses to touch a non-empty directory. For a repository that already
exists, `scripts/adopt.sh` is the one to use.

## What the scaffolder writes

Twenty-odd files: the front door (`README.md`), the three documents that carry
durable truth (`PRODUCT.md`, `DESIGN.md`, `AGENTS.md`), the paperwork
(`CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
`LICENSE`), the GitHub furniture in `.github/`, the design sidecar in
`.impeccable/`, and an empty `docs/` with its index.

The content is a skeleton with the real sentences already in place. The
paragraphs that state what the product does are placeholders and are meant to
be replaced.

## The five things GitHub needs

**A description that is a sentence.** Not the repository name repeated. The
checker reports an empty description or one that repeats the name (HS101), and
only under `--remote`, because it needs the API.

**`main` as the default branch.** The standard asks for it (HS100). More
importantly, `.github/workflows/house-style.yml` and `ci.yml` filter on a
branch name, and a filter that names a branch that does not exist runs
nothing and looks green. If you keep another default branch, change the filter
in both workflows on the same day.

**Topics, if the project belongs to a group.** `telegram-bot`, `cli`,
`fastapi`. They are how the collection stays navigable after sixty
repositories.

**The pin.** `.github/workflows/house-style.yml` references
`aa-blinov/golden-repo/.github/actions/house-style@v1.0.10`. That tag is what
this repository follows, and improvements to the standard reach it by moving
the pin. `scripts/bump.py` moves it in every adopting repository at once.

**Protection on `main`.** Require the `house style` and `CI` checks before a
merge. Without it the standard is advice.

## Filling it in, in order

1. **`PRODUCT.md`.** The durable truth: who it is for, what it does, what it
   refuses to do, the vocabulary. Everything else is derived from this file,
   and the README is a summary of it.
2. **`DESIGN.md`.** The visual system, if the project has one. The frontmatter
   carries the palette ramps and the motion tokens. If the project has no
   interface, delete the file and say so in `PRODUCT.md`.
3. **`README.md`.** In the order the standard fixes: what it is, a quick start
   that works from a clean machine, what it does, how it is built, how to
   develop, the licence. The order is in `format.md`.
4. **`CHANGELOG.md`.** One `## [Unreleased]` section at the top, empty. It
   fills as you go, not at release time.
5. **`docs/architecture.md`.** When there is a decision worth explaining. Not
   before: a file that says "TBD" is worse than no file.
6. **`docs/screenshots/`.** Add the images when the interface exists, and
   reference them from the README.

## Before the first feature commit

```bash
python3 ../golden-repo/scripts/housecheck.py --strict .
python3 -m unittest discover -s tests
python3 ../golden-repo/scripts/anti_ai.py .
```

All three exit 0. Then push and watch the two workflows. A red first commit is
much easier to fix than a red fiftieth.

## Traps

These are the ones that cost real time on this collection, in the order they
bite.

**The directory name becomes the slug.** `new-repo.sh my-project` writes
`my-project` into every file, into the CI matrix, and into the badge URLs.
Renaming later means editing every file that names the project. Pick the name
before you run the command.

**A bare `config.json` in `.gitignore` matches at every depth.** It swallowed
`.impeccable/config.json` in a repository here, and the checker then reported
the missing file for weeks. Patterns for the sidecar need a leading slash or a
directory prefix. A negation cannot rescue a file inside an ignored directory,
so ignore `.impeccable/*` and not `.impeccable/`.

**A landing page goes in `site/`.** Not in `docs/`, and not at the root,
unless the repository is itself a site. `scripts/apply_docs.py` detects the
folder by the page's doctype and its companion stylesheet.

**If a test reads the page, the page keeps what the test reads.** Replacing a
landing page has broken somebody's test three times here: a class the test
splits on, a table it parses by name, an anchor it follows. Read the tests
that mention the page before you rewrite it.

**A link that differs only in case is broken for everyone but you.** The
checker compares the path exactly, so `docs/ARCHITECTURE.md` no longer passes
against `docs/architecture.md`, even on a machine that cannot tell them apart.

**Skills are installed, not vendored.** Do not copy an agent skill into the
repository. The checker skips `.agents/`, `.claude/` and `skills/` because
that content is somebody else's work, and a copy in every repository is one
more thing to keep current by hand.

**Do not tag a release to mark progress.** The tag on `golden-repo` is what
every other repository pulls. Tag when the rules change, not when the work
feels finished.
