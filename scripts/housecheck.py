#!/usr/bin/env python3
"""housecheck — check a repository against the house standard.

The standard is defined in docs/house-style.md. This script is the normative
implementation of it: where the prose and this code disagree, this code is
the standard and the prose is a bug.

Plain Python 3, standard library only. It has to run on a bare machine,
because it runs in CI for every repository that adopts the standard.

    housecheck.py [PATH] [--strict] [--json] [--remote]

Exit code is 0 when no hard rule failed, 1 otherwise. Soft findings do not
affect the exit code unless --strict is given.
"""

import argparse
import json
import os
import re
import subprocess
import sys

# --------------------------------------------------------------------------
# The standard
# --------------------------------------------------------------------------

# The standard, as data. standard.json is the single source of truth for
# what a repository must contain; the checker reads it rather than repeating
# it, so a rule is written in one place.
#
# A missing or malformed manifest is fatal. A checker that silently skipped
# the rules it could not read would report a clean repository and be wrong.

def manifest_path():
    """Where standard.json lives, relative to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (
        os.path.join(here, "..", "standard.json"),
        os.path.join(here, "standard.json"),
    ):
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    return None


def load_manifest():
    """Read standard.json, or explain why it cannot be read."""
    path = manifest_path()
    if path is None:
        raise RuntimeError(
            "housecheck: standard.json is missing. It holds the rules this "
            "checker enforces, and the checker does not guess them. It sits "
            "next to the standard, in the repository root."
        )
    try:
        with open(path) as handle:
            manifest = json.load(handle)
    except ValueError as error:
        raise RuntimeError(
            "housecheck: %s is not valid JSON: %s" % (path, error)
        )
    except IOError as error:
        raise RuntimeError("housecheck: cannot read %s: %s" % (path, error))
    for key in ("root", "readme", "product", "design"):
        if key not in manifest:
            raise RuntimeError(
                "housecheck: %s has no '%s' section." % (path, key)
            )
    return manifest


MANIFEST = load_manifest()
STANDARD_VERSION = MANIFEST.get("version", "unknown")

# Every file the manifest marks as required, at whatever level it sits.
# The list is one list, so a file cannot be required in the checker and
# missing from the tree, or the other way round.
REQUIRED_FILES = [
    entry["path"] for entry in MANIFEST["root"]["files"]
    if entry.get("required")
]
# Every file the standard knows about, required or not. The scaffolder builds
# from this list, and the tests build their fixture from it.
MANIFEST_FILES = [entry["path"] for entry in MANIFEST["root"]["files"]]
REQUIRED_DIRS = [entry["path"] for entry in MANIFEST["root"]["directories"]]

PRODUCT_SECTIONS = [entry["label"] for entry in MANIFEST["product"]["sections"]]
DESIGN_SECTIONS = [entry["label"] for entry in MANIFEST["design"]["sections"]]

# A README must answer these four questions. The keywords are matched against
# the normalised heading text, so a project in Russian passes with Russian
# headings. The intent is the section, not the wording.
README_SECTIONS = [
    (entry["label"], list(entry["keywords"]))
    for entry in MANIFEST["readme"]["sections"]
]

# Recognisable licence identifiers, matched against the first line of the
# LICENSE file.
KNOWN_LICENSES = [
    "MIT License",
    "MIT license",
    "Apache License",
    "GNU GENERAL PUBLIC LICENSE",
    "GNU AFFERO GENERAL PUBLIC LICENSE",
    "GNU LESSER GENERAL PUBLIC LICENSE",
    "Mozilla Public License",
    "BSD 3-Clause",
    "BSD 2-Clause",
    "ISC License",
    "The Unlicense",
    "Boost Software License",
]

# Emoji live in these ranges. Ordinary punctuation, arrows and typographic
# marks are deliberately outside them: a house style that bans "->" is a house
# style nobody keeps.
EMOJI_RANGES = (
    (0x1F000, 0x1FAFF),   # Mahjong, cards, pictographs, symbols, transport
    (0x2600, 0x26FF),     # Miscellaneous symbols
    (0x2700, 0x27BF),     # Dingbats
    (0x2B00, 0x2BFF),     # Miscellaneous symbols and arrows
    (0x231A, 0x231B),     # Watch, hourglass
    (0x23E9, 0x23FA),     # Media controls, alarm clock
)

# Check marks and cross marks are punctuation in a technical document, and
# the standard uses them as such.
EMOJI_ALLOWED = frozenset({
    0x2610, 0x2611,       # Ballot box
    0x2713, 0x2714,       # Check marks
    0x2715, 0x2716, 0x2717, 0x2718,  # Cross marks
    0xFE0F,               # Variation selector-16
    0x200D,               # Zero-width joiner
    0x20E3,               # Combining enclosing keycap
})

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", "out", "target", "vendor",
    ".venv", "venv", "__pycache__", ".next", ".nuxt", ".output", "coverage",
    "site-packages", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".gradle", ".idea", ".cache", "third_party", "third-party",
    # A skill or a prompt the owner copied in. It is somebody else's work:
    # restyling it is not the standard's business, and the emoji in it are
    # the upstream author's.
    ".agents", ".claude", "skills",
}


def is_vendored(rel):
    """Third-party code is not the owner's code, and the house style does
    not apply to it."""
    return any(part in SKIP_DIRS for part in rel.split("/")[:-1])

MAX_FILE_BYTES = 100 * 1024 * 1024      # GitHub rejects anything above this
WARN_FILE_BYTES = 50 * 1024 * 1024      # Beyond this, use LFS or a release asset

# How many findings of one rule the text report shows before counting the
# rest. The full list is always in the JSON output.
MAX_FINDINGS_PER_RULE = 8

# The marker a template file carries until it is filled in. It is a comment,
# so it costs nothing in the rendered document, and it is unambiguous in a
# way that "the file mentions a placeholder somewhere" is not.
TEMPLATE_MARKER = "house-style: template"

# The per-project documents. A placeholder left in one of these is always a
# mistake: the document was meant to be written, not scaffolded.
PROJECT_DOCUMENTS = frozenset({
    "README.md",
    "AGENTS.md",
    "PRODUCT.md",
    "DESIGN.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
})

# A file may declare that its emoji are a product decision rather than
# decoration. A Telegram bot whose buttons carry emoji, or a message format
# table, is not a document that forgot the rule: the glyphs are what the
# user sees. The marker is visible and it is in the file, so a reader can
# see that the rule was considered.
EMOJI_OPT_OUT = "house-style: emoji-ok"

# The documents whose emptiness is a real loss. The community health files
# are boilerplate and are allowed to be short; a README that says nothing is
# not a README.
WRITTEN_DOCUMENTS = frozenset({
    "README.md",
    "AGENTS.md",
    "PRODUCT.md",
    "DESIGN.md",
})

# --------------------------------------------------------------------------
# Findings
# --------------------------------------------------------------------------


class Finding(object):
    """One rule outcome. `hard` findings fail the check."""

    def __init__(self, code, severity, path, message):
        self.code = code
        self.severity = severity
        self.path = path
        self.message = message

    def as_dict(self):
        return {
            "code": self.code,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
        }

    def __repr__(self):
        return "<%s %s %s>" % (self.severity, self.code, self.path)


def hard(code, path, message):
    return Finding(code, "hard", path, message)


def soft(code, path, message):
    return Finding(code, "soft", path, message)


# --------------------------------------------------------------------------
# Repository
# --------------------------------------------------------------------------


class Repo(object):
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self._files = None
        self._cache = {}

    # -- file listing ------------------------------------------------------

    def files(self):
        """Tracked files, relative to the root, sorted."""
        if self._files is None:
            self._files = self._collect_files()
        return self._files

    def _collect_files(self):
        listed = self._git_ls_files()
        if listed is not None:
            return [f for f in listed if not is_vendored(f)]

        found = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, self.root)
                if not rel.startswith(".."):
                    found.append(rel)
        return sorted(found)

    def _git_ls_files(self):
        try:
            out = subprocess.run(
                [
                    "git", "-C", self.root, "ls-files",
                    "-z", "--cached", "--others", "--exclude-standard",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except (OSError, ValueError):
            return None
        if out.returncode != 0:
            return None
        raw = out.stdout.decode("utf-8", "replace")
        entries = [e for e in raw.split("\0") if e]
        if not entries:
            # An empty repository is legal, but so is a git failure. Treat an
            # empty result as "not a git repo" and fall back to the filesystem.
            return None
        return sorted(entries)

    # -- file access -------------------------------------------------------

    def path(self, rel):
        return os.path.join(self.root, rel)

    def exists(self, rel):
        return os.path.exists(self.path(rel))

    def is_dir(self, rel):
        return os.path.isdir(self.path(rel))

    def read(self, rel):
        """Text content of a file, or None if it is missing or binary."""
        if rel in self._cache:
            return self._cache[rel]
        full = self.path(rel)
        content = None
        try:
            with open(full, "rb") as handle:
                raw = handle.read()
            if b"\x00" not in raw:
                content = raw.decode("utf-8", "replace")
        except (IOError, OSError):
            content = None
        self._cache[rel] = content
        return content

    def size(self, rel):
        try:
            return os.path.getsize(self.path(rel))
        except (IOError, OSError):
            return 0

    def is_text(self, rel):
        """A tracked file is text if it has no NUL byte and is not empty of
        content. Binary files are exempt from the style rules, which are
        about prose."""
        if rel in self._cache:
            return self._cache[rel] is not None
        full = self.path(rel)
        try:
            with open(full, "rb") as handle:
                chunk = handle.read(8192)
        except (IOError, OSError):
            return False
        return b"\x00" not in chunk


# --------------------------------------------------------------------------
# Markdown helpers
# --------------------------------------------------------------------------

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REF_DEF_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(\S+)", re.MULTILINE)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_html_comments(text):
    """Remove HTML comments. GitHub does not render them, so a link inside
    one is an example, not a link."""
    return HTML_COMMENT_RE.sub("", text)


def strip_code_blocks(text):
    """Remove fenced code blocks. A link inside a fence is an example, not a
    link, and must not be checked."""
    out = []
    fence = None
    for line in text.split("\n"):
        match = FENCE_RE.match(line)
        if fence is None and match:
            fence = match.group(1)
            out.append("")
            continue
        if fence is not None:
            if line.strip().startswith(fence):
                fence = None
            out.append("")
            continue
        out.append(line)
    return "\n".join(out)


def headings(text):
    """(level, text) for every heading outside a fenced block."""
    result = []
    fence = None
    for line in text.split("\n"):
        match = FENCE_RE.match(line)
        if fence is None and match:
            fence = match.group(1)
            continue
        if fence is not None:
            if line.strip().startswith(fence):
                fence = None
            continue
        heading = HEADING_RE.match(line)
        if heading:
            result.append((len(heading.group(1)), heading.group(2).strip()))
    return result


def normalise_heading(text):
    """Lowercase, punctuation stripped. Used for keyword matching."""
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^\w\s]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def markdown_links(text):
    """(target, is_image) for every inline link and image, plus reference
    definitions."""
    body = strip_html_comments(strip_code_blocks(text))
    links = []
    for match in INLINE_LINK_RE.finditer(body):
        is_image = match.group(1) == "!"
        target = match.group(3)
        links.append((target, is_image))
    for match in REF_DEF_RE.finditer(body):
        links.append((match.group(2), False))
    return links


def is_external(target):
    lowered = target.lower()
    if lowered.startswith("#"):
        return True
    if "://" in lowered:
        return True
    if lowered.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return True
    return False


def resolve_target(target, rel_path, repo):
    """Turn a Markdown target into a path relative to the repository root, or
    None when the target is not ours to check.

    Returns the path, or the string "absolute" for a target that points
    outside the repository (an absolute path on someone's machine, or a
    route into an application), or None when the target is not a file
    reference at all.
    """
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if is_external(target):
        return None

    # Drop the anchor and the query string.
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None

    # GitHub accepts a line number or a range after a colon: `file.py:12`.
    target = re.sub(r":\d+(-\d+)?$", "", target)

    target = target.replace("%20", " ")

    if target.startswith("/"):
        return "absolute"

    base = os.path.dirname(rel_path)
    candidate = os.path.normpath(os.path.join(base, target))

    if candidate.startswith(".."):
        return None
    return candidate


def has_emoji(text):
    for char in text:
        code = ord(char)
        if code in EMOJI_ALLOWED:
            continue
        for low, high in EMOJI_RANGES:
            if low <= code <= high:
                return char
    return None


# --------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------


def check_root_files(repo):
    findings = []
    for rel in REQUIRED_FILES:
        if not repo.exists(rel):
            findings.append(hard("HS001", rel, "%s is missing" % rel))
    return findings


def check_required_dirs(repo):
    findings = []
    for rel in REQUIRED_DIRS:
        if not repo.is_dir(rel):
            findings.append(hard("HS002", rel, "%s/ is missing" % rel))
    return findings


# How much prose a document needs before it counts as written. Measured in
# characters rather than lines: a line is a line, and a short document is
# short rather than hollow.
MIN_PROSE_CHARACTERS = 200


def prose_length(text):
    """The characters of actual prose: not blank, not a heading, not inside
    an HTML comment. This is what separates a written document from a stub."""
    total = 0
    for line in strip_html_comments(text).split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if HEADING_RE.match(stripped):
            continue
        total += len(stripped)
    return total


def check_documents_are_written(repo):
    """A document that no longer carries the template marker has been
    claimed as finished, and it has to be finished.

    The marker is the promise. Leaving it on says "not written yet", which
    is a state and not a failure. Taking it off says "this is the document",
    and a hollow document under that claim is the one thing the standard
    cannot accept.
    """
    findings = []
    for rel in repo.files():
        if not rel.endswith(".md"):
            continue
        if rel not in WRITTEN_DOCUMENTS and not rel.startswith("docs/"):
            continue
        text = repo.read(rel)
        if text is None:
            continue
        if TEMPLATE_MARKER in "\n".join(text.split("\n")[:3]):
            continue  # still a starting point, and HS025 says so
        length = prose_length(text)
        if length < MIN_PROSE_CHARACTERS:
            findings.append(hard(
                "HS026", rel,
                "the template marker is gone but the file holds %d character(s) "
                "of prose; the marker was a promise that this document is "
                "written" % length,
            ))
    return findings


def check_placeholders(repo):
    """A template that was scaffolded but never filled in is not a finished
    repository.

    Two signals: the file still carries the template marker, or it still
    contains an unfilled placeholder. The marker is what makes the check
    precise — a document that merely *mentions* the placeholder syntax in
    prose is not a template.
    """
    findings = []
    for rel in repo.files():
        # The templates directory holds the placeholders on purpose.
        if rel.startswith("templates/"):
            continue
        text = repo.read(rel)
        if text is None:
            continue

        found = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", text)))
        # The marker is only a marker when it is at the top of the file. A
        # document that mentions it in prose — or the checker's own source,
        # which defines the string — is not a template.
        head = "\n".join(text.split("\n")[:3])
        marked = TEMPLATE_MARKER in head

        if marked:
            # The marker says the file has not been written yet. That is a
            # state, not a mistake: the file is a starting point and the
            # owner will write it when they next work on the project. A
            # personal collection would spend all its red builds here.
            findings.append(soft(
                "HS025", rel,
                "this file is still a starting point; it carries the template "
                "marker, and it is not written yet",
            ))
        elif found and rel in PROJECT_DOCUMENTS:
            findings.append(hard(
                "HS025", rel,
                "template placeholders are still unfilled: %s"
                % ", ".join("{{%s}}" % token for token in found),
            ))
    return findings


def check_license(repo):
    findings = []
    if not repo.exists("LICENSE"):
        return findings  # already reported by HS001

    text = repo.read("LICENSE")
    if text is None:
        findings.append(hard("HS003", "LICENSE", "LICENSE is not a readable text file"))
        return findings

    stripped = text.strip()
    if not stripped:
        findings.append(hard("HS003", "LICENSE", "LICENSE is empty"))
        return findings

    head = "\n".join(stripped.split("\n")[:5])
    if not any(marker in head for marker in KNOWN_LICENSES):
        findings.append(hard(
            "HS003", "LICENSE",
            "LICENSE does not look like a standard licence",
        ))

    if not re.search(r"copyright\s*\(?c\)?\s*[\(\[]?\d{4}", text, re.IGNORECASE):
        findings.append(hard(
            "HS004", "LICENSE",
            "LICENSE has no copyright line naming a holder",
        ))
    elif not re.search(r"copyright\s*\(?c\)?[^.\n]*\b(19|20)\d{2}\b", text, re.IGNORECASE):
        findings.append(hard(
            "HS004", "LICENSE",
            "LICENSE copyright line names no year",
        ))

    return findings


def check_ci_workflow(repo):
    findings = []
    if not repo.is_dir(".github/workflows"):
        return findings  # already reported by HS002

    workflows = [
        rel for rel in repo.files()
        if rel.startswith(".github/workflows/") and rel.endswith((".yml", ".yaml"))
    ]
    if not workflows:
        findings.append(hard(
            "HS005", ".github/workflows",
            "no workflow file; CI is required",
        ))
        return findings

    triggers_on_pr = False
    for rel in workflows:
        text = repo.read(rel) or ""
        if re.search(r"^\s*pull_request\s*:", text, re.MULTILINE):
            triggers_on_pr = True
            break
    if not triggers_on_pr:
        findings.append(hard(
            "HS005", ".github/workflows",
            "no workflow triggers on pull_request",
        ))
    return findings


def check_issue_templates(repo):
    findings = []
    if not repo.is_dir(".github/ISSUE_TEMPLATE"):
        return findings  # already reported by HS002

    entries = [
        rel for rel in repo.files()
        if rel.startswith(".github/ISSUE_TEMPLATE/") and not rel.endswith("/")
    ]
    if not entries:
        findings.append(hard(
            "HS006", ".github/ISSUE_TEMPLATE",
            "no issue template; the directory is empty",
        ))
    return findings


def check_file_sizes(repo):
    findings = []
    for rel in repo.files():
        size = repo.size(rel)
        if size > MAX_FILE_BYTES:
            findings.append(hard(
                "HS008", rel,
                "%s is %d bytes; GitHub rejects files above 100 MB" % (rel, size),
            ))
        elif size > WARN_FILE_BYTES:
            findings.append(hard(
                "HS007", rel,
                "%s is %d bytes; use Git LFS or a release asset" % (rel, size),
            ))
    return findings


def check_readme_structure(repo):
    findings = []
    if not repo.exists("README.md"):
        return findings  # already reported by HS001

    text = repo.read("README.md")
    if text is None:
        findings.append(hard("HS010", "README.md", "README.md is not a readable text file"))
        return findings

    # The headings are read from the body, not from the raw text. A "#"
    # comment inside a fenced code block is a comment, and a README that
    # shows a shell script is full of them.
    body = strip_html_comments(strip_code_blocks(text))
    lines = body.split("\n")

    # HS011 — exactly one H1, and it opens the file.
    h1s = [(i + 1, line) for i, line in enumerate(lines)
           if HEADING_RE.match(line) and len(HEADING_RE.match(line).group(1)) == 1]
    if len(h1s) == 0:
        findings.append(hard("HS011", "README.md", "README.md has no level-1 heading"))
    elif len(h1s) > 1:
        findings.append(hard(
            "HS011", "README.md",
            "README.md has %d level-1 headings; it must have exactly one" % len(h1s),
        ))
    else:
        first_content = next(
            (i for i, line in enumerate(lines)
             if line.strip() and not line.strip().startswith("<!--")),
            None,
        )
        if first_content is not None and h1s[0][0] - 1 != first_content:
            findings.append(hard(
                "HS011", "README.md",
                "the level-1 heading is not the first thing in README.md",
            ))

    # HS012 / HS013 — required sections, present and in order.
    all_headings = headings(body)
    level2 = [
        (index, normalise_heading(name))
        for index, (level, name) in enumerate(all_headings)
        if level == 2
    ]

    found_positions = []
    for key, keywords in README_SECTIONS:
        position = None
        for index, name in level2:
            if any(word in name for word in keywords):
                position = index
                break
        if position is None:
            findings.append(hard(
                "HS012", "README.md",
                "README.md has no section about %s" % key,
            ))
        else:
            found_positions.append((key, position))

    if len(found_positions) == len(README_SECTIONS):
        ordered = [pos for _, pos in found_positions]
        if ordered != sorted(ordered):
            findings.append(soft(
                "HS013", "README.md",
                "README.md sections are not in the canonical order: %s"
                % ", ".join(key for key, _ in found_positions),
            ))

    # HS014 — the README says something.
    if len(text.strip()) < 400:
        findings.append(soft(
            "HS014", "README.md",
            "README.md is shorter than 400 characters and cannot hold the "
            "required sections",
        ))

    # HS015 — the README links to the licence.
    links = markdown_links(text)
    points_at_license = False
    for target, is_image in links:
        if is_image:
            continue
        resolved = resolve_target(target, "README.md", repo)
        if resolved and os.path.basename(resolved).upper().startswith("LICENSE"):
            points_at_license = True
            break
    if not points_at_license:
        findings.append(soft(
            "HS015", "README.md",
            "README.md does not link to LICENSE",
        ))

    return findings


def check_product_md(repo):
    findings = []
    if not repo.exists("PRODUCT.md"):
        return findings  # already reported by HS001

    text = repo.read("PRODUCT.md")
    if text is None:
        findings.append(hard("HS020", "PRODUCT.md", "PRODUCT.md is not a readable text file"))
        return findings

    if "impeccable:product-schema" not in text:
        findings.append(hard(
            "HS020", "PRODUCT.md",
            "PRODUCT.md has no <!-- impeccable:product-schema --> marker",
        ))

    present = [normalise_heading(name) for _, name in headings(text)]
    for section in PRODUCT_SECTIONS:
        wanted = normalise_heading(section)
        if wanted not in present:
            findings.append(hard(
                "HS021", "PRODUCT.md",
                "PRODUCT.md has no '%s' section" % section,
            ))

    return findings


def check_design_md(repo):
    findings = []
    if not repo.exists("DESIGN.md"):
        return findings  # already reported by HS001

    text = repo.read("DESIGN.md")
    if text is None:
        findings.append(hard("HS022", "DESIGN.md", "DESIGN.md is not a readable text file"))
        return findings

    frontmatter = ""
    # The frontmatter has to be the first thing in the file, but a leading
    # template marker or comment is allowed above it.
    body = text
    while True:
        stripped = body.lstrip("\n")
        if stripped.startswith("<!--"):
            end = stripped.find("-->")
            if end == -1:
                break
            body = stripped[end + 3:]
            continue
        break
    body = body.lstrip("\n")

    if body.startswith("---"):
        end = body.find("\n---", 3)
        if end == -1:
            findings.append(hard(
                "HS022", "DESIGN.md",
                "the frontmatter block is never closed",
            ))
        else:
            frontmatter = body[3:end]
    else:
        findings.append(hard(
            "HS022", "DESIGN.md",
            "DESIGN.md does not open with a YAML frontmatter block",
        ))

    if frontmatter:
        keys = set()
        for line in frontmatter.split("\n"):
            match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:", line)
            if match:
                keys.add(match.group(1).lower())
        for key in ("name", "description"):
            if key not in keys:
                findings.append(hard(
                    "HS022", "DESIGN.md",
                    "the frontmatter has no '%s' key" % key,
                ))

    present = [normalise_heading(name) for _, name in headings(text)]
    positions = []
    for section in DESIGN_SECTIONS:
        wanted = normalise_heading(section)
        if wanted in present:
            positions.append((section, present.index(wanted)))

    ordered = [pos for _, pos in positions]
    if ordered != sorted(ordered):
        findings.append(hard(
            "HS023", "DESIGN.md",
            "DESIGN.md sections are out of order: %s"
            % ", ".join(section for section, _ in positions),
        ))

    return findings


def check_design_sidecar(repo):
    findings = []
    if not repo.is_dir(".impeccable"):
        return findings  # already reported by HS002

    rel = ".impeccable/design.json"
    if not repo.exists(rel):
        findings.append(hard(
            "HS024", rel,
            "the design sidecar is missing; it carries what the frontmatter cannot",
        ))
        return findings

    text = repo.read(rel)
    if text is None:
        findings.append(hard("HS024", rel, "the design sidecar is not valid UTF-8"))
        return findings
    try:
        data = json.loads(text)
    except ValueError as error:
        findings.append(hard("HS024", rel, "the design sidecar is not valid JSON: %s" % error))
        return findings

    for key in ("schemaVersion", "title"):
        if key not in data:
            findings.append(hard("HS024", rel, "the design sidecar has no '%s' key" % key))

    return findings


def check_links(repo):
    findings = []
    for rel in repo.files():
        if not rel.endswith(".md"):
            continue
        text = repo.read(rel)
        if text is None:
            continue

        for target, is_image in markdown_links(text):
            resolved = resolve_target(target, rel, repo)
            if resolved is None:
                continue
            if resolved == "absolute":
                findings.append(soft(
                    "HS030", rel,
                    "link '%s' points outside the repository and will not "
                    "resolve for anyone else" % target,
                ))
                continue
            if not repo.exists(resolved):
                if is_image:
                    findings.append(hard(
                        "HS031", rel,
                        "image '%s' does not resolve to a file in the repository" % target,
                    ))
                else:
                    findings.append(hard(
                        "HS030", rel,
                        "link '%s' does not resolve to a file in the repository" % target,
                    ))
    return findings


def governs_text(rel):
    """Whether the standard has a say in this file.

    The standard governs the documents it defines and every Markdown file,
    because those are the ones it writes and the ones a visitor reads. The
    product's own source code is the owner's business: a bot's button
    labels, a game's playing cards and a parser's error messages are the
    product, and the standard does not rewrite them.
    """
    if rel.endswith(".md"):
        return True
    if rel.endswith((".markdown", ".mdx")):
        return True
    return rel.startswith((".github/", ".impeccable/")) or rel in (
        "LICENSE", "CHANGELOG.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md",
        "DESIGN.md", "SECURITY.md", "README.md", "AGENTS.md", "PRODUCT.md",
    )


def is_test_path(rel):
    """A test file, where a string is a value rather than prose."""
    if re.search(r"(^|/)(test|tests|spec|specs)/", rel):
        return True
    return bool(re.search(r"(^|/)(test_[^/]*|[^/]*_test|[^/]*\.test|[^/]*\.spec)\.[a-z]+$", rel))


def check_markdown_hygiene(repo):
    findings = []
    for rel in repo.files():
        if not repo.is_text(rel):
            continue

        text = repo.read(rel)
        if text is None:
            continue

        is_markdown = rel.endswith(".md")

        # HS040 — no emoji. The rule is about the documents the standard
        # governs. A product's own source is the owner's: the glyphs in a
        # Telegram bot's button labels are what the user sees, and the
        # standard does not rewrite a product's interface.
        #
        # Two exemptions inside the documents, both explicit. A test file:
        # an emoji inside a test value is data, like a password with a lock
        # glyph in it, and removing it would weaken the test. A file that
        # says so: the emoji are the product, and the file says so in the
        # open.
        head = "\n".join(text.split("\n")[:3])
        exempt = (not governs_text(rel)
                  or is_test_path(rel)
                  or EMOJI_OPT_OUT in head)
        char = None if exempt else has_emoji(text)
        if char is not None:
            line = next(
                (i + 1 for i, l in enumerate(text.split("\n")) if char in l),
                0,
            )
            findings.append(hard(
                "HS040", rel,
                "emoji %r on line %d; the house style bans emoji in every file"
                % (char, line),
            ))

        # HS043 — a trailing newline.
        if text and not text.endswith("\n"):
            findings.append(hard(
                "HS043", rel,
                "the file does not end with a newline",
            ))

        lines = text.split("\n")
        if lines and lines[-1] == "":
            lines = lines[:-1]

        # HS042 — no trailing whitespace. In Markdown exactly two trailing
        # spaces are a hard line break and are allowed.
        whitespace_lines = []
        for number, line in enumerate(lines, start=1):
            if not line:
                continue
            stripped = line.rstrip(" \t")
            trailing = line[len(stripped):]
            if not trailing:
                continue
            if is_markdown and trailing == "  ":
                continue
            whitespace_lines.append(number)
        if whitespace_lines:
            findings.append(hard(
                "HS042", rel,
                "%d line(s) have trailing whitespace, first on line %d"
                % (len(whitespace_lines), whitespace_lines[0]),
            ))

        # HS044 — no tabs indenting a Markdown file.
        if is_markdown:
            tab_lines = [
                number for number, line in enumerate(lines, start=1)
                if line.startswith("\t")
            ]
            if tab_lines:
                findings.append(hard(
                    "HS044", rel,
                    "%d line(s) are indented with a tab, first on line %d"
                    % (len(tab_lines), tab_lines[0]),
                ))

        # HS041 — no skipped heading level.
        previous = 0
        for level, _ in headings(text):
            if previous and level > previous + 1:
                findings.append(hard(
                    "HS041", rel,
                    "a heading jumps from level %d to level %d" % (previous, level),
                ))
            previous = level

    return findings


def check_gitignore(repo):
    if not repo.exists(".gitignore"):
        return []  # already reported by HS001
    text = repo.read(".gitignore")
    if text is None or not text.strip():
        return [soft("HS009", ".gitignore", ".gitignore is empty")]
    return []


def check_agents_md(repo):
    if not repo.exists("AGENTS.md"):
        return []  # already reported by HS001
    text = repo.read("AGENTS.md")
    if text is None or len(text.strip()) < 200:
        return [soft(
            "HS104", "AGENTS.md",
            "AGENTS.md is too short to be a useful re-entry surface",
        )]
    return []


def check_changelog(repo):
    if not repo.exists("CHANGELOG.md"):
        return []  # already reported by HS001
    text = repo.read("CHANGELOG.md")
    if text is None:
        return []
    found = headings(text)
    if not found:
        return [soft("HS103", "CHANGELOG.md", "CHANGELOG.md has no headings")]
    versions = [
        name for _, name in found
        if re.match(r"^\[?\d+\.\d+", name) or re.match(r"^v\d", name, re.IGNORECASE)
    ]
    if not versions:
        return [soft("HS103", "CHANGELOG.md", "CHANGELOG.md has no version heading")]
    return []


def check_docs_index(repo):
    if not repo.is_dir("docs"):
        return []  # already reported by HS002

    rel = "docs/README.md"
    if not repo.exists(rel):
        if repo.exists("docs/index.html"):
            return []  # a landing page is an index too
        return [soft("HS102", "docs/README.md", "docs/ has no index")]

    text = repo.read(rel)
    if text is None:
        return []

    others = [
        other for other in repo.files()
        if other.startswith("docs/") and other != rel and other.endswith(".md")
    ]
    if not others:
        return []
    for other in others:
        base = os.path.basename(other)
        if base in text or other in text:
            return []
    return [soft(
        "HS102", "docs/README.md",
        "docs/README.md links to none of the %d other documents in docs/" % len(others),
    )]


def check_default_branch(repo):
    """The CI has to run on the branch the repository actually uses.

    A filter on `main` is a filter that silently does nothing in a
    repository whose default branch is `master`, and most of the repositories
    in this collection are on master. The name of the branch is the
    repository's business; whether the check runs on it is the standard's.
    """
    try:
        out = subprocess.run(
            ["git", "-C", repo.root, "symbolic-ref", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except (OSError, ValueError):
        return []
    branch = out.stdout.decode("utf-8", "replace").strip()
    if not branch:
        return []

    findings = []
    workflows = [
        rel for rel in repo.files()
        if rel.startswith(".github/workflows/") and rel.endswith((".yml", ".yaml"))
    ]
    for rel in workflows:
        text = repo.read(rel)
        if text is None:
            continue
        # The branch list under `push:`, if there is one. The line break
        # has to be matched explicitly: a greedy \s* eats it, the optional
        # group matches nothing, and the rule never fires.
        match = re.search(
            r"push:[ \t]*\n[ \t]*branches:[ \t]*\[([^\]]*)\]", text
        )
        if not match:
            continue  # no filter: every branch, so the default one is covered
        listed = match.group(1)
        branches = [b.strip().strip("'\"") for b in listed.split(",") if b.strip()]
        if branches and branch not in branches and "**" not in branches:
            findings.append(soft(
                "HS100", rel,
                "the workflow listens for %s, and the default branch is '%s', "
                "so it never runs on it" % (", ".join(branches), branch),
            ))
    return findings


def check_remote(repo, remote):
    """Repository settings that need the GitHub API. Only run with --remote."""
    findings = []
    if not remote:
        return findings

    try:
        out = subprocess.run(
            ["gh", "repo", "view", "--json", "name,description,defaultBranchRef"],
            cwd=repo.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except (OSError, ValueError):
        return [soft("HS101", ".", "could not run gh; skipping the remote checks")]

    if out.returncode != 0:
        return [soft("HS101", ".", "could not read the repository settings over the network")]

    try:
        data = json.loads(out.stdout.decode("utf-8", "replace"))
    except ValueError:
        return [soft("HS101", ".", "could not parse the repository settings")]

    description = (data.get("description") or "").strip()
    name = (data.get("name") or "").strip()
    if not description:
        findings.append(soft("HS101", ".", "the repository description is empty"))
    elif description.lower() == name.lower():
        findings.append(soft("HS101", ".", "the repository description repeats the name"))

    branch = (data.get("defaultBranchRef") or {}).get("name")
    if branch and branch != "main":
        findings.append(soft("HS100", ".", "the default branch is '%s', not 'main'" % branch))

    return findings


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------

ALL_RULES = [
    check_root_files,
    check_required_dirs,
    check_license,
    check_ci_workflow,
    check_issue_templates,
    check_file_sizes,
    check_readme_structure,
    check_product_md,
    check_design_md,
    check_design_sidecar,
    check_documents_are_written,
    check_placeholders,
    check_links,
    check_markdown_hygiene,
    check_gitignore,
    check_agents_md,
    check_changelog,
    check_docs_index,
    check_default_branch,
]


def run(repo, remote=False):
    findings = []
    for rule in ALL_RULES:
        findings.extend(rule(repo))
    if remote:
        findings.extend(check_remote(repo, remote))
    findings.sort(key=lambda f: (f.code, f.path))
    return findings


def report_text(repo, findings):
    hard_failures = [f for f in findings if f.severity == "hard"]
    soft_findings = [f for f in findings if f.severity == "soft"]

    lines = []
    lines.append("%s — house style check" % os.path.basename(repo.root))
    lines.append("")

    if not findings:
        lines.append("ok  no findings")
    else:
        # One rule can fire on every file in a repository. Showing them all
        # buries the other rules, so each rule is capped and the rest are
        # counted.
        by_code = {}
        for finding in findings:
            by_code.setdefault(finding.code, []).append(finding)
        for code in sorted(by_code):
            group = by_code[code]
            for finding in group[:MAX_FINDINGS_PER_RULE]:
                marker = "FAIL" if finding.severity == "hard" else "warn"
                location = finding.path if finding.path != "." else "repository"
                lines.append("%s  %s  %s: %s" % (
                    marker, finding.code, location, finding.message))
            if len(group) > MAX_FINDINGS_PER_RULE:
                lines.append("     %s  ... and %d more" % (code, len(group) - MAX_FINDINGS_PER_RULE))

    lines.append("")
    lines.append("%d hard failure(s), %d soft finding(s)" % (len(hard_failures), len(soft_findings)))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="housecheck",
        description="Check a repository against the house standard.",
    )
    parser.add_argument("path", nargs="?", default=".", help="the repository to check")
    parser.add_argument(
        "--strict", action="store_true",
        help="treat soft findings as failures",
    )
    parser.add_argument(
        "--json", action="store_true", dest="as_json",
        help="print the findings as JSON",
    )
    parser.add_argument(
        "--remote", action="store_true",
        help="also check the repository settings over the GitHub API",
    )
    args = parser.parse_args(argv)

    if not os.path.isdir(args.path):
        sys.stderr.write("housecheck: %s is not a directory\n" % args.path)
        return 2

    repo = Repo(args.path)
    findings = run(repo, remote=args.remote)

    if args.as_json:
        payload = {
            "standard": STANDARD_VERSION,
            "repository": repo.root,
            "findings": [f.as_dict() for f in findings],
            "hard": len([f for f in findings if f.severity == "hard"]),
            "soft": len([f for f in findings if f.severity == "soft"]),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(report_text(repo, findings))

    hard_failures = [f for f in findings if f.severity == "hard"]
    if hard_failures:
        return 1
    if args.strict and [f for f in findings if f.severity == "soft"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
