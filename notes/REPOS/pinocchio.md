## short
not stated
## quote
> No AI section and no CONTRIBUTING file. No PR template either. The only workflow rule that matters: CI runs on `pull_request`, and release notes are built from commit subjects (git-cliff).
> [lit:https://github.com/anza-xyz/pinocchio]
## ours
<!--n:obs.t.by_repo.anza_xyz_pinocchio.open--><!--/n--> open (<!--n:obs.prs.anza_xyz_pinocchio.open--><!--/n-->). pinocchio#472 was opened as a draft on 2026-11-28 for issue #471. CI is waiting for a maintainer to approve the run. A maintainer suggested a different fix (heap variant) on the issue; the PR body says why it took another route and offers to switch. No review yet.
## process
- Reviewer: no one is assigned. There is no CODEOWNERS file and no bot; a maintainer picks PRs up, and most sampled merged PRs never had a reviewer request. (observed: pinocchio#429, #434, #435)
- Easy to miss: a draft PR is not looked at; mark it ready when the work is done. CI on a fork PR stops at `action_required` until a maintainer approves it. If a maintainer proposed an approach on the issue, answer there before or when opening. (observed: pinocchio#472, issue #471)
## rounds
Slow and uneven. On 8 sampled merged outside PRs, first review took from under 1 hour to about 48 days; 4 of 8 came within a week. 28 PRs are open and waiting.
## do
- Do: read the issue thread first; a maintainer's suggested approach is the one likely to be accepted (observed: #471).
- Do: start the title with the area, such as `programs:` or `sdk:` (observed: #445, #446, #458).
- Do: expect to wait for a maintainer to approve the CI run on a fork PR (observed: #472 action_required).
- Do: mark the PR ready when the work is done; nothing documented says otherwise, and every sampled merged PR was non-draft (observed: #429, #434, #435).
- Don't: expect a reviewer to be assigned; no CODEOWNERS file or bot does it (observed: 5 of 8 sampled PRs had no reviewer request).
