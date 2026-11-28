# ArkLib

`Verified-zkEVM/ArkLib` · profile: `merge-kit/repos/Verified-zkEVM__ArkLib.yaml`

## AI policy

> "Authors remain responsible for content produced with an AI agent or another tool: Read the headline statements and the full description before requesting review. Keep temporary plans, handoff notes, and session logs out of the contribution." ... "A prose task does not itself authorize a comment, PR, or merge. Agents must keep the user's task scope and publication instructions."
> [lit:https://github.com/Verified-zkEVM/ArkLib/blob/main/CONTRIBUTING.md]

- **Stance:** AI-assisted work allowed; the author is responsible (CONTRIBUTING.md 'Tool-Assisted Contributions')
- **Who may write PR text and replies:** an agent may draft; the author must read the headline statements and the full description before requesting review
- **Disclosure:** not required; no AI-attribution line in file headers ('Do not add a separate AI-attribution line'). Our PR body states the AI authorship anyway
- **Forbidden content:** temporary plans, handoff notes and session logs in the contribution; competing PRs for the same target
- Source: https://github.com/Verified-zkEVM/ArkLib/blob/main/CONTRIBUTING.md lines 142-154 and 359-361; AGENTS.md (fetched 2026-11-28)

## Ready signal

No reviewer is assigned: no CODEOWNERS, no auto-assign, no label bot. Open the PR non-draft with CI green and the template filled in; a maintainer picks it up. The `/review` LLM command works only for maintainers. (source: .github/workflows/review.yml; absence of CODEOWNERS; ArkLib#1498, #1506, #1507, #1512, #1514, #1524, #1526 (no review_requested events))

Open-PR cap: no written cap; our default 2 (source: ArkLib CONTRIBUTING.md (none stated))

## CI to run locally

```sh
lake exe cache get
./scripts/validate.sh
./scripts/validate.sh --axioms
uv run --no-project --python 3.12 python scripts/check-pr-title.py
```
Note: git add new files before validation; --axioms for any proof change; --docs is optional; no maxHeartbeats, no linter suppression, files at most 1500 lines
Source: CONTRIBUTING.md 'Set Up and Validate'; AGENTS.md 'Fast Start'; .github/workflows/pr-checks.yml (fetched 2026-11-28)

## PR body skeleton

```
## Summary
<Problem, change, purpose.>

## Formalized statements
<Headline declarations and how each relates to its source.>

## Admissions and axioms
<Admissions added or closed; #print axioms for each headline theorem.>

## Validation
<Each command, its result, and the commit it ran on.>

## Breaking changes
<Renamed or removed declarations; omit if none.>

## Known gaps
<What is not formalized.>

## Related work
<Closes #...; stack base; overlapping PRs.>

## Checklist
- [ ] I searched the open pull requests and issues for overlapping work.
- [ ] I did the applicable statement checks in CONTRIBUTING.md, "Statement Correctness".
- [ ] The description matches the code and the evidence.
- [ ] The pull request contains no working files from a tool session.
```

## What reviewers here actually ask for (our data)

Review style: human maintainers review unprompted; observed first review from about 1 day to about 8 days on 7 sampled merged PRs; bots comment at open (PR Summary, build timing)

None recorded: no review has landed on our PR yet.

Source: ArkLib#1498, #1506, #1507, #1512, #1514, #1524, #1526 timelines; ArkLib#1617 timeline (fetched 2026-11-28)

## How a PR gets a reviewer, and what the author must do

- Reviewer: no one is assigned and the author requests no one. A maintainer picks the PR up unprompted. (observed: ArkLib#1498, #1506, #1507, #1512, #1514, #1524, #1526)
- Easy to miss: CI runs on fork PRs without approval, so every check must be green before anyone looks. The title check and the PR Summary bot run too. The Validation section must hold the commands that were run and their results. (documented: `CONTRIBUTING.md`; observed: ArkLib#1617)

## Our PRs here

<!--n:obs.t.by_repo.verified_zkevm_arklib.open--><!--/n--> open (<!--n:obs.prs.verified_zkevm_arklib.open--><!--/n-->). ArkLib#1617 (2026-11-27) moves the even/odd row helpers to `Fin` and shares them with DG25. Non-draft, branch not behind, every check green (CI, imports, docs, title, PR Summary). Two bot comments, no human comment, no reviewer assigned.

## Typical rounds

Unmeasured for us. On 7 sampled merged PRs by repeat outside contributors the first human review came after about 1 day (two PRs) to about 8 days; none had a reviewer requested by the author.

## Do / don't

- Do: use the title `type(scope)!: subject` and fill every template heading that applies (documented: CONTRIBUTING.md 'Title Format', pull_request_template.md).
- Do: run `./scripts/validate.sh` (and `--axioms` for proofs) and put the commands and results in the Validation section (documented: CONTRIBUTING.md).
- Do: search open PRs for the same declarations and link any overlap (documented: CONTRIBUTING.md 'Check for Overlap').
- Do: expect no assigned reviewer; a maintainer picks the PR up unprompted (observed: #1498, #1506, #1507, #1512, #1514, #1524, #1526).
- Don't: leave plans, handoff notes or session logs in the diff, or add an AI-attribution line to file headers (documented: CONTRIBUTING.md).
