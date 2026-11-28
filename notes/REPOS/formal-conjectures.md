## short
NO (follows Mathlib)
## quote
> "Follow the same AI usage conventions as Mathlib."
> [lit:https://github.com/google-deepmind/formal-conjectures/blob/main/CONTRIBUTING.md]
## ours
<!--n:obs.t.by_repo.google_deepmind_formal_conjectures.open--><!--/n--> open (<!--n:obs.prs.google_deepmind_formal_conjectures.open--><!--/n-->). formal-conjectures#8069 and #8218 each got an approving review and then waited for a merge: an example of slow merge after approval, not of rejection.
## process
- Reviewer: no CODEOWNERS file and no reviewer request on our PRs. A label bot tags the PR by directory. (observed: formal-conjectures#8069, #8218)
- Easy to miss: an approval from a reviewer without write access does not satisfy the branch rule. Both our PRs have an approving review from an account GitHub lists as a contributor, and both still read "review required". (observed: formal-conjectures#8069, #8218)
- Easy to miss: the `cla/google` check. It is green on both. (documented: CONTRIBUTING.md; observed: formal-conjectures#8069, #8218)
## rounds
One round: the reviewer's only asks were optional citations of the primary source (page and equation).
## do
- Do: sign the Google CLA; one problem per file; cite the primary source with page and equation.
- Do: claim the issue by commenting before you start.
- Do: keep proofs short; statements may use `sorry` by design (the repo states problems).
- Don't: let an agent write the description or replies (inherited Mathlib rule).
