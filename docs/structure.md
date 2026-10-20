# Structure

The canonical tree, and what each file is for.

Read this when you need to know what a file means, not what the rules are —
those are in [`house-style.md`](house-style.md).

```
<repo>/
├── README.md               # The front door. First thing a visitor reads.
├── AGENTS.md               # Re-entry surface. Commands, layout, traps, rails.
├── PRODUCT.md              # Durable product truth. What the product is.
├── DESIGN.md               # The visual system. Tokens, then how to apply them.
├── CHANGELOG.md            # What changed, newest first, and why it mattered.
├── CONTRIBUTING.md         # How to propose a change.
├── CODE_OF_CONDUCT.md     # How to behave.
├── SECURITY.md             # How to report a vulnerability, privately.
├── LICENSE                 # MIT, © Alexander Blinov.
├── .editorconfig           # Charset, indentation, final newline.
├── .gitignore              # What must never be committed.
├── .gitattributes          # Line endings, binary files, diff behaviour.
│
├── .impeccable/
│   ├── config.json         # Workflow settings, e.g. buildPath.
│   └── design.json         # The design sidecar: ramps, motion, components.
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md   # What happens, what was expected, how to reproduce.
│   │   ├── feature_request.md
│   │   └── config.yml      # Blank issues off, contact links on.
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml          # Install, test, build.
│       ├── release.yml     # Tag-triggered release.
│       └── house-style.yml # The standard, enforced.
│
├── docs/
│   ├── README.md           # Index of the documents.
│   ├── architecture.md     # How it is put together, and why.
│   └── screenshots/        # Images referenced from the README.
│
├── scripts/                # Everything executable that is not source.
├── src/                    # The code.
├── tests/                  # The tests.
├── assets/                 # Icons, fonts, static files. If the project has any.
└── ...                     # Whatever else the project needs.
```

## The root files

### `README.md`

The front door, and the only file most visitors will read. It answers, in this
order: how do I run this, what does it do, what does it look like, how is it
configured, how is it built, how do I work on it, what licence is it under.

The section order is fixed. The wording is not — a project in Russian uses
Russian headings.

### `AGENTS.md`

The re-entry surface. Its job is to save the next session — human or agent —
from rediscovering the project. It contains:

- **How to run, build and test it.** The exact commands, not the shapes of
  commands.
- **Where things live.** A table, not a paragraph.
- **The traps.** The things that cost a rebuild to learn, written down.
- **The rails.** What may not be changed without asking.

It is not a tutorial and not a design document. It is the notes you would
otherwise leave in a chat message that will not be found.

### The template marker

Every file that comes from `templates/` opens with a marker:

```html
<!-- house-style: template — fill this file in, then delete this line -->
```

The marker is how the checker knows the file is still a template rather than
a finished document. It costs nothing in the rendered output, and deleting
it is the last step of filling the file in.

Files that need no per-project content — `CHANGELOG.md`, `CONTRIBUTING.md`,
`SECURITY.md`, `CODE_OF_CONDUCT.md` — carry no marker. They are ready to
use once the tokens are substituted.

### `PRODUCT.md`

Durable product truth, in the `impeccable:product-schema` format. It records
what the product is, who it is for, what it promises, what it may not do, and
what evidence actually exists.

Its most important job is the negative one: it says what is *not* true, so
that a later session does not invent a user, a benchmark, a testimonial or a
feature. A repository whose `PRODUCT.md` claims a metric that nobody measured
will, eventually, have that metric quoted back at it.

It is written once and changed rarely. If it changes often, it is a task
list, and it belongs somewhere else.

### `DESIGN.md`

The visual system, in the official DESIGN.md format: YAML frontmatter with the
tokens, then up to eight prose sections that explain how to apply them.

The frontmatter is normative. If the prose and the frontmatter disagree about
a colour, the frontmatter is right.

### `CHANGELOG.md`

Keep a Changelog format, newest first. Each entry says what changed and why it
was worth changing. The traps do not go here — they go in `AGENTS.md`, because
the changelog is read by users and the traps are read by whoever works on the
code next.

### `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`

The community health files. GitHub surfaces them automatically: a
"Contributing" tab, a "Code of conduct" tab, and a place to report a
vulnerability privately. All three are short, and all three are better than
nothing.

### `LICENSE`, `.editorconfig`, `.gitignore`, `.gitattributes`

The terms, and the text-file conventions. MIT, with the holder named.

## The directories

### `.github/`

`workflows/` holds the CI. `ISSUE_TEMPLATE/` holds the forms. The forms
matter more than they look: a form that asks for the environment and the
expected behaviour turns a bug report into a reproducible one.

The `house-style.yml` workflow checks the standard against the repository. In
the golden repository it runs the checker from the checkout; in a repository
that adopts the standard, it runs the checker from
`aa-blinov/golden-repo`, so that the standard can be updated in one place and
every repository picks the change up.

### `.impeccable/`

`design.json` is the sidecar to `DESIGN.md`: the tonal ramps, shadows,
motion, breakpoints, component snippets and the narrative rules, none of which
fit in the frontmatter schema. `config.json` holds workflow settings.

### `docs/`

The documents the README points at, and the screenshots it shows. `docs/` has
its own `README.md` index, because a folder of documents with no entry point
is a folder nobody opens.

### `scripts/`, `src/`, `tests/`

Everything executable that is not source goes in `scripts/`. The code goes in
`src/`, the tests in `tests/`. A project whose stack does not use `src/` —
a Go project with packages at the root, a single-file script — keeps its
layout and says so in its `AGENTS.md`.

## What a project may add

Anything it needs. The standard is a floor, not a ceiling.

A project with a landing page adds `docs/index.html` and a `pages.yml`
workflow. A project with a CLI adds `docs/cli-reference.md`. A monorepo adds
one package per directory and keeps the root file set once, at the root.

What a project may not do is remove one of the root files, or reorder the
README's required sections, without saying so in its own `AGENTS.md`. An
exception that is written down is an exception. One that is not is an
accident.
