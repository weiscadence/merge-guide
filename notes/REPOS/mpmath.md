## short
not stated; disclosed AI accepted
## quote
> No written AI policy (no CONTRIBUTING file at master). The maintainer reviewed our disclosed AI PRs on the merits.
> [ours:mpmath#1244]
## ours
<!--n:obs.t.by_repo.mpmath_mpmath.open--><!--/n--> open (mpmath#1241, #1244). Review came within hours.
## rounds
One fast round per PR, all asks in one pass: where the fix belongs (`format_digits()` should return the prefix), and which existing test function each assertion belongs in. On mpmath#1241 the whole review was "CI fails."
## do
- Do: extend the maintainer's existing mechanism; he often wrote it and names the lines to reuse.
- Do: put assertions in the existing `test_<format>` function.
- Do: run `pytest` both with and without gmpy before asking; link every issue the PR also fixes.
- Don't: patch the caller when the callee owns the behaviour.
