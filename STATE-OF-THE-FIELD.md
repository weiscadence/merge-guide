# State of the field: how AI contributes to formal mathematics (late 2026)

Data as of <!--asof-->2026-11-28<!--/asof-->. Three evidence layers, weakest claims flagged inline:

- **Literature**: large studies of agent PRs on GitHub, nearly all general code, mostly 2025 data.
- **Field sample**: <!--n:field.n_rows-->1496<!--/n--> PRs by other people in seven repos (TauCeti, mathlib4,
  formal-conjectures, cslib, FLT, mpmath, sympy), <!--n:field.n_bot_authored-->78<!--/n--> of them bot-authored and
  excluded. "Declared" means the PR names an AI tool (trailer, label, or a sentence); nothing is inferred
  from writing style. [data:numbers.json#obs-detection]
- **Field census**: every PR in the census window for TauCeti, formal-conjectures and mathlib4, with
  sampled comment bodies. If the census output is missing, its cells read "(census pending)" and
  `make collect && make` fills them. [data:numbers.json#census]
- **Our PRs**: <!--n:obs.prs_total-->85<!--/n--> external PRs by one agent, one operator.
  [data:numbers.json#obs-1]

## 1. Four models of AI contribution

| model | repos | what it looks like |
|---|---|---|
| AI-native, AI-reviewed | TauCeti | Agents write the library; an open rubric engine reviews; humans write roadmaps and rubrics |
| Human-gated, LLM text banned | mathlib4, cslib, formal-conjectures | AI-assisted code allowed with disclosure; GitHub/Zulip text must be the human's own words |
| Claim-workflow, no AI rule | FLT | Tasks are issues; a bot assigns on `claim`; no AI section in CONTRIBUTING |
| Two-tier | physlib | A lighter-review "Alpha" area built for large or AI-generated contributions |
| No written policy | mpmath, clean, sympy (dev guide not checked) | Normal review; disclosed AI PRs have been accepted (ours on mpmath) |

### TauCeti: AI-authored by design
> "implemented and maintained by AI contributors, subject to adversarial review."
> "Review of implementation PRs is entirely driven by AIs. These operate according to a fixed open source rubric. Humans write the rubric, and update it as the project evolves."
[lit:https://github.com/TauCetiProject/TauCeti/blob/main/README.md]

How review works in practice: the TauCetiReview engine runs one agent per rubric (correctness, reuse,
scope, attribution, api-design, generality, placement, naming, documentation, proof-quality, plus a
quality-pass check of the PR template). Each comment carries a `tauceti-meta` blob naming the reviewer
model, and is posted under whichever maintainer ran the tool. Automatic review "is currently switched
off. For now, reviews are run from the command line." [lit:https://github.com/TauCetiProject/TauCeti/blob/main/README.md]

What that means for counting "human review": on our TauCeti PRs, <!--n:obs.rubric_under_human_login-->179<!--/n-->
of <!--n:obs.rubric_comments-->194<!--/n--> rubric comments sit under maintainers' personal logins. Typed
by login they look human; typed by marker, none of them are. [data:numbers.json#obs-3.1]
In the field sample the same correction took the median "human review comments" on TauCeti PRs to
<!--n:field.by_repo.taucetiproject_tauceti_declared.median_human_comments-->0<!--/n-->.
[data:numbers.json#obs-correction]

Reviewer models on our <!--n:obs.reviewer_prs-->32<!--/n--> reviewed TauCeti PRs: <!--n:obs.reviewer_family_codex-->165<!--/n-->
rubric comments from codex-family models, <!--n:obs.reviewer_family_claude-->29<!--/n--> from Claude, across
<!--n:obs.reviewer_models_n-->9<!--/n--> model versions. Models change with the month, so no model ranking is
supported. [data:numbers.json#obs-3.2]

### Mathlib family: LLM-written text is banned
> "Using an LLM when writing comments on GitHub or Zulip is not allowed: use your own words."
> "Members of the review team will summarily close without comment any low quality PR produced using LLMs [...] we will suspend (or permanently ban) you both from opening new PRs and from the Zulip chat."
> "If your PR contains a substantial amount of LLM-generated code, add the LLM-generated label"
[lit:https://leanprover-community.github.io/contribute/index.html]

cslib quotes the disclosure part ("Explain which tool(s) you used and how you used it")
[lit:https://github.com/leanprover/cslib/blob/main/CONTRIBUTING.md]. formal-conjectures says "Follow the
same AI usage conventions as Mathlib" and needs a Google CLA [lit:https://github.com/google-deepmind/formal-conjectures/blob/main/CONTRIBUTING.md].
formal-conjectures states open problems, so `sorry` is allowed by design (`warn.sorry = false`).
[data:numbers.json#obs-2]

### FLT: claim workflow
Comment `claim` on the issue, `propose #PR` once the PR exists, then `awaiting-review` on the PR; maintainers
answer with `awaiting-author`. There is no AI section. [lit:https://github.com/ImperialCollegeLondon/FLT/blob/main/CONTRIBUTING.md]

### physlib: two tiers
> "PhyslibAlpha has lower review-standards than Physlib making it easier to contribute large PRs, AI-generated content, or formalizations which are not-quite-perfect."
[lit:https://github.com/leanprover-community/physlib/blob/master/README.md]

### mpmath, clean and others
No written AI policy (mpmath has no CONTRIBUTING at master; clean has none). Review is by one or two
maintainers who answer fast and care about root cause and test placement. [ours:mpmath#1244] [ours:clean#515]

## 2. Field numbers

Merge rate = landed / (landed + closed); open PRs are excluded from n. Intervals are Wilson 95%.

### 2.1 Unselected baseline (newest PRs per repo, no keyword filter)
| baseline, pooled | PRs | merge rate |
|---|---|---|
| declared AI | <!--n:field.baseline_pooled.declared_any.prs-->309<!--/n--> | <!--frac:field.baseline_pooled.declared_any.rate-->172/196 (88%, 95% CI 82–92%)<!--/frac--> |
| undeclared | <!--n:field.baseline_pooled.undeclared.prs-->340<!--/n--> | <!--frac:field.baseline_pooled.undeclared.rate-->150/184 (82%, 95% CI 75–86%)<!--/frac--> |

The pooled gap is a repo-mix effect: most of TauCeti's baseline is declared and it merges almost
everything. Inside single repos the intervals overlap except cslib, where undeclared PRs merged more.
**No claim that declaring, or any tool, raises merge rate is supported.** [data:numbers.json#obs-baseline]

### 2.2 By repo, all samples (keyword + label + baseline; read as "who declares what", not as tool rankings)
| repo | declared: merge rate | undeclared: merge rate |
|---|---|---|
| TauCeti | <!--frac:field.by_repo.taucetiproject_tauceti_declared.rate-->79/83 (95%, 95% CI 88–98%)<!--/frac--> | <!--frac:field.by_repo.taucetiproject_tauceti_undeclared.rate-->9/12 (75%, 95% CI 47–91%)<!--/frac--> |
| mathlib4 | <!--frac:field.by_repo.leanprover_community_mathlib4_declared.rate-->10/43 (23%, 95% CI 13–38%)<!--/frac--> | <!--frac:field.by_repo.leanprover_community_mathlib4_undeclared.rate-->21/25 (84%, 95% CI 65–94%)<!--/frac--> |
| formal-conjectures | <!--frac:field.by_repo.google_deepmind_formal_conjectures_declared.rate-->31/34 (91%, 95% CI 77–97%)<!--/frac--> | <!--frac:field.by_repo.google_deepmind_formal_conjectures_undeclared.rate-->21/29 (72%, 95% CI 54–85%)<!--/frac--> |
| cslib | <!--frac:field.by_repo.leanprover_cslib_declared.rate-->21/30 (70%, 95% CI 52–83%)<!--/frac--> | <!--frac:field.by_repo.leanprover_cslib_undeclared.rate-->44/45 (98%, 95% CI 88–100%)<!--/frac--> |
| FLT | <!--frac:field.by_repo.imperialcollegelondon_flt_declared.rate-->48/53 (91%, 95% CI 80–96%)<!--/frac--> | <!--frac:field.by_repo.imperialcollegelondon_flt_undeclared.rate-->13/16 (81%, 95% CI 57–93%)<!--/frac--> |
| mpmath | <!--frac:field.by_repo.mpmath_mpmath_declared.rate-->18/22 (82%, 95% CI 61–93%)<!--/frac--> | <!--frac:field.by_repo.mpmath_mpmath_undeclared.rate-->61/76 (80%, 95% CI 70–88%)<!--/frac--> |
| sympy | <!--frac:field.by_repo.sympy_sympy_declared.rate-->32/47 (68%, 95% CI 54–80%)<!--/frac--> | <!--frac:field.by_repo.sympy_sympy_undeclared.rate-->12/31 (39%, 95% CI 24–56%)<!--/frac--> |

Open PRs (not in n): mathlib4 declared <!--n:field.by_repo.leanprover_community_mathlib4_declared.open-->176<!--/n--> of
<!--n:field.by_repo.leanprover_community_mathlib4_declared.prs-->219<!--/n-->. The mathlib4 gap is the one large one,
but the `LLM-generated` label and search order select for it, and most declared mathlib4 PRs are still open.

By declared family (all samples): Claude <!--frac:field.by_family.claude.rate-->164/196 (84%, 95% CI 78–88%)<!--/frac-->, codex/OpenAI
<!--frac:field.by_family.codex_openai.rate-->47/59 (80%, 95% CI 68–88%)<!--/frac-->, Gemini <!--frac:field.by_family.gemini_deepmind.rate-->9/17 (53%, 95% CI 31–74%)<!--/frac-->,
Aristotle <!--frac:field.by_family.aristotle.rate-->9/12 (75%, 95% CI 47–91%)<!--/frac-->. Claude and codex overlap; the others are too small to rank.

### 2.3 Census (every PR in the window; comment bodies sampled)

Window end <!--n:census.census_end-->2026-11-25T00:00:00Z<!--/n-->; sampling seed <!--n:census.seed-->20261125<!--/n-->. [data:numbers.json#census]

**Who contributes.**

| repo | non-bot PRs | distinct authors | top-10 authors' share | declared share |
|---|---|---|---|---|
| TauCeti | <!--n:census.size.taucetiproject_tauceti.prs_nonbot-->31567<!--/n--> | <!--n:census.authors.taucetiproject_tauceti.distinct-->114<!--/n--> | <!--frac:census.authors.taucetiproject_tauceti.top10_share-->26293/31567 (83%, 95% CI 83–84%)<!--/frac--> | <!--frac:census.declared_share.taucetiproject_tauceti-->23873/31567 (76%, 95% CI 75–76%)<!--/frac--> |
| formal-conjectures | <!--n:census.size.google_deepmind_formal_conjectures.prs_nonbot-->5483<!--/n--> | <!--n:census.authors.google_deepmind_formal_conjectures.distinct-->493<!--/n--> | <!--frac:census.authors.google_deepmind_formal_conjectures.top10_share-->2898/5483 (53%, 95% CI 52–54%)<!--/frac--> | <!--frac:census.declared_share.google_deepmind_formal_conjectures-->2448/5483 (45%, 95% CI 43–46%)<!--/frac--> |
| mathlib4 (since the label existed) | <!--n:census.size.leanprover_community_mathlib4.prs_nonbot-->19758<!--/n--> | <!--n:census.authors.leanprover_community_mathlib4.distinct-->938<!--/n--> | <!--frac:census.authors.leanprover_community_mathlib4.top10_share-->6141/19758 (31%, 95% CI 30–32%)<!--/frac--> | <!--frac:census.declared_share.leanprover_community_mathlib4-->2425/19758 (12%, 95% CI 12–13%)<!--/frac--> |

TauCeti is the extreme case: a few operator accounts submit most PRs, so its rates describe those
operators' pipelines more than "AI PRs" in general.

**Merge rates and the operator check.** Removing the three most active declared authors tests whether one
pipeline drives the declared rate.

| repo | merge rate, declared | merge rate, undeclared | same, without the top-3 declared authors: declared | … undeclared | median days to land, declared / undeclared |
|---|---|---|---|---|---|
| TauCeti | <!--frac:census.merge_by_family.taucetiproject_tauceti.declared_any-->21408/23105 (93%, 95% CI 92–93%)<!--/frac--> | <!--frac:census.merge_by_family.taucetiproject_tauceti.undeclared-->6971/7425 (94%, 95% CI 93–94%)<!--/frac--> | <!--frac:census.operators.taucetiproject_tauceti.without_top3_declared.declared-->11986/13123 (91%, 95% CI 91–92%)<!--/frac--> | <!--frac:census.operators.taucetiproject_tauceti.without_top3_declared.undeclared-->6188/6561 (94%, 95% CI 94–95%)<!--/frac--> | <!--n:census.time_to_land.taucetiproject_tauceti_declared.median-->0.41<!--/n--> / <!--n:census.time_to_land.taucetiproject_tauceti_undeclared.median-->0.61<!--/n--> |
| formal-conjectures | <!--frac:census.merge_by_family.google_deepmind_formal_conjectures.declared_any-->908/1983 (46%, 95% CI 44–48%)<!--/frac--> | <!--frac:census.merge_by_family.google_deepmind_formal_conjectures.undeclared-->2144/2597 (83%, 95% CI 81–84%)<!--/frac--> | <!--frac:census.operators.google_deepmind_formal_conjectures.without_top3_declared.declared-->641/757 (85%, 95% CI 82–87%)<!--/frac--> | <!--frac:census.operators.google_deepmind_formal_conjectures.without_top3_declared.undeclared-->2096/2536 (83%, 95% CI 81–84%)<!--/frac--> | <!--n:census.time_to_land.google_deepmind_formal_conjectures_declared.median-->3.35<!--/n--> / <!--n:census.time_to_land.google_deepmind_formal_conjectures_undeclared.median-->1.55<!--/n--> |
| mathlib4 (since the label existed) | <!--frac:census.merge_by_family.leanprover_community_mathlib4.declared_any-->1186/1776 (67%, 95% CI 65–69%)<!--/frac--> | <!--frac:census.merge_by_family.leanprover_community_mathlib4.undeclared-->13347/15179 (88%, 95% CI 87–88%)<!--/frac--> | <!--frac:census.operators.leanprover_community_mathlib4.without_top3_declared.declared-->758/1203 (63%, 95% CI 60–66%)<!--/frac--> | <!--frac:census.operators.leanprover_community_mathlib4.without_top3_declared.undeclared-->12939/14660 (88%, 95% CI 88–89%)<!--/frac--> | <!--n:census.time_to_land.leanprover_community_mathlib4_declared.median-->5.07<!--/n--> / <!--n:census.time_to_land.leanprover_community_mathlib4_undeclared.median-->4.49<!--/n--> |

How to read it:
- **TauCeti:** declared PRs merge within a few points of undeclared ones and land faster.
- **formal-conjectures:** the low declared rate is an operator effect. With the three most active declared
  authors removed, declared and undeclared PRs merge at about the same rate. A few high-volume AI
  pipelines with many closed PRs pull the pooled number down.
- **mathlib4:** declared PRs merge less often than undeclared ones, and the gap survives removing the top
  three declared authors. This fits the written policy (low-quality LLM PRs are closed), but it does not
  show AI code is worse: declared PRs also differ in task, author experience and timing.
- Per-family rates vary a lot within a repo, because one operator can dominate a family, so no tool
  ranking is drawn.

**Who reviews.**

| repo | AI share of review comments (marked) | sampled PRs with any unmarked comment | sampled PRs with a rubric comment |
|---|---|---|---|
| TauCeti | <!--frac:census.review_mix.taucetiproject_tauceti.ai_share_of_review-->5004/5069 (99%, 95% CI 98–99%)<!--/frac--> | <!--frac:census.review_mix.taucetiproject_tauceti.prs_with_any_human_unmarked-->29/1000 (3%, 95% CI 2–4%)<!--/frac--> | <!--frac:census.review_mix.taucetiproject_tauceti.prs_with_any_rubric-->592/1000 (59%, 95% CI 56–62%)<!--/frac--> |
| formal-conjectures | <!--frac:census.review_mix.google_deepmind_formal_conjectures.ai_share_of_review-->9/2401 (0%, 95% CI 0–1%)<!--/frac--> | <!--frac:census.review_mix.google_deepmind_formal_conjectures.prs_with_any_human_unmarked-->690/1000 (69%, 95% CI 66–72%)<!--/frac--> | <!--frac:census.review_mix.google_deepmind_formal_conjectures.prs_with_any_rubric-->0/1000 (0%, 95% CI 0–0%)<!--/frac--> |
| mathlib4 (since the label existed) | <!--frac:census.review_mix.leanprover_community_mathlib4.ai_share_of_review-->79/13751 (1%, 95% CI 0–1%)<!--/frac--> | <!--frac:census.review_mix.leanprover_community_mathlib4.prs_with_any_human_unmarked-->2106/2739 (77%, 95% CI 75–78%)<!--/frac--> | <!--frac:census.review_mix.leanprover_community_mathlib4.prs_with_any_rubric-->0/2739 (0%, 95% CI 0–0%)<!--/frac--> |

"AI share" counts comments with an AI marker (rubric engine, machine output, self-labelled); everything
else is "unmarked", which is not proof of a human. Outside TauCeti no marker exists, so the AI share there
is a floor; on TauCeti almost every review comment is engine output.

## 3. Our own PRs, for scale

<!--n:obs.prs_total-->85<!--/n--> PRs: <!--n:obs.prs_landed-->42<!--/n--> landed, <!--n:obs.prs_closed-->14<!--/n--> closed,
<!--n:obs.prs_open-->29<!--/n--> open; merge rate <!--n:obs.prs_landed/(obs.prs_landed+obs.prs_closed)%-->75%<!--/n-->
(95% CI <!--n:obs.merge_rate_lo-->62<!--/n-->–<!--n:obs.merge_rate_hi-->84<!--/n-->%). TauCeti
<!--n:obs.t.by_repo.taucetiproject_tauceti.landed-->25<!--/n--> landed of <!--n:obs.t.by_repo.taucetiproject_tauceti.n-->34<!--/n-->.
Of <!--n:obs.comments_total-->375<!--/n--> review comments, <!--n:obs.comments_human-->43<!--/n--> carry no AI marker
(<!--n:obs.comments_human/obs.comments_total%-->11%<!--/n-->), and none of those are on TauCeti.
Of <!--n:obs.lean_landed-->29<!--/n--> Lean landings, <!--n:obs.verified-->4<!--/n--> had a human sign-off; the rest
were bot-merged after AI review, which is TauCeti's design. [data:numbers.json#obs-1] [data:numbers.json#obs-2]

## 4. What the literature says (general code)

- Overall agent-PR merge rate in AIDev is high, but it mostly describes owners merging their own agents' PRs; stratified, the co-authorship effect disappears. Not a benchmark for outside contributors. [lit:https://arxiv.org/abs/2606.22711] [lit:https://arxiv.org/abs/2601.15195]
- Rejection causes for agent PRs that the merge metrics miss: no meaningful reviewer engagement, duplicate PRs, unwanted features, agent misalignment. [lit:https://arxiv.org/abs/2601.15195]
- Documentation tasks are accepted far more often than new features (82.1% vs 66.1%). [lit:https://arxiv.org/abs/2602.08915]
- Agents reuse less than humans and reviewers are, if anything, more lenient toward AI PRs. [lit:https://arxiv.org/abs/2601.21276]
- Merged agent PRs draw verified follow-up fixes at 1.62× the odds of human merges. [lit:https://arxiv.org/abs/2609.26847]
- Most agent PRs get no human review; where reviewed, AI reviewers dominate. [lit:https://arxiv.org/abs/2605.02273]
- AI reviewers: 56% of CodeRabbit comments are rejected by developers. [lit:https://arxiv.org/abs/2607.03316]

Nothing in the literature measures formal-math repos specifically. The "generality" and "api-design"
classes that dominate TauCeti review have no named analogue there.

## 5. Where the evidence is thin

- Our sample is one agent and one operator; per-repo n outside TauCeti is 1–9 PRs.
- Field merge rates for declared vs undeclared are confounded by repo, search order and time.
- TauCeti review comments are edited in place on resolution, so first-pass texts are partly lost.
- "Human" outside TauCeti means "no AI marker", which overcounts humans.
- The census covers three repos only; FLT, cslib, mpmath and sympy rows come from the smaller field sample.
Details: [LIMITS.md](LIMITS.md).
