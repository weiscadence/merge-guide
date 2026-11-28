## short
allowed with disclosure
## quote
> "Say so in the PR body — one line is enough (`Made with Claude Code`, or the tool's own `Co-Authored-By:` footer). Much of this repository is expected to be AI-assisted; the disclosure lets reviewers calibrate, not disqualify."
> [lit:https://github.com/teorth/IEANTN/blob/main/CONTRIBUTING.md]
## ours
One open issue (IEANTN#289, wrong journal and wrong locators in node metadata, no statement changes), opened 2026-11-27 with an AI disclosure and an offer to send a PR. No comments, labels or PRs yet. An earlier issue of ours (#271) was closed two days after it was opened, when the owner fixed it in their own PR (#277), merged 13 minutes after that PR was opened.
## process
- Reviewer: CODEOWNERS covers only Vocabulary, workflows and receipts. For anything else no one is requested and the maintainer picks the PR up. (documented: `.github/CODEOWNERS`; observed: IEANTN#220, #247, #263, #270, #274)
- Easy to miss: run `fingerprint` and `gen-challenges` and commit their output, and leave the generated state and graph files out of the commit. An issue may be fixed by the owner's own PR instead of yours. Whether CI on a fork PR needs approval is unknown. (documented: `CONTRIBUTING.md`, `CLAUDE.md`; observed: IEANTN#271, #277)
## rounds
Sampled merged outside PRs: first review was a comment, not a formal review, on most; time to merge ranged from about 3 hours to about 15 days. On one PR the first review came after about 13 hours.
## do
- Do: put a one-line AI disclosure in the PR body (documented: CONTRIBUTING.md).
- Do: comment `claim` on the board issue before starting work; it is a courtesy, not a lock (documented: CONTRIBUTING.md).
- Do: run `fingerprint` and `gen-challenges` and commit their output; leave STATE.md, GRAPH.md, docs/graph.html and docs/nodes/ out of the commit (documented: CONTRIBUTING.md, CLAUDE.md).
- Do: expect no reviewer to be assigned unless you touch Vocabulary, workflows or receipts; the maintainer picks PRs up (documented: .github/CODEOWNERS; observed: #220, #247, #263, #270, #274).
- Don't: edit a conclusion other nodes depend on; add a new version instead (documented: CLAUDE.md).
