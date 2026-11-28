## short
allowed with disclosure
## quote
> "AI assisted PRs: Please indicate whether the PR was AI assisted, and by how much: did you use AI in a limited way or did you completely vibe-code the PR? We welcome AI assisted PRs but need this information to adjust our level of scrutinee during the review". The same template says "avoid AI generated PR descriptions: they tend to be verbose and imprecise".
> [lit:https://github.com/AeneasVerif/aeneas/blob/main/.github/pull_request_template.md]
## ours
<!--n:obs.t.by_repo.aeneasverif_aeneas.open--><!--/n--> open (<!--n:obs.prs.aeneasverif_aeneas.open--><!--/n-->). aeneas#1606 is a new `bvify ... by` tactic for issue #621, opened 2026-11-26. It states that the code, tests and description were AI-written. CI is waiting for a maintainer to approve the run, the branch is one commit behind main, and there is no review yet.
## process
- Reviewer: no one is assigned. A maintainer picks PRs up; two outside authors requested the maintainer who owned the issue. (observed: aeneas#1373, #1386)
- Easy to miss: CI on a fork PR stops at `action_required` until a maintainer approves it, and the branch must be rebased when it falls behind main. The template asks for a short description written by the author and says to avoid AI-written ones. Which checks are required is unknown. (observed: aeneas#1606; documented: `.github/pull_request_template.md`)
## rounds
Sampled merged outside PRs: 6 of 9 got a first review within about 4 days (from about 2 hours to about 4 days); 3 were merged with no review recorded. Time to merge ranged from about 1 hour to about 41 days.
## do
- Do: say how much of the PR was AI-generated, in the PR body (documented: pull_request_template.md).
- Do: keep the description short and exact; the template says AI-written descriptions run verbose (documented: pull_request_template.md).
- Do: for anything beyond a small scoped fix, talk on Zulip or the issue first (documented: README.md, pull_request_template.md).
- Do: expect no reviewer to be assigned; maintainers pick PRs up, and two authors requested the maintainer who owned the issue (observed: #1373, #1386).
- Do: expect a maintainer to approve CI on a fork PR, and rebase when behind (observed: #1606 action_required, BEHIND).
