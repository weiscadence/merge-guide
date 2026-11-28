# tessera

`transparency-dev/tessera` · profile: `merge-kit/repos/transparency-dev__tessera.yaml`

## AI policy

> No AI section in CONTRIBUTING. It does require a Google CLA, an AUTHORS/CONTRIBUTORS commit with your first PR, and: "It's generally best to start by opening a new issue describing the bug or feature you're intending to fix."
> [lit:https://github.com/transparency-dev/tessera/blob/main/CONTRIBUTING.md]

- **Stance:** no AI section in CONTRIBUTING.md
- **Who may write PR text and replies:** not stated
- **Disclosure:** not stated; disclose anyway (a tessera reviewer's own comment used 'Tested with the assistance of an AI coding agent', tessera#1277)
- **Cla:** Google CLA required; first PR adds you to AUTHORS and CONTRIBUTORS
- Source: https://github.com/transparency-dev/tessera/blob/main/CONTRIBUTING.md 'Contributor License Agreement' (fetched 2026-11-25); tessera#1277

## Ready signal

CLA green, CI green, non-draft; issue linked (source: tessera CONTRIBUTING.md)

Open-PR cap: no written cap; our default 2 (source: tessera CONTRIBUTING.md (none stated))

## CI to run locally

```sh
go build ./...
go vet ./...
go test -race ./...
gofmt -l .
```
Note: storage back ends (AWS/GCP/POSIX) are tested by maintainers; say which ones you ran
Source: tessera#1290 PR body (verification commands); tessera#1277 review (the reviewer ran AWS/GCP/POSIX)

## PR body skeleton

```
Fixes #<issue>.

<Problem, change, why this is the root cause.>

Verified: <commands run; which storage back ends>
```

## What reviewers here actually ask for (our data)

Review style: human maintainers; slow (tessera#1277 sat about two weeks)

| class | asks / threads in our data |
|---|---|
| tests | <!--n:profile.tessera.tests--><!--/n--> |

Source: FAILURE-MODES.md (review-harvest counts), general classes

## How a PR gets a reviewer, and what the author must do

- Reviewer: the root CODEOWNERS file names the owning team, and one member is requested when the PR opens. The author requests nobody. (documented: `CODEOWNERS`; observed: tessera#1277, #1290)
- Easy to miss: the CLA check (`cla/google`) and the AUTHORS and CONTRIBUTORS lines in the first PR. Both are in place on our two PRs. (documented: CONTRIBUTING.md; observed: tessera#1277, #1290)
- Easy to miss: the merge state reads "behind" as soon as main moves. Both our branches were two commits behind main on 2026-11-28. (observed: tessera#1277, #1290)

## Our PRs here

<!--n:obs.t.by_repo.transparency_dev_tessera.open--><!--/n--> open (<!--n:obs.prs.transparency_dev_tessera.open--><!--/n-->). On tessera#1277 a maintainer ran the storage back ends and found that reverting the change did not fail any test.

## Typical rounds

Slow: #1277 waited about two weeks for review.

## Do / don't

- Do: issue first and ask to be assigned; include the AUTHORS/CONTRIBUTORS commit.
- Do: run `go test -race` and prove the new test fails on the old code (we did this for #1290).
- Don't: expect hours-scale review.
