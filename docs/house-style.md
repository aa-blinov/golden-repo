# House style

The rules. Every repository I own follows them, and
[`scripts/housecheck.py`](../scripts/housecheck.py) checks them.

This document explains what each rule is for. Where the document and the
checker disagree, **the checker is the standard** and this file is a bug to be
filed. A standard that two people read and disagree about is not a standard.

## How to read this

Each rule has a stable code (`HS###`). The code never changes and is never
reused, so a finding from a report written last year still points at the same
rule.

- **Hard** — the check fails. CI goes red. A repository that violates a hard
  rule is not finished.
- **Soft** — the check reports it. CI stays green unless `--strict` is passed.
  Soft rules are either preferences, or rules that need information the
  checker cannot get without a network call.

A rule that cannot be checked is a preference, and preferences live in
[`writing.md`](writing.md), where they inform a human without blocking a
build.

## Where the rules came from

Not from an external template. They were read off the repositories that
already look like one author's work — `lazy-to-text`, `cast`, `puuush`, `petzy`,
`monos`, `koloda`, `better-ssh`, `templates-mcp` — and written down. Where a
rule comes from a specific observation, the rule says so.

Three traits survived the survey of every repository, without exception:

- **No emoji**, in any file. Across every Markdown file of the repositories
  that read correctly: zero.
- **A README that answers in a fixed order**: quick start, what it does, then
  everything else.
- **A `PRODUCT.md` with the same ten sections** and a `DESIGN.md` with the
  `impeccable` frontmatter.

The rest is the shape of a well-kept repository, confirmed against GitHub's own
documentation on best practices, README discovery order, community health
files and template repositories.

---

## Structure

### HS001 — The canonical root file set exists

**Hard.** These files must be present in every repository:

<!-- BEGIN:standard-files -->
| File | What it carries |
| --- | --- |
| `README.md` | The front door. H1 = product name, then a pitch. |
| `AGENTS.md` | Commands, layout, traps, rails. For humans and agents alike. |
| `PRODUCT.md` | Durable product truth. impeccable:product-schema 1. |
| `DESIGN.md` | Visual system. YAML frontmatter + 8 canonical sections. |
| `CHANGELOG.md` | Keep a Changelog. Newest first. |
| `CONTRIBUTING.md` | How to propose a change. |
| `CODE_OF_CONDUCT.md` | How to behave. |
| `SECURITY.md` | How to report a vulnerability. |
| `LICENSE` | MIT, © Alexander Blinov. |
| `.editorconfig` | Charset, indentation, final newline. |
| `.gitignore` | What must never be committed. |
| `.github/workflows/ci.yml` | Install, test, build. |
| `.github/workflows/house-style.yml` | The standard, enforced. |
| `.github/ISSUE_TEMPLATE/bug_report.md` | What happens, what was expected, how to reproduce. |
| `.impeccable/config.json` | Workflow settings, e.g. buildPath. |
| `.impeccable/design.json` | The design sidecar: ramps, motion, components. |
| `docs/README.md` | Index of the documents. |
<!-- END:standard-files -->

**Why.** The point of the standard is that a reader who learns one repository
has learned all of them. The file set is the part of that which can be checked
without reading anything.

A repository with a code of conduct gets a "Code of conduct" tab and a
"Contributing" link in the sidebar, automatically, from these two files. A
repository with a `SECURITY.md` gets a security policy surface and a place for
a reporter to go. These are GitHub's own mechanisms, and they are free.

### HS002 — The canonical directory set exists

**Hard.** These directories must be present:

<!-- BEGIN:standard-directories -->
| Directory | What goes in it |
| --- | --- |
| `.github/` | GitHub's own directory: workflows, forms, templates. |
| `.github/workflows/` | CI, release, and the house-style check. |
| `.github/ISSUE_TEMPLATE/` | Issue forms. |
| `.impeccable/` | The design sidecar and its config. |
| `docs/` | Guides, architecture, screenshots. |
| `docs/screenshots/` | Images referenced from the README. |
| `scripts/` | Everything executable that is not source. |
| `src/` | The code. |
| `tests/` | The tests. |
<!-- END:standard-directories -->

