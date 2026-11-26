# mathlib4

`leanprover-community/mathlib4` · profile: `merge-kit/repos/leanprover-community__mathlib4.yaml`

## AI policy

> "Using an LLM when writing comments on GitHub or Zulip is not allowed: use your own words." · "As of mid-2026, code written by an AI without the supervision of a Lean subject expert fails to meet that bar by a large margin." · "we will suspend (or permanently ban) you both from opening new PRs and from the Zulip chat."
> [lit:https://leanprover-community.github.io/contribute/index.html]

- **Stance:** RESTRICT, strict
- **Who may write PR text and replies:** humans only for GitHub/Zulip comments: 'Using an LLM when writing comments on GitHub or Zulip is not allowed'. An agent must not write the PR description or review replies.
- **Disclosure:** PR description must say which AI tools were used and how; add the `LLM-generated` label for substantial generated code
- **Consequence:** low-quality LLM PRs closed without comment; repeated low-effort PRs -> PR and Zulip ban
- Source: https://leanprover-community.github.io/contribute/index.html (Use of AI), via STATE-OF-THE-FIELD.md policy table §2

## Ready signal

CI green, then remove `WIP`/draft; `awaiting-review` label is applied by the queue (verify on the PR page before relying on it) (source: mathlib4 PULL_REQUEST_TEMPLATE.md ('most reviewers will only notice your PR if it passes CI'); label OPEN)

Open-PR cap: no written numeric cap found; our default 2 (STATE-OF-THE-FIELD.md policy table, NumPy rule) (source: STATE-OF-THE-FIELD.md policy table §2 (NumPy row) and T8)

## CI to run locally

```sh
lake exe cache get
lake build --wfail
lake exe runLinter Mathlib
lake exe shake
lake exe lint-style
```
Note: We have never opened a mathlib4 PR; commands are the standard Mathlib ones, not re-verified against the workflow today.
Source: mathlib4 README / contribute docs (OPEN: workflow file not fetched 2026-11-25)

## PR body skeleton

```
<Human-written summary. Text above the `---` becomes the squash-commit message.>

Moves:
- (Old.name -> New.name, if any)

Deletions:
- (removed declarations, if any)

---
AI use: <tools and how they were used>  (and add the `LLM-generated` label)

- [ ] depends on: #
```

## What reviewers here actually ask for (our data)

Review style: human maintainers + bors; reviewers only notice PRs that pass CI

None recorded: none in our data: we have no mathlib4 PRs (unpublished observatory FIELD.md 'Mathlib itself is not in our data').

Source: unpublished observatory FIELD.md; mathlib4 PULL_REQUEST_TEMPLATE.md

## Our PRs here

None. We have never opened a mathlib4 PR, so every review statement here comes from the written rules and the field sample, not from our reviews.

## Typical rounds

Unmeasured for us. In the field sample, declared-AI mathlib4 PRs merged at <!--frac:field.by_repo.leanprover_community_mathlib4_declared.rate--><!--/frac--> with most still open; see STATE-OF-THE-FIELD for why that number is biased.

## Do / don't

- Do: only with a Lean expert as the human author, who writes the description and every reply.
- Do: say which tools were used and how; add the `LLM-generated` label for substantial generated code.
- Don't: open several PRs without engaging on Zulip first; low-quality LLM PRs are closed without comment.
- Don't: let an agent answer review. A ban here also covers Zulip, i.e. the whole Lean community.
