## short
allowed with author responsibility
## quote
> "Authors remain responsible for content produced with an AI agent or another tool: Read the headline statements and the full description before requesting review. Keep temporary plans, handoff notes, and session logs out of the contribution." ... "A prose task does not itself authorize a comment, PR, or merge. Agents must keep the user's task scope and publication instructions."
> [lit:https://github.com/Verified-zkEVM/ArkLib/blob/main/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.verified_zkevm_arklib.open--><!--/n--> open (<!--n:obs.prs.verified_zkevm_arklib.open--><!--/n-->). ArkLib#1617 (2026-11-27) moves the even/odd row helpers to `Fin` and shares them with DG25. Non-draft, branch not behind, every check green (CI, imports, docs, title, PR Summary). Two bot comments, no human comment, no reviewer assigned.
## process
- Reviewer: no one is assigned and the author requests no one. A maintainer picks the PR up unprompted. (observed: ArkLib#1498, #1506, #1507, #1512, #1514, #1524, #1526)
- Easy to miss: CI runs on fork PRs without approval, so every check must be green before anyone looks. The title check and the PR Summary bot run too. The Validation section must hold the commands that were run and their results. (documented: `CONTRIBUTING.md`; observed: ArkLib#1617)
## rounds
Unmeasured for us. On 7 sampled merged PRs by repeat outside contributors the first human review came after about 1 day (two PRs) to about 8 days; none had a reviewer requested by the author.
## do
- Do: use the title `type(scope)!: subject` and fill every template heading that applies (documented: CONTRIBUTING.md 'Title Format', pull_request_template.md).
- Do: run `./scripts/validate.sh` (and `--axioms` for proofs) and put the commands and results in the Validation section (documented: CONTRIBUTING.md).
- Do: search open PRs for the same declarations and link any overlap (documented: CONTRIBUTING.md 'Check for Overlap').
- Do: expect no assigned reviewer; a maintainer picks the PR up unprompted (observed: #1498, #1506, #1507, #1512, #1514, #1524, #1526).
- Don't: leave plans, handoff notes or session logs in the diff, or add an AI-attribution line to file headers (documented: CONTRIBUTING.md).
