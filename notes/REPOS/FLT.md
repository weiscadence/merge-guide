## short
not stated
## quote
> No AI section in CONTRIBUTING. The workflow rule that matters: "To claim a task, comment the single word `claim` on the relevant GitHub issue." · "After submitting the PR, comment `propose #PR_NUMBER` on the original issue." · "comment `awaiting-review` on the PR."
> [lit:https://github.com/ImperialCollegeLondon/FLT/blob/main/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.imperialcollegelondon_flt.open--><!--/n--> open (<!--n:obs.prs.imperialcollegelondon_flt.open--><!--/n-->). On FLT#1215 we commented `claim` and `propose #1215` on the task issue on 2026-11-23, and `awaiting-review` on the PR on 2026-11-25; the bot added the label in the same minute. As of 2026-11-28 the issue is still unassigned, the `Build project` run still reads `action_required` (no CI has run), and there is no review.
## process
- Reviewer: the author requests nobody. The `awaiting-review` comment adds the label and moves the task on the project board; maintainers review from there. (documented: CONTRIBUTING.md; observed: FLT#1215)
- Easy to miss: three comments in order: `claim` on the issue, `propose #PR` on the issue, `awaiting-review` on the PR. The last one is the only thing that puts the PR in the queue. (documented: CONTRIBUTING.md)
- Easy to miss: a first-time contributor's CI does not start until a maintainer approves the run. The label does not start it. (observed: FLT#1215, run conclusion `action_required` from 2026-11-23 to 2026-11-28)
## rounds
Unmeasured (no review yet).
## do
- Do: `claim` and wait until you are actually assigned; then `propose #PR`; then `awaiting-review` on the PR; answer `awaiting-author` with a fresh `awaiting-review`.
- Do: run `scripts/run_before_push.sh` (or install the pre-push hook).
- Don't: assume the PR is in the review queue without the label, or that CI ran because no check is red.
