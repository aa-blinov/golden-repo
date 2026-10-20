# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The owner of the repositories, working alone, in a terminal, and occasionally
through an AI coding agent. The second audience is whoever lands on one of the
repositories from GitHub search, a link in a chat, or a `pip install` that
someone recommended.

The owner's situation: dozens of unrelated projects, each started on a different
day, in a different mood, in a different language. The work is done. The
problem is that the repositories do not look like they come from the same
person — different README shapes, different section names, different amounts of
documentation, sometimes nothing at all. It reads as a portfolio of strangers
rather than a body of work.

The visitor's situation: they found a repository and want to know, in about
thirty seconds, what it does, whether it fits their problem, and how to run
it. They are not reading the architecture. They are deciding whether to keep
looking.

## Product Purpose

The standard turns a pile of repositories into a body of work. It does that in
three ways:

1. **A canonical file set.** Every repository carries the same root: README,
   AGENTS, PRODUCT, DESIGN, CHANGELOG, LICENSE, the community health files, the
   `.github` directory, `docs/`, `scripts/`, `src/`, `tests/`. A reader who
   learns one repository has learned all of them.

2. **A canonical README order.** Quick start, what it does, screens,
   configuration, how it works, development, license. The reader's questions
   are answered in the order they ask them.

3. **A canonical voice.** Facts over adjectives, no emojis, no hype, honest
   about what is unresolved. The reader trusts the first repository they read
   and carries that trust to the next.

Success for the owner: a new project starts in one command and already looks
right. Success for a visitor: the README of any repository answers "what, why,
how" in the same order, in the same tone, so the reader's attention goes to
the content instead of to the formatting.

Success for the standard itself: it is enforced, not merely documented. A
repository that violates it fails a check that runs in CI.

## Positioning

The mechanism that a neighbouring "collection of good practices" document
cannot copy: **the standard is executable**.

`scripts/housecheck.py` is a plain Python 3 program with no dependencies that
reads a repository and reports every deviation from the standard, with a stable
code per rule and an exit code CI can gate on. The prose in `docs/` explains
the rules; the checker is what makes them binding.

The second mechanism is the **migration path**. A standard that only applies to
projects started after it exists leaves every existing repository untouched,
which is precisely the problem it was meant to solve. `scripts/adopt.sh` brings
an existing repository up to the standard without touching its code and without
overwriting a file the owner has already written. The standard therefore
reaches backwards as well as forwards.

The third is that the standard is derived, not invented. Every rule traces to
something observable in the repositories that already look right — the
`lazy-to-text` README section order, the `PRODUCT.md` section list, the
`impeccable` design sidecar, the MIT license line, the absolute absence of
emoji. It is a pattern found in the owner's own best work and written down, not
a template imported from elsewhere.

## Operating Context

The standard is used in three situations, and each has a different entry point.

**Starting a project.** The owner creates the repository from the GitHub
template, clones it, and runs `scripts/new-repo.sh`. The new repository already
passes the checker before a line of product code exists. `PRODUCT.md` is filled
in first, because the product truth is what the rest of the repository is
derived from.

**Shipping a project.** The `README.md` is the release surface. It states what
the software does, how to install it, what the known limitations are. A visitor
should be able to decide without asking a question.

**Coming back to a project.** `AGENTS.md` is the re-entry surface. Six months
later, for a person or an agent, it answers: how do I run this, where does
this live, what are the traps, what may I not do without asking. Everything
that cost a rebuild to learn is written down there instead of in a message
that will not be found.

The standard lives in a terminal and a browser, in that order. Everything in it
runs with `python3` and `bash` and nothing else, because the moment it needs a
package manager it stops being usable in the one place it matters most: a new
repository on a fresh machine.

## Capabilities and Constraints

Confirmed and enforced by the checker:

- The canonical root file set exists, and `LICENSE` names a real license and a
  real copyright holder.
- `README.md` opens with exactly one H1 and carries the required sections in
  the canonical order.
- `PRODUCT.md` carries the `impeccable:product-schema` marker and its
  documented sections.
- `DESIGN.md` has YAML frontmatter and its eight canonical sections in order.
- Every relative link and every image reference in every Markdown file
  resolves to a file that exists.
- No emoji appears in any tracked text file.
- No heading level is skipped, no line has trailing whitespace, every text file
  ends in a newline.
- No committed file exceeds 50 MB, and nothing exceeds GitHub's 100 MB limit.

Confirmed by the tooling:

