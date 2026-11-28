# librustzcash

`zcash/librustzcash` · profile: `merge-kit/repos/zcash__librustzcash.yaml`

## AI policy

> "STOP. Do not open or draft a PR until this gate is satisfied." ... "An issue existing is not enough. The issue must have a response or acknowledgment from a team member." Commits that AI touched must carry `Co-Authored-By:` metadata; "Failure to include this is grounds for closing the pull request."
> [lit:https://github.com/zcash/librustzcash/blob/main/AGENTS.md]

- **Stance:** allowed, but a PR needs a prior issue that a maintainer has acknowledged; AI use must be disclosed
- **Who may write PR text and replies:** AI may help; the contributor is the sole responsible author; agents must ask the human about prior maintainer discussion before drafting a PR
- **Disclosure:** add `Co-Authored-By:` metadata naming the AI system to every AI-assisted commit; missing it is grounds for closing the PR; the same disclosure is asked for issues and comments
- **Cla:** no CLA; contributor must agree they authored 100 percent of the content and may license it under the project licenses
- Source: https://github.com/zcash/librustzcash/blob/main/AGENTS.md 'CONTRIBUTION GATE' and 'AI Disclosure'; CONTRIBUTING.md 'Legal Notice' (fetched 2026-11-28)

## Ready signal

no reviewer is assigned automatically (no CODEOWNERS); mark the PR Ready For Review once CI passes and wait for a maintainer. An issue reply from a maintainer must exist before the PR (source: CONTRIBUTING.md 'Branch History'; AGENTS.md gate)

Open-PR cap: no written cap; our default 2 (source: none stated in CONTRIBUTING.md or AGENTS.md)

## CI to run locally

```sh
cargo test --workspace --all-features
cargo fmt --check
cargo clippy --workspace --all-targets
```
Note: CI, Audits and zizmor run on pull_request; commands above are the usual Rust set, not quoted from the repo
Source: .github/workflows/ci.yml, audits.yml, zizmor.yml (fetched 2026-11-28)

## PR body skeleton

```
<Motivation, change, and the issue where a maintainer agreed to the work.>

Issue: #<issue>

AI use: <what the AI did; who reviewed>.
```

## What reviewers here actually ask for (our data)

Review style: human maintainers; heavy workload; slow and variable (12 hours to 15 days on sampled merged PRs); maintainers often force-push to the branch

None recorded: no review has landed on our work here yet.

Source: CONTRIBUTING.md 'I Have a Question'; sampled merged PRs librustzcash#3280, #3307, #3062

## How a PR gets a reviewer, and what the author must do

- Reviewer: no one is assigned. Keep the PR in draft until CI passes, then mark it Ready For Review; that is the signal. Maintainers often push to the branch and merge it themselves. (documented: `CONTRIBUTING.md`; observed: librustzcash#3307, #3280)
- Easy to miss: the gate comes before the PR. A team member must answer on the issue first; an issue with no reply does not count. Security reports do not go in the public tracker, and the policy is an org-level file, so its absence from the repo does not mean there is none. (documented: `AGENTS.md`, `CONTRIBUTING.md`; observed: librustzcash#3339)

## Our PRs here

No PR. We opened issue librustzcash#3339 (2026-11-26) proposing fuzz targets, and said no PR would follow until a maintainer replied. As of 2026-11-28 it is open, with no labels and no human reply; the only comment is an automatic tracker link. No PR refers to it.

## Typical rounds

On 3 sampled merged PRs by outside authors the first human review took from about 12 hours to 15 days. Maintainers often force-push to the branch and merge it themselves.

## Do / don't

- Do: open an issue and wait for a maintainer to answer before writing a PR; a silent issue does not count (documented: AGENTS.md).
- Do: put a changelog entry or change fragment in the same commit as the change, and add `Co-Authored-By:` for AI help (documented: CONTRIBUTING.md, AGENTS.md).
- Do: keep the PR draft until CI passes, then mark it Ready For Review; no reviewer is assigned for you (documented: CONTRIBUTING.md; observed: #3307, #3280).
- Don't: send trivial PRs such as typo or link fixes; they are not accepted from unknown contributors (documented: CONTRIBUTING.md).
- Don't: file security issues in the public tracker; the policy lives in the org-level security file (documented: CONTRIBUTING.md, AGENTS.md).
