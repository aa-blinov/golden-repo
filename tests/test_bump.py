"""Tests for the bump script.

The bump script decides which repositories to touch and which pin to write.
Those two decisions are worth testing; the API calls in between are GitHub's
problem, and testing them would mean testing the network.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import bump  # noqa: E402


class VersionTest(unittest.TestCase):
    def test_a_semver_tag_becomes_a_tuple(self):
        self.assertEqual(bump.version_tuple("v1.2.3"), (1, 2, 3))
        self.assertEqual(bump.version_tuple("1.2.3"), (1, 2, 3))

    def test_a_tag_that_is_not_semver_is_refused(self):
        for tag in ("main", "v1.0", "release-1", "", "v1.0.0-rc1"):
            self.assertIsNone(bump.version_tuple(tag))

    def test_a_newer_version_compares_greater(self):
        self.assertGreater(bump.version_tuple("v1.0.1"), bump.version_tuple("v1.0.0"))
        self.assertGreater(bump.version_tuple("v1.1.0"), bump.version_tuple("v1.0.9"))
        self.assertGreater(bump.version_tuple("v2.0.0"), bump.version_tuple("v1.99.99"))

    def test_an_older_version_does_not(self):
        self.assertLess(bump.version_tuple("v1.0.0"), bump.version_tuple("v1.0.1"))
        self.assertEqual(bump.version_tuple("v1.0.0"), bump.version_tuple("v1.0.0"))


class ReferenceTest(unittest.TestCase):
    def test_the_standard_is_recognised(self):
        text = "      - uses: aa-blinov/golden-repo/.github/actions/house-style@v1.0.0\n"
        matches = bump.REFERENCE_RE.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "aa-blinov/golden-repo/.github/actions/house-style")
        self.assertEqual(matches[0][1], "v1.0.0")

    def test_another_action_is_not_the_standard(self):
        text = "      - uses: actions/checkout@v4\n"
        for dependency, _ in bump.REFERENCE_RE.findall(text):
            self.assertNotEqual(dependency.split("/")[1], bump.STANDARD_NAME)

    def test_a_pinned_sha_is_still_a_reference(self):
        text = "      - uses: aa-blinov/golden-repo/.github/actions/house-style@abc123\n"
        matches = bump.REFERENCE_RE.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][1], "abc123")

    def test_several_references_are_all_found(self):
        text = (
            "      - uses: aa-blinov/golden-repo/.github/actions/house-style@v1.0.0\n"
            "      - uses: actions/checkout@v4\n"
            "      - uses: aa-blinov/golden-repo/.github/actions/house-style@v1.0.1\n"
        )
        matches = bump.REFERENCE_RE.findall(text)
        self.assertEqual(len(matches), 3)


if __name__ == "__main__":
    unittest.main()
