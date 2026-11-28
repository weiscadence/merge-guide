# SparsePostQuantumRatchet-verify

`Beneficial-AI-Foundation/SparsePostQuantumRatchet-verify` · profile: `merge-kit/repos/Beneficial-AI-Foundation__SparsePostQuantumRatchet-verify.yaml`

## AI policy

> "Specifications: PRs introducing AI-generated specifications of any kind are strictly prohibited, and their submission may result in a contribution ban at the maintainers' discretion." "Proofs: AI-generated proofs are welcome, as long as they are compliant with the style guide and requirements listed in this document. The human submitting the PR is held responsible for the contents of the PR."
> [lit:https://github.com/Beneficial-AI-Foundation/SparsePostQuantumRatchet-verify/blob/main/doc/WORKFLOW_AND_PR_GUIDE.md]

- **Stance:** AI-generated proofs welcome; AI-generated specifications strictly prohibited
- **Who may write PR text and replies:** an agent may write proofs; the human submitter is responsible for the whole PR
- **Disclosure:** not required by the guide; our PRs disclose anyway and say which statements are the maintainer's and which helper statements the AI wrote
- **Consequence:** a submission with AI-generated specifications may result in a contribution ban at the maintainers' discretion
- Source: https://github.com/Beneficial-AI-Foundation/SparsePostQuantumRatchet-verify/blob/main/doc/WORKFLOW_AND_PR_GUIDE.md 'Contribution policy' (fetched 2026-11-28)

## Ready signal

CODEOWNERS auto-requests the fc-team review team when the PR opens and again at ready_for_review. Reviewers look at non-draft PRs whose checks have passed. First-time fork PRs sit in action_required until a maintainer approves workflows; Radar is skipped for non-members and a maintainer can request it with a !radar comment. (source: .github/CODEOWNERS; doc/WORKFLOW_AND_PR_GUIDE.md line 42 and 'Performance'; .github/workflows/radar.yml; #836 and #837 runs)

Open-PR cap: no written cap; our default 2 (source: doc/WORKFLOW_AND_PR_GUIDE.md (none stated))

## CI to run locally

```sh
lake build
lake exe runLinter Spqr
lake exe mk_all --git
```
Note: run mk_all after adding, removing or renaming a .lean file; never edit generated Aeneas files or the Rust sources; new sorry is flagged by CI; fork workflows wait for maintainer approval
Source: doc/WORKFLOW_AND_PR_GUIDE.md 'Updating the Import File', 'Linting', 'Proof cheats'; .github/workflows/lean.yml (fetched 2026-11-28)

## PR body skeleton

```
This PR <imperative statement of the change, with the full function name>. <Motivation and contrast with the old behaviour.>

<Checks run.>

Breaking changes: <none, or description, justification, migration notes>

Closes #<issue>
```

## What reviewers here actually ask for (our data)

Review style: team reviews; fast for insiders (first review within minutes to about a day on 7 sampled merged PRs); no outsider merge found to compare

None recorded: no review has landed on our PRs yet.

Source: SparsePostQuantumRatchet-verify#636, #677, #761, #817, #820, #822, #832 timelines; #836 and #837 (fetched 2026-11-28)

## How a PR gets a reviewer, and what the author must do

- Reviewer: CODEOWNERS requests the review team when the PR opens. (documented: `.github/CODEOWNERS`; observed: SparsePostQuantumRatchet-verify#836, #837)
- Easy to miss: all three workflows stop at `action_required` on a fork PR until a maintainer approves them. The body must start with "This PR", have no headings and end with `Closes #N`. Any statement an AI wrote or reworded counts against the no-AI-specifications rule, so say which statements are the maintainers'. (documented: `doc/WORKFLOW_AND_PR_GUIDE.md`; observed: #836, #837)

## Our PRs here

<!--n:obs.t.by_repo.beneficial_ai_foundation_sparsepostquantumratchet_verify.open-->2<!--/n--> open (<!--n:obs.prs.beneficial_ai_foundation_sparsepostquantumratchet_verify.open-->SparsePostQuantumRatchet-verify#836, #837<!--/n-->), non-draft, opened 2026-11-26. SparsePostQuantumRatchet-verify#836 proves the data-equality statement from issue #818 and #837 flips `public import` to `import` (closes #659). Each requested the review team automatically. All three workflows are in `action_required` (a maintainer has to approve them), Radar was skipped, and there is no review or comment yet. #836 names the helper statements the AI formulated and offers to rework them if they count as specifications.

## Typical rounds

Unmeasured for outsiders: every sampled merged PR is by a team member who merges their own PR. For them the first review came within minutes to about a day.

## Do / don't

- Do: start the body with "This PR", use no markdown headings, and end with `Closes #N` (documented: doc/WORKFLOW_AND_PR_GUIDE.md).
- Do: have the PR close an open issue; discuss first if others may be on it (documented: doc/WORKFLOW_AND_PR_GUIDE.md).
- Do: expect the review team to be requested by CODEOWNERS, and workflows to wait for a maintainer's approval on a fork PR (documented: .github/CODEOWNERS; observed: #836, #837).
- Do: run `lake exe mk_all --git` after adding files and `lake exe runLinter Spqr` before opening (documented: guide).
- Don't: write or reformulate specifications with an AI; state which statements are the maintainers' (documented: guide 'Contribution policy').
- Don't: edit generated Aeneas files, translation.json or the Rust sources (documented: guide).
