# Security Policy

## Supported versions

The standard is a set of documents and a script, not a runtime dependency. The
security surface is small: the checker reads files in a repository, and the
scaffolder and migrator write files.

| Version | Supported |
| --- | --- |
| 1.x | Yes |

## Reporting a vulnerability

Report a vulnerability privately to the maintainer through GitHub's
[private vulnerability reporting][private-reporting] on this repository, or
through the address in the repository owner's profile.

Please include:

- what the problem is, and which file or command is involved,
- how to reproduce it,
- the impact you expect.

You should get an acknowledgement within a few days. If the report is valid,
a fix and a release follow; if it is not, you will be told why.

[private-reporting]: https://github.com/aa-blinov/golden-repo/security/advisories/new

## What counts as a vulnerability here

The checker runs in CI on repositories that adopt it, usually with write
access to the repository it is checking. Two classes of problem matter:

- **Path traversal.** A crafted repository whose file names cause the checker
  or the migrator to read or write outside the repository directory.
- **Command injection.** A crafted file whose name or contents are passed to a
  shell without being quoted.

A bug that makes the checker report the wrong finding is a bug, and worth
reporting, but it is not a security issue unless it can be turned into one of
the two above.

## What is not a vulnerability

- The checker finding a rule violation that you disagree with. That is a
  change request against the standard, not a security report.
- A repository that the standard flags incorrectly, with no way to influence
  what the checker executes.
- Missing hardening that has no exploit path.
