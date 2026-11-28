## short
proofs yes, specs no
## quote
> "Specifications: PRs introducing AI-generated specifications of any kind are strictly prohibited, and their submission may result in a contribution ban at the maintainers' discretion." "Proofs: AI-generated proofs are welcome, as long as they are compliant with the style guide and requirements listed in this document. The human submitting the PR is held responsible for the contents of the PR."
> [lit:https://github.com/Beneficial-AI-Foundation/SparsePostQuantumRatchet-verify/blob/main/doc/WORKFLOW_AND_PR_GUIDE.md]
## ours
<!--n:obs.t.by_repo.beneficial_ai_foundation_sparsepostquantumratchet_verify.open--><!--/n--> open (<!--n:obs.prs.beneficial_ai_foundation_sparsepostquantumratchet_verify.open--><!--/n-->), non-draft, opened 2026-11-26. SparsePostQuantumRatchet-verify#836 proves the data-equality statement from issue #818 and #837 flips `public import` to `import` (closes #659). Each requested the review team automatically. All three workflows are in `action_required` (a maintainer has to approve them), Radar was skipped, and there is no review or comment yet. #836 names the helper statements the AI formulated and offers to rework them if they count as specifications.
## process
- Reviewer: CODEOWNERS requests the review team when the PR opens. (documented: `.github/CODEOWNERS`; observed: SparsePostQuantumRatchet-verify#836, #837)
- Easy to miss: all three workflows stop at `action_required` on a fork PR until a maintainer approves them. The body must start with "This PR", have no headings and end with `Closes #N`. Any statement an AI wrote or reworded counts against the no-AI-specifications rule, so say which statements are the maintainers'. (documented: `doc/WORKFLOW_AND_PR_GUIDE.md`; observed: #836, #837)
## rounds
Unmeasured for outsiders: every sampled merged PR is by a team member who merges their own PR. For them the first review came within minutes to about a day.
## do
- Do: start the body with "This PR", use no markdown headings, and end with `Closes #N` (documented: doc/WORKFLOW_AND_PR_GUIDE.md).
- Do: have the PR close an open issue; discuss first if others may be on it (documented: doc/WORKFLOW_AND_PR_GUIDE.md).
- Do: expect the review team to be requested by CODEOWNERS, and workflows to wait for a maintainer's approval on a fork PR (documented: .github/CODEOWNERS; observed: #836, #837).
- Do: run `lake exe mk_all --git` after adding files and `lake exe runLinter Spqr` before opening (documented: guide).
- Don't: write or reformulate specifications with an AI; state which statements are the maintainers' (documented: guide 'Contribution policy').
- Don't: edit generated Aeneas files, translation.json or the Rust sources (documented: guide).