**Why.** Same reason as HS001, for the parts of a repository that are
directories.

A stack that does not use `src/` — a Go project with packages at the root, a
single-file script — still has the directory, with a short `README.md` in it
saying what the project does instead. The point is that a reader, and an
agent, knows where to look without being told. The exception is written down
in the place a reader will find it, rather than being tolerated silently.

An empty directory does not survive a git clone, so the directory has to
carry a file. That is the whole reason the golden repository's `src/`
contains a README and no code.

### HS003 — `LICENSE` names a real license

**Hard.** `LICENSE` must be recognisable as one of the standard licenses
(GitHub's licensee library identifies it), and it must not be empty.

**Why.** A repository without a license is a repository nobody may use. The
check is on the license's identity, not on its text, so the standard does not
dictate the wording.

### HS004 — The copyright holder is named

**Hard.** `LICENSE` must contain a `Copyright` line with a holder.

**Why.** A license without a copyright holder is a template that was never
filled in. The house holder is **Alexander Blinov**. Repositories that say
`aa-blinov` instead are using the account name rather than the holder, and
should be corrected to the real name.

### HS005 — CI exists

**Hard.** `.github/workflows/` must contain a workflow that runs on pull
requests.

**Why.** A repository with no CI is a repository where "it works" is an
opinion. The workflow's contents are the project's business; that it exists is
the standard's business.

### HS006 — Issue forms exist

**Hard.** `.github/ISSUE_TEMPLATE/` must exist and contain at least one file.

**Why.** A blank issue form is a blank issue. The forms in this repository
ask for the reproduction, the environment and the expected behaviour, which is
the difference between a report that can be acted on and one that cannot.

### HS007 / HS008 — No large files

**Hard.** No committed file above 50 MB. Nothing above 100 MB, which GitHub
rejects outright.

**Why.** A 60 MB file in a repository makes every clone slow, for everyone,
forever, for a file that almost certainly belongs in a release asset or in
Git LFS.

### HS009 — `.gitignore` is not empty

**Soft.** `.gitignore` must exist and have at least one entry.

**Why.** An empty `.gitignore` is a placeholder that was never filled in, and
it is where a `.env` with a key in it ends up.

---

## The README

### HS010 — The README exists

**Hard.** `README.md` must be in the root.

**Why.** GitHub surfaces a README in the repository overview, the file browser
and the search result. Without one, a visitor has to guess what a repository
is from its file list.

### HS011 — Exactly one H1, and it is first

**Hard.** The README must open with a single level-1 heading, and there must be
no second one.

**Why.** The H1 is the product's name. A second H1 either duplicates it or
introduces a second subject, and both make the document's outline ambiguous —
which matters because GitHub builds a table of contents from the headings.

### HS012 — The required sections are present

**Hard.** The README must contain, in this order:

1. A section about **installing or starting** the project.
2. A section about **what the project does**.
3. A section about **development** — how to work on it.
4. A section about the **license**.

**Why.** These four are the questions a visitor has, in the order they ask
them. Every repository in the survey that reads well answers all four; every
repository that reads badly is missing one of them, usually development.

The checker accepts the English and the Russian headings for each, and any
heading that contains the concept's keywords. The intent is the section, not
the wording.

### HS013 — The README sections are in the canonical order

**Soft.** The four required sections must appear in the order above.

**Why.** A reader who learns the first repository should not have to relearn
the second. The order is also the order of the reader's questions, so it is
the fastest order for them too.

### HS014 — The README says something

**Soft.** `README.md` must be longer than 400 characters.

**Why.** A README shorter than that cannot contain the install command, the
capabilities, the development instructions and the license, which HS012
requires. The length check is a cheap proxy for "the sections are filled in
rather than present but hollow".

### HS015 — The README links to the license

**Soft.** `README.md` must contain a link to `LICENSE`.

**Why.** GitHub shows the license in the sidebar, but the README is what
people read, and a reader who has been told there is no license does not go
looking for one.

---

## Product and design records

### HS020 — `PRODUCT.md` carries the schema marker

**Hard.** `PRODUCT.md` must exist and contain
`<!-- impeccable:product-schema 1 -->`.

**Why.** The marker records which version of the product record the file
follows. Without it, a tool cannot tell a deliberately short record from one
written before a section existed, and it will re-ask a question the owner has
already answered.

### HS021 — `PRODUCT.md` has its sections

**Hard.** `PRODUCT.md` must contain: `Platform`, `Users`, `Product Purpose`,
`Positioning`, `Operating Context`, `Capabilities and Constraints`, `Brand
Commitments`, `Evidence on Hand`, `Product Principles`, `Accessibility &
Inclusion`.

**Why.** The ten sections are the questions a product has to answer before it
can be designed, built, or handed to someone else. `Platform` and `Users` say
who it is for. `Positioning` says why it exists when a neighbour exists.
`Capabilities and Constraints` says what it may not do. `Evidence on Hand` says
what is real, and — just as important — what is *not*, so that a later
session does not invent it. `Brand Commitments` says what must survive a
redesign.

`Stack` is a section too, but only for a project that has no code yet.

### HS022 — `DESIGN.md` has frontmatter

**Hard.** `DESIGN.md` must exist and open with a YAML frontmatter block
containing at least `name` and `description`.

**Why.** The frontmatter is the machine-readable layer. Tools that render or
lint design systems read the tokens from it, and an agent generating a new
screen reads them from there. The prose is context; the frontmatter is the
contract.

### HS023 — `DESIGN.md` has its sections, in order

**Hard.** The canonical sections, when present, must appear in this order:
`Overview`, `Colors`, `Typography`, `Layout`, `Elevation & Depth`, `Shapes`,
`Components`, `Do's and Don'ts`.

**Why.** Tooling parses these headers by exact name. `Colors` is not
`Colour Palette`, and a renamed heading breaks the tooling that reads it.
Sections may be omitted when they do not apply; the ones that are present
keep their order.

### HS024 — The design sidecar exists

**Hard.** `.impeccable/design.json` must exist and be valid JSON with
`schemaVersion` and `title`.

**Why.** The sidecar carries what the frontmatter cannot: tonal ramps,
shadow and motion tokens, breakpoints, and the component snippets a live
panel renders. A `DESIGN.md` without it is a design document that no tool
can use.

### HS025 — No template is left unfilled

**Hard.** A file that came from `templates/` still carries the marker
`<!-- house-style: template -->` in its first three lines, or still contains
an unfilled `{{TOKEN}}` placeholder. Both are reported.

**Why.** A repository that was scaffolded and never written is worse than one
that was never scaffolded, because it looks finished. The marker is a
comment, so it costs nothing in the rendered document, and it is precise in
a way that "the file mentions a placeholder somewhere" is not — a document
that *describes* the placeholder syntax is not a template.

The owner deletes the marker line as the last step of filling the file in.

### HS026 — `PRODUCT.md` is written, not scaffolded

**Hard.** `PRODUCT.md` must contain at least five lines of prose. Headings,
comments and blank lines do not count.

**Why.** The product truth cannot be defaulted. A `PRODUCT.md` with the right
headings and nothing in them is a template, and the whole point of the
document is the part that cannot be generated: who it is for, what it
promises, and — most importantly — what is *not* true yet.

This is why `adopt.sh` writes a stub rather than a guess. The stub fails the
checker until it is filled in, which is correct.

---

## Links and references

### HS030 — Every relative link resolves

**Hard.** Every relative Markdown link in every tracked Markdown file must
point at a file that exists in the repository.

**Why.** A broken link in a README is a reader who reaches the end of the
page and finds nothing. Broken links are common in a repository that is
edited over months, and they are trivially checkable.

Absolute URLs to other hosts are not checked — they are not the
repository's business — but a link to a path inside the repository is.

**Soft.** A link that starts with `/` points outside the repository: an
absolute path on someone's machine, or a route into an application. It will
not resolve for any other reader, and on GitHub it resolves to the site
rather than to a file. Reported, not enforced, because the intent is often
correct and the form is a matter of taste.

### HS031 — Every image resolves

**Hard.** Every image reference must point at a file that exists.

**Why.** Same reason, worse consequence: a broken image in a README is a
visible empty box, and it is often the first thing in the document.

---

## Markdown hygiene

### HS040 — No emoji

**Hard.** No emoji in any tracked text file.

**Why.** This is the one rule with no exceptions anywhere in the survey. Emoji
render inconsistently in terminals, in diffs, in issue trackers and in
notification emails, and in a monospaced code block they occupy two columns
and break the alignment of everything beside them. More importantly, they are
the signal that a document is a brochure rather than an engineering record.

The checker looks for the Unicode ranges that emoji live in, and it excludes
the ranges that contain ordinary punctuation and symbols.

### HS041 — No heading level is skipped

**Hard.** A document may not jump from `##` to `####`.

**Why.** The heading tree is the table of contents GitHub generates, and the
outline an agent reads to find a section. A skipped level breaks both.

### HS042 — No trailing whitespace

**Hard.** No line ends in a space or a tab.

**Why.** Trailing whitespace is invisible in a diff but shows up as a changed
line in every commit that touches it, and it breaks Markdown's two-space line
break. The checker excludes Markdown files for the line-break rule, since two
trailing spaces are meaningful there — but the trailing whitespace rule still
applies to them, because a third space is not a line break.

### HS043 — Every text file ends with a newline

**Hard.**

**Why.** A file without a trailing newline shows up as "no newline at end of
file" in every diff that touches its last line, and it breaks every tool that
concatenates files.

### HS044 — No tabs in Markdown

**Hard.** Markdown files are indented with spaces.

**Why.** Tabs render as different widths in different viewers. Two spaces is
the house width.

---

## Git and GitHub hygiene

### HS100 — The default branch is `main`

**Soft.** The default branch is `main`.

**Why.** `master` is a name from a different default. More practically, the
CI workflows in the standard trigger on `main`, and a repository whose default
branch is named something else never runs them on its own pushes.

### HS101 — The repository has a description

**Soft.** The GitHub description is set and is not just the repository name.

**Why.** The description is what appears in search results, in a link preview,
and in `gh repo list`. An empty description is a repository that announces
nothing.

### HS102 — `docs/` has an index

**Soft.** `docs/` contains a `README.md` that links to at least one other
file in `docs/`.

**Why.** A folder of documents with no entry point is a folder nobody opens.
The index is the table of contents.

### HS103 — `CHANGELOG.md` is a changelog

**Soft.** It must have a title and at least one version heading.

**Why.** A changelog that says "initial commit" is a changelog that will
never be updated. The first real entry is the hard part, and the standard
ships one in `templates/`.

### HS104 — `AGENTS.md` is present and useful

**Soft.** `AGENTS.md` must exist and be longer than 200 characters.

**Why.** `AGENTS.md` is the re-entry surface. Six months later, for a person
or an agent, it answers: how do I run this, where does this live, what are the
traps, what may I not do without asking. Everything that cost a rebuild to
learn goes there instead of into a message that will not be found.

The name is the convention that agent harnesses look for, and it is also the
name a person will look for.

---

## What the standard deliberately does not check

- **Whether the content is true.** The checker can tell that a README has an
  Install section. It cannot tell whether the install command works. Content
  quality is a review job.
- **Which language a repository is written in.** Russian, English or both is
  a per-project decision. The standard fixes the policy in
  [`writing.md`](writing.md) and not the choice.
- **The stack.** A Python project and a Go project share the root file set,
  not their build tooling.
- **Whether a repository is worth keeping.** The standard says how a
  repository should look. It does not say which ones matter.

These are the lines between a standard and a straitjacket. A repository that
violates one of them is still a repository that follows the standard.

---

## Changing a rule

1. Write the rule here, with its rationale, and a passing and a failing
   example.
2. Implement it in `scripts/housecheck.py` with a code that is never reused.
3. Add a test in `tests/test_housecheck.py`.
4. Run `scripts/housecheck.py --strict .` — the golden repository must still
   pass. If it cannot, the rule is wrong.
5. Update `CHANGELOG.md` and, if the canonical file set changed, the version
   number and `adopt.sh`.
