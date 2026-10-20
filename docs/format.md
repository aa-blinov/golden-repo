# Format

The shape every document and every landing site takes.

This is the pattern the documents are written to. It is the standard's
prose half: [`standard.json`](../standard.json) says what files a repository
carries, and this says what is inside them.

Everything here is in English, in every repository. A repository whose audience
is Russian still has an English README, because a README is what a visitor
reads before deciding whether to read more, and the visitor is whoever found
the link. The language of the code, the comments and the commits is the
owner's, and stays as it is.

## The rules of the writing

These come from [`writing.md`](writing.md) and are not repeated here. The two
that matter most for generation:

- **Facts over adjectives.** Sizes, versions, limits, error paths and counts
  are named precisely. "Faster" is not a fact; "97,469,540 B" is.
- **No emoji, anywhere.** Not in a document, not in a page, not in a comment.

And the one that decides whether a document is finished:

- **Every claim comes from the code.** A command in a README is a command that
  exists in `package.json`, `pyproject.toml` or a `Makefile`. A dependency is
  one the project actually depends on. A file in the tree is one that is
  there. If the code does not say it, the document does not say it.

## `README.md`

The front door. The section order is fixed; the wording is not.

```markdown
# <Product name>

<One paragraph. What it does, in the words a user would use. Two or three
sentences, no preamble, no "Welcome to".>

<Badges: licence, release, CI. Only ones that mean something.>

---

## Quick start

<The shortest path from nothing to running. One command if there is one.>

```bash
<the real command>
```

<Platforms, alternatives, and what each one is for. A table when there are
more than two.>

## What it does

- **<Capability>.** <What it does, and what the user does with it.>

## How it works

<The architecture, for someone who wants to change it. A diagram in text
form, the main data flow, the decisions that are not obvious. The reasoning
for a non-obvious choice goes in AGENTS.md, not here.>

## Configuration

<The options and their defaults. A table beats prose for anything with more
than two options.>

## Development

```bash
<install>   # bootstrap
<test>      # run the tests
<build>     # produce the artefact
```

<Where things live, in two or three lines.>

## License

<SPDX name>, © <holder>. See [LICENSE](LICENSE).
```

Rules the generator follows:

- The first paragraph is the product, not the problem domain. "Press a hotkey,
  speak, paste", not "In today's fast-paced world, dictation is important".
- The `Quick start` section comes before `What it does`, because a reader who
  cannot run it stops reading.
- A command appears only if it exists. The `scripts` map in `package.json`,
  the `[project.scripts]` in `pyproject.toml`, the targets in a `Makefile`.
- Capabilities come from what the code does: the CLI verbs, the HTTP routes,
  the exported functions, the screens. Not from a wish.
- The `How it works` section names the modules and the data flow. It does not
  explain the reasoning; `AGENTS.md` does that.
- Screenshots go in `docs/screenshots/` and are referenced by relative path.

## `AGENTS.md`

The re-entry surface. For a person or an agent opening the repository for the
first time, and for one who has not opened it in six months.

```markdown
# AGENTS.md — agent context for `<name>`

<One paragraph: what this project is and what this file is for.>

## Run / build / test

```bash
<the real commands, with a comment each>
```

## Where things live

| Path | What it is |
| --- | --- |
| `<path>` | <what it holds> |

## Traps

- **<The thing that costs a rebuild to learn>.** <What it is, and what it
  costs.>

## Style / safety rails

- **<The rule this project has that another project would not.>**
```

Rules the generator follows:

- The commands are the project's own. A `npm test` that does not exist is
  not in the file.
- The traps are real and specific. "Be careful with the cache" is not a trap;
  "the cache key does not include the locale, so switching language does not
  invalidate it" is.
- The rails are the ones this project has, not the house style's list
  repeated. A project with no opinions does not get a rails section.

## `PRODUCT.md`

The product truth, in the `impeccable:product-schema` format. The ten
sections, in order.

The generator can write the factual half from the code: the platform, the
capabilities, the constraints, the evidence. It cannot write the rest, and
does not try:

- `Users` — who it is for, and the job they are doing. Read from the
  repository description and the README; if that is not enough, say so.
