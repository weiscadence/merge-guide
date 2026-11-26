# merge-kit validation (2026-11-25)

Ground truth, split and LLM numbers: rubric-prereview v2 (`rubric-prereview/v2/gt_v3.json`,
`split.py`, `judged-*.json`). Same n: test 15 asks / 7 PRs, dev 35 asks / 14 PRs (8486 and 1256
dropped as in v2). Unit = one first-round rubric comment (may hold several sub-asks; a match on
any sub-ask counts, as in v2). Judged by hand (`judgements.json`, a reason for every ask).
Reproduce: `python3 validate/fetch_bodies.py && python3 validate/validate.py run && python3 validate/validate.py score`.

| split | n | deterministic strict | lenient | precision (ask+maybe) | precision (ask only) | v2 sol/opus | v2 gemini | union sol + checks | union gemini + checks |
|---|---|---|---|---|---|---|---|---|---|
| dev | 35 | **5/35** | 9/35 | 16/256 | 5/80 | 3/35 | 8/35 | **8/35** | **12/35** |
| test | 15 | 13/15 | 13/15 | 17/106 | 7/48 | 5/15 | 7/15 | 14/15 | 14/15 |

## Read the dev row, not the test row
- **The test split is contaminated for merge-kit.** The brief sent me to v2's report and I printed
  the 15 test asks before writing any check; four fixtures mirror test asks (1202 L2Product sibling,
  8954 tensorProduct_mk_injective, 19002 minpoly ℚ, 44204 golden-ratio import), and the exact-statement
  `have` matcher and the class-namespace name tokens were added after looking at 19002/8954 misses.
  13/15 measures "the rules reproduce the cases they were written from", not generalisation.
- Dev ask texts were not read while writing the rules (only review-lessons' aggregated summaries).
  They were read for judging, after the configuration was frozen; nothing was tuned afterwards.
- n = 35: 5/35 strict is a 95% Wilson interval of 6%–29%.

## Where it hits (dev, strict)
45756 private list lemmas → export/move (api-design + placement, the P5 rule), 45763 analytic lemmas
in `Polynomial` (naming N6), 8955 missing `Roadmap:` line and 45797 missing `Quality pass:` block
(PR-body rules, from the ORIGINAL body version recovered through GraphQL edit history).
Lenient (right declaration, wrong replacement): 1283, 1850 and 8953 reuse; 1334 proof-quality.

## Per class (dev strict / lenient)
reuse 0/4 / 3/4; placement 1/2; naming 1/5; documentation 0/6; api-design 1/6; generality 0/5;
proof-quality 0/2 / 1/2; attribution 1/1; quality-pass 1/1; scope 0/1; correctness 0/2.

## Precision
Low by design of the `maybe` tier: 256 dev findings for 35 asks across 14 PRs (7.3 per ask, 18.3 per PR). Only 5 of 80 `ask`
findings match a real first-round ask. Caveat: GT is "what the bot asked in round 1"; a finding the
bot did not ask for is not necessarily wrong (e.g. 8954 `isBaseChange_rationalificationMap` vs
Mathlib `TensorProduct.isBaseChange`, flagged here, matches a maintainer's later block). Not scored.

## Leakage controls
- Index = current local Mathlib + TauCeti (laguerre worktree, 815k decls). TauCeti candidates are kept
  only if their name already occurs in that file at the PR's merge base (`git show <base>:<file>`):
  this removed the PR's own later-merged `minpoly.natDegree_inv` (19002), which had produced a fake hit.
- Placement sibling/import rules read the tree at the merge base (`git ls-tree <base>`).
- Mathlib is the current pin, not the PR-time pin (residual leak, probably small).
