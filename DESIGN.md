---
name: golden-repo
description: The visual language of the house standard: warm paper, ink, one monospaced face.
colors:
  bg: "#1d2021"
  surface: "#282828"
  surface-deep: "#3c3836"
  fg: "#ebdbb2"
  muted: "#a89984"
  faint: "#928374"
  rule: "#504945"
  control: "#928374"
  ring: "#ebdbb2"
  ok: "#b8bb26"
  danger: "#ff8a7a"
  info: "#83a598"
  selection-bg: "#ebdbb2"
  selection-fg: "#282828"
  overlay-pill: "rgba(29, 32, 33, 0.94)"
  scrim: "rgba(0, 0, 0, 0.45)"
  bg-light: "#fbf1c7"
  surface-light: "#ebdbb2"
  surface-deep-light: "#d5c4a1"
  fg-light: "#3c3836"
  muted-light: "#665c54"
  faint-light: "#928374"
  rule-light: "#d5c4a1"
  control-light: "#928374"
  ring-light: "#3c3836"
  ok-light: "#5f5f0e"
  danger-light: "#cc241d"
  info-light: "#076678"
typography:
  body:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.55
  title:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "20px"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.025em"
  label:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "11px"
    fontWeight: 500
    lineHeight: 1.45
    letterSpacing: "0.12em"
  hint:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
  tag:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "11px"
    fontWeight: 500
    lineHeight: 1.45
    letterSpacing: "0.08em"
rounded:
  ui: "6px"
  pill: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "40px"
components:
  button-primary:
    backgroundColor: "{colors.fg}"
    textColor: "{colors.bg}"
    rounded: "{rounded.ui}"
    padding: "8px 20px"
  button-primary-hover:
    backgroundColor: "{colors.bg-light}"
    textColor: "{colors.bg}"
    rounded: "{rounded.ui}"
    padding: "8px 20px"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.fg}"
    rounded: "{rounded.ui}"
    padding: "8px 20px"
  field-underline:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.fg}"
    rounded: "{rounded.ui}"
    padding: "8px 12px"
  tag:
    backgroundColor: "transparent"
    textColor: "{colors.muted}"
    rounded: "{rounded.ui}"
    padding: "2px 8px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.fg}"
    rounded: "{rounded.ui}"
    padding: "16px"
---

# Design System: golden-repo

## Overview

**Creative North Star: "The Reference Card"**

The house standard is a reference card: a single printed sheet, kept in the
drawer above the bench, that says exactly how the parts fit together and
nothing more. It is not a brand. It does not have a logo, a campaign, or a
personality that it wants to perform. What it has is the authority of a
correct document — every line is there because something failed without it.

The visual language follows from that. The reference card is printed on warm
paper, in ink, in one typewriter face. It is quiet. Nothing glows, nothing
gradients, nothing is centred for the sake of it. The only thing that stands
out is the thing that is wrong: a failed check in red, a rule that was broken
in a warning amber, a passing check in olive. A reader scanning a page of
output should be able to find the failure without reading the failures.

The system is deliberately monochrome. A standard that carries colour has to
decide what each colour means, and every repository that adopts it inherits
that decision whether it wanted it or not. Instead the palette provides one
warm ground, one ink, three functional colours, and every other surface is
built from those. Repositories that have a visual identity of their own keep
it — `lazy-to-text` has its own tokens, `puuush` has its own — and the standard
governs the *documents*, not the pixels.

**Key Characteristics:**

- warm paper and ink; no pure white, no pure black
- one monospaced face for everything, including prose
- status is carried by text and colour together, never by colour alone
- flat surfaces: depth comes from tone, not from shadow
- one radius, one spacing scale, no exceptions

## Colors

A warm, low-chroma palette in the tradition of a well-kept terminal theme.
Dark is the primary surface, because most of the artefacts this standard
governs — diffs, CI logs, a terminal — are dark. A full light set is provided
because a README is read on GitHub, and GitHub is light.

### Primary

- **Ink** (`#ebdbb2`): the primary text colour on dark ground. Warm, never
  bright; at full strength on `#282828` it reads at roughly 11:1 contrast.
- **Ground** (`#1d2021`): the base surface. Almost black, but with a green-grey
  cast that keeps it from reading as a dead panel.

### Secondary

- **Paper** (`#fbf1c7`): the light-theme ground. The counterpart of
  `#1d2021`; the same warm family at the other end of the scale.

### Tertiary

- **Olive** (`#b8bb26`): success. A passing check, a rule satisfied.
- **Clay Red** (`#ff8a7a`): failure. A hard rule broken. Used sparingly and
  never for decoration.
- **Slate Blue** (`#83a598`): information. Soft findings, notices, secondary
  status. Reads as "look here" without reading as "broken".

### Neutral

- **Surface** (`#282828`): raised ground. Cards, code blocks, table headers.
- **Deep Surface** (`#3c3836`): one step further forward. Hover states,
  nested panels.
- **Muted** (`#a89984`): secondary text, captions, table borders in dense
  layouts.
- **Faint** (`#928374`): disabled text, decorative rules, axis labels.
- **Rule** (`#504945`): separators and borders. Deliberately a step above
  `#3c3836` so that a border is visible without being loud.

### Named Rules

**The Warm Ground Rule.** Every background is built warm. `#ffffff` and
`#000000` do not appear as surfaces. A pure black background next to a warm
palette looks like a hole in the page.

**The Contrast Floor Rule.** Body text is never below 4.5:1 against its
background. Borders, underlines and focus rings are never below 3:1
(WCAG 1.4.11). Muted text is `#a89984` on `#282828`, which clears the floor;
`#928374` is only ever used for decoration.

