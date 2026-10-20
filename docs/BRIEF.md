# The brief for writing a repository's documents

You are writing the documentation of one repository. Three documents, in
English, from the facts.

## What you have

- **`/tmp/facts/<repository>.json`** — what the repository actually contains.
  The language, the runtime, the commands, the dependencies, the shape of the
  source tree, the configuration, the entry points, the CI, the tests, and
  the first paragraphs of the README that is already there.
- **`/Users/justcomex/Documents/pet/golden-repo/docs/format.md`** — the shape
  the documents take. Read it. It is the pattern, and following it is what
  makes the collection look like one body of work.
- **`/tmp/reference-puuush/`** — a finished example. `README.md`,
  `AGENTS.md`, `PRODUCT.md`. This is the target quality, not a template to
  copy: the words are about a different project, and yours must be about
  yours.
- The repository itself: `git clone --depth=1 https://github.com/aa-blinov/<repository>.git`
  and read the code. The facts packet is a summary, not a substitute.

## The house rules

From `docs/writing.md` in the standard. The short version:

- **Facts over adjectives.** Sizes, versions, limits, counts and error paths
  are named precisely. "Faster" is not a fact; "97,469,540 B" is.
- **No emoji, anywhere.** Not in a document, not in a heading, not in a
  comment.
- **Every claim comes from the code.** A command in the README is a command
  that exists in `package.json`, `pyproject.toml` or a `Makefile`. A
  dependency is one the project actually has. If the code does not say it,
  you do not say it.
- **English, in every document.** The code, the comments and the commits keep
  the language they are in. The documents are English, because a README is
  what a visitor reads before deciding whether to read more, and the visitor
  is whoever found the link. If the existing README is in Russian, translate
  it, keep the facts, and do not lose anything in the translation.

## The humanizer

The documents go through the humanizer. The patterns it removes are in
`/Users/justcomex/Documents/pet/golden-repo/scripts/anti_ai.py`, and you can
run it on your work:

```bash
python3 /Users/justcomex/Documents/pet/golden-repo/scripts/anti_ai.py <your files>
```

It must report zero findings. The patterns it looks for, in short:

- **Not X but Y.** "It's not just faster; it's better." Say the thing.
- **One-line closers.** A short paragraph at the end of a section that
  repeats what the section said.
- **Sayings that sound deep.** "The real question is", "at its core", "what
  really matters", "the deeper issue".
- **Staged run-ups.** "Let's dive in", "here's what you need to know",
  "without further ado", "honestly?".
- **Arguing with no one.** "This isn't mainly about", "to be clear", "an
  obvious approach would be", "it would be easy to just".
- **Dashes doing the work a conjunction should do.** The house style runs
  under one dash per thousand words. The reference documents have none.
- **Inflated significance.** "stands as a testament", "plays a key role",
  "underscores its importance", "the future looks bright".
- **Borrowed authority.** "Experts argue", "industry reports", "cited in".
- **Sales language.** "nestled in the heart of", "groundbreaking",
  "breathtaking", "stunning".
- **Chatbot residue.** "I hope this helps", "let me know", "Great
  question!".
- **Writing about the document instead of its subject.** "The table below
  compares", "this section is organized by".
- **AI vocabulary.** "delve", "showcase", "tapestry", "pivotal", "crucial",
  "meticulous", "vibrant", "testament", "interplay", "enhance".
- **Headings in title case.** Use sentence case, except the canonical section
  names in `PRODUCT.md`, which the schema fixes.
- **Curly quotes.** Use straight quotes.

Two things it cannot see, so you have to: **vary the sentence length**, and
**do not put a label in bold on every list item** unless the label carries
information the rest of the item does not.

## What to write

Three files, into `/tmp/docs/<repository>/`:

### `README.md`

The section order is fixed by `docs/format.md`:

1. The title and a first paragraph of two or three sentences: what the
   software does, in the words a user would use.
2. A hero image or screenshot, if the repository has one in `docs/`.
3. Badges, only the ones that mean something.
4. A horizontal rule.
5. `## Quick start` — the shortest path from nothing to running.
6. `## What it does` — the capabilities, as a list.
7. `## Screenshots` — only if the repository has images.
8. `## How it works` — the architecture, the modules, the data flow.
9. `## Configuration` — the options and their defaults, if there are any.
10. `## Development` — the commands, and where things live.
11. `## License`.

The checker requires the sections about installing, about what it does, about
development, and about the licence. It also requires exactly one level-1
heading, and it checks that every link and every image resolves.

### `AGENTS.md`

How to run, test and build it. Where things live. The traps: the things that
cost a rebuild to learn, and they are specific to this project. The rails:
the rules this project has that another project would not.

Read the code to find the traps. A trap is not "be careful with the cache".
A trap is "the cache key does not include the locale, so switching language
does not invalidate it".

### `PRODUCT.md`

The ten sections of the `impeccable:product-schema`, in order, with the
`<!-- impeccable:product-schema 1 -->` marker under the title.

Write the factual half from the code: the platform, the capabilities, the
constraints, the evidence. For `Users`, `Positioning`, `Brand Commitments`,
`Product Principles` and `Accessibility & Inclusion`, use what the existing
README, the repository description and the code tell you. Where they do not
tell you, say so in the section rather than inventing an answer. A product
record that guesses is worse than one that says the question is open.

The starter files in the repository's `templates/` directory have the shape.
Use them as the shape and write the content.

## What you must not do

- Do not change the code. Only the documents.
- Do not write about the product's future. The standard forbids invented
  metrics, testimonials and comparisons, and the checker cannot see them.
- Do not leave a `{{TOKEN}}` placeholder in the text.
- Do not leave the `house-style: template` marker in a file you have
  written. The marker means "not written yet", and a file you have written
  is written.

## Before you finish

```bash
cd <your clone>
python3 /Users/justcomex/Documents/pet/golden-repo/scripts/anti_ai.py \
    /tmp/docs/<repository>/*.md
```

It must report zero findings. Then check the repository:

```bash
python3 /Users/justcomex/Documents/pet/golden-repo/scripts/housecheck.py \
    --strict .
```

Any hard finding in a file you wrote has to be fixed before you finish. A
soft finding about a file that still carries the template marker is expected
and fine.

Write the three files into `/tmp/docs/<repository>/` and report what you
wrote and anything you could not determine from the code.
