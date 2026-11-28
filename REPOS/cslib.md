# cslib

`leanprover/cslib` · profile: `merge-kit/repos/leanprover__cslib.yaml`

## AI policy

> "CSLib in general follows the Mathlib policy on use of AI. In particular, take note of: If you use artificial intelligence [...] please explain this in the PR description. Explain which tool(s) you used and how you used it."
> [lit:https://github.com/leanprover/cslib/blob/main/CONTRIBUTING.md]

- **Stance:** follows the Mathlib AI policy
- **Who may write PR text and replies:** NO agent-written comments/descriptions (inherits Mathlib). Our cslib#1263/#1274 bodies are agent-written: policy risk (STATE-OF-THE-FIELD.md policy table).
- **Disclosure:** 'explain this in the PR description. Explain which tool(s) you used and how you used it'
- Source: https://raw.githubusercontent.com/leanprover/cslib/main/CONTRIBUTING.md lines 57-60 (gh api 2026-11-25)

## Ready signal

non-draft PR with CI green; ask on the working-group Zulip topic for review of big files (source: cslib CONTRIBUTING.md lines 47-55, 122; maintainer notes (asked for a domain expert, cslib#1242))

Open-PR cap: no written cap; our default 2 (source: cslib CONTRIBUTING.md (none stated); STATE-OF-THE-FIELD.md policy table)

## CI to run locally

```sh
lake build --wfail --iofail
lake test
lake exe checkInitImports
lake exe mk_all
lake shake --add-public --keep-implied --keep-prefix
lake lint
```
Source: cslib CONTRIBUTING.md lines 88-105; .github/workflows/lean_action_ci.yml line 18 (build-args --wfail --iofail)

## PR body skeleton

```
<Human-written summary of the change and why.>

AI use: <tools and how they were used>
```

## What reviewers here actually ask for (our data)

Review style: human maintainers; at least one maintainer approval

| class | asks / threads in our data |
|---|---|
| proof-quality | <!--n:profile.cslib.proof_quality-->4<!--/n--> |
| scope | <!--n:profile.cslib.scope-->1<!--/n--> |

Source: maintainer notes; FAILURE-MODES.md (review-harvest counts), general classes; cslib CONTRIBUTING.md line 47

## How a PR gets a reviewer, and what the author must do

- Reviewer: the CODEOWNERS file requests all code owners when the PR opens. The timeline shows the requests with the author as actor at the minute of opening; the author did not make them and need not request anyone. (documented: `.github/CODEOWNERS`; observed: cslib#1263, #1274)
- Easy to miss: a comment-only review leaves the PR at "review required". Reply in each thread and leave resolving to the reviewer; cslib#1263 has one open thread where the reviewer asked a second maintainer for an opinion. (observed: cslib#1263)

## Our PRs here

<!--n:obs.t.by_repo.leanprover_cslib.landed-->2<!--/n--> landed, <!--n:obs.t.by_repo.leanprover_cslib.closed-->1<!--/n--> closed, <!--n:obs.t.by_repo.leanprover_cslib.open-->2<!--/n--> open. cslib#1242 and #1261 both landed, and both had a human approval and a human merge. Our bodies disclosed AI correctly but were agent-written, which the inherited Mathlib rule does not allow.

## Typical rounds

One round on both landings: cslib#1261 landed with no inline comments; cslib#1242 after one inline ask and two comments. Reviewers are soft and say when they are unsure; a maintainer pulls in a domain expert for big unfamiliar files.

## Do / don't

- Do: conventional title prefix (`feat:`, `fix:`, `doc:`); run `lake build --wfail --iofail`, `lake test`, `lake exe checkInitImports`, `lake shake`.
- Do: check the Zulip topic before touching shared definitions (cslib#1242 revert).
- Do: fold case splits into one `rintro` pattern when the reviewer suggests it, or say why not (cslib#1263).
- Don't: let an agent write the description or replies.
