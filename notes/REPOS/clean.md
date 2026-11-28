## short
not stated
## quote
> No written AI policy (no CONTRIBUTING file; README has none). Recorded maintainer stance on content: a PR that "documents (and thereby cements) a problem instead of fixing it" is refused.
> [ours:clean#512]
## ours
<!--n:obs.t.by_repo.verified_zkevm_clean.landed--><!--/n--> landed, <!--n:obs.t.by_repo.verified_zkevm_clean.closed--><!--/n--> closed, <!--n:obs.t.by_repo.verified_zkevm_clean.open--><!--/n--> open. clean#515 landed after two "why the detour?" questions; clean#512 was refused.
## process
- Reviewer: unknown. No CODEOWNERS file, no reviewer was requested on our PRs, and the docs name no step. On the landed clean#515 a maintainer picked it up unasked. (observed: clean#515, #519, #526)
- Easy to miss: a first-time contributor's CI waits for a maintainer to approve the run. clean#519 and #526 showed no checks at all; the `CI` run for each had the conclusion `action_required` (from 2026-11-24 and 2026-11-25, still so on 2026-11-28). An empty check list is not a green one. (observed: clean#519, #526)
## rounds
One round; the maintainer approves and merges fast.
## do
- Do: use the simplest direct term ("any reason not to just use `body init 0` here?"), or justify the detour in a comment.
- Do: run the empty-lines script, `lake build --wfail`, and `lake build CleanTests`.
- Don't: open a PR that only pins a known-bad behaviour in a test or doc.
