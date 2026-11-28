## short
allowed with disclosure
## quote
> "Any use of AI tools for preparing code, documentation, tests, commit messages, pull requests, issue comments, or reviews for this repository must be disclosed." Also: "Agents can only open PRs or post comments once the human user gives them explicit permission." Commits get the trailer `Assisted-by: Generative AI`.
> [lit:https://github.com/gap-system/gap/blob/master/AGENTS.md]
## ours
<!--n:obs.t.by_repo.gap_system_gap.open--><!--/n--> open (<!--n:obs.prs.gap_system_gap.open--><!--/n-->). gap#6905: one commit, not draft, branch not behind. Opened 2026-11-27. As of 2026-11-28 no review, no labels, no comments, and all four workflows (CI, CI with GAP.jl, Lint, Wrap releases) sit at `action_required` until a maintainer approves the first-time run.
## process
- Reviewer: no one is assigned for you and there is no CODEOWNERS file. A maintainer picks the PR up, labels it and reviews it. Do not ask for a reviewer by name. (documented: `AGENTS.md`; observed: gap#6889, #6780, #6190)
- Easy to miss: on a first fork PR every workflow stops at `action_required` until a maintainer approves the run, so "no red marks" means nothing ran. How that approval gets asked for is unknown. The release-notes labels are set by maintainers; the author's part is the "Text for release notes" section in the body. (observed: gap#6905; documented: `.github/pull_request_template.md`)
## rounds
First human response on 8 sampled merged PRs by outside contributors ranged from about 2.5 hours to 3.5 days. In most of them a maintainer labelled and reviewed without being asked.
## do
- Do: keep the PR template's "Text for release notes" section; write "see title" and make the title a self-contained user-facing sentence (documented: AGENTS.md, pull_request_template.md).
- Do: end every AI-touched commit with `Assisted-by: Generative AI` and add a short AI note to the PR body (documented: AGENTS.md).
- Do: expect to wait. No reviewer is assigned automatically; a maintainer picks PRs up, applies the `release notes:`, `kind:` and `topic:` labels, and approves first-time CI runs (observed: gap#6889, #6780, #6190).
- Don't: ask for a reviewer by name or edit CHANGES.md; the file is generated from titles (documented: AGENTS.md).
- Don't: open a PR or post a comment before the human has said so (documented: AGENTS.md).
