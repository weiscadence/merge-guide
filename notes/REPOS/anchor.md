## short
mostly hand-written; no autonomous replies
## quote
> "You may use an LLM to help draft your PR description. However, we'd encourage you to write out the majority of the description by hand." · "Please do not use LLMs to autonomously respond to PR feedback (this includes blindly copy-pasting responses)."
> [lit:https://github.com/otter-sec/anchor/blob/master/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.otter_sec_anchor.landed--><!--/n--> landed (<!--n:obs.prs.otter_sec_anchor.landed--><!--/n-->), <!--n:obs.t.by_repo.otter_sec_anchor.open--><!--/n--> open (<!--n:obs.prs.otter_sec_anchor.open--><!--/n-->). anchor#5360 had no asks and a human merge.
## process
- Reviewer: the CODEOWNERS file requests the three code owners when the PR opens. On anchor#5366 the two approvals came from other team members, and the PR stayed "review required" after both. (documented: `.github/CODEOWNERS`; observed: anchor#5366)
- Easy to miss: the changelog line cites the PR number, not the issue number. A reviewer fixed ours with a suggestion. (observed: anchor#5366)
- **Not yours to fix:** the three Vercel checks fail on a fork PR until a team member authorizes the deploy. (observed: anchor#5366)
## rounds
Zero asks on the landed PR.
## do
- Do: open a draft early, then mark ready after build, test, fmt and clippy pass locally.
- Do: breaking changes target `anchor-next`.
- Don't: typo-only PRs; don't let an agent answer review.
- Note: a full `cargo test` needs several GB of disk.
