# Migration

How to bring an existing repository to the standard without breaking it.

The order of the sections matters: read the first one, then the second, and
only then run the tools.

## The principle

**The migrator adds what is missing and overwrites nothing.**

A repository that has been running for a year has opinions its owner never
wrote down. The migration does not get to decide those opinions. It installs
the scaffolding around them and leaves the content alone.

This is why `adopt.sh` is not a formatter and not a rewrite. It is a
copier with a short list of files that are always safe to add.

The exception: two files cannot be added safely, because their content is
product truth and the migrator cannot invent it.

- `PRODUCT.md` — who it is for, what it promises, what is real.
- `DESIGN.md` — the visual system.

For those, `adopt.sh` writes a **stub**: the right headings, with the
questions to answer written inline. The stub fails the checker until it is
filled in, which is correct — an unfilled `PRODUCT.md` is not a product
record.

Every file that comes from a template carries a marker in its first line:

```html
<!-- house-style: template — fill this file in, then delete this line -->
```

The marker is how the checker knows a file is still a template (HS025). It is
a comment, so it costs nothing in the rendered document. Delete it as the
last step of filling the file in, and the checker stops asking.

## Before you start

1. **Make sure the repository is clean.** `git status` should be empty. The
   migrator refuses to run otherwise, because it does not know how to merge
   its changes with yours.
2. **Push your work.** The migration is one commit. It should be revertable
   with `git revert`, not with archaeology.
3. **Read the audit for this repository.** `scripts/housecheck.py` tells you
   what is missing. The migration fixes the mechanical parts; the rest is
   writing.

## Step one — apply the standard

```bash
cd ~/code/some-project
../golden-repo/scripts/adopt.sh .
```

What it does:

- Copies the missing standard files from `templates/`, substituting
  `{{PROJECT_NAME}}` and the other tokens.
- Creates `.github/`, `docs/`, `scripts/`, `src/`, `tests/` if they are
  missing. Existing directories are left alone.
- Writes `PRODUCT.md` and `DESIGN.md` as stubs **only if they do not exist**.
- Never touches a file that is already there. If `README.md` exists, it is
  not modified — not even a byte.
- Never touches the code.

What it prints is a list of what it created and what it left alone, and a
pointer to the checker.

## Step two — see what is left

```bash
../golden-repo/scripts/housecheck.py .
```

The output is a list of findings, each with a stable code, a path and what to
do about it. Most of the remaining work is of three kinds.

**Fix the links.** HS030 and HS031. A link that pointed at a file that has
since been renamed, and an image that was deleted. These are mechanical, and
there are usually a handful.

**Fill in the stubs.** `PRODUCT.md` and `DESIGN.md` if they were created.
This is the real work, and it is writing, not administration. Write what is
true; leave a question open rather than inventing an answer.

**Decide about the README.** HS012 and HS013 want the four required sections
in a fixed order. If your README has all of them in a different order, there
are two options:

- Reorder them. Usually right, and it takes ten minutes.
- Keep the order and note the exception in the repository's `AGENTS.md`.

The second option is legitimate. The first is usually better.

## Step three — enable the check in CI

Copy the house-style workflow into the repository:

```bash
mkdir -p .github/workflows
cp ../golden-repo/templates/.github/workflows/house-style.yml .github/workflows/
```

The template's workflow checks out the golden repository and runs the
checker from there, so the standard can be improved in one place and every
repository picks the change up. A repository that prefers a vendored copy can
copy `scripts/housecheck.py` instead; it then has to be updated by hand.

The workflow is a hard gate. Every repository that adopts the standard is
expected to run it on every pull request, because a standard nobody enforces
is a convention, and conventions decay.

## Step four — check the repository settings

The checker cannot see these, and they are part of the standard:

- **Description.** Not empty, and not the repository name. It is what appears
  in search results and in `gh repo list`.
  `gh repo edit <name> --description "..."`
- **Default branch.** `main`.
  `gh api -X PATCH repos/<owner>/<name> -f default_branch=main`
- **Topics.** Three to five words that say what it is. They are how a
  repository is found by people who do not know it exists.
  `gh repo edit <name> --add-topic "..."`
- **Security features.** Dependabot alerts, secret scanning, push protection
  and code scanning are free on public repositories and are on by default;
  confirm they are enabled.

## What is deliberately not migrated

**The code.** Nothing about the code changes. A migration that reformats
source is a migration that produces a large diff, and a large diff is a diff
nobody reviews.

**The README's voice.** `adopt.sh` will not rewrite a README that already
exists. Rewriting somebody's writing to match a tone guide produces a worse
README than the original, and it removes the owner's voice from the thing
that is supposed to carry it.

**The stack.** No `package.json`, no `pyproject.toml`, no `go.mod`. The
standard does not know what your project is built with, and a wrong guess is
worse than none.

**Private and archived repositories.** `adopt.sh` works on them, but there is
no reason to spend the effort on a repository that is archived or is a
throwaway test sandbox. The audit in [`audit.md`](audit.md) marks which
repositories are worth the effort.

## The order to do the work in

If the standard has to be applied to a large body of repositories, it is worth
doing it in this order:

1. **The ones people actually visit.** The repositories with stars, the ones
   linked from a profile, the ones a colleague has mentioned. A visitor's
   first impression is made by these.
2. **The ones that are actively worked on.** A standard applied to a project
   under development is adopted rather than endured, because the author is
   there to notice when it is wrong.
3. **The rest that are public.** Same work, lower stakes.
4. **The private ones**, if there is a reason to.
5. **The throwaways.** Test sandboxes, archived forks, and repositories that
   exist only to hold an experiment. These are exempt, and the standard says
   so: a rule that cannot be applied everywhere is not a rule.

The audit in [`audit.md`](audit.md) has the current classification.
