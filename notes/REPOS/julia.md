## short
allowed with disclosure
## quote
> "If your pull request contains substantive contributions from a generative AI tool, please disclose so with details, and review all changes before opening. This also applies to other content, such as issues, discussions, and comments." AGENTS.md adds a commit trailer `Assisted-by: <tool> (<model>)` and: "Agents can only open PRs or post comments once the human user gives them explicit permission."
> [lit:https://github.com/JuliaLang/julia/blob/master/CONTRIBUTING.md]
## ours
No PR. We commented once on julia#64271 (2026-11-26) offering a fix for `round(Float16, x)`, with an AI disclosure line. As of 2026-11-28 the issue is open, assigned to someone else, and has no reply and no linked PR.
## process
- Reviewer: there is no auto-assign. A committer reviews or requests a reviewer. (observed: julia#65072, #64990)
- Easy to miss: no need to ask or claim an issue first; the guide says to open the PR. An issue assigned to someone else is a sign to check with them before starting. A `needs *` label left on the PR fails a check at merge time. Whether a small fix needs a NEWS.md entry is unknown. (documented: `CONTRIBUTING.md`, `.github/workflows/LabelCheck.yml`; observed: julia#64271)
## rounds
On 6 sampled merged PRs the first human response came within about 1 hour to 14 hours; one tiny doc fix was merged with no review.
## do
- Do: just open the PR; contributors are told there is no need to ask or claim an issue first (documented: CONTRIBUTING.md 'Working on issues').
- Do: end each AI-touched commit with `Assisted-by: <tool> (<model>)` and disclose AI use with details in the PR text (documented: AGENTS.md, CONTRIBUTING.md).
- Do: expect a committer to review or request a reviewer; there is no auto-assign (observed: #65072, #64990).
- Don't: leave a `needs *` label on at merge time; a check fails on it (documented: LabelCheck.yml).
- Don't: let a tool open the PR without the human's permission (documented: AGENTS.md, CONTRIBUTING.md).
