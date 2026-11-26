## short
not stated
## quote
> No AI section in CONTRIBUTING. The workflow rule that matters: "To claim a task, comment the single word `claim` on the relevant GitHub issue." · "After submitting the PR, comment `propose #PR_NUMBER` on the original issue." · "comment `awaiting-review` on the PR."
> [lit:https://github.com/ImperialCollegeLondon/FLT/blob/main/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.imperialcollegelondon_flt.open--><!--/n--> open (FLT#1215). We commented `claim` and `propose`, but the bot never assigned the issue and we never posted `awaiting-review`, so by the written workflow the PR never entered review.
## rounds
Unmeasured (no review yet).
## do
- Do: `claim` and wait until you are actually assigned; then `propose #PR`; then `awaiting-review` on the PR; answer `awaiting-author` with a fresh `awaiting-review`.
- Do: run `scripts/run_before_push.sh` (or install the pre-push hook).
- Don't: assume the PR is in the review queue without the label.
