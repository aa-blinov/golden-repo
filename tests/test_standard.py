"""Tests that the standard's three layers agree.

The standard is described three times: as data in standard.json, as code in
scripts/housecheck.py, and as starting files in templates/. Each layer was
once written out by hand, and each pair drifted.

These tests keep them together. A rule added to the manifest and nowhere
else fails here, before it reaches a repository that does not know about it.
"""

import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import housecheck  # noqa: E402
import render  # noqa: E402

TEMPLATES = os.path.join(ROOT, "templates")


def manifest():
    with open(os.path.join(ROOT, "standard.json")) as handle:
        return json.load(handle)


class ManifestTest(unittest.TestCase):
    def test_the_manifest_is_valid_json(self):
        data = manifest()
        self.assertIn("version", data)
        self.assertRegex(data["version"], r"^\d+\.\d+\.\d+$")

    def test_the_manifest_has_the_sections_the_checker_reads(self):
        data = manifest()
        for key in ("root", "readme", "product", "design"):
            self.assertIn(key, data)

    def test_every_required_file_has_a_comment(self):
        for entry in manifest()["root"]["files"]:
            self.assertTrue(
                entry.get("comment"),
                "%s has no comment, so the tree would describe it with "
                "nothing" % entry["path"],
            )

    def test_no_path_is_listed_twice(self):
        paths = [entry["path"] for entry in manifest()["root"]["files"]]
        self.assertEqual(len(paths), len(set(paths)))

    def test_every_required_file_is_inside_a_known_directory(self):
        known = {entry["path"] for entry in manifest()["root"]["directories"]}
        for entry in manifest()["root"]["files"]:
            path = entry["path"]
            if "/" not in path:
                continue
            parent = path.rsplit("/", 1)[0]
            self.assertIn(
                parent, known,
                "%s sits in %s, which the manifest does not list as a "
                "directory" % (path, parent),
            )


class CheckerAgreementTest(unittest.TestCase):
    def test_the_checker_reads_the_required_files_from_the_manifest(self):
        data = manifest()
        expected = [
            entry["path"] for entry in data["root"]["files"]
            if entry.get("required")
        ]
        self.assertEqual(housecheck.REQUIRED_FILES, expected)

    def test_the_checker_reads_the_directories_from_the_manifest(self):
        data = manifest()
        expected = [entry["path"] for entry in data["root"]["directories"]]
        self.assertEqual(housecheck.REQUIRED_DIRS, expected)

    def test_the_checker_reads_the_sections_from_the_manifest(self):
        data = manifest()
        self.assertEqual(
            housecheck.PRODUCT_SECTIONS,
            [entry["label"] for entry in data["product"]["sections"]],
        )
        self.assertEqual(
            housecheck.DESIGN_SECTIONS,
            [entry["label"] for entry in data["design"]["sections"]],
        )
        self.assertEqual(
            [label for label, _ in housecheck.README_SECTIONS],
            [entry["label"] for entry in data["readme"]["sections"]],
        )


class TemplateAgreementTest(unittest.TestCase):
    def test_every_file_the_standard_demands_has_a_template(self):
        """A repository that adopts the standard gets its starting files
        from templates/. A file the standard knows with no template behind it
        is a file the owner has to write from nothing."""
        for entry in manifest()["root"]["files"]:
            path = entry["path"]
            template = os.path.join(TEMPLATES, path)
            self.assertTrue(
                os.path.exists(template),
                "the standard knows %s and templates/%s does not exist"
                % (path, path),
            )

    def test_every_required_file_has_a_template(self):
        for entry in manifest()["root"]["files"]:
            if not entry.get("required"):
                continue
            path = entry["path"]
            self.assertTrue(
                os.path.exists(os.path.join(TEMPLATES, path)),
                "the standard demands %s and templates/%s does not exist"
                % (path, path),
            )

    def test_every_template_is_a_file_the_standard_knows(self):
        """A template the standard does not mention is a file that reaches a
        new repository without anyone having decided it should."""
        known = set(housecheck.MANIFEST_FILES)
        for rel in template_files():
            self.assertIn(
                rel, known,
                "templates/%s is not in standard.json" % rel,
            )

    def test_the_templates_have_a_license(self):
        self.assertTrue(os.path.exists(os.path.join(TEMPLATES, "LICENSE")))


class RenderAgreementTest(unittest.TestCase):
    def test_the_documents_match_the_manifest(self):
        """The tree and the tables in the documentation are generated. If
        they have fallen behind the manifest, the generator has not been
        run."""
        for name in ("docs/structure.md", "docs/house-style.md"):
            path = os.path.join(ROOT, name)
            with open(path) as handle:
                current = handle.read()
            expected = render.render_file(path, manifest())
            self.assertEqual(
                current, expected,
                "%s is out of date; run scripts/render.py" % name,
            )

    def test_the_tree_lists_every_file_the_standard_demands(self):
        tree = render.tree(manifest())
        for entry in manifest()["root"]["files"]:
            name = entry["path"].rsplit("/", 1)[-1]
            self.assertIn(name, tree)


def template_files():
    """Every file under templates/, relative to it."""
    found = []
    for dirpath, dirnames, filenames in os.walk(TEMPLATES):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in filenames:
            if name == ".DS_Store":
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), TEMPLATES)
            found.append(rel)
    return sorted(found)


if __name__ == "__main__":
    unittest.main()
