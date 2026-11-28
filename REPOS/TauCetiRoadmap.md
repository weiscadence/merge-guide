# TauCetiRoadmap

`TauCetiProject/TauCetiRoadmap` · profile: `merge-kit/repos/TauCetiProject__TauCetiRoadmap.yaml`

## AI policy

> "Attribute AI assistance. Most roadmaps here are written with AI help and that is fine, but unlike the code repository this one is human-curated, so say which models you used, in the PR description. The same goes for review comments written with AI assistance: mark them, conventionally with a :robot: prefix. Nobody should post a roadmap or a review comment they have not read carefully themselves."
> [lit:https://github.com/TauCetiProject/TauCetiRoadmap/blob/main/CONTRIBUTING.md]

- **Stance:** AI use welcome; attribute it
- **Who may write PR text and replies:** AI may write roadmap prose, Suggested.lean and review comments; the author must have read them carefully
- **Disclosure:** required: name the models used in the PR description; mark AI-written review comments with a :robot: prefix
- Source: https://github.com/TauCetiProject/TauCetiRoadmap/blob/main/CONTRIBUTING.md 'Attribute AI assistance' (fetched 2026-11-28)

## Ready signal

Post the awaiting-review label when you open the PR (directly or by a comment line `awaiting-review`) and again after each review round. CODEOWNERS requests the roadmap-reviewers team automatically, a bot arms auto-merge, and one approval from a team member plus a green build merges it. Ask for review on the Lean Zulip topic 'Getting started: roadmaps'. (source: CONTRIBUTING.md 'Opening a pull request', 'The review workflow: labels'; .github/CODEOWNERS; .github/workflows/auto-merge.yml)

Open-PR cap: no written cap; our default 2 (source: TauCetiRoadmap CONTRIBUTING.md (none stated))

## CI to run locally

```sh
lake exe cache get
lake build
python3 .github/scripts/check_roadmap_topics.py
python3 .github/scripts/check_roadmap_areas.py --fix (then discard the result)
```
Note: Suggested.lean may use sorry honestly; the build check fails without a metadata.toml topic; a branch need not be up to date (merge queue tests the merge)
Source: README.md 'Building', 'Filing a roadmap'; CONTRIBUTING.md 'Opening a pull request'; .github/workflows/ci.yml (fetched 2026-11-28)

## PR body skeleton

```
<What roadmap this adds or revises, and its directory.>

## Checks
<What was run and what was not.>

## Subject-area expert
<Who could confirm the scope, or "needed: ...".>

## AI assistance
<Models used and what they did; what the human decided.>
```

## What reviewers here actually ask for (our data)

Review style: a roadmap-reviewers member comments within about an hour, a bot applies the AI-review label, then one member approval plus green build merges through the queue; first-comment latency 30 minutes to 6 hours on 5 sampled PRs (all by org members)

None recorded: no review has landed on our PR yet.

Source: TauCetiRoadmap#3074, #3081, #3170, #3182, #3189 timelines; #3243 (fetched 2026-11-28)

## How a PR gets a reviewer, and what the author must do

- Reviewer: CODEOWNERS requests the roadmap-reviewers team when the PR opens. One team approval plus a green `build` check merges it through the merge queue. (documented: `CODEOWNERS`, `CONTRIBUTING.md`; observed: TauCetiRoadmap#3243, #3189, #3182)
- Easy to miss: the author sets `awaiting-review` at open and again after each round of replies; a push does not move the label. Being behind `main` is fine because the queue tests the merge. The guide also suggests asking on Zulip for someone who can check the mathematics. A `progress-merge` run shows `startup_failure` on our PR; the cause is unknown and `build` is the check that counts. (documented: `CONTRIBUTING.md`; observed: TauCetiRoadmap#3243)

## Our PRs here

<!--n:obs.t.by_repo.taucetiproject_taucetiroadmap.landed-->2<!--/n--> landed (<!--n:obs.prs.taucetiproject_taucetiroadmap.landed-->TauCetiRoadmap#117, #2112<!--/n-->), <!--n:obs.t.by_repo.taucetiproject_taucetiroadmap.closed-->1<!--/n--> closed (<!--n:obs.prs.taucetiproject_taucetiroadmap.closed-->TauCetiRoadmap#122<!--/n-->), <!--n:obs.t.by_repo.taucetiproject_taucetiroadmap.open-->3<!--/n--> open (<!--n:obs.prs.taucetiproject_taucetiroadmap.open-->TauCetiRoadmap#3243, #3248, #3249<!--/n-->). TauCetiRoadmap#3243 (2026-11-27) is a new `ZerosOfOrthogonalPolynomials` roadmap with README, `Suggested.lean` and `metadata.toml`. The `build` check is green, `awaiting-review` is applied, the review team was requested automatically and a bot armed auto-merge. No human comment yet. The branch is 12 commits behind `main`, which is allowed because a merge queue tests the merge.

## Typical rounds

Unmeasured for our PR. On 5 sampled merged PRs (all by org members) a reviewer commented within about 30 minutes to 6 hours; merges followed in about 19 hours to 3.5 days.

## Do / don't

- Do: apply `awaiting-review` when you open, and again after each round of replies; pushes do not move it (documented: CONTRIBUTING.md 'The review workflow: labels').
- Do: expect the roadmap-reviewers team to be requested for you; one team approval plus green `build` merges the PR (documented: CODEOWNERS, CONTRIBUTING.md; observed: #3243, #3189, #3182).
- Do: add `metadata.toml` with a valid `topic` and touch only your own directory (documented: CONTRIBUTING.md; `build` fails otherwise).
- Do: name the models in the PR description, mark AI-written review comments with a robot prefix, and say who could check the mathematics (documented: CONTRIBUTING.md).
- Don't: write "optional", "deferred" or the history of the draft in the README, or edit the generated roadmap lists (documented: README.md 'Writing a roadmap').