- `new-repo.sh` scaffolds a project from `templates/` with token substitution.
- `adopt.sh` adds the missing standard files to an existing repository and
  never overwrites an existing file.
- The checker reports in a human-readable form, in JSON for CI, and with a
  stable rule code per finding.

Deliberately out of scope, and therefore not enforced:

- **Content quality.** The checker can tell that a `README.md` has an
  "Install" section; it cannot tell whether the install instructions are
  correct. That is a job for review, not for a linter.
- **The language of a repository.** Russian, English or both is a per-project
  decision. The standard fixes the *policy* — the README speaks to its
  audience, the internal documents speak to the owner — and not the choice.
- **Stack-specific conventions.** The standard is language-agnostic. A Python
  project and a Go project share the root file set, not their build tooling.
- **Enforcing the check on repositories that do not want it.** The checker is
  opt-in per repository, though every repository that adopts the standard is
  expected to run it in CI.

## Brand Commitments

**Name:** golden-repo. **Slogan:** one author, one shape.

**Tone:** engineering, plain, unhurried. The standard explains its reasoning
because a rule the reader does not understand is a rule the reader will
special-case away. It admits when a rule is a preference rather than a
requirement.

**The three rules that carry the identity:**

- Facts over adjectives. Sizes, versions, error paths and limits are named
  precisely.
- No emojis, anywhere. They render inconsistently in terminals, diffs and
  issue trackers, and they make a repository look like a brochure.
- The standard is enforced, not documented. If it is not checkable, it is a
  preference, and preferences live in `docs/writing.md` where they inform a
  human without blocking a build.

**Voice of the artefacts themselves:** the template files are written the way
the standard asks projects to be written. The README of a project that adopts
the standard should be readable as a document, not as a landing page.

## Evidence on Hand

- The repositories that already look right: `lazy-to-text`, `cast`, `puuush`,
  `petzy`, `monos`, `koloda`, `better-ssh`, `templates-mcp`. The rules are
  extracted from their file trees, README section orders, `PRODUCT.md`
  section lists, `DESIGN.md` frontmatter, `.impeccable/design.json` sidecars
  and CI workflows.
- The GitHub documentation on repository best practices, README discovery
  order (`.github` over root over `docs`), community health files, template
  repositories, and the standard-file set (README, license, citation,
  contribution guidelines, code of conduct).
- The `impeccable` product and design record formats, used verbatim so that
  the standard composes with the rest of the toolchain.

Absent, and not to be invented:

- Any evidence that the owner's other repositories will be brought to the
  standard. The migration is proposed, not agreed.
- Any measured effect on adoption or on time spent maintaining repositories.
  Nobody has measured it, so no claim is made.
- Any decision about which existing repositories are worth keeping at all. The
  standard says how a repository should look; it does not say which ones
  matter.

## Product Principles

1. **A rule that cannot be checked is a preference.** The checker is the
   standard. Prose explains it; a linter enforces it. Anything that only
   exists in prose decays within a month, because prose fails nothing.
2. **Standardise the surface, not the substance.** The file set, the order, the
   tone and the vocabulary are fixed. The product, the stack and the language
   are not. A standard that dictated those would be rejected by the first
   project it did not fit.
3. **The standard reaches backwards.** A rule that only governs new work
   leaves the existing body of work unchanged, which is the actual problem.
   `adopt.sh` is therefore part of the product, not an afterthought.
4. **Never overwrite the owner's work.** The migrator adds missing files and
   leaves everything else alone. A repository that has been running for a year
   has opinions its owner never wrote down, and those opinions outrank a
   template.
5. **Show the reasoning.** Every rule states what it is for. A reader who
   understands a rule follows it; a reader who merely obeys it works around it
   the first time it is inconvenient.
6. **One command to start, one command to check.** The cost of adopting the
   standard has to be close to zero, or it will not be adopted.

## Accessibility & Inclusion

The standard governs text documents and GitHub's own rendered surface, so the
accessibility requirements are mostly about the reader rather than the product.

- **Language is not a decoration.** The repository's audience decides the
  README's language, and the standard records the decision rather than
  assuming one. A Russian-language tool with a Russian README is not a
  violation.
- **No images as the only source of a fact.** Screenshots illustrate; they do
  not carry information that is missing from the text. A reader using a screen
  reader, or reading the README in a terminal, gets the same facts.
- **Plain Markdown.** No HTML in the README beyond what GitHub renders
  natively, no images-of-text, no colour as the only carrier of meaning. The
  rules this standard borrows from the design system — contrast floors, visible
  focus, status shown by text as well as colour — apply to documentation too.
