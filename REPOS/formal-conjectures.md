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
| attribution | <!--n:profile.formal_conjectures.attribution-->2<!--/n--> |

Source: FAILURE-MODES.md (review-harvest counts), general classes 'Cite the primary source'

## Our PRs here

<!--n:obs.t.by_repo.google_deepmind_formal_conjectures.open-->2<!--/n--> open (<!--n:obs.prs.google_deepmind_formal_conjectures.open-->formal-conjectures#8069, #8218<!--/n-->). formal-conjectures#8069 and #8218 each got an approving review and then waited for a merge: an example of slow merge after approval, not of rejection.

## Typical rounds

One round: the reviewer's only asks were optional citations of the primary source (page and equation).

## Do / don't

- Do: sign the Google CLA; one problem per file; cite the primary source with page and equation.
- Do: claim the issue by commenting before you start.
- Do: keep proofs short; statements may use `sorry` by design (the repo states problems).
- Don't: let an agent write the description or replies (inherited Mathlib rule).
