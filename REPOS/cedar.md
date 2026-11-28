# cedar

`cedar-policy/cedar` · profile: `merge-kit/repos/cedar-policy__cedar.yaml`

## AI policy

> No AI section in CONTRIBUTING.md. It says "Only submit your own work (or work you have sufficient rights to submit)" and asks for a changelog entry: "Add your entry under the 'Unreleased' section, as part of the same PR that introduces the change."
> [lit:https://github.com/cedar-policy/cedar/blob/main/CONTRIBUTING.md]

- **Stance:** no AI policy found; CONTRIBUTING says only submit your own work or work you have the rights to submit
- **Who may write PR text and replies:** not stated
- **Disclosure:** not stated; disclose anyway
- **Cla:** no CLA; a DCO check runs on the PR (sign off commits with git commit -s); CONTRIBUTING says you will be asked to confirm licensing
- Source: https://github.com/cedar-policy/cedar/blob/main/CONTRIBUTING.md 'First Things First' and 'Licensing' (fetched 2026-11-28); cedar#2736 DCO check

## Ready signal

a maintainer requests reviewers; authors cannot. The ruleset needs 2 approvals and code-owner review. Before that: DCO green, changelog entry added, template filled, and a maintainer approves the CI run on a fork PR (source: cedar CONTRIBUTING.md; ruleset on main; cedar#2736 timeline; sampled merged PRs)

Open-PR cap: no written cap; our default 2 (source: cedar CONTRIBUTING.md (none stated))

## CI to run locally

```sh
cargo build
cargo test
cargo test -p cedar-policy-cli --all-features
cargo clippy --all-features
cargo fmt --all --check
```
Note: CI on a fork PR waits for a maintainer to approve the run (cedar#2736 showed action_required); CI also checks coverage and semver
Source: https://github.com/cedar-policy/cedar/blob/main/.github/workflows/build_and_test.yml (fetched 2026-11-28); cedar#2736

## PR body skeleton

```
## Description of changes

<Problem, change, how tested.>

## Issue #, if available

Fixes #<issue>

## Checklist for requesting a review

<Keep one option per group; delete the rest.>
```

## What reviewers here actually ask for (our data)

Review style: human maintainers; a maintainer requests reviewers; first review took about 2 to 5 days on most sampled PRs, one took about 30

None recorded: no review has landed on our work here yet.

Source: cedar#2735, #2638, #2651, #2713, #2726, #2696

## How a PR gets a reviewer, and what the author must do

- Reviewer: a maintainer requests the reviewers; nothing does it at open. Whether a CODEOWNERS file plays a part is unknown. (observed: cedar#2735, #2713, #2726)
- Easy to miss: CI on a fork PR stops at `action_required` until a maintainer approves it. The DCO check does run, so the commit needs a `Signed-off-by` line; whether DCO blocks the merge is unknown. The changelog entry goes in the same PR. (observed: cedar#2736; documented: `CONTRIBUTING.md`)

## Our PRs here

<!--n:obs.t.by_repo.cedar_policy_cedar.open-->1<!--/n--> open (<!--n:obs.prs.cedar_policy_cedar.open-->cedar#2736<!--/n-->). cedar#2736 is a CLI fix for issue #2732, opened 2026-11-27. It has the changelog entry, a filled template and a green DCO check. CI is waiting for a maintainer to approve the run, and no reviewer has been requested yet.

## Typical rounds

Sampled merged outside PRs: first review came after about 1.6 to 5 days on 5 of 6, and after about 30 days on one. Merge came 1.6 to 37 days after opening.

## Do / don't

- Do: add a changelog line under Unreleased in the crate you changed, in the same PR (documented: CONTRIBUTING.md; observed: #2638, #2651, #2713, #2696).
- Do: keep the PR template, pick one option per group, delete the rest (documented: PULL_REQUEST_TEMPLATE.md).
- Do: sign off the commit; a DCO check runs (observed: #2736).
- Do: expect a maintainer to request reviewers and to approve CI on a fork PR (observed: #2736 action_required; #2735, #2713, #2726 reviewer requests came from maintainers).
- Don't: skip the issue for anything beyond a trivial change (documented: CONTRIBUTING.md 'First Things First').
