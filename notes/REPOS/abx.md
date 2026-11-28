## short
not stated
## quote
> No AI section in CONTRIBUTING. Content rule: "Do not add planning, strategy, research notebooks, review transcripts, or private triage records."
> [lit:https://github.com/ArtBlocks/abx/blob/main/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.artblocks_abx.landed--><!--/n--> landed, <!--n:obs.t.by_repo.artblocks_abx.closed--><!--/n--> closed, <!--n:obs.t.by_repo.artblocks_abx.open--><!--/n--> open; all landings human-merged. Two closed PRs (abx#152, #186) were superseded by the maintainer's own PRs, with credit, that extended the shared script preparation instead.
## process
- Reviewer: unknown. No CODEOWNERS file and no reviewer request on our PRs; the maintainer picks PRs up. (observed: abx#222)
- Easy to miss: fork workflow runs wait for maintainer approval. On abx#222 the `CI` run has read `action_required` since 2026-11-16, and the branch was 16 commits behind main on 2026-11-28. (documented: CONTRIBUTING.md; observed: abx#222)
- Easy to miss: an open issue here may already be fixed. abx#148 is open, and the maintainer's merged abx#177 cross-references it. Read the timeline before pinging. (observed: abx#148)
## rounds
Usually none: the maintainer merges or reimplements.
## do
- Do: say how the change was verified (`pnpm test`, `forge test`); fork CI needs maintainer approval on each push.
- Do: extend the shared mechanism rather than adding a branch.
- Don't: raise code-size test limits to make a change pass.
