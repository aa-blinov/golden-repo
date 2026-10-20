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

## The landing site

A repository that publishes a site gets the house site: one `style.css`, one
`site.js`, and an `index.html` that uses the house class vocabulary.

**Where the site lives.** It is a marketing page, and it is separate from the
product. In this collection the sites live in `docs/`, `site/`, `website/`,
`web/` or `landing/`, and each repository keeps the one it has. Do not move a
site to a different directory.

**What you change.** The HTML: the class names, the section order, the
structure of the hero. The content: the text, taken from the repository's own
README and from the code.

**What you do not change.** The images, the fonts, the screenshots. They are
the repository's own material and they are already right.

**The class vocabulary.** Use these, and no others:

| Class | What it is |
| --- | --- |
| `skip-link` | The first element in the body. Goes to `#main`. |
| `site-header`, `header-inner` | The bar at the top. |
| `brand`, `brand-mark` | The name, and its mark if it has one. |
| `site-nav` | The links to the sections. |
| `header-github` | The link to the repository. |
| `wrap` | The width limit. Every section is inside one. |
| `hero`, `hero-copy` | The first section. |
| `lede` | The paragraph under the `h1`. |
| `actions`, `button`, `button-ghost` | The calls to action. |
| `fine` | The small print under the actions. |
| `section` | Every section after the hero. |
| `rail` | A row of three or more short items. |
| `table-wrap`, `shot`, `tag`, `tag-ok`, `tag-warn`, `tag-bad` | Tables, images, status. |
| `site-footer`, `footer-inner`, `footer-nav` | The bottom. |
| `command` | A pasteable command block. |
| `cards`, `card` | A fixed grid of items, when the grid should not reflow. |
| `compare`, `compare-arrow` | Two columns with an arrow between them. |
| `shell`, `prompt`, `cmt`, `out` | A terminal transcript, and its parts. |

A site that invents its own class names is a site that cannot be restyled by
the next person. If a page genuinely needs a class the vocabulary does not
have, add it to `style.css` and to this table, so the next site can use it.

**The structure.**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><name>: <the promise></title>
  <meta name="description" content="<the promise, in a sentence>">
  <meta name="color-scheme" content="dark light">
  <meta property="og:title" content="<name>">
  <meta property="og:description" content="<the promise>">
  <meta property="og:type" content="website">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="#top"><span><name></span></a>
      <nav class="site-nav" aria-label="Sections">…</nav>
      <a class="header-github" href="https://github.com/<owner>/<repo>">GitHub</a>
    </div>
  </header>
  <main id="main">
    <section class="hero wrap" id="top" aria-labelledby="hero-title">
      <div class="hero-copy">
        <h1 id="hero-title">…</h1>
        <p class="lede">…</p>
        <div class="actions">…</div>
        <p class="fine">…</p>
      </div>
    </section>
    <section class="section wrap" id="…" aria-labelledby="…-title">
      <h2 id="…-title">…</h2>
    </section>
  </main>
  <footer class="site-footer">
    <div class="wrap footer-inner">…</div>
  </footer>
  <script src="site.js"></script>
</body>
</html>
```

**The rules.**

- The `h1` is the promise, in one sentence, in the same words as the
  README's first paragraph. The two pages are the same argument at two
  lengths.
- Three to six sections. Each answers a question the reader has.
- Every `section` has an `id` and an `aria-labelledby` pointing at its own
  heading. The skip link works.
- The primary action is a command the reader can paste, not a link to a
  store page.
- The footer carries the licence, the source link and the version.
- The page is in English, like the documents.

**The assets.** `style.css` and `site.js` come from the house template:

- `/Users/justcomex/Documents/pet/golden-repo/templates/site/style.css`
- `/Users/justcomex/Documents/pet/golden-repo/templates/site/site.js`

Copy them into the site directory as they are, and add to `style.css` only
the rules the page genuinely needs beyond the vocabulary. Keep those rules
at the end of the file, under a comment saying what they are for.

**Before you finish.** Open the HTML and check it: every class you used
exists in `style.css`, every `id` a link points at exists in the page, the
images resolve, and the page says what the README says.