**The Status Is Doubled Rule.** A status is always carried by a word as well
as a colour — "pass", "fail", "warn". Colour is the fast channel, text is the
reliable one, and a reader with a colour vision deficiency or a screen reader
must not lose the information.

## Typography

**Display Font:** JetBrains Mono (with `ui-monospace, SFMono-Regular, Menlo,
monospace` as the fallback)
**Body Font:** JetBrains Mono (same stack)
**Label/Mono Font:** JetBrains Mono (same stack)

**Character:** one face, used for everything, including running prose. A
reference card is typed, not typeset. The monospaced face also makes
documentation diffs readable: a changed word shows as a changed word, and
aligned tables stay aligned in a plain-text editor.

### Hierarchy

- **Title** (700, 20px/1.3, −0.025em): the one H1 on a page.
- **Section** (700, 15px/1.4): the H2 that names a section of a document.
- **Body** (400, 13px/1.55): running prose, list items, table cells. Hard-wrapped
  at roughly 76 characters so the raw file stays readable in an editor.
- **Label** (500, 11px/1.45, 0.12em, uppercase): field labels, table headers,
  section markers. Uppercase is used for labels only, never for sentences.
- **Hint** (400, 12px/1.5): secondary explanation under a control or a
  command.
- **Tag** (500, 11px/1.45, 0.08em): status tags — pass, fail, warn, blocked.

### Named Rules

**The One Face Rule.** A document mixes no other face. A second font means a
second opinion about the content, and a reference card has one.

**The Uppercase Is A Label Rule.** Uppercase marks a label, never a sentence
and never a heading. A heading in all caps reads as a banner, and the standard
does not shout.

## Layout

Documents are a single column of prose, hard-wrapped at 76 characters, with a
maximum of 76 columns. Tables are used for anything with more than two
dimensions and are always given a header row. Code blocks are fenced and
labelled with a language.

Code and output are indented one level (2 spaces) from the prose they belong
to, and a command's output is shown as a separate block, never merged into the
command. The standard is read in a diff as often as in a browser, and an
indistinguishable command/output pair is unreadable in a diff.

Spacing follows one scale: `4, 8, 16, 24, 40`. There is no `10px` and no
`12px` step anywhere in the system.

## Elevation & Depth

This system uses **no shadows**. Surfaces are flat at all times; depth is
expressed by tone — `#1d2021` for the ground, `#282828` for a raised card,
`#3c3836` for a nested or hovered panel.

A shadow in a documentation context always means "this is a floating layer
over content", and the artefacts this standard governs — a README on GitHub, a
terminal, a CI log — are all flat surfaces. A shadow there is a lie about the
depth.

### Named Rules

**The Flat-By-Default Rule.** Surfaces are flat at rest. A shadow appears only
as a response to state, and in this system that state is the hover on a raised
overlay.

## Shapes

One radius, `6px`, applied to every rectangular element: buttons, inputs,
cards, tags and the overlay pill. The one exception is the pill itself, which
is fully rounded (`999px`) because it is a floating label over other content,
not a container.

Borders are `1px` in `#504945`. A filled, bordered or pill-shaped button is
the exception that proves the rule: the primary action is a solid ink block
with no border, and everything else is a text button with no fill.

## Components

### Buttons

- **Shape:** 6px radius, no border.
- **Primary:** ink fill (`#ebdbb2`), ground text (`#1d2021`), 8px/20px padding.
  One per screen; it is the action the document exists for.
- **Hover / Focus:** the fill lightens to `#fbf1c7`; focus shows a 2px
  `#ebdbb2` ring at 2px offset.
- **Ghost:** transparent fill, ink text, same geometry. This is the default for
  every secondary action, and there should be no third variant.

### Tags

- **Style:** transparent fill, 1px `#504945` border, 6px radius, 2px/8px
  padding, uppercase 11px label.
- **State:** colour carries the meaning and the text repeats it — `ok` in
  olive, `fail` in clay red, `warn` in slate blue. Never colour alone.

### Cards / Containers

- **Corner Style:** 6px radius.
- **Background:** `#282828` on the `#1d2021` ground.
- **Shadow Strategy:** none; see Elevation & Depth.
- **Border:** 1px `#504945` when a card sits on a surface of the same tone.
- **Internal Padding:** 16px.

### Inputs / Fields

- **Style:** a single bottom border in `#faint`, no other border, no fill
  beyond the surface colour.
- **Focus:** the bottom border becomes `#ebdbb2` and a 1px glow appears
  beneath it. The caret is `#ebdbb2`.
- **Error:** the border becomes clay red *and* the message appears in text.
  The border alone is not an error state.

### Navigation

Navigation in a document is a table of contents at the top, built from the
headings in order. It is a list of links, not a menu, and it is not styled
differently from the body text except for a slightly brighter tone.

### Output Blocks

A terminal or CI output is a code block with a surface background and no
border. A failing line is the only part that is coloured, and it is coloured
in clay red. The rest is `muted`.

## Do's and Don'ts

### Do:

- **Do** read every colour through the token names, never as a literal hex
  inside a rule or a component.
- **Do** show status as a word and a colour together.
- **Do** keep one radius (`6px`) and one spacing scale.
- **Do** check the dark ground first and the light one second, when a
  document has to work in both.
- **Do** let the ink do the work. The palette is quiet on purpose.

### Don't:

- **Don't** add a second font, even for code. One face, including code.
- **Don't** use shadow to create depth. Use tone.
- **Don't** use pure `#ffffff` or `#000000`.
- **Don't** colour a thing to make it prettier. Functional colours are
  functional, and only three of them exist.
- **Don't** put uppercase in a heading or a sentence.
- **Don't** make colour the only carrier of a status.
