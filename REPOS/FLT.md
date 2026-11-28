# FLT

`ImperialCollegeLondon/FLT` · profile: `merge-kit/repos/ImperialCollegeLondon__FLT.yaml`

## AI policy

> No AI section in CONTRIBUTING. The workflow rule that matters: "To claim a task, comment the single word `claim` on the relevant GitHub issue." · "After submitting the PR, comment `propose #PR_NUMBER` on the original issue." · "comment `awaiting-review` on the PR."
> [lit:https://github.com/ImperialCollegeLondon/FLT/blob/main/CONTRIBUTING.md]

- **Stance:** no AI section in CONTRIBUTING
- **Who may write PR text and replies:** unknown (no written rule); disclose anyway
- **Disclosure:** not required in writing
- Source: https://raw.githubusercontent.com/ImperialCollegeLondon/FLT/main/CONTRIBUTING.md (gh api 2026-11-25); STATE-OF-THE-FIELD.md policy table

## Ready signal

comment `awaiting-review` on the PR (adds the label, moves the task to In Review). FLT#1215 never got it. (source: FLT CONTRIBUTING.md line 61; STATE-OF-THE-FIELD.md policy table)

Open-PR cap: one PR per claimed task; no numeric cap (source: FLT CONTRIBUTING.md lines 19-57)

## CI to run locally

```sh
lake exe cache get
lake build --iofail
scripts/run_before_push.sh
```
Note: sorry allowed by design (warn.sorry = false)
Source: FLT CONTRIBUTING.md lines 36-45; ci-evidence.json (blueprint.yml TEST_ARGS=--iofail; lakefile.toml:14-15)

## PR body skeleton

```
Closes #<issue>

<What the task asked and what this proves.>
```

## What reviewers here actually ask for (our data)

Review style: human maintainers via the project dashboard columns

None recorded: FLT#1215 has no review yet (our only FLT PR).

Source: unpublished observatory REPORT.md §1.1 (FLT: 1 PR, open)

## Our PRs here

<!--n:obs.t.by_repo.imperialcollegelondon_flt.open-->1<!--/n--> open (<!--n:obs.prs.imperialcollegelondon_flt.open-->FLT#1215<!--/n-->). On FLT#1215 we commented `claim` and `propose`, but the bot never assigned the issue and we never posted `awaiting-review`, so by the written workflow the PR never entered review.

## Typical rounds

Unmeasured (no review yet).

## Do / don't

- Do: `claim` and wait until you are actually assigned; then `propose #PR`; then `awaiting-review` on the PR; answer `awaiting-author` with a fresh `awaiting-review`.
- Do: run `scripts/run_before_push.sh` (or install the pre-push hook).
- Don't: assume the PR is in the review queue without the label.
