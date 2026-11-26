## short
not stated
## quote
> No written AI policy (no CONTRIBUTING file; README has none). Recorded maintainer stance on content: a PR that "documents (and thereby cements) a problem instead of fixing it" is refused.
> [ours:clean#512]
## ours
<!--n:obs.t.by_repo.verified_zkevm_clean.landed--><!--/n--> landed, <!--n:obs.t.by_repo.verified_zkevm_clean.closed--><!--/n--> closed, <!--n:obs.t.by_repo.verified_zkevm_clean.open--><!--/n--> open. clean#515 landed after two "why the detour?" questions; clean#512 was refused.
## rounds
One round; the maintainer approves and merges fast.
## do
- Do: use the simplest direct term ("any reason not to just use `body init 0` here?"), or justify the detour in a comment.
- Do: run the empty-lines script, `lake build --wfail`, and `lake build CleanTests`.
- Don't: open a PR that only pins a known-bad behaviour in a test or doc.
