# Failure modes: what agents get wrong, ranked

Data as of <!--asof-->2026-11-28<!--/asof-->. Two counts per mode:
- **TauCeti threads**: distinct PR × rubric threads on our <!--n:obs.reviewer_prs-->32<!--/n--> rubric-reviewed
  TauCeti PRs (<!--n:obs.threads_total-->153<!--/n--> threads). Source: the merge-kit TauCeti profile, built from the review harvest.
- **All asks**: findings classified by the observatory keyword classifier over all <!--n:obs.prs_reviewed-->53<!--/n-->
  reviewed PRs (<!--n:obs.findings_asks-->231<!--/n--> asks; classifier agrees with a hand label on
  <!--n:obs.gold_agree-->29<!--/n--> of <!--n:obs.gold_n-->40<!--/n--> gold findings, CI <!--n:obs.gold_lo-->57<!--/n-->–<!--n:obs.gold_hi-->84<!--/n-->%).

merge-kit recall is the **dev split**, strict (same declaration and same kind of fix), from
`merge-kit/validate/results.json`. n per rubric is tiny; read it as "catches some" or "catches none".
Resolved TauCeti findings are edited in place to ✅, so early texts are lost and classes with quick fixes
are undercounted (see [LIMITS.md](LIMITS.md)).

## Summary

