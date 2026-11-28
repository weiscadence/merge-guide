# mpmath

`mpmath/mpmath` · profile: `merge-kit/repos/mpmath__mpmath.yaml`

## AI policy

> No written AI policy (no CONTRIBUTING file at master). The maintainer reviewed our disclosed AI PRs on the merits.
> [ours:mpmath#1244]

- **Stance:** no written policy (CONTRIBUTING.rst 404 at master)
- **Who may write PR text and replies:** not stated; maintainer accepted disclosed AI PRs (mpmath#1244)
- **Disclosure:** disclose (our practice)
- Source: gh api contents/CONTRIBUTING.rst -> 404 (2026-11-25); STATE-OF-THE-FIELD.md policy table

## Ready signal

CI green; non-draft (source: mpmath#1241 ('CI fails.'))

Open-PR cap: no written cap; our default 2 (source: none found)

## CI to run locally

```sh
pip install --upgrade .[ci]
pytest
./mpmath/tests/test_version_frozen.sh
(also run with gmpy2 uninstalled: pip uninstall -y gmpy2 python-gmp; pytest)
```
Source: .github/workflows/test.yml lines 28, 64-72

## PR body skeleton

```
Closes #<issue>

<Root cause and where it was fixed (inside the existing mechanism).>
```

## What reviewers here actually ask for (our data)

Review style: human maintainer, fast

| class | asks / threads in our data |
|---|---|
| tests | <!--n:profile.mpmath.tests-->2<!--/n--> |
| ci | <!--n:profile.mpmath.ci-->1<!--/n--> |
| root-cause | <!--n:profile.mpmath.root_cause-->1<!--/n--> |

Source: FAILURE-MODES.md (review-harvest counts), general classes (mpmath#1244 x2 tests, #1241 CI)

## Our PRs here

<!--n:obs.t.by_repo.mpmath_mpmath.landed-->2<!--/n--> landed (<!--n:obs.prs.mpmath_mpmath.landed-->mpmath#1244, #1246<!--/n-->), <!--n:obs.t.by_repo.mpmath_mpmath.open-->1<!--/n--> open (<!--n:obs.prs.mpmath_mpmath.open-->mpmath#1241<!--/n-->). Review came within hours.

## Typical rounds

One fast round per PR, all asks in one pass: where the fix belongs (`format_digits()` should return the prefix), and which existing test function each assertion belongs in. On mpmath#1241 the whole review was "CI fails."

## Do / don't

- Do: extend the maintainer's existing mechanism; he often wrote it and names the lines to reuse.
- Do: put assertions in the existing `test_<format>` function.
- Do: run `pytest` both with and without gmpy before asking; link every issue the PR also fixes.
- Don't: patch the caller when the callee owns the behaviour.