- `Positioning` — what a neighbour could not copy. A judgement, not a fact.
- `Brand Commitments` — the name, the voice, the assets.
- `Product Principles` — three to five decisions a later session is measured
  against.
- `Accessibility & Inclusion` — the known needs, or an honest "not decided".

A `PRODUCT.md` that guesses at these is worse than one that leaves them
marked as open. The house style's HS026 rule exists for exactly this: a
product record that is not written should not pass for one that is.

## `DESIGN.md`

Only for a repository with a visual identity of its own. A repository whose
only interface is a command line does not have a design system, and a
`DESIGN.md` that says so is honest.

For a repository that has one, the format is the official one: YAML frontmatter
with the tokens, then up to eight sections in the canonical order. The
frontmatter is normative; the prose explains how to apply the tokens.

## The landing site

The site a repository publishes on GitHub Pages. Not every repository has one,
and a repository whose product is a web page does not need a landing page for
it.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title><name>: <one-line promise></title>
  <meta name="description" content="<the same promise, in a sentence>">
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
      <nav class="site-nav" aria-label="Sections">
        <a href="#one">…</a>
      </nav>
      <a class="header-github" href="https://github.com/<owner>/<repo>">GitHub</a>
    </div>
  </header>

  <main id="main">
    <section class="hero wrap" id="top" aria-labelledby="hero-title">
      <div class="hero-copy">
        <h1 id="hero-title"><the promise, as a sentence></h1>
        <p class="lede"><what it does, and what it does not do></p>
        <div class="actions">
          <a class="button" href="<the install command>">Get it</a>
        </div>
        <p class="fine"><licence, platforms, sizes></p>
      </div>
    </section>

    <section class="section wrap" id="one" aria-labelledby="one-title">
      <h2 id="one-title"><the section, named for what it holds></h2>
      <p>…</p>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap">…</div>
  </footer>
</body>
</html>
```

Rules the generator follows:

- The same class vocabulary everywhere: `site-header`, `wrap`, `hero`,
  `section`, `site-footer`, `button`, `lede`, `fine`. A site that invents
  its own names is a site that cannot be restyled by the next person.
- The `H1` is the promise, in one sentence, in the same words as the README's
  first paragraph. The two pages are the same argument at two lengths.
- Every `section` has an `id` and an `aria-labelledby` that points at its
  own heading. The skip link works.
- Three to six sections. Each one answers a question the reader has: what is
  it, how does it work, how do I get it, what does it cost, what is it for.
- The primary action is a command the reader can paste. A button that opens a
  store page is not the same as a button that installs.
- The footer carries the licence, the source link, and the version.

## The CSS

One `style.css` per site, from the house tokens. Dark is the primary surface
because most of what a reader sees next to a landing page is a terminal, and
a light set is provided because a README is read on GitHub.

```css
:root {
  --bg: #1d2021;
  --surface: #282828;
  --fg: #ebdbb2;
  --muted: #a89984;
  --rule: #504945;
  --accent: #b8bb26;
  --danger: #ff8a7a;
  --radius: 6px;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --sans: system-ui, -apple-system, "Segoe UI", sans-serif;
}

@media (prefers-color-scheme: light) { :root { --bg: #fbf1c7; --fg: #3c3836; … } }
```

Rules the generator follows:

- The tokens are named, and the CSS refers to them. A literal hex inside a
  rule is a second source of truth.
- One radius, one spacing scale, one family for the interface and one for
  the code.
- Surfaces are flat. Depth is tone.
- `prefers-reduced-motion` turns every transition off.
- Contrast holds: body text at 4.5:1, borders and focus rings at 3:1.

## The order of the work

For a repository that gets the treatment:

1. The README, from the code.
2. The `AGENTS.md`, from the code.
3. The `PRODUCT.md`, from the code and from what the owner has already
   written. The parts the code cannot answer are left marked.
4. The `DESIGN.md`, if the repository has a visual identity.
5. The landing site, if the repository has one.

The documents come first because they are what a visitor reads. The site comes
last because it is a rendering of the same argument.
