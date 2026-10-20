#!/usr/bin/env python3
"""anti_ai — the humanizer's patterns, as a linter.

    scripts/anti_ai.py <file> [<file> ...]
    scripts/anti_ai.py --dir <path>

The humanizer is a list of writing patterns: the constructions a model reaches
for because they are the most likely next words, rather than because the
sentence wants them. Most of them are cheap to detect, and detecting them
mechanically is what makes it possible to run the same check over sixty-five
repositories.

What this cannot do is judge the prose. It reports the patterns; a reader
decides whether the sentence wanted them. A line in a quotation, a title, or
a passage about the pattern itself is not a finding, and the report says
where it is so that a reader can skip it.

The rule numbers are the humanizer's own sections, so a finding can be looked
up.
"""

import argparse
import json
import os
import re
import sys

# Each pattern is (section, name, regex, severity). The severity is a hint
# for the reader: "strong" means the pattern justifies an edit on one
# sighting, "weak" means it needs company from another pattern.
PATTERNS = [
    # 1. Not X but Y
    (1, "not just X but Y", r"\bnot (?:just|only|merely)\b[^.!?\n]{0,80}\bbut\b", "strong"),
    (1, "it's not X, it's Y", r"\b(?:it'?s|that'?s|this is) not [^.!?\n]{2,60}, (?:it'?s|that'?s|this is)\b", "strong"),
    (1, "not X but Y, split", r"\bdoes not mean\b[^.!?\n]{0,60}\.\s*(?:It|That|This) means\b", "strong"),
    (1, "not a X, it is a Y", r"\bis not an? \w+[^.!?\n]{0,40}, it is an?\b", "strong"),

    # 2. One-line closers
    (2, "one-line closer", r"^(?:That is the real win|That distinction matters|Read that again|Let that sink in)\.?$", "strong"),
    (2, "fragment row", r"^(?:No [\w' ]+\. ){2,}$", "weak"),

    # 3. Sayings that sound deep
    (3, "the real question is", r"\bthe real (?:question|issue|point) is\b", "strong"),
    (3, "at its core", r"\bat (?:its|their) core\b", "strong"),
    (3, "what really matters", r"\bwhat really matters\b", "strong"),
    (3, "the deeper issue", r"\bthe deeper (?:issue|question)\b", "strong"),
    (3, "the heart of the matter", r"\bthe heart of the matter\b", "strong"),
    (3, "X is the Y of Z", r"\bis the \w+ of \w+\b", "weak"),
    (3, "becomes a trap", r"\bbecomes? a trap\b", "strong"),
    (3, "not a tool but a mirror", r"\bnot a tool but a mirror\b", "strong"),
    (3, "the language/architecture/currency of", r"\bthe (?:language|architecture|currency|grammar) of\b", "strong"),

    # 4. Staged run-up
    (4, "let's dive in", r"(?i)^\s*(?:let'?s|lets)\s+(?:dive|explore|look|break|dig|go)\b", "strong"),
    (4, "here's what you need to know", r"(?i)\bhere'?s what you need to know\b", "strong"),
    (4, "now let's look at", r"(?i)^\s*now,? let'?s look\b", "strong"),
    (4, "without further ado", r"(?i)\bwithout further ado\b", "strong"),
    (4, "heads up", r"(?i)^\s*heads up[,:]?", "strong"),
    (4, "quick note", r"(?i)^\s*quick note[,:]?", "strong"),
    (4, "honestly?", r"(?i)\bhonestly\?", "strong"),
    (4, "here's the thing", r"(?i)\bhere'?s the thing\b", "strong"),
    (4, "let's be honest", r"(?i)\blet'?s be honest\b", "strong"),

    # 5. Arguing with no one
    (5, "this isn't mainly about", r"(?i)^\s*this isn'?t (?:mainly |just |about )", "strong"),
    (5, "I'm not saying", r"(?i)\bI'?m not saying\b", "strong"),
    (5, "to be clear", r"(?i)\bto be clear\b", "strong"),
    (5, "don't get me wrong", r"(?i)\bdon'?t get me wrong\b", "strong"),
    (5, "this is not to say", r"(?i)\bthis is not to say\b", "strong"),
    (5, "a tempting approach would be", r"(?i)\ba tempting approach would be\b", "strong"),
    (5, "one might be tempted to", r"(?i)\bone might be tempted to\b", "strong"),
    (5, "an obvious approach would be", r"(?i)\ban obvious approach would be\b", "strong"),
    (5, "it would be easy to just", r"(?i)\bit would be easy to (?:just )?", "strong"),

    # 9. Stacked qualifiers
    (9, "stacked qualifiers", r"(?i)\b(?:to be fair|it'?s also possible|could potentially|might arguably|this is an inference)\b", "weak"),

    # 10. Hyphenated pairs after the noun
    (10, "hyphenated pair after noun", r"\b(?:the|a|an|this|that|every|each)\s+[\w-]+-(?:quality|known|documented|term|time|ready)\b", "weak"),

    # 12. Overused words
    (12, "actually", r"(?i)\bactually\b", "weak"),
    (12, "additionally", r"(?i)\badditionally\b", "weak"),
    (12, "bolstered", r"(?i)\bbolstered\b", "weak"),
    (12, "crucial", r"(?i)\bcrucial\b", "weak"),
    (12, "deep dive", r"(?i)\bdeep dive\b", "strong"),
    (12, "delve", r"(?i)\bdelve[sd]?\b", "strong"),
    (12, "enduring", r"(?i)\benduring\b", "weak"),
    (12, "enhance", r"(?i)\benhance[sd]?\b", "weak"),
    (12, "garner", r"(?i)\bgarner(?:ed|s)?\b", "weak"),
    (12, "interplay", r"(?i)\binterplay\b", "weak"),
    (12, "intricate", r"(?i)\bintricat(?:e|es|ed|ely)\b", "weak"),
    (12, "meticulous", r"(?i)\bmeticulous(?:ly)?\b", "weak"),
    (12, "pivotal", r"(?i)\bpivotal\b", "weak"),
    (12, "showcase", r"(?i)\bshowcas(?:e|es|ed|ing)\b", "weak"),
    (12, "tapestry", r"(?i)\btapestry\b", "weak"),
    (12, "testament", r"(?i)\btestament\b", "weak"),
    (12, "underscore", r"(?i)\bunderscor(?:e|es|ed|ing)\b", "weak"),
    (12, "vibrant", r"(?i)\bvibrant\b", "weak"),

    # 13. Inflated significance
    (13, "inflated significance", r"(?i)\b(?:stands as a testament|a pivotal moment|plays a key role|marking or shaping|underscores its importance|reflects a broader|setting the stage for|evolving landscape|continues to thrive|exciting times ahead|the future looks bright)\b", "strong"),

    # 14. Vague connection
    (14, "vague connection", r"(?i)\b(?:associated with|in association with|in connection with|linked to|tied to)\b", "weak"),

    # 15. Shallow -ing riders
    (15, "shallow -ing rider", r"(?i),\s*(?:highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|contributing to|cultivating|fostering|encompassing|showcasing)\b", "strong"),

    # 16. Sales language
    (16, "sales language", r"(?i)\b(?:nestled in the heart of|groundbreaking|natural beauty|diverse array|must-visit|breathtaking|stunning|renowned)\b", "strong"),
    (16, "commitment to", r"(?i)\bcommitment to\b", "weak"),

    # 17. Borrowed authority
    (17, "borrowed authority", r"(?i)\b(?:experts argue|observers have cited|industry reports|some critics|several publications|trade publications|independent coverage|active social media presence)\b", "strong"),

    # 18. Avoiding is, are and has
    (18, "serves as", r"(?i)\bserves as\b", "weak"),
    (18, "stands as", r"(?i)\bstands as\b", "weak"),
    (18, "functions as", r"(?i)\bfunctions as\b", "weak"),
    (18, "boasts", r"(?i)\bboasts\b", "weak"),
    (18, "features, offers, maintains", r"(?i)\b(?:features|offers|maintains|refers to)\b", "weak"),

    # 22. Chatbot residue
    (22, "chatbot residue", r"(?i)\b(?:I hope this helps|Of course!|Certainly!|Great question!|You're absolutely right|Would you like|Want me to|Should I continue|let me know|here is a)\b", "strong"),

    # 23. Knowledge-limit disclaimers
    (23, "knowledge-limit disclaimer", r"(?i)\b(?:as of \w+ \d{4}|up to my last training update|not publicly available|not widely documented|maintains a low profile|it is believed that|likely (?:grew up|studied|began))\b", "strong"),

    # 25. Writing about the document
    (25, "writing about the document", r"(?i)\b(?:the table below compares|this section is organized by|was added to replace|generated from|compiled from|anything unconfirmed is flagged)\b", "strong"),
    (25, "the list below", r"(?i)\bthe (?:list|table|figure) below\b", "weak"),
]