| rank | mode | TauCeti threads | all asks (PRs) | literature match | merge-kit dev recall |
|---|---|---|---|---|---|
| 1 | reuse / duplicate of existing code | <!--n:profile.tauceti.reuse-->23<!--/n--> | <!--n:obs.t.classes.reuse.findings-->29<!--/n--> (<!--n:obs.t.classes.reuse.prs-->17<!--/n-->) | strong | <!--n:mk.dev.per_rubric.reuse.strict.k-->0<!--/n-->/<!--n:mk.dev.per_rubric.reuse.strict.n-->4<!--/n--> strict, <!--n:mk.dev.per_rubric.reuse.lenient.k-->3<!--/n-->/<!--n:mk.dev.per_rubric.reuse.lenient.n-->4<!--/n--> lenient |
| 2 | API design (public/private, missing simp lemmas) | <!--n:profile.tauceti.api_design-->21<!--/n--> | <!--n:obs.t.classes.api_design.findings-->21<!--/n--> (<!--n:obs.t.classes.api_design.prs-->12<!--/n-->) | none named | <!--n:mk.dev.per_rubric.api_design.strict.k-->1<!--/n-->/<!--n:mk.dev.per_rubric.api_design.strict.n-->6<!--/n--> |
| 3 | generality (needless hypotheses, wrong base type) | <!--n:profile.tauceti.generality-->22<!--/n--> | <!--n:obs.t.classes.generality.findings-->24<!--/n--> (<!--n:obs.t.classes.generality.prs-->16<!--/n-->) | none named | <!--n:mk.dev.per_rubric.generality.strict.k-->0<!--/n-->/<!--n:mk.dev.per_rubric.generality.strict.n-->5<!--/n--> |
| 4 | documentation (overclaim, proof mechanics, process talk) | <!--n:profile.tauceti.documentation-->20<!--/n--> | <!--n:obs.t.classes.docs.findings-->38<!--/n--> (<!--n:obs.t.classes.docs.prs-->15<!--/n-->) | match | <!--n:mk.dev.per_rubric.documentation.strict.k-->0<!--/n-->/<!--n:mk.dev.per_rubric.documentation.strict.n-->6<!--/n--> |
| 5 | naming / namespace | <!--n:profile.tauceti.naming-->16<!--/n--> | <!--n:obs.t.classes.naming.findings-->10<!--/n--> (<!--n:obs.t.classes.naming.prs-->6<!--/n-->) | match (style) | <!--n:mk.dev.per_rubric.naming.strict.k-->1<!--/n-->/<!--n:mk.dev.per_rubric.naming.strict.n-->5<!--/n--> |
| 6 | placement (wrong file, unused imports) | <!--n:profile.tauceti.placement-->16<!--/n--> | <!--n:obs.t.classes.placement.findings-->10<!--/n--> (<!--n:obs.t.classes.placement.prs-->7<!--/n-->) | match (style) | <!--n:mk.dev.per_rubric.placement.strict.k-->1<!--/n-->/<!--n:mk.dev.per_rubric.placement.strict.n-->2<!--/n--> |
| 7 | proof quality (rw chains, detours) | <!--n:profile.tauceti.proof_quality-->13<!--/n--> | <!--n:obs.t.classes.proof_quality.findings-->23<!--/n--> (<!--n:obs.t.classes.proof_quality.prs-->11<!--/n-->) | match (refactoring) | <!--n:mk.dev.per_rubric.proof_quality.strict.k-->0<!--/n-->/<!--n:mk.dev.per_rubric.proof_quality.strict.n-->2<!--/n--> strict, <!--n:mk.dev.per_rubric.proof_quality.lenient.k-->1<!--/n-->/<!--n:mk.dev.per_rubric.proof_quality.lenient.n-->2<!--/n--> lenient |
| 8 | attribution and PR-body template | <!--n:profile.tauceti.attribution+profile.tauceti.quality_pass-->12<!--/n--> | <!--n:obs.t.classes.attribution.findings-->10<!--/n--> (<!--n:obs.t.classes.attribution.prs-->8<!--/n-->) | match (unverifiable claims) | <!--n:mk.dev.per_rubric.attribution.strict.k+mk.dev.per_rubric.quality_pass.strict.k-->2<!--/n-->/<!--n:mk.dev.per_rubric.attribution.strict.n+mk.dev.per_rubric.quality_pass.strict.n-->2<!--/n--> |
| 9 | scope (off-target, premature, unrelated hunks) | <!--n:profile.tauceti.scope-->5<!--/n--> | <!--n:obs.t.classes.scope.findings-->12<!--/n--> (<!--n:obs.t.classes.scope.prs-->8<!--/n-->) | match | <!--n:mk.dev.per_rubric.scope.strict.k-->0<!--/n-->/<!--n:mk.dev.per_rubric.scope.strict.n-->1<!--/n--> |
| 10 | correctness of documented claims | <!--n:profile.tauceti.correctness-->5<!--/n--> | <!--n:obs.t.classes.correctness.findings-->25<!--/n--> (<!--n:obs.t.classes.correctness.prs-->10<!--/n-->) | match | <!--n:mk.dev.per_rubric.correctness.strict.k-->0<!--/n-->/<!--n:mk.dev.per_rubric.correctness.strict.n-->2<!--/n--> |
| 11 | symptom fix instead of root cause | – | human repos only | match | not covered |
| 12 | tests in the wrong place, or tests that do not bite | – | <!--n:obs.t.classes.tests.findings-->6<!--/n--> (<!--n:obs.t.classes.tests.prs-->3<!--/n-->) | partial | not covered |
| 13 | CI red when review was requested | – | <!--n:obs.t.classes.ci.findings-->1<!--/n--> (<!--n:obs.t.classes.ci.prs-->1<!--/n-->) | strong | hygiene only (sorry, set_option) |
| 14 | AI-policy violation | – | <!--n:obs.t.classes.policy.findings-->5<!--/n--> (<!--n:obs.t.classes.policy.prs-->3<!--/n-->) | match (rare, severe) | disclosure regex only |
| 15 | fix does not answer the ask (re-raised thread) | <!--n:obs.threads_recurred_loose-->38<!--/n--> re-raised | – | match, larger for us | not covered |

