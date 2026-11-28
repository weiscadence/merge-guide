# IEANTN

`teorth/IEANTN` · profile: `merge-kit/repos/teorth__IEANTN.yaml`

## AI policy

> "Say so in the PR body — one line is enough (`Made with Claude Code`, or the tool's own `Co-Authored-By:` footer). Much of this repository is expected to be AI-assisted; the disclosure lets reviewers calibrate, not disqualify."
> [lit:https://github.com/teorth/IEANTN/blob/main/CONTRIBUTING.md]

- **Stance:** AI assistance expected and welcome; disclose it in the PR body
- **Who may write PR text and replies:** AI-assisted work is expected; the submitter must understand the diff
- **Disclosure:** one line in the PR body, for example 'Made with Claude Code' or the tool's Co-Authored-By footer
- **Cla:** none found
- Source: https://github.com/teorth/IEANTN/blob/main/CONTRIBUTING.md 'Disclose AI assistance' (fetched 2026-11-28)

## Ready signal

no reviewer is assigned by default. CODEOWNERS requests the maintainer only for PRs that touch Vocabulary, workflows, the verify script or receipts. Otherwise the maintainer picks PRs up. Required checks green and branch up to date with main (source: IEANTN .github/CODEOWNERS; ruleset on main; sampled merged PRs)

Open-PR cap: no written cap; one person per node solution; our default 2 (source: https://github.com/teorth/IEANTN/blob/main/CONTRIBUTING.md 'Large tasks')

## CI to run locally

```sh
lake build
python scripts/ieantn.py check
python scripts/ieantn.py fingerprint
python scripts/ieantn.py gen-challenges
python scripts/ieantn.py diff
```
Note: required checks: Build Vocabulary and Nodes, Check the node network, Network impact; branch must be up to date with main; CI fails a PR that commits STATE.md, GRAPH.md, docs/graph.html or docs/nodes/
Source: https://github.com/teorth/IEANTN/blob/main/CLAUDE.md 'Build'; CONTRIBUTING.md 'Generated files'; ruleset on main (fetched 2026-11-28)

## PR body skeleton

```
<What changed and which source or claim it was checked against.>

Made with <tool>.

Closes #<issue>
```

## What reviewers here actually ask for (our data)

Review style: one maintainer; PRs are read as comments, with no formal review on most sampled PRs; sampled merges took about 3 hours to 15 days

None recorded: no review has landed on our work here yet.

Source: IEANTN#220, #226, #235, #243, #247, #263, #270, #274; CODEOWNERS

## How a PR gets a reviewer, and what the author must do

- Reviewer: CODEOWNERS covers only Vocabulary, workflows and receipts. For anything else no one is requested and the maintainer picks the PR up. (documented: `.github/CODEOWNERS`; observed: IEANTN#220, #247, #263, #270, #274)
- Easy to miss: run `fingerprint` and `gen-challenges` and commit their output, and leave the generated state and graph files out of the commit. An issue may be fixed by the owner's own PR instead of yours. Whether CI on a fork PR needs approval is unknown. (documented: `CONTRIBUTING.md`, `CLAUDE.md`; observed: IEANTN#271, #277)

## Our PRs here

One open issue (IEANTN#289, wrong journal and wrong locators in node metadata, no statement changes), opened 2026-11-27 with an AI disclosure and an offer to send a PR. No comments, labels or PRs yet. An earlier issue of ours (#271) was closed two days after it was opened, when the owner fixed it in their own PR (#277), merged 13 minutes after that PR was opened.

## Typical rounds

Sampled merged outside PRs: first review was a comment, not a formal review, on most; time to merge ranged from about 3 hours to about 15 days. On one PR the first review came after about 13 hours.

## Do / don't

- Do: put a one-line AI disclosure in the PR body (documented: CONTRIBUTING.md).
- Do: comment `claim` on the board issue before starting work; it is a courtesy, not a lock (documented: CONTRIBUTING.md).
- Do: run `fingerprint` and `gen-challenges` and commit their output; leave STATE.md, GRAPH.md, docs/graph.html and docs/nodes/ out of the commit (documented: CONTRIBUTING.md, CLAUDE.md).
- Do: expect no reviewer to be assigned unless you touch Vocabulary, workflows or receipts; the maintainer picks PRs up (documented: .github/CODEOWNERS; observed: #220, #247, #263, #270, #274).
- Don't: edit a conclusion other nodes depend on; add a new version instead (documented: CLAUDE.md).
