## short
not stated
## quote
> No AI section in CONTRIBUTING or AGENTS.md (the repo ships an agent guide). One rule: "AI assistance: Do not add a separate AI-attribution line. Use the repo's normal header format and list only the credited author name(s)." Merge rule: "Do not merge `sorry`: `lake exe axiomsweep --check` fails on any `sorryAx` dependency."
> [lit:https://github.com/Verified-zkEVM/VCVio/blob/main/CONTRIBUTING.md]
## ours
No PR. One comment (2026-11-26) on issue VCVio#1154, a list of follow-ups to position binding and hiding for vector commitments, asking whether an item is free for an outside contributor. As of 2026-11-28 there is no reply, no assignee, no label and no linked PR; our comment is the newest event on the issue.
## process
- Reviewer: no one is assigned. A collaborator picks the PR up and merges through the merge queue. After replying, the author can re-request the earlier reviewer. (observed: VCVio#1187)
- Easy to miss: every check on the head commit must pass before the PR is queued, including lint and the downstream builds. A bot checks the title format. A question on an issue may sit for days with no answer. (documented: `CONTRIBUTING.md`; observed: VCVio#1154, #1165, #1187)
## rounds
Unmeasured for us. On 5 sampled merged PRs by repeat contributors the first human comment came after about 3 hours to about 8 days; a collaborator merged each through the merge queue.
## do
- Do: ask on the issue before starting, and expect that a reply may take days (observed: #1154 has had none).
- Do: run `./scripts/update-lib.sh` and `lake exe axiomsweep --check`, and check every check on the head, including lint and downstream builds, before the PR is queued (documented: CONTRIBUTING.md).
- Do: expect no assigned reviewer; a collaborator picks the PR up, and an author can re-request the earlier reviewer after replying (observed: #1187).
- Do: use a `feat(scope): subject` style title; a bot checks it (observed: #1165, #1187, #1215, #1223).
- Don't: add an AI-attribution line to file headers or disable a linter (documented: CONTRIBUTING.md).