Ranks 1–10 come from the TauCeti rubric data, which is most of our review volume. Ranks 11–15 come
from a handful of hand-typed human reviews on other repos, so their order is not meaningful. The row order was
set when the guide was first built. The counts are restamped on every data refresh, so neighbouring rows can
trade places: read the counts, not the position.
The overall merge-kit dev recall is <!--frac:mk.dev.recall_strict-->5/35 (14%, 95% CI 6–29%)<!--/frac--> strict and
<!--frac:mk.dev.recall_lenient-->9/35 (26%, 95% CI 14–42%)<!--/frac--> lenient; precision is low (<!--n:mk.dev.precision_ask_only.k-->5<!--/n-->
of <!--n:mk.dev.precision_ask_only.n-->80<!--/n--> `ask` findings matched a real first-round ask).

Blocking verdicts: <!--n:obs.prs_blocked-->5<!--/n--> PRs got a ⛔ and <!--n:obs.prs_blocked_closed-->4<!--/n--> of them closed
unmerged. The blocks were on reuse, scope and correctness: those are the modes that kill a PR; the
others cost rounds. [data:numbers.json#obs-6]

---

## 1. Reuse
- **Example.** TauCeti#8953: the new `TauCeti.topAbelianization` was Mathlib's `TopologicalAbelianization`; the PR closed. TauCeti#8486 (⛔): the public theorem was `Subgroup.le_topologicalClosure` unfolded. [ours:TauCeti#8953] [ours:TauCeti#8486]
- **Root cause.** The agent proves what it is asked without first searching the library; a wrapper or alias with no consumer looks like progress.
- **Literature.** Agents show more redundancy than humans; reviewers point at an out-of-diff item in 6.5% of comments; duplicate PRs are a named rejection cause. [lit:https://arxiv.org/abs/2601.21276] [lit:https://arxiv.org/abs/2610.15567] [lit:https://arxiv.org/abs/2601.15195]
- **Pre-PR check.** For every new declaration and every non-trivial `have`: `exact?` / `rw?`, grep Mathlib and the repo for the statement shape, and delete wrappers with no consumer.
- **merge-kit.** `reuse`: exact normalised-statement match (ask) plus a token-score candidate list (maybe). Lenient hits on dev (right declaration, wrong candidate) show it points at the spot but rarely names the replacement.

## 2. API design
- **Example.** TauCeti#45756: three list lemmas were `private` in a domain file but are general facts; TauCeti#1267: add `@[simp]` to headed normal forms and make non-vacuity witnesses `private` or `example`. [ours:TauCeti#45756] [ours:TauCeti#1267]
- **Root cause.** The agent sizes visibility to its own proof, not to the library's consumers.
- **Literature.** No named class; closest is "refactoring" in review themes. [lit:https://arxiv.org/abs/2601.19287]
- **Pre-PR check.** A helper stated only in library types is public in its natural home; a helper that only serves this proof is private. Add `@[simp]` to `*_apply` / `eval_*` forms.
- **merge-kit.** `placement` P5 flags private lemmas about library notions (its one dev hit). Missing lemmas are not detected.

## 3. Generality
- **Example.** TauCeti#19680: "drop needless `2 ≤ p` hypothesis and handle p=0,1"; TauCeti#1256: drop `[SigmaFinite ν]` when integrability gives finiteness. TauCeti#45763 shows the counter-case: keep positivity where the formula fails. [ours:TauCeti#19680] [ours:TauCeti#1256] [ours:TauCeti#45763]
- **Root cause.** The agent keeps every hypothesis that made the first proof attempt go through.
- **Literature.** None found; this is specific to mathematical libraries.
- **Pre-PR check.** Delete each hypothesis in turn and re-run; try the next more general type (ℕ→ℤ, ℚ→field, ℝ→RCLike).
- **merge-kit.** `generality` G1–G4 are heuristics; dev recall shown in the table (none). The G1 guard suppressed the exact `0 < t` → `t ≠ 0` case on TauCeti#45763; fix pending.

## 4. Documentation
- **Example.** TauCeti#1850 (⛔ correctness): the docstring claimed convergence that is false without a dense domain. TauCeti#19035: heading says "Liouville number" while the statement is `LiouvilleWith r`. [ours:TauCeti#1850] [ours:TauCeti#19035]
- **Root cause.** Docstrings written from intent, not reread against the final hypotheses; proof narration and roadmap status leak in.
- **Literature.** Documentation gaps are the main review theme after correctness. [lit:https://arxiv.org/abs/2601.19287]
- **Pre-PR check.** Reread every "is a", "converges", "for all" against the hypotheses; no proof mechanics, no process words; module overview names declarations in their real namespace.
- **merge-kit.** `docs` D1–D3 find missing docstrings and process words; overclaims are semantic and were missed on dev.

## 5. Naming
- **Example.** TauCeti#19680: `padicValNat.mul_log_le_log` should live under `Nat.`; TauCeti#1283: `coe` → `coeFn`; TauCeti#45797: moving one lemma out of `Polynomial` split a family across namespaces. [ours:TauCeti#19680] [ours:TauCeti#1283] [ours:TauCeti#45797]
- **Root cause.** Names chosen from the file being edited, not from the conclusion and the receiver type.
- **Literature.** Style and convention comments are a main theme. [lit:https://arxiv.org/abs/2601.19287]
- **Pre-PR check.** Name from the conclusion; namespace = the argument type for dot notation; do not rename one member of a family.
- **merge-kit.** `naming` N1–N7; N6 (receiver namespace) caught the TauCeti#45763 case on dev. Function namespaces like `padicValNat.` are not yet in N6's list.

## 6. Placement
- **Example.** TauCeti#45354: "general convergent identities belong in `ContinuedFractions/Basic.lean` not the later `BestApproximation.lean`". [ours:TauCeti#45354]
- **Root cause.** New facts go in the file of the feature being built.
- **Pre-PR check.** Find the file where the nearest existing lemmas about the same objects live; drop unused imports.
- **merge-kit.** P1–P4 (sibling files, redundant imports, `import Mathlib`, name-neighbour file).

## 7. Proof quality
- **Example.** TauCeti#19035: long positional `rw` chains → `simp only` or a named lemma. Human reviewers ask the same in other words: "any reason not to just use `body init 0` here?" (clean#515); fold `cases` splits into one `rintro` (cslib#1263). [ours:TauCeti#19035] [ours:clean#515] [ours:cslib#1263]
- **Root cause.** The first proof that compiles is kept.
- **Pre-PR check.** After it works, try the shorter direct form; comment any `show` that unfolds; keep main proofs ≤ 50 lines (TauCeti template Q5).
- **merge-kit.** `proof_shape`: proof length cap, ≥6-step `rw`, undocumented `show`.

## 8. Attribution and the PR-body template
- **Example.** TauCeti#45797: missing `Quality pass:` block (Q1–Q5), because `gh pr create --body` skips the template; TauCeti#8954: wrong Stacks tag; TauCeti#1267: credit the in-tree file the proof plan follows. [ours:TauCeti#45797] [ours:TauCeti#8954] [ours:TauCeti#1267]
- **Root cause.** The body is generated, not filled from the repo's template; citations are recalled, not checked.
- **Literature.** curl and the kernel ask for verifiable claims and reproducers. [lit:https://curl.se/dev/contribute.html] [lit:https://docs.kernel.org/process/coding-assistants.html]
- **Pre-PR check.** Fill the template by hand (`merge-kit template`); open every cited tag and theorem number.
- **merge-kit.** `attribution` body regexes; caught both template asks on dev.

## 9. Scope
- **Example.** TauCeti#5762 (⛔): new API for a roadmap layer already marked complete; cslib#1242: "revert" an unrelated edit to a file under Zulip discussion. [ours:TauCeti#5762] [ours:cslib#1242]
- **Root cause.** The agent optimises for an issue number, not for what the maintainers want next; drive-by edits ride along.
- **Literature.** Unwanted features are 4% of rejections; larger PRs merge less. [lit:https://arxiv.org/abs/2601.15195]
- **Pre-PR check.** Every hunk belongs to the stated change; the target is unfinished and its prerequisites are on main.
- **merge-kit.** `scope`: allowed paths, size caps, topic spread, whitespace-only hunks.

## 10. Correctness of documented claims
- See TauCeti#1850 above. Most "all asks" in this class (<!--n:obs.t.classes.correctness.findings-obs.t.classes.correctness.ai_rubric-obs.t.classes.correctness.human-->17<!--/n--> of <!--n:obs.t.classes.correctness.findings-->25<!--/n-->) come from AI-assisted roadmap reviews, not code review. Lean checks the statement, not the prose around it. Check documented domains (`q > 0` vs `q ≠ 0`). Not automated.

## 11. Symptom fix instead of root cause
- **Example.** mpmath#1244: the maintainer asked that `format_digits()` return the prefix and reuse its zero-padding path, instead of patching `format_mpf`. rust-analyzer#22906: restore the lost `#[deprecated]` instead of deleting it. abx#152 and #186 were superseded by the maintainer's own PRs that extended the shared script preparation. [ours:mpmath#1244] [ours:rust-analyzer#22906] [ours:abx#186]
- **Literature.** Fix tasks have the lowest merge rate (64%). [lit:https://arxiv.org/abs/2601.15195]
- **Pre-PR check.** Find the existing mechanism (`git log -S`, grep), ask why the broken case is excluded, extend it there.

## 12. Tests
- **Example.** "Please move this to test_hexadecimal_fmt()" (mpmath#1244, twice in one pass). tessera#1277: reverting the change did not fail any test. [ours:mpmath#1244] [ours:tessera#1277]
- **Pre-PR check.** Add assertions to the existing test for that feature; mutation-check (break the fix, a test must fail).

## 13. CI red at review time
- **Example.** mpmath#1241: the whole review was "CI fails." [ours:mpmath#1241]
- **Literature.** Failed CI is the largest effect on non-merge (Cliff's δ −0.24) and 17% of rejections. [lit:https://arxiv.org/abs/2601.15195]
- **Pre-PR check.** Run the profile's `ci.local` commands; merge-kit prints them.

## 14. AI-policy violation
- **Example.** rust-analyzer#22906: closed; the repo's policy forbids AI-written comments and PR bodies and autonomous agents opening PRs. [ours:rust-analyzer#22906] [lit:https://github.com/rust-lang/rust-analyzer/blob/master/AI_POLICY.md]
- **Latent risk.** Our cslib and formal-conjectures PRs disclose correctly but have agent-written bodies, which the Mathlib-family rule does not allow. [lit:https://leanprover-community.github.io/contribute/index.html]
- **Pre-PR check.** Gate 0 in [PLAYBOOK.md](PLAYBOOK.md).

## 15. The fix does not answer the ask
- **Example.** TauCeti#19035 needed many flagged rubric rounds before it closed. [ours:TauCeti#19035]
- **Data.** <!--n:obs.threads_recurred_loose-->38<!--/n--> of <!--n:obs.threads_total-->153<!--/n--> threads needed a second comment (CI <!--n:obs.recur_loose_lo-->19<!--/n-->–<!--n:obs.recur_loose_hi-->32<!--/n-->%); <!--n:obs.threads_recurred_strict-->7<!--/n--> came back after being marked ✅.
- **Literature.** Agent misalignment with reviewer instructions is a named, rare rejection class (1%); it is larger for us. [lit:https://arxiv.org/abs/2601.15195]
- **Pre-PR check.** Quote each ask, write the fix next to it, re-read every passing rubric before the push.

## Did friction fall with experience?
No. TauCeti asks per PR did not drop across cohorts; only reuse fell. The rubric set grew and resolved
texts were lost, so the trend is unreliable in both directions. [data:numbers.json#obs-7]
