## short
not stated
## quote
> No AI section in CONTRIBUTING. It does require a Google CLA, an AUTHORS/CONTRIBUTORS commit with your first PR, and: "It's generally best to start by opening a new issue describing the bug or feature you're intending to fix."
> [lit:https://github.com/transparency-dev/tessera/blob/main/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.transparency_dev_tessera.open--><!--/n--> open (<!--n:obs.prs.transparency_dev_tessera.open--><!--/n-->). On tessera#1277 a maintainer ran the storage back ends and found that reverting the change did not fail any test.
## rounds
Slow: #1277 waited about two weeks for review.
## do
- Do: issue first and ask to be assigned; include the AUTHORS/CONTRIBUTORS commit.
- Do: run `go test -race` and prove the new test fails on the old code (we did this for #1290).
- Don't: expect hours-scale review.
