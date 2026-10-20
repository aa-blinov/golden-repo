"""Tests for the house-style checker.

A rule with no test is a rule with a bug in it. These tests build a
throwaway repository in a temporary directory, break it in one specific way,
and assert that the right rule fires.

Run them with:

    python3 -m unittest discover -s tests -v
"""

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import housecheck  # noqa: E402


VALID_README = """# Example

One line that says what this does.

## Quick start

```bash
make run
```

## What it does

- Does a thing.

## Development

```bash
make test
```

## License

[MIT](LICENSE)
"""

VALID_PRODUCT = """# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

People.

## Product Purpose

A thing.

## Positioning

Distinctive.

## Operating Context

Everyday.

## Capabilities and Constraints

Some.

## Brand Commitments

A name.

## Evidence on Hand

Files.

## Product Principles

1. One.

## Accessibility & Inclusion

Some.
"""

VALID_DESIGN = """---
name: Example
description: A thing
colors:
  primary: "#000000"
---

# Design System: Example

## Overview

Something.

## Colors

Something.

## Typography

Something.

## Layout

Something.

## Elevation & Depth

Something.

## Shapes

Something.

## Components

Something.

## Do's and Don'ts

Something.
"""


class RepoFixture(object):
    """Builds a repository that passes the checker, so that each test can
    break exactly one thing and know that the finding is its own.

    The fixture is built from standard.json, not from a list written out
    here. A rule added to the standard therefore arrives in the tests
    automatically, and the fixture cannot drift away from the standard
    without a test failing.
    """

    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="housecheck-test-")

    def write(self, rel, content):
        path = os.path.join(self.root, rel)
        directory = os.path.dirname(path)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)
        with open(path, "w") as handle:
            handle.write(content)
        return path

    def mkdir(self, rel):
        path = os.path.join(self.root, rel)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def remove(self, rel):
        path = os.path.join(self.root, rel)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)

    def build_valid(self):
        # The files whose content a rule actually reads.
        self.write("README.md", VALID_README)
        self.write("AGENTS.md", "# AGENTS\n\n" + ("x" * 300) + "\n")
        self.write("PRODUCT.md", VALID_PRODUCT)
        self.write("DESIGN.md", VALID_DESIGN)
        self.write("CHANGELOG.md", "# Changelog\n\n## 0.1.0 — 2026-01-01\n\n- First.\n")
        self.write(
            "LICENSE",
            "MIT License\n\nCopyright (c) 2026 Alexander Blinov\n\n"
            "Permission is hereby granted, free of charge...\n",
        )

        # Everything else the standard demands, with the content its rule
        # needs rather than the content it would really have.
        for path in housecheck.MANIFEST_FILES:
            if os.path.exists(os.path.join(self.root, path)):
                continue
            self.write(path, self.placeholder_for(path))

        for path in housecheck.REQUIRED_DIRS:
            self.mkdir(path)

        return self

    def placeholder_for(self, path):
        """The content a placeholder needs for the rules to pass."""
        if path.endswith(".github/workflows/ci.yml") or \
                path.endswith(".github/workflows/house-style.yml"):
            return "on:\n  pull_request:\n"
        if path.endswith("design.json"):
            return '{"schemaVersion": 2, "title": "Example"}\n'
        if path.endswith(".impeccable/config.json"):
            return '{"buildPath": "code"}\n'
        if path.endswith("docs/README.md"):
            return "# Docs\n\nSee [architecture](architecture.md).\n"
        if path.endswith("docs/architecture.md"):
            return "# Architecture\n"
        if path.endswith(".gitignore"):
            return "node_modules/\n"
        if path.endswith(".editorconfig"):
            return "root = true\n"
        if path.endswith("dependabot.yml"):
            return "version: 2\nupdates: []\n"
        return "# %s\n" % os.path.basename(path)

    def check(self, **kwargs):
        return housecheck.run(housecheck.Repo(self.root), **kwargs)

    def codes(self, severity=None):
        return sorted(
            f.code for f in self.check()
            if severity is None or f.severity == severity
        )

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)


class CheckerTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = RepoFixture().build_valid()

    def tearDown(self):
        self.repo.cleanup()

    # -- structure ---------------------------------------------------------

    def test_a_valid_repository_has_no_hard_findings(self):
        self.assertEqual(self.repo.codes("hard"), [])

    def test_a_missing_root_file_is_reported(self):
        self.repo.remove("README.md")
        self.assertIn("HS001", self.repo.codes("hard"))

    def test_a_missing_directory_is_reported(self):
        self.repo.remove("docs")
        self.assertIn("HS002", self.repo.codes("hard"))

    def test_a_missing_ci_workflow_is_reported(self):
        # The manifest names the workflows a repository carries, so removing
        # one is a missing file. Removing all of them leaves a repository
        # whose CI never runs.
        self.repo.remove(".github/workflows/ci.yml")
        self.assertIn("HS001", self.repo.codes("hard"))
        self.repo.remove(".github/workflows/house-style.yml")
        self.assertIn("HS005", self.repo.codes("hard"))

    def test_an_empty_issue_template_directory_is_reported(self):
        self.repo.remove(".github/ISSUE_TEMPLATE/bug_report.md")
        self.assertIn("HS001", self.repo.codes("hard"))
        for name in ("feature_request.md", "config.yml"):
            self.repo.remove(".github/ISSUE_TEMPLATE/" + name)
        self.assertIn("HS006", self.repo.codes("hard"))

    def test_an_empty_gitignore_is_soft(self):
        self.repo.write(".gitignore", "")
        self.assertIn("HS009", self.repo.codes("soft"))
        self.assertNotIn("HS009", self.repo.codes("hard"))

    # -- licence -----------------------------------------------------------

    def test_a_licence_that_is_not_a_licence_is_reported(self):
        self.repo.write("LICENSE", "Do whatever you want.\n")
        self.assertIn("HS003", self.repo.codes("hard"))

    def test_a_licence_without_a_copyright_holder_is_reported(self):
        self.repo.write(
            "LICENSE",
            "MIT License\n\nPermission is hereby granted, free of charge...\n",
        )
        self.assertIn("HS004", self.repo.codes("hard"))

    def test_a_licence_with_a_holder_passes(self):
        self.assertNotIn("HS004", self.repo.codes("hard"))
        self.assertNotIn("HS003", self.repo.codes("hard"))

    # -- README ------------------------------------------------------------

    def test_a_readme_without_a_heading_is_reported(self):
        self.repo.write("README.md", "Just some text, no heading.\n" + "x" * 500)
        self.assertIn("HS011", self.repo.codes("hard"))

    def test_a_hash_inside_a_code_block_is_not_a_heading(self):
        """A README that shows a shell script is full of "#" comments.
        They are comments, not headings."""
        with_script = (
            "# Example\n\n"
            "## Quick start\n\n"
            "```bash\n"
            "# install the thing\n"
            "# then run it\n"
            "make install\n"
            "```\n\n"
            "## What it does\n\n- A thing.\n\n"
            "## Development\n\n```bash\nmake test\n```\n\n"
            "## License\n\n[MIT](LICENSE)\n"
        )
        self.repo.write("README.md", with_script)
        self.assertNotIn("HS011", self.repo.codes("hard"))

    def test_a_readme_with_two_h1s_is_reported(self):
        self.repo.write("README.md", "# One\n\ntext\n\n# Two\n\ntext\n")
        self.assertIn("HS011", self.repo.codes("hard"))

    def test_a_readme_missing_a_section_is_reported(self):
        broken = VALID_README.replace("## Development", "## Notes")
        self.repo.write("README.md", broken)
        self.assertIn("HS012", self.repo.codes("hard"))

    def test_a_readme_with_the_sections_out_of_order_is_soft(self):
        reordered = (
            "# Example\n\n"
            "## What it does\n\n- A thing.\n\n"
            "## Quick start\n\n```bash\nmake run\n```\n\n"
            "## Development\n\n```bash\nmake test\n```\n\n"
            "## License\n\n[MIT](LICENSE)\n"
        )
        self.repo.write("README.md", reordered)
        self.assertIn("HS013", self.repo.codes("soft"))
        self.assertNotIn("HS013", self.repo.codes("hard"))

    def test_a_russian_readme_passes_the_section_check(self):
        russian = (
            "# Пример\n\n"
            "Одна строка о том, что это делает.\n\n"
            "## Быстрый старт\n\n```bash\nmake run\n```\n\n"
            "## Что внутри\n\n- Делает дело.\n\n"
            "## Разработка\n\n```bash\nmake test\n```\n\n"
            "## Лицензия\n\n[MIT](LICENSE)\n"
        )
        self.repo.write("README.md", russian)
        self.assertNotIn("HS012", self.repo.codes("hard"))

    def test_a_short_readme_is_soft(self):
        self.repo.write("README.md", "# Example\n\nShort.\n")
        self.assertIn("HS014", self.repo.codes("soft"))

    def test_a_readme_without_a_licence_link_is_soft(self):
        without = VALID_README.replace("[MIT](LICENSE)", "MIT")
        self.repo.write("README.md", without)
        self.assertIn("HS015", self.repo.codes("soft"))

    # -- product and design ------------------------------------------------

    def test_a_product_md_without_the_schema_marker_is_reported(self):
        self.repo.write("PRODUCT.md", VALID_PRODUCT.replace("impeccable:product-schema 1", ""))
        self.assertIn("HS020", self.repo.codes("hard"))

    def test_a_product_md_missing_a_section_is_reported(self):
        self.repo.write(
            "PRODUCT.md",
            VALID_PRODUCT.replace("## Brand Commitments", "## Notes"),
        )
        self.assertIn("HS021", self.repo.codes("hard"))

    def test_a_design_md_without_frontmatter_is_reported(self):
        self.repo.write("DESIGN.md", VALID_DESIGN.replace("---\n", "", 1))
        self.assertIn("HS022", self.repo.codes("hard"))

    def test_a_design_md_with_sections_out_of_order_is_reported(self):
        broken = """---
name: Example
description: A thing
colors:
  primary: "#000000"
---

# Design System: Example

## Overview

Something.

## Typography

Something.

## Colors

Something.

## Layout

Something.
"""
        self.repo.write("DESIGN.md", broken)
        self.assertIn("HS023", self.repo.codes("hard"))

    def test_a_missing_design_sidecar_is_reported(self):
        self.repo.remove(".impeccable/design.json")
        self.assertIn("HS024", self.repo.codes("hard"))

    def test_an_invalid_design_sidecar_is_reported(self):
        self.repo.write(".impeccable/design.json", "{not json")
        self.assertIn("HS024", self.repo.codes("hard"))

    # -- links -------------------------------------------------------------

    def test_a_broken_relative_link_is_reported(self):
        self.repo.write("README.md", VALID_README + "\nSee [gone](docs/gone.md).\n")
        self.assertIn("HS030", self.repo.codes("hard"))

    def test_a_broken_image_is_reported(self):
        self.repo.write("README.md", VALID_README + "\n![gone](docs/gone.png)\n")
        self.assertIn("HS031", self.repo.codes("hard"))

    def test_an_external_link_is_not_checked(self):
        self.repo.write(
            "README.md",
            VALID_README + "\nSee [github](https://github.com/aa-blinov).\n",
        )
        self.assertNotIn("HS030", self.repo.codes("hard"))

    def test_a_link_inside_a_code_block_is_not_checked(self):
        self.repo.write(
            "README.md",
            VALID_README + "\n```\n[gone](docs/gone.md)\n```\n",
        )
        self.assertNotIn("HS030", self.repo.codes("hard"))

    def test_a_link_to_an_anchor_is_not_checked(self):
        self.repo.write("README.md", VALID_README + "\nSee [above](#quick-start).\n")
        self.assertNotIn("HS030", self.repo.codes("hard"))

    def test_a_link_with_a_line_number_resolves_to_the_file(self):
        self.repo.write("docs/notes.md", "# Notes\n\nSee [config](notes.md:12).\n")
        self.assertNotIn("HS030", self.repo.codes("hard"))

    def test_a_link_outside_the_repository_is_soft(self):
        self.repo.write("README.md", VALID_README + "\nSee [local](/Users/me/thing.md).\n")
        self.assertIn("HS030", self.repo.codes("soft"))
        self.assertNotIn("HS030", self.repo.codes("hard"))

    # -- markdown hygiene --------------------------------------------------

    def test_an_emoji_is_reported(self):
        self.repo.write("docs/notes.md", "# Notes\n\nShip it \U0001F680\n")
        self.assertIn("HS040", self.repo.codes("hard"))

    def test_a_check_mark_is_not_an_emoji(self):
        self.repo.write("docs/notes.md", "# Notes\n\nDone \u2713\n")
        self.assertNotIn("HS040", self.repo.codes("hard"))

    def test_a_skipped_heading_level_is_reported(self):
        self.repo.write("docs/notes.md", "# Notes\n\n### Deep\n")
        self.assertIn("HS041", self.repo.codes("hard"))

    def test_trailing_whitespace_is_reported(self):
        self.repo.write("docs/notes.md", "# Notes\n\nword   \n")
        self.assertIn("HS042", self.repo.codes("hard"))

    def test_two_trailing_spaces_in_markdown_are_allowed(self):
        self.repo.write("docs/notes.md", "# Notes\n\nline one  \nline two\n")
        self.assertNotIn("HS042", self.repo.codes("hard"))

    def test_a_missing_final_newline_is_reported(self):
        self.repo.write("docs/notes.md", "# Notes\n\nno newline at the end")
        self.assertIn("HS043", self.repo.codes("hard"))

    def test_a_tab_indent_in_markdown_is_reported(self):
        self.repo.write("docs/notes.md", "# Notes\n\n\tindented with a tab\n")
        self.assertIn("HS044", self.repo.codes("hard"))

    # -- documents ---------------------------------------------------------

    def test_a_missing_agents_md_is_reported_by_the_root_file_rule(self):
        self.repo.remove("AGENTS.md")
        self.assertIn("HS001", self.repo.codes("hard"))

    def test_a_short_agents_md_is_soft(self):
        self.repo.write("AGENTS.md", "# AGENTS\n\nToo short.\n")
        self.assertIn("HS104", self.repo.codes("soft"))

    def test_a_changelog_without_a_version_is_soft(self):
        self.repo.write("CHANGELOG.md", "# Changelog\n\nNothing yet.\n")
        self.assertIn("HS103", self.repo.codes("soft"))

    def test_a_docs_index_that_links_to_nothing_is_soft(self):
        self.repo.write("docs/README.md", "# Docs\n\nNothing here yet.\n")
        self.assertIn("HS102", self.repo.codes("soft"))

    def test_a_product_md_stub_is_reported(self):
        stub = "\n".join([
            "# Product",
            "",
            "<!-- impeccable:product-schema 1 -->",
            "",
            "## Platform",
            "",
            "<!-- web -->",
        ])
        self.repo.write("PRODUCT.md", stub)
        self.assertIn("HS026", self.repo.codes("hard"))

    # -- placeholders ------------------------------------------------------

    def test_an_unfilled_placeholder_is_reported(self):
        self.repo.write("README.md", VALID_README + "\nRun {{INSTALL_COMMAND}}.\n")
        self.assertIn("HS025", self.repo.codes("hard"))

    def test_the_templates_directory_is_exempt_from_the_placeholder_rule(self):
        self.repo.write("templates/README.md", "Run {{INSTALL_COMMAND}}.\n")
        self.assertNotIn("HS025", self.repo.codes("hard"))

    def test_a_template_marker_is_reported(self):
        self.repo.write(
            "docs/notes.md",
            "<!-- house-style: template — fill this file in -->\n\n# Notes\n",
        )
        self.assertIn("HS025", self.repo.codes("hard"))

    def test_a_document_that_merely_mentions_the_placeholder_syntax_is_not_flagged(self):
        self.repo.write(
            "docs/notes.md",
            "# Notes\n\nThe scaffolder substitutes the `{{ ... }}` tokens.\n",
        )
        self.assertNotIn("HS025", self.repo.codes("hard"))

    def test_a_comment_before_the_h1_is_allowed(self):
        with_comment = "<!-- a note for the reader -->\n\n" + VALID_README
        self.repo.write("README.md", with_comment)
        self.assertNotIn("HS011", self.repo.codes("hard"))

    def test_a_reference_style_link_is_checked(self):
        self.repo.write(
            "README.md",
            VALID_README + "\nSee [the notes][n].\n\n[n]: docs/gone.md\n",
        )
        self.assertIn("HS030", self.repo.codes("hard"))

    # -- runner ------------------------------------------------------------

    def test_the_exit_code_is_zero_when_nothing_hard_failed(self):
        fixture = RepoFixture().build_valid()
        try:
            self.assertEqual(
                housecheck.main([fixture.root]),
                0,
            )
        finally:
            fixture.cleanup()

    def test_the_exit_code_is_one_when_a_hard_rule_failed(self):
        fixture = RepoFixture().build_valid()
        try:
            fixture.remove("LICENSE")
            self.assertEqual(housecheck.main([fixture.root]), 1)
        finally:
            fixture.cleanup()

    def test_strict_mode_fails_on_a_soft_finding(self):
        fixture = RepoFixture().build_valid()
        try:
            fixture.write(".gitignore", "")
            self.assertEqual(housecheck.main([fixture.root]), 0)
            self.assertEqual(housecheck.main([fixture.root, "--strict"]), 1)
        finally:
            fixture.cleanup()

    def test_json_output_is_parseable(self):
        import json
        fixture = RepoFixture().build_valid()
        try:
            fixture.remove("LICENSE")
            import io
            import contextlib
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                housecheck.main([fixture.root, "--json"])
            payload = json.loads(buffer.getvalue())
            self.assertGreaterEqual(payload["hard"], 1)
            self.assertTrue(
                any(f["code"] == "HS001" for f in payload["findings"])
            )
        finally:
            fixture.cleanup()


if __name__ == "__main__":
    unittest.main()
