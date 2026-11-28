# VCVio

`Verified-zkEVM/VCVio` · profile: `merge-kit/repos/Verified-zkEVM__VCVio.yaml`

## AI policy

> No AI section in CONTRIBUTING or AGENTS.md (the repo ships an agent guide). One rule: "AI assistance: Do not add a separate AI-attribution line. Use the repo's normal header format and list only the credited author name(s)." Merge rule: "Do not merge `sorry`: `lake exe axiomsweep --check` fails on any `sorryAx` dependency."
> [lit:https://github.com/Verified-zkEVM/VCVio/blob/main/CONTRIBUTING.md]

- **Stance:** no AI section; repo ships an agent guide (AGENTS.md, docs/agents/)
- **Who may write PR text and replies:** not stated
- **Disclosure:** not stated; one rule: 'Do not add a separate AI-attribution line' in file headers. Disclose in the PR body anyway
- Source: https://github.com/Verified-zkEVM/VCVio/blob/main/CONTRIBUTING.md 'Attribution And File Headers' item 5 and AGENTS.md (fetched 2026-11-28)

## Ready signal

No reviewer is assigned (no CODEOWNERS, no auto-assign). Open non-draft, or mark ready_for_review, with every check green on the head; a collaborator picks it up, then enqueues it in the merge queue. After replying to review, re-request the earlier reviewer (observed on #1187). (source: CONTRIBUTING.md 'Pull Request Checks And Merge Queue'; VCVio#1123, #1165, #1187, #1215, #1223 timelines)

Open-PR cap: no written cap; our default 2 (source: VCVio CONTRIBUTING.md (none stated))

## CI to run locally

```sh
lake exe cache get && lake build
./scripts/update-lib.sh
lake exe axiomsweep --check
lake lint -- --env-only
lake exe lint-style <libs>
uv run --no-project --python 3.12 python scripts/check-agent-docs.py
```
Note: no sorry on main; no linter set_option; inspect every check on the head (lint and downstream builds too) and re-run cancelled ones before the merge queue
Source: CONTRIBUTING.md 'Pull Request Checks And Merge Queue'; .github/PULL_REQUEST_TEMPLATE.md (fetched 2026-11-28)

## PR body skeleton

```
## Summary
<What changes and why.>

## Verification
<lake build ... VCVioTest; lake exe axiomsweep --check; ./scripts/update-lib.sh; lint commands.>

## Checklist
<Tick the template boxes that apply.>
```

## What reviewers here actually ask for (our data)

Review style: human collaborators review unprompted; observed first human comment from about 3 hours to about 8 days on 5 sampled merged PRs; bots comment at open

None recorded: no PR of ours; one comment on issue #1154 with no reply.

Source: VCVio#1123, #1165, #1187, #1215, #1223 timelines; issue #1154 (fetched 2026-11-28)

## How a PR gets a reviewer, and what the author must do

- Reviewer: no one is assigned. A collaborator picks the PR up and merges through the merge queue. After replying, the author can re-request the earlier reviewer. (observed: VCVio#1187)
- Easy to miss: every check on the head commit must pass before the PR is queued, including lint and the downstream builds. A bot checks the title format. A question on an issue may sit for days with no answer. (documented: `CONTRIBUTING.md`; observed: VCVio#1154, #1165, #1187)

## Our PRs here

No PR. One comment (2026-11-26) on issue VCVio#1154, a list of follow-ups to position binding and hiding for vector commitments, asking whether an item is free for an outside contributor. As of 2026-11-28 there is no reply, no assignee, no label and no linked PR; our comment is the newest event on the issue.

## Typical rounds

Unmeasured for us. On 5 sampled merged PRs by repeat contributors the first human comment came after about 3 hours to about 8 days; a collaborator merged each through the merge queue.

## Do / don't

- Do: ask on the issue before starting, and expect that a reply may take days (observed: #1154 has had none).
- Do: run `./scripts/update-lib.sh` and `lake exe axiomsweep --check`, and check every check on the head, including lint and downstream builds, before the PR is queued (documented: CONTRIBUTING.md).
- Do: expect no assigned reviewer; a collaborator picks the PR up, and an author can re-request the earlier reviewer after replying (observed: #1187).
- Do: use a `feat(scope): subject` style title; a bot checks it (observed: #1165, #1187, #1215, #1223).
- Don't: add an AI-attribution line to file headers or disable a linter (documented: CONTRIBUTING.md).