COMPILED = [
    (section, name, re.compile(pattern, re.MULTILINE), severity)
    for section, name, pattern, severity in PATTERNS
]

# The dashes, counted rather than matched.
DASH_RE = re.compile(r"[—–]")
MAX_DASHES_PER_1000 = 3.0

# A heading in title case, with more than one capitalised word.
TITLE_CASE_RE = re.compile(r"^#{1,6}\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+")


# The canonical section names. They are title case on purpose, because a
# schema fixes them, and a linter that flags them would be flagging the
# standard itself.
def canonical_headings():
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "standard.json",
    )
    names = set()
    try:
        with open(path) as handle:
            manifest = json.load(handle)
    except (IOError, OSError, ValueError):
        return names
    for key in ("product", "design"):
        for entry in manifest.get(key, {}).get("sections", []):
            names.add(entry["label"].lower())
    return names


CANONICAL = canonical_headings()


def findings_in(text, path):
    found = []
    for number, line in enumerate(text.split("\n"), start=1):
        if line.strip().startswith("```"):
            continue
        for section, name, pattern, severity in COMPILED:
            if pattern.search(line):
                found.append((number, section, name, severity, line.strip()[:90]))

    words = max(1, len(text.split()))
    dashes = len(DASH_RE.findall(text))
    rate = dashes * 1000.0 / words
    if rate > MAX_DASHES_PER_1000:
        found.append((
            0, 8, "dashes at %.1f per 1000 words" % rate, "strong",
            "the sample this house follows runs at under 1",
        ))

    for number, line in enumerate(text.split("\n"), start=1):
        if TITLE_CASE_RE.match(line):
            heading = line.lstrip("#").strip().lower()
            if heading in CANONICAL:
                continue
            found.append((
                number, 20, "heading in title case", "weak", line.strip()[:90],
            ))
    return found


def check_file(path):
    try:
        with open(path, "r", errors="replace") as handle:
            text = handle.read()
    except (IOError, OSError) as error:
        print("%s: cannot read: %s" % (path, error))
        return 1

    found = findings_in(text, path)
    if not found:
        return 0
    print("%s" % path)
    for number, section, name, severity, line in found:
        where = "line %d" % number if number else "whole file"
        print("  %-5s %-3d %-34s %s" % (severity, section, name, where))
    print("")
    return len(found)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="anti_ai")
    parser.add_argument("files", nargs="*")
    parser.add_argument("--dir", help="check every Markdown file under this path")
    parser.add_argument("--quiet", action="store_true", help="only the count")
    args = parser.parse_args(argv)

    paths = list(args.files)
    if args.dir:
        for dirpath, dirnames, filenames in os.walk(args.dir):
            dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
            for name in filenames:
                if name.endswith(".md"):
                    paths.append(os.path.join(dirpath, name))

    if not paths:
        parser.error("no files to check")

    total = 0
    for path in sorted(paths):
        total += check_file(path)

    print("anti_ai: %d finding(s) in %d file(s)" % (total, len(paths)))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
