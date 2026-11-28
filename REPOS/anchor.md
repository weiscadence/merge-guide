# anchor

`otter-sec/anchor` · profile: `merge-kit/repos/otter-sec__anchor.yaml`

## AI policy

> "You may use an LLM to help draft your PR description. However, we'd encourage you to write out the majority of the description by hand." · "Please do not use LLMs to autonomously respond to PR feedback (this includes blindly copy-pasting responses)."
> [lit:https://github.com/otter-sec/anchor/blob/master/CONTRIBUTING.md]

- **Stance:** DISCLOSE / restrict replies
- **Who may write PR text and replies:** LLM may help draft the PR description but 'write out the majority of the description by hand'; 'do not use LLMs to autonomously respond to PR feedback'
- **Disclosure:** not mandated in writing
- Source: https://github.com/otter-sec/anchor/blob/master/CONTRIBUTING.md lines 52-53 (gh api 2026-11-25)

## Ready signal

move the draft to ready for review after build/test/fmt/lint pass locally (source: anchor CONTRIBUTING.md lines 41, 51)

Open-PR cap: no written cap; 'submit a draft PR asap' (source: anchor CONTRIBUTING.md line 41)

## CI to run locally

```sh
cargo build
yarn build
cargo test
yarn test
anchor test
cargo fmt --check
cargo clippy
```
Source: anchor CONTRIBUTING.md 'Building and Testing Locally' lines 90-130, line 51

## PR body skeleton

```
<Concise, hand-written: problem, change, tests (including adversarial ones).>
```

## What reviewers here actually ask for (our data)

Review style: human maintainers

None recorded: anchor#5360 landed with zero friction.

Source: FAILURE-MODES.md (review-harvest counts), general classes

## How a PR gets a reviewer, and what the author must do

- Reviewer: the CODEOWNERS file requests the three code owners when the PR opens. On anchor#5366 the two approvals came from other team members, and the PR stayed "review required" after both. (documented: `.github/CODEOWNERS`; observed: anchor#5366)
- Easy to miss: the changelog line cites the PR number, not the issue number. A reviewer fixed ours with a suggestion. (observed: anchor#5366)
- **Not yours to fix:** the three Vercel checks fail on a fork PR until a team member authorizes the deploy. (observed: anchor#5366)

## Our PRs here

<!--n:obs.t.by_repo.otter_sec_anchor.landed-->1<!--/n--> landed (<!--n:obs.prs.otter_sec_anchor.landed-->anchor#5360<!--/n-->), <!--n:obs.t.by_repo.otter_sec_anchor.open-->1<!--/n--> open (<!--n:obs.prs.otter_sec_anchor.open-->anchor#5366<!--/n-->). anchor#5360 had no asks and a human merge.

## Typical rounds

Zero asks on the landed PR.

## Do / don't

- Do: open a draft early, then mark ready after build, test, fmt and clippy pass locally.
- Do: breaking changes target `anchor-next`.
- Don't: typo-only PRs; don't let an agent answer review.
- Note: a full `cargo test` needs several GB of disk.
