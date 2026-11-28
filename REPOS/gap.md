# gap

`gap-system/gap` · profile: `merge-kit/repos/gap-system__gap.yaml`

## AI policy

> "Any use of AI tools for preparing code, documentation, tests, commit messages, pull requests, issue comments, or reviews for this repository must be disclosed." Also: "Agents can only open PRs or post comments once the human user gives them explicit permission." Commits get the trailer `Assisted-by: Generative AI`.
> [lit:https://github.com/gap-system/gap/blob/master/AGENTS.md]

- **Stance:** AI use is allowed if disclosed; AGENTS.md sets three rules
- **Who may write PR text and replies:** an agent may write code and text; it may open PRs or post comments only after the human gives explicit permission
- **Disclosure:** end every AI-touched commit with the trailer `Assisted-by: Generative AI` (no tool or model name, no Co-authored-by); add a brief note in the PR, issue comment or review saying AI was used and how
- Source: https://github.com/gap-system/gap/blob/master/AGENTS.md 'AI disclosure' (fetched 2026-11-28)

## Ready signal

no reviewer is requested automatically (no CODEOWNERS); a maintainer picks the PR up, labels it and reviews it. A first-time contributor's CI waits for a maintainer to approve it. Do not use a reviewer request as the signal; ask on Slack if nothing happens (source: gap#6889, #6780, #6788 (maintainer triage without a request); CONTRIBUTING.md 'Contact')

Open-PR cap: no written cap; our default 2 (source: none stated in CONTRIBUTING.md or AGENTS.md)

## CI to run locally

```sh
make check
./gap tst/testinstall.g
```
Note: CI (CI, CI with GAP.jl, Lint, Wrap releases) runs on pull_request; a first-time contributor's runs wait as action_required until a maintainer approves them (gap#6905)
Source: AGENTS.md 'Run tests'; gap#6905 workflow runs (fetched 2026-11-28)

## PR body skeleton

```
<Short summary of the change and why.>

Fixes #<issue>

AI assistance was used to prepare <what: code, tests, this text>.

## Text for release notes

see title
```

## What reviewers here actually ask for (our data)

Review style: human core developers with write access; one approving review is required before merge; first response in 8 sampled merged PRs took from about 2.5 hours to 3.5 days

None recorded: no review has landed on our work here yet.

Source: CONTRIBUTING.md 'The reviewing process'; sampled merged PRs gap#6889, #6780, #6788, #6521, #6441, #6190, #6668, #6725

## How a PR gets a reviewer, and what the author must do

- Reviewer: no one is assigned for you and there is no CODEOWNERS file. A maintainer picks the PR up, labels it and reviews it. Do not ask for a reviewer by name. (documented: `AGENTS.md`; observed: gap#6889, #6780, #6190)
- Easy to miss: on a first fork PR every workflow stops at `action_required` until a maintainer approves the run, so "no red marks" means nothing ran. How that approval gets asked for is unknown. The release-notes labels are set by maintainers; the author's part is the "Text for release notes" section in the body. (observed: gap#6905; documented: `.github/pull_request_template.md`)

## Our PRs here

<!--n:obs.t.by_repo.gap_system_gap.open-->1<!--/n--> open (<!--n:obs.prs.gap_system_gap.open-->gap#6905<!--/n-->). gap#6905: one commit, not draft, branch not behind. Opened 2026-11-27. As of 2026-11-28 no review, no labels, no comments, and all four workflows (CI, CI with GAP.jl, Lint, Wrap releases) sit at `action_required` until a maintainer approves the first-time run.

## Typical rounds

First human response on 8 sampled merged PRs by outside contributors ranged from about 2.5 hours to 3.5 days. In most of them a maintainer labelled and reviewed without being asked.

## Do / don't

- Do: keep the PR template's "Text for release notes" section; write "see title" and make the title a self-contained user-facing sentence (documented: AGENTS.md, pull_request_template.md).
- Do: end every AI-touched commit with `Assisted-by: Generative AI` and add a short AI note to the PR body (documented: AGENTS.md).
- Do: expect to wait. No reviewer is assigned automatically; a maintainer picks PRs up, applies the `release notes:`, `kind:` and `topic:` labels, and approves first-time CI runs (observed: gap#6889, #6780, #6190).
- Don't: ask for a reviewer by name or edit CHANGES.md; the file is generated from titles (documented: AGENTS.md).
- Don't: open a PR or post a comment before the human has said so (documented: AGENTS.md).
