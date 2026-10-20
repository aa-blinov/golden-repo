# Screenshots

Images referenced from the README and the documents.

For the golden repository itself there are no screenshots: the repository is
a set of documents and a script, and a picture of a terminal would say less
than the text does.

A project that has an interface puts its images here and references them
from the README:

```markdown
![The main window](docs/screenshots/main.png)
```

Images are referenced by relative path, so they resolve both on GitHub and in
a local checkout. The house-style checker verifies that every image
reference points at a file that exists — HS031 — so a renamed screenshot
cannot quietly break the README.
