# julia

`JuliaLang/julia` · profile: `merge-kit/repos/JuliaLang__julia.yaml`

## AI policy

> "If your pull request contains substantive contributions from a generative AI tool, please disclose so with details, and review all changes before opening. This also applies to other content, such as issues, discussions, and comments." AGENTS.md adds a commit trailer `Assisted-by: <tool> (<model>)` and: "Agents can only open PRs or post comments once the human user gives them explicit permission."
> [lit:https://github.com/JuliaLang/julia/blob/master/CONTRIBUTING.md]

- **Stance:** allowed with disclosure; the human opens the PR
- **Who may write PR text and replies:** AI may help; substantive AI contributions to PRs, issues, discussions and comments must be disclosed with details and reviewed by the human before opening
- **Disclosure:** say how AI was used in the PR, issue or comment; end every AI-touched commit with `Assisted-by: <tool> (<model>)` naming both tool and model; no Co-authored-by for tools
- Source: https://github.com/JuliaLang/julia/blob/master/CONTRIBUTING.md (AI notes) and AGENTS.md 'For all changes' (fetched 2026-11-28)

## Ready signal

no reviewer is assigned automatically (CODEOWNERS covers few paths); a committer reviews or requests a reviewer. Nothing for the author to click (source: julia#65072, #64990, #64746 (committer-driven review); .github/CODEOWNERS)

Open-PR cap: no written cap; our default 2 (source: none stated in CONTRIBUTING.md)

## CI to run locally

```sh
make
./usr/bin/julia test/runtests.jl <test>
make clean testall
```
Note: CI is Buildkite plus small GitHub workflows (Labels, Typos, Whitespace); a PR must not carry any `needs *` or DO NOT MERGE label when merged
Source: doc/src/devdocs/contributing/code-changes.md; .github/workflows/LabelCheck.yml (fetched 2026-11-28)

## PR body skeleton

```
<What was wrong, what the change does, one before/after example.>

Fixes #<issue>

AI use: <what the AI did; what the human checked>.
```

## What reviewers here actually ask for (our data)

Review style: human committers; no assignment bot; response from 1 hour to a day on sampled merged PRs

None recorded: no review has landed on our work here yet.

Source: sampled merged PRs julia#65072, #65044, #64990, #64746, #65075, #64873

## How a PR gets a reviewer, and what the author must do

- Reviewer: there is no auto-assign. A committer reviews or requests a reviewer. (observed: julia#65072, #64990)
- Easy to miss: no need to ask or claim an issue first; the guide says to open the PR. An issue assigned to someone else is a sign to check with them before starting. A `needs *` label left on the PR fails a check at merge time. Whether a small fix needs a NEWS.md entry is unknown. (documented: `CONTRIBUTING.md`, `.github/workflows/LabelCheck.yml`; observed: julia#64271)

## Our PRs here

No PR. We commented once on julia#64271 (2026-11-26) offering a fix for `round(Float16, x)`, with an AI disclosure line. As of 2026-11-28 the issue is open, assigned to someone else, and has no reply and no linked PR.

## Typical rounds

On 6 sampled merged PRs the first human response came within about 1 hour to 14 hours; one tiny doc fix was merged with no review.

## Do / don't

- Do: just open the PR; contributors are told there is no need to ask or claim an issue first (documented: CONTRIBUTING.md 'Working on issues').
- Do: end each AI-touched commit with `Assisted-by: <tool> (<model>)` and disclose AI use with details in the PR text (documented: AGENTS.md, CONTRIBUTING.md).
- Do: expect a committer to review or request a reviewer; there is no auto-assign (observed: #65072, #64990).
- Don't: leave a `needs *` label on at merge time; a check fails on it (documented: LabelCheck.yml).
- Don't: let a tool open the PR without the human's permission (documented: AGENTS.md, CONTRIBUTING.md).
