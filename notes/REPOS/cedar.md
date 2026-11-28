## short
not stated
## quote
> No AI section in CONTRIBUTING.md. It says "Only submit your own work (or work you have sufficient rights to submit)" and asks for a changelog entry: "Add your entry under the 'Unreleased' section, as part of the same PR that introduces the change."
> [lit:https://github.com/cedar-policy/cedar/blob/main/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.cedar_policy_cedar.open--><!--/n--> open (<!--n:obs.prs.cedar_policy_cedar.open--><!--/n-->). cedar#2736 is a CLI fix for issue #2732, opened 2026-11-27. It has the changelog entry, a filled template and a green DCO check. CI is waiting for a maintainer to approve the run, and no reviewer has been requested yet.
## process
- Reviewer: a maintainer requests the reviewers; nothing does it at open. Whether a CODEOWNERS file plays a part is unknown. (observed: cedar#2735, #2713, #2726)
- Easy to miss: CI on a fork PR stops at `action_required` until a maintainer approves it. The DCO check does run, so the commit needs a `Signed-off-by` line; whether DCO blocks the merge is unknown. The changelog entry goes in the same PR. (observed: cedar#2736; documented: `CONTRIBUTING.md`)
## rounds
Sampled merged outside PRs: first review came after about 1.6 to 5 days on 5 of 6, and after about 30 days on one. Merge came 1.6 to 37 days after opening.
## do
- Do: add a changelog line under Unreleased in the crate you changed, in the same PR (documented: CONTRIBUTING.md; observed: #2638, #2651, #2713, #2696).
- Do: keep the PR template, pick one option per group, delete the rest (documented: PULL_REQUEST_TEMPLATE.md).
- Do: sign off the commit; a DCO check runs (observed: #2736).
- Do: expect a maintainer to request reviewers and to approve CI on a fork PR (observed: #2736 action_required; #2735, #2713, #2726 reviewer requests came from maintainers).
- Don't: skip the issue for anything beyond a trivial change (documented: CONTRIBUTING.md 'First Things First').
