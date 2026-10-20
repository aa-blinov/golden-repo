# Writing

How the standard reads. These are preferences rather than rules: the checker
does not enforce them, because a preference that blocks a build stops being
informative.

The rules themselves are in [`house-style.md`](house-style.md).

## The voice

### Facts over adjectives

"Faster" is not a fact. "97,469,540 B" is. "The cache is warm" is not a fact.
"Second run: 40 ms, first run: 900 ms" is.

This is the single most useful thing to copy from the repositories that already
read well. The rule is simple: **if a claim can be given a number, give it
the number.** Sizes, versions, timeouts, error messages, counts, limits.

The payoff is that a README written this way can be checked. A README written
in adjectives cannot be checked by anyone, including the author, which is why
it is usually wrong.

### The mechanism, and the cost

When a choice is not obvious, say why it was made and what it costs.

> A bare `uv sync` re-resolves and rewrites `uv.lock`, which is a silent
> rebuild of the dependency set underneath a green run, and it fails on a
> missing lockfile only when you did not pass the flag.

That sentence tells the next person what will happen if they take the
shortcut. Without it, the shortcut is taken.

### Say what is not resolved

Every repository in the survey that reads well has a section — or a paragraph
— that says what is still an open question, and who has to answer it. A
reader who knows a question is open can work with it. A reader who thinks
everything is settled cannot.

This is also what keeps a later session from inventing things. `PRODUCT.md`'s
"Evidence on Hand" says what is real *and* what is absent, and the absence is
the part that gets fabricated.

### No hype

No "blazing fast", no "seamless", no "revolutionary", no "effortless". If a
product is fast, the number is right there and the adjective adds nothing. If
it is slow, the adjective is a lie and the number would have been fixable.

### No emoji

Everywhere, always, in every file. They render inconsistently in terminals,
diffs, issue trackers and notification email; in a monospaced code block they
occupy two columns and break the alignment of everything around them.

More to the point, they are the signal that a document is a brochure. The
repositories that read as one author's work have none.

### Comments explain why, never what

```python
# Increment the counter
counter += 1
```

is noise. The code says what it does. The comment is for the thing the code
cannot say: why the counter starts at -1, why this is not a lock, why the
retry is bounded.

## The README

### The order

The reader's questions, in the order they ask them:

1. **Quick start / Install.** How do I get it running? Command first, prose
   after.
2. **What it does.** The capabilities, as a list. Each one says what it does,
   not what category it belongs to.
3. **Screenshots.** What it looks like. Usually a table of images with
   captions, or one hero image and a link to the rest.
4. **Configuration.** The options, and their defaults. A table beats prose
   for anything with more than two options.
5. **How it works.** The architecture, for someone who wants to change it.
6. **Development.** How to work on the code: install, test, build.
7. **License.** The terms, and a link to the file.

Extra sections are welcome. The required ones keep their order.

### The opening

The first paragraph is the one-sentence version of what the software does,
in the words a user would use, not an introduction to the problem domain.

> Press a hotkey, speak, paste.

> Снимок области экрана и ссылка на него в буфере обмена. Нажал горячую
> клавишу, протянул рамку, нажал Enter, ссылка уже в буфере, вставляешь её в
> чат.

Both are good. Both answer "what is this" in the first two lines, without
requiring the reader to know a domain first.

Then badges, then a hero image, then a horizontal rule, then the sections. The
rule is what separates the summary from the body.

### Screenshots

A screenshot is evidence, so it has to be of the current version. In
`lazy-to-text` the screenshots are generated from the code by a script, so
they cannot drift. Where a project cannot generate them, the README should
say when they were taken.

## The language

**The README speaks to its audience. The internal documents speak to the
owner.**

That is the whole policy. The rules below say which language goes where:

| Document | Language |
| --- | --- |
| `README.md` | The language of the people who will read it. A tool for the world gets English. A tool for a team gets Russian. |
| `PRODUCT.md`, `DESIGN.md`, `AGENTS.md` | The owner's working language. These are read by the owner and by agents, and there is no external audience. |
| Code, comments, commit messages | The owner's working language, consistently within a repository. |
| GitHub description, issue forms | The language of the people who will file issues. |

The rule that matters is the last one: **be consistent within a repository.**
A repository whose README is English and whose `PRODUCT.md` is Russian is
fine. A repository whose README is half English and half Russian is not.

There is no rule against a repository having two audiences. `monos` has a
public site and a private sync protocol; the README covers the public one.

## Length

There is no target length. There are two failure modes and they are opposite:

- **Too short to be useful.** A README that says "a tool for X" and nothing
  else makes the reader ask a question they should not have to.
- **Too long to be read.** A README that documents every function of every
  module is a manual, and manuals are not read by people deciding whether to
  use something.

The test is whether each paragraph answers a question the reader actually
has. If it does not, it belongs in `docs/`, linked from the section that
raised the question.

## Terminology

Pick one word for each concept and use it everywhere. If the README says
"workspace", the code says "workspace", the docs say "workspace", and the
error messages say "workspace".

The projects that read worst usually have three names for one thing: the
concept in the code, a different one in the README, and a third in the
comments. A reader who has to learn the mapping is reading two documents
instead of one.
