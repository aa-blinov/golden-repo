<!-- house-style: template — fill this file in, then delete this line -->

# {{PROJECT_NAME}}

<!--
  The opening paragraph is the one-sentence version of what this does, in
  the words a user would use. Two or three lines, no preamble.

  Then badges, then a hero image, then a horizontal rule, then the sections
  in this order:

    1. Quick start / Install   — the command first, prose after
    2. What it does            — the capabilities, as a list
    3. Screenshots             — what it looks like
    4. Configuration           — the options and their defaults
    5. How it works            — the architecture
    6. Development             — how to work on the code
    7. License                 — the terms

  Section order is fixed by the house style. Wording is yours.
-->

{{PROJECT_TAGLINE}}

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Quick start

<!-- The shortest path from nothing to running. One command if there is one. -->

```bash
{{INSTALL_COMMAND}}
```

<!--
  Then the alternatives, if there are any, and what each one is for. A
  table works well:

  | Platform | Command | Notes |
  | --- | --- | --- |
  | macOS | `brew install ...` | Apple silicon only |
-->

## What it does

<!--
  One bullet per capability. Each bullet says what it does, not what
  category it belongs to.

  - **Hotkey in, text out.** `Ctrl+F2` starts, `Ctrl+F3` stops and
    transcribes, and the result is pasted into the focused window.
-->

- **Capability one.** What it does, and what the user does with it.
- **Capability two.** What it does, and what the user does with it.

## Screenshots

<!--
  Images live in docs/screenshots/ and are referenced from here. The lines
  below are examples — delete them, or point them at the real files, and
  delete this comment.

  | Main window | Settings |
  | :---: | :---: |
  | ![Main window](docs/screenshots/main.png) | ![Settings](docs/screenshots/settings.png) |
-->

<!--
  No screenshot yet. Put the files in docs/screenshots/ and reference them
  here, then delete this comment.
-->

## Configuration

<!--
  The options and their defaults. A table beats prose for anything with
  more than two options.
-->

| Option | Default | What it does |
| --- | --- | --- |
| `option_name` | `default` | What changing it does. |

## How it works

<!--
  The architecture, for someone who wants to change it. A diagram in text
  form, the main data flow, and the decisions that are not obvious.
  The reasoning for a non-obvious choice goes in AGENTS.md.
-->

```
main → module → module → output
```

## Development

```bash
{{INSTALL_COMMAND}}      # bootstrap
{{TEST_COMMAND}}         # run the tests
```

## License

[MIT](LICENSE) — © {{LICENSE_HOLDER}}.
