# TauCeti

`TauCetiProject/TauCeti` · profile: `merge-kit/repos/TauCetiProject__TauCeti.yaml`

## AI policy

> "implemented and maintained by AI contributors, subject to adversarial review." · "Review of implementation PRs is entirely driven by AIs. These operate according to a fixed open source rubric. Humans write the rubric, and update it as the project evolves." · "it is currently switched off. For now, reviews are run from the command line."
> [lit:https://github.com/TauCetiProject/TauCeti/blob/main/README.md]

- **Stance:** WELCOME (AI-authored by design, AI-reviewed under a fixed open rubric)
- **Who may write PR text and replies:** agents may write code, PR descriptions and replies
- **Disclosure:** none required
- Source: TauCeti README.md lines 8, 64 (gh api, 2026-11-25); STATE-OF-THE-FIELD.md policy table §2

## Ready signal

open as a normal (non-draft) PR with a filled Quality pass and green CI. Automatic review is currently switched off (README: 'it is currently switched off. For now, reviews are run from the command line'), so a maintainer or worker runs it. Editing the description alone does not re-trigger review: reply on the thread. (source: TauCeti README.md 'Review' section (fetched 2026-11-25); review.yml gates on vars.CI_REVIEW_ENABLED; FAILURE-MODES.md quality-pass row)

Open-PR cap: no written cap; stacked PRs are prohibited (each prerequisite must land first) (source: TauCeti AGENTS.md 'The rules of the repo' (no-stacking policy))

## CI to run locally

```sh
lake exe cache get
bash scripts/lake-cache-get.sh .
lake build --iofail
lake test
lake lint
```
Note: lake lint = source guards, style, doc lint, diff guards (3000 added / 2000 removed lines, new file <= 1250 lines, paths). On this box: no full builds; merge-kit runs the grep-level subset.
Source: TauCeti README.md 'Building' lines 236-252

## PR body skeleton

```
Roadmap: <CanonicalAreaName or none>

<What this adds, which roadmap file and target it advances, and what it draws on (paper /
textbook section / in-tree file it follows).>

New declarations:
{{decls}}

Quality pass:
- Q1 Mathlib duplicates: …
- Q2 Tau Ceti duplicates, on main and in open PRs: …
- Q3 Hypotheses: …
- Q4 Section variables: …
- Q5 Proofs of at most 50 lines: …
```

## What reviewers here actually ask for (our data)

Review style: AI rubric bot (TauCetiReview), one thread per rubric; humans write the rubric, not the reviews

| class | asks / threads in our data |
|---|---|
| reuse | <!--n:profile.tauceti.reuse-->23<!--/n--> |
| generality | <!--n:profile.tauceti.generality-->22<!--/n--> |
| api-design | <!--n:profile.tauceti.api_design-->21<!--/n--> |
| documentation | <!--n:profile.tauceti.documentation-->20<!--/n--> |
| naming | <!--n:profile.tauceti.naming-->16<!--/n--> |
| placement | <!--n:profile.tauceti.placement-->16<!--/n--> |
| proof-quality | <!--n:profile.tauceti.proof_quality-->13<!--/n--> |
| attribution | <!--n:profile.tauceti.attribution-->7<!--/n--> |
| correctness | <!--n:profile.tauceti.correctness-->5<!--/n--> |
| quality-pass | <!--n:profile.tauceti.quality_pass-->5<!--/n--> |
| scope | <!--n:profile.tauceti.scope-->5<!--/n--> |

Source: FAILURE-MODES.md (review-harvest counts), TauCeti classes (recounted from the review harvest on every data refresh)

## Our PRs here

<!--n:obs.t.by_repo.taucetiproject_tauceti.landed-->25<!--/n--> landed, <!--n:obs.t.by_repo.taucetiproject_tauceti.closed-->7<!--/n--> closed, <!--n:obs.t.by_repo.taucetiproject_tauceti.open-->2<!--/n--> open of <!--n:obs.t.by_repo.taucetiproject_tauceti.n-->34<!--/n-->. All landings were bot-merged after AI-rubric review; no human-typed review comment exists on our TauCeti PRs. Closed PRs were reuse or scope blocks and premature roadmap slices (TauCeti#8953, #8954, #8955, #5762).

## Typical rounds

Rubric rounds per reviewed PR: median <!--n:obs.rubric_rounds_median-->1<!--/n-->, max <!--n:obs.rubric_rounds_max-->3<!--/n--> recorded rounds; but a single PR can draw seven rubric classes at once (TauCeti#45333), and TauCeti#19035 went through many flagged rounds before closing. Every push restarts the sweep.

## Do / don't

- Do: put `Roadmap: <name>` and the full `Quality pass:` block (Q1–Q5) in the body; `gh pr create --body` skips the template.
- Do: run every rubric angle yourself before pushing (reuse first); merge-kit's TauCeti profile maps its checks to the rubric names.
- Do: reply on the thread to re-trigger review after a description edit.
- Don't: stack PRs, use `set_option`, or open API for a roadmap layer marked complete.
- Don't: run `tauceti-review --post` on your own PR; on a dry run pass `--no-archive`.

## Profile corrections

- 2026-11-25: earlier profile said 'review runs automatically on push'; the README says it is switched off
