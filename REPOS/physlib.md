# physlib

`leanprover-community/physlib` · profile: `merge-kit/repos/leanprover-community__physlib.yaml`

## AI policy

> "PhyslibAlpha exists for the rapid development of physics digitalizations, enabled by a lighter review process built to handle large-scale, human- or AI-generated contributions." · "The project shall not be tied to any specific AI model or tool."
> [lit:https://github.com/leanprover-community/physlib/blob/master/README.md]

- **Stance:** AI contributions expected in PhyslibAlpha (lighter review); main Physlib has higher review standards; no explicit ban found
- **Who may write PR text and replies:** not stated (OPEN: docs/ReviewGuidelines.md not fetched)
- **Disclosure:** not stated; disclose anyway
- Source: physlib README.md lines 55, 95, 102 (gh api 2026-11-25)

## Ready signal

CI green, non-draft (source: physlib CONTRIBUTING.md)

Open-PR cap: no written cap; our default 2 (source: physlib CONTRIBUTING.md (none stated))

## CI to run locally

```sh
lake exe cache get
lake build -KCI --iofail
lake exe lint_all (per docs/ReviewGuidelines.md, OPEN)
```
Source: .github/workflows/build.yml line 68 (`lake build -KCI --iofail`), ci-evidence.json

## PR body skeleton

```
<Summary; link the Zulip discussion for larger proposals.>
```

## What reviewers here actually ask for (our data)

Review style: human maintainers

None recorded: physlib#2168 landed with zero friction (review harvest scoreboard).

Source: FAILURE-MODES.md (review-harvest counts), general classes 'Zero-friction landings'

## Our PRs here

<!--n:obs.t.by_repo.leanprover_community_physlib.landed-->1<!--/n--> landed (<!--n:obs.prs.leanprover_community_physlib.landed-->physlib#2168<!--/n-->). physlib#2168 had no review asks and a human merge.

## Typical rounds

Zero asks on our one PR; n is one.

## Do / don't

- Do: send large or AI-generated work to PhyslibAlpha; main Physlib has the higher bar.
- Do: build with `lake build -KCI --iofail` (fails on `sorry`).
- Don't: open a large proposal without Zulip discussion.
