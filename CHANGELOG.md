# Changelog

All notable changes to the house standard. Versions are ordered newest first.

Entries describe what changed and why it was worth changing. The rules
themselves live in [docs/house-style.md](docs/house-style.md); this file
records the changes to the standard, not the standard.

The standard has a version number. Repositories that adopt it record which
version they follow in their own `AGENTS.md`, so that a rule change is
traceable to a point in time.

## 1.0.0 — 2026-10-20

### Added

- The canonical root file set: `README.md`, `AGENTS.md`, `PRODUCT.md`,
  `DESIGN.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, `LICENSE`, `.editorconfig`, `.gitignore`.
- The canonical directory set: `.github/workflows/`,
  `.github/ISSUE_TEMPLATE/`, `.impeccable/`, `docs/`, `scripts/`, `src/`,
  `tests/`.
- `scripts/housecheck.py` — the checker. Plain Python 3, no dependencies.
  Reports a stable code per rule, exits non-zero on a hard failure, and
  supports `--strict` and `--json`.
- `scripts/new-repo.sh` — scaffolds a new project from `templates/`.
- `scripts/adopt.sh` — brings an existing repository up to the standard
  without overwriting any file the owner has already written.
- `templates/` — placeholder files for every per-project document.
- `docs/house-style.md`, `docs/structure.md`, `docs/writing.md`,
  `docs/migration.md`, `docs/audit.md`.
- GitHub Actions workflows: `ci.yml`, `release.yml`, `house-style.yml`.

### Notes

The rules were extracted from the repositories that already read as one
author's work — `lazy-to-text`, `cast`, `puuush`, `petzy`, `monos`, `koloda`,
`better-ssh`, `templates-mcp` — rather than imported from an external
template. Every rule in `docs/house-style.md` names the observation it came
from.
