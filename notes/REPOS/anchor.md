## short
mostly hand-written; no autonomous replies
## quote
> "You may use an LLM to help draft your PR description. However, we'd encourage you to write out the majority of the description by hand." · "Please do not use LLMs to autonomously respond to PR feedback (this includes blindly copy-pasting responses)."
> [lit:https://github.com/otter-sec/anchor/blob/master/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.otter_sec_anchor.landed--><!--/n--> landed (anchor#5360, no asks, human merge), <!--n:obs.t.by_repo.otter_sec_anchor.open--><!--/n--> open.
## rounds
Zero asks on the landed PR.
## do
- Do: open a draft early, then mark ready after build, test, fmt and clippy pass locally.
- Do: breaking changes target `anchor-next`.
- Don't: typo-only PRs; don't let an agent answer review.
- Note: a full `cargo test` needs several GB of disk.
