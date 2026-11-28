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

comment `awaiting-review` on the PR (adds the label, moves the task to In Review). No reviewer is requested by the author. On FLT#1215 the comment was posted on 2026-11-25 and the bot added the label within a minute; the `Build project` workflow still showed `action_required` on 2026-11-28 (a maintainer has to approve a first-time contributor's run), and the task issue was still unassigned. (source: FLT CONTRIBUTING.md line 61; STATE-OF-THE-FIELD.md policy table; FLT#1215 timeline and workflow runs (read 2026-11-28))

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

## How a PR gets a reviewer, and what the author must do

- Reviewer: the author requests nobody. The `awaiting-review` comment adds the label and moves the task on the project board; maintainers review from there. (documented: CONTRIBUTING.md; observed: FLT#1215)
- Easy to miss: three comments in order: `claim` on the issue, `propose #PR` on the issue, `awaiting-review` on the PR. The last one is the only thing that puts the PR in the queue. (documented: CONTRIBUTING.md)
- Easy to miss: a first-time contributor's CI does not start until a maintainer approves the run. The label does not start it. (observed: FLT#1215, run conclusion `action_required` from 2026-11-23 to 2026-11-28)

## Our PRs here

<!--n:obs.t.by_repo.imperialcollegelondon_flt.open--><!--/n--> open (<!--n:obs.prs.imperialcollegelondon_flt.open--><!--/n-->). On FLT#1215 we commented `claim` and `propose #1215` on the task issue on 2026-11-23, and `awaiting-review` on the PR on 2026-11-25; the bot added the label in the same minute. As of 2026-11-28 the issue is still unassigned, the `Build project` run still reads `action_required` (no CI has run), and there is no review.

## Typical rounds

Unmeasured (no review yet).

## Do / don't

- Do: `claim` and wait until you are actually assigned; then `propose #PR`; then `awaiting-review` on the PR; answer `awaiting-author` with a fresh `awaiting-review`.
- Do: run `scripts/run_before_push.sh` (or install the pre-push hook).
- Don't: assume the PR is in the review queue without the label, or that CI ran because no check is red.
