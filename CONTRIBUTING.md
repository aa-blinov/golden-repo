# Contributing

This repository is the house standard. Contributions that change the standard
change every repository that follows it, so the bar for a change is higher than
it looks.

Read [AGENTS.md](AGENTS.md) first: it describes how the three layers of this
standard — the prose, the checker and the templates — are meant to stay in
agreement.

## What a change to the standard involves

A rule is not a rule until something fails because of it. Every change to the
standard therefore touches three places:

1. **`docs/house-style.md`** — the rule, its rationale, and a passing and a
   failing example.
2. **`scripts/housecheck.py`** — the implementation, with a stable rule code
   that is never renumbered.
3. **`tests/test_housecheck.py`** — a test that fails without the change and
   passes with it.

If a change touches the canonical file set, it also touches:

4. **`templates/`** — the placeholder that ships to new projects.
5. **`docs/structure.md`** — the annotated tree.

## House rules for the pull request

- One concern per pull request. A new rule and a reworded paragraph are two
  pull requests.
- Every rule gets a stable code (`HS###`). Codes are never reused or
  renumbered, so that an audit report from last year still reads correctly.
- The golden repository must pass `scripts/housecheck.py --strict .` after
  your change. If it cannot, either the rule is wrong or the golden repository
  is not a valid example. Both are worth a conversation before the change
  lands.
- A rule that cannot be checked goes in `docs/writing.md` as a preference, not
  into the checker.
- Do not weaken a rule to make a repository pass. If a rule is genuinely
  wrong, change it deliberately, with a test, and note it in the changelog.
- No emojis, in any file. The checker will fail the build.

## Running the checks

```bash
scripts/housecheck.py --strict .
python3 -m unittest discover -s tests -v
```

Both must be green before you open a pull request.

## Commit messages

```
standard: add a rule for <what it covers>

<why the rule exists, and what it costs to follow>

Rule code: HS###
```

The subject is short and describes the effect on the standard, not the
mechanism. The body explains the reason — a rule the reader does not
understand is a rule the reader will work around.

## Changing the canonical file set

Adding a required file to every repository is a breaking change for the
standard, no matter how small the file is. It means:

- the version number goes up,
- the changelog says which repositories are affected and what to do,
- `adopt.sh` is updated in the same pull request, so that the migration path
  exists before the rule does.

A rule that cannot be applied to an existing repository by tooling is not
ready to be made mandatory.
