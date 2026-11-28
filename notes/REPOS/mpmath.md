## short
not stated; disclosed AI accepted
## quote
> No written AI policy (no CONTRIBUTING file at master). The maintainer reviewed our disclosed AI PRs on the merits.
> [ours:mpmath#1244]
## ours
<!--n:obs.t.by_repo.mpmath_mpmath.landed--><!--/n--> landed (<!--n:obs.prs.mpmath_mpmath.landed--><!--/n-->), <!--n:obs.t.by_repo.mpmath_mpmath.open--><!--/n--> open (<!--n:obs.prs.mpmath_mpmath.open--><!--/n-->). Review came within hours.
## process
- Reviewer: unknown from the docs. No CODEOWNERS file; on mpmath#1241 the maintainer commented unasked within hours and later put a review request on himself. (observed: mpmath#1241)
- Easy to miss: nothing found beyond green CI. mpmath#1241 has all checks green and no merge conflict and waits on the maintainer. (observed: mpmath#1241)
## rounds
One fast round per PR, all asks in one pass: where the fix belongs (`format_digits()` should return the prefix), and which existing test function each assertion belongs in. On mpmath#1241 the whole review was "CI fails."
## do
- Do: extend the maintainer's existing mechanism; he often wrote it and names the lines to reuse.
- Do: put assertions in the existing `test_<format>` function.
- Do: run `pytest` both with and without gmpy before asking; link every issue the PR also fixes.
- Don't: patch the caller when the callee owns the behaviour.
