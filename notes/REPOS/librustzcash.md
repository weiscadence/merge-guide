## short
allowed; maintainer sign-off on an issue first
## quote
> "STOP. Do not open or draft a PR until this gate is satisfied." ... "An issue existing is not enough. The issue must have a response or acknowledgment from a team member." Commits that AI touched must carry `Co-Authored-By:` metadata; "Failure to include this is grounds for closing the pull request."
> [lit:https://github.com/zcash/librustzcash/blob/main/AGENTS.md]
## ours
No PR. We opened issue librustzcash#3339 (2026-11-26) proposing fuzz targets, and said no PR would follow until a maintainer replied. As of 2026-11-28 it is open, with no labels and no human reply; the only comment is an automatic tracker link. No PR refers to it.
## process
- Reviewer: no one is assigned. Keep the PR in draft until CI passes, then mark it Ready For Review; that is the signal. Maintainers often push to the branch and merge it themselves. (documented: `CONTRIBUTING.md`; observed: librustzcash#3307, #3280)
- Easy to miss: the gate comes before the PR. A team member must answer on the issue first; an issue with no reply does not count. Security reports do not go in the public tracker, and the policy is an org-level file, so its absence from the repo does not mean there is none. (documented: `AGENTS.md`, `CONTRIBUTING.md`; observed: librustzcash#3339)
## rounds
On 3 sampled merged PRs by outside authors the first human review took from about 12 hours to 15 days. Maintainers often force-push to the branch and merge it themselves.
## do
- Do: open an issue and wait for a maintainer to answer before writing a PR; a silent issue does not count (documented: AGENTS.md).
- Do: put a changelog entry or change fragment in the same commit as the change, and add `Co-Authored-By:` for AI help (documented: CONTRIBUTING.md, AGENTS.md).
- Do: keep the PR draft until CI passes, then mark it Ready For Review; no reviewer is assigned for you (documented: CONTRIBUTING.md; observed: #3307, #3280).
- Don't: send trivial PRs such as typo or link fixes; they are not accepted from unknown contributors (documented: CONTRIBUTING.md).
- Don't: file security issues in the public tracker; the policy lives in the org-level security file (documented: CONTRIBUTING.md, AGENTS.md).
