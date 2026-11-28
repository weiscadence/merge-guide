## short
allowed, attribute models
## quote
> "Attribute AI assistance. Most roadmaps here are written with AI help and that is fine, but unlike the code repository this one is human-curated, so say which models you used, in the PR description. The same goes for review comments written with AI assistance: mark them, conventionally with a :robot: prefix. Nobody should post a roadmap or a review comment they have not read carefully themselves."
> [lit:https://github.com/TauCetiProject/TauCetiRoadmap/blob/main/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.taucetiproject_taucetiroadmap.landed--><!--/n--> landed (<!--n:obs.prs.taucetiproject_taucetiroadmap.landed--><!--/n-->), <!--n:obs.t.by_repo.taucetiproject_taucetiroadmap.closed--><!--/n--> closed (<!--n:obs.prs.taucetiproject_taucetiroadmap.closed--><!--/n-->), <!--n:obs.t.by_repo.taucetiproject_taucetiroadmap.open--><!--/n--> open (<!--n:obs.prs.taucetiproject_taucetiroadmap.open--><!--/n-->). TauCetiRoadmap#3243 (2026-11-27) is a new `ZerosOfOrthogonalPolynomials` roadmap with README, `Suggested.lean` and `metadata.toml`. The `build` check is green, `awaiting-review` is applied, the review team was requested automatically and a bot armed auto-merge. No human comment yet. The branch is 12 commits behind `main`, which is allowed because a merge queue tests the merge.
## process
- Reviewer: CODEOWNERS requests the roadmap-reviewers team when the PR opens. One team approval plus a green `build` check merges it through the merge queue. (documented: `CODEOWNERS`, `CONTRIBUTING.md`; observed: TauCetiRoadmap#3243, #3189, #3182)
- Easy to miss: the author sets `awaiting-review` at open and again after each round of replies; a push does not move the label. Being behind `main` is fine because the queue tests the merge. The guide also suggests asking on Zulip for someone who can check the mathematics. A `progress-merge` run shows `startup_failure` on our PR; the cause is unknown and `build` is the check that counts. (documented: `CONTRIBUTING.md`; observed: TauCetiRoadmap#3243)
## rounds
Unmeasured for our PR. On 5 sampled merged PRs (all by org members) a reviewer commented within about 30 minutes to 6 hours; merges followed in about 19 hours to 3.5 days.
## do
- Do: apply `awaiting-review` when you open, and again after each round of replies; pushes do not move it (documented: CONTRIBUTING.md 'The review workflow: labels').
- Do: expect the roadmap-reviewers team to be requested for you; one team approval plus green `build` merges the PR (documented: CODEOWNERS, CONTRIBUTING.md; observed: #3243, #3189, #3182).
- Do: add `metadata.toml` with a valid `topic` and touch only your own directory (documented: CONTRIBUTING.md; `build` fails otherwise).
- Do: name the models in the PR description, mark AI-written review comments with a robot prefix, and say who could check the mathematics (documented: CONTRIBUTING.md).
- Don't: write "optional", "deferred" or the history of the draft in the README, or edit the generated roadmap lists (documented: README.md 'Writing a roadmap').
