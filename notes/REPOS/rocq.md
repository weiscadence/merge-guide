## short
allowed with disclosure
## quote
> "AI assistance is permitted in Rocq and its satellite projects. Contributors and maintainers remain responsible for their work" ... "Be transparent. Disclose how you used an AI, not which agent or model you used." Reviewers are requested by CODEOWNERS; only a maintainer can run the full CI.
> [lit:https://rocq-prover.org/policies/ai-policy]
## ours
<!--n:obs.t.by_repo.rocq_prover_rocq.open--><!--/n--> open (<!--n:obs.prs.rocq_prover_rocq.open--><!--/n-->). rocq#22942 (opened 2026-11-28, one commit, not draft, branch not behind). The CODEOWNERS bot requested two maintainer teams and added `needs: full CI`. GitHub Actions passed; the GitLab pipeline is `neutral` (light CI only). No review, assignee, milestone or `kind:` label yet. We cannot add labels or request full CI.
## process
- Reviewer: a bot reads CODEOWNERS and requests the maintainer teams when the PR opens. One of them becomes the assignee and does the merge. The author cannot self-assign. (documented: `CONTRIBUTING.md`; observed: rocq#22942, #22926, #22869)
- Easy to miss: an outside PR gets light CI only, and the bot adds `needs: full CI`. Only a maintainer can start the full run, so a green mark here is not the full test. If nothing happens for a few days, the contributing guide allows a ping to the requested maintainers. Milestone and `kind:` label come from the assignee. (documented: `CONTRIBUTING.md`; observed: rocq#22942)
## rounds
On 4 sampled merged PRs by outside or occasional authors, the first review came after about 2 to 3 hours on three, and after 3 days on one.
## do
- Do: fill the PR template, link the issue with `Fixes #N`, and add a test-suite case (documented: PULL_REQUEST_TEMPLATE.md, CONTRIBUTING.md).
- Do: add a changelog entry only for features, user-visible changes and important bug fixes; small fixes do not need one (documented: doc/changelog/README.md).
- Do: let CODEOWNERS request reviewers; wait a few days, then ping the requested maintainers. You cannot self-assign or merge (documented: CONTRIBUTING.md; observed: #22926, #22869).
- Don't: expect the `kind:` label, milestone or full CI to come from you; the assignee sets them (observed: #22926, #22873, #22869).
- Don't: bother naming the model in the disclosure; the policy asks how the AI was used, not which model (documented: AI policy).
