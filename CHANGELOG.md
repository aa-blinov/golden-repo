# Changelog

All notable changes to the house standard. Versions are ordered newest first.

Entries describe what changed and why it was worth changing. The rules
themselves live in [docs/house-style.md](docs/house-style.md). This file
records the changes to the standard.

The standard has a version number. A repository that adopts it records the
version it follows in its own workflow file, where the checker is referenced:

```yaml
- uses: aa-blinov/golden-repo/.github/actions/house-style@v1.0.0
```

Dependabot reads that reference as a dependency, but it does not propose a
bump for a standard published in the same repository as its own tooling. The
bump workflow in this repository does it instead: `scripts/bump.py` opens the
pull request that moves the pin, so a rule change is traceable to a point in
time and arrives as a reviewable diff rather than as a red build.

## 1.0.0 — 2026-10-20

### Added

- The canonical root file set: `README.md`, `AGENTS.md`, `PRODUCT.md`,
  `DESIGN.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, `LICENSE`, `.editorconfig`, `.gitignore`.
- The canonical directory set: `.github/workflows/`,
  `.github/ISSUE_TEMPLATE/`, `.impeccable/`, `docs/`, `scripts/`, `src/`,
  `tests/`.
- The checker, `scripts/housecheck.py`. Plain Python 3, no dependencies.
  Reports a stable code per rule, exits non-zero on a hard failure, and
  supports `--strict` and `--json`.
- The scaffolder, `scripts/new-repo.sh`, which starts a new project from
  `templates/`.
- The migrator, `scripts/adopt.sh`, which brings an existing repository up to
  the standard without overwriting any file the owner has already written.
- Placeholder files for every per-project document, in `templates/`.
- The guides: `docs/house-style.md`, `docs/structure.md`, `docs/writing.md`,
  `docs/migration.md`, `docs/audit.md`.
- GitHub Actions workflows: `ci.yml`, `release.yml`, `house-style.yml`.
- The checker as a composite action, `.github/actions/house-style`, so a
  repository depends on the standard at a pinned version instead of copying
  it.
- `scripts/bump.py` and the `bump` workflow, which open the pull request that
  moves the pin in every repository listed in `adopters.json`.

### Notes

The rules were extracted from the repositories that already read as one
author's work, rather than imported from an external template: `lazy-to-text`,
`cast`, `puuush`, `petzy`, `monos`, `koloda`, `better-ssh`, `templates-mcp`.
Every rule in `docs/house-style.md` names the observation it came from.
