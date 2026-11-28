## short
NO (follows Mathlib)
## quote
> "CSLib in general follows the Mathlib policy on use of AI. In particular, take note of: If you use artificial intelligence [...] please explain this in the PR description. Explain which tool(s) you used and how you used it."
> [lit:https://github.com/leanprover/cslib/blob/main/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.leanprover_cslib.landed--><!--/n--> landed, <!--n:obs.t.by_repo.leanprover_cslib.closed--><!--/n--> closed, <!--n:obs.t.by_repo.leanprover_cslib.open--><!--/n--> open. cslib#1242 and #1261 both landed, and both had a human approval and a human merge. Our bodies disclosed AI correctly but were agent-written, which the inherited Mathlib rule does not allow.
## rounds
One round on both landings: cslib#1261 landed with no inline comments; cslib#1242 after one inline ask and two comments. Reviewers are soft and say when they are unsure; a maintainer pulls in a domain expert for big unfamiliar files.
## do
- Do: conventional title prefix (`feat:`, `fix:`, `doc:`); run `lake build --wfail --iofail`, `lake test`, `lake exe checkInitImports`, `lake shake`.
- Do: check the Zulip topic before touching shared definitions (cslib#1242 revert).
- Do: fold case splits into one `rintro` pattern when the reviewer suggests it, or say why not (cslib#1263).
- Don't: let an agent write the description or replies.
