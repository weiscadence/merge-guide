# formal-conjectures

`google-deepmind/formal-conjectures` · profile: `merge-kit/repos/google-deepmind__formal-conjectures.yaml`

## AI policy

> "Follow the same AI usage conventions as Mathlib."
> [lit:https://github.com/google-deepmind/formal-conjectures/blob/main/CONTRIBUTING.md]

- **Stance:** follows Mathlib AI conventions
- **Who may write PR text and replies:** NO agent-written PR text/comments (inherits Mathlib)
- **Disclosure:** state AI tools and how they were used in the PR description
- **Cla:** Google CLA required
- Source: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/CONTRIBUTING.md lines 11-19, ~419 (gh api 2026-11-25)

## Ready signal

CLA signed, CI green, non-draft (source: CONTRIBUTING.md lines 92-106)

Open-PR cap: no written cap; claim issues by commenting first (source: CONTRIBUTING.md (claim by comment); STATE-OF-THE-FIELD.md policy table)

## CI to run locally

```sh
lake exe cache get
lake build
```
Note: sorry is allowed by design (warn.sorry = false): conjecture statements are `sorry`
Source: CONTRIBUTING.md lines 106-119; unpublished observatory raw/ci-evidence.json (lakefile.toml:47-55)

## PR body skeleton

```
<Human-written: which problem, source (paper, page, equation), and what is formalised.>

AI use: <tools and how>
```

## What reviewers here actually ask for (our data)

Review style: human maintainers; cite the primary source (bocowgill, formal-conjectures#8069/#8218)

| class | asks / threads in our data |
|---|---|
| attribution | <!--n:profile.formal_conjectures.attribution--><!--/n--> |

Source: FAILURE-MODES.md (review-harvest counts), general classes 'Cite the primary source'

## How a PR gets a reviewer, and what the author must do

- Reviewer: no CODEOWNERS file and no reviewer request on our PRs. A label bot tags the PR by directory. (observed: formal-conjectures#8069, #8218)
- Easy to miss: an approval from a reviewer without write access does not satisfy the branch rule. Both our PRs have an approving review from an account GitHub lists as a contributor, and both still read "review required". (observed: formal-conjectures#8069, #8218)
- Easy to miss: the `cla/google` check. It is green on both. (documented: CONTRIBUTING.md; observed: formal-conjectures#8069, #8218)

## Our PRs here

<!--n:obs.t.by_repo.google_deepmind_formal_conjectures.open--><!--/n--> open (<!--n:obs.prs.google_deepmind_formal_conjectures.open--><!--/n-->). formal-conjectures#8069 and #8218 each got an approving review and then waited for a merge: an example of slow merge after approval, not of rejection.

## Typical rounds

One round: the reviewer's only asks were optional citations of the primary source (page and equation).

## Do / don't

- Do: sign the Google CLA; one problem per file; cite the primary source with page and equation.
- Do: claim the issue by commenting before you start.
- Do: keep proofs short; statements may use `sorry` by design (the repo states problems).
- Don't: let an agent write the description or replies (inherited Mathlib rule).
