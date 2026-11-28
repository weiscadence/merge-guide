# LNSym

`leanprover/LNSym` · profile: `merge-kit/repos/leanprover__LNSym.yaml`

## AI policy

> No AI section in CONTRIBUTING, README or the PR template. No CLA either; the template only asks you to confirm Apache 2.0. The rule that matters: "Note that before a PR to the `main` branch can be merged: No changes must be requested. All conversations must be resolved. Approval from a maintainer is required."
> [lit:https://github.com/leanprover/LNSym/blob/main/.github/pull_request_template.md]

- **Stance:** no AI section in CONTRIBUTING.md, README or the PR template
- **Who may write PR text and replies:** not stated
- **Disclosure:** not stated; disclose anyway (LNSym#267 has a one-line disclosure in the body)
- **Cla:** no CLA; the PR template asks you to confirm the Apache 2.0 license
- Source: https://github.com/leanprover/LNSym/blob/main/CONTRIBUTING.md and .github/pull_request_template.md (fetched 2026-11-28)

## Ready signal

CODEOWNERS requests the single code owner automatically when the PR opens. First-time fork CI stays in action_required until a maintainer approves it; the author cannot do that. Merge needs an approval from a maintainer and all conversations resolved. (source: .github/CODEOWNERS; .github/pull_request_template.md; LNSym#267 timeline and runs (fetched 2026-11-28))

Open-PR cap: no written cap; our default 2 (source: LNSym CONTRIBUTING.md (none stated))

## CI to run locally

```sh
make specs correctness proofs tests
lake build AWSLCELFTests
lake build lnsym
lake build Doc
```
Note: no nonterminal simp (use simp only unless it closes the goal); no new external dependencies; every .lean file starts with the copyright header (CI checks it); cosim needs an Aarch64 machine, say if you did not run it
Source: .github/workflows/ci.yml; CONTRIBUTING.md 'Submitting a Pull Request' (fetched 2026-11-28)

## PR body skeleton

```
### Issues:
Resolves #<issue>.   (omit if none)

### Description:
<What changed and why.>

### Testing:
<make / lake build commands run; whether cosim ran.>

### License:
By submitting this pull request, I confirm that my contribution is
made under the terms of the Apache 2.0 license.
```

## What reviewers here actually ask for (our data)

Review style: one code owner reviews; slow and bursty (no outside PR merged since 2024-10-08; four outside PRs open without review)

None recorded: no review has landed on our PR yet.

Source: LNSym#264, #265, #266, #267 timelines (fetched 2026-11-28)

## How a PR gets a reviewer, and what the author must do

- Reviewer: CODEOWNERS requests one code owner when the PR opens. The author need not ask. (documented: `.github/CODEOWNERS`; observed: LNSym#267)
- Easy to miss: CI on a first fork PR stops at `action_required`, so the build has not run until a maintainer approves it. Merge needs a maintainer approval, no requested changes and every conversation resolved. Reviews come in bursts; three other outside PRs wait in the same state. (documented: `.github/pull_request_template.md`; observed: LNSym#264, #265, #266, #267)

## Our PRs here

<!--n:obs.t.by_repo.leanprover_lnsym.open-->1<!--/n--> open (<!--n:obs.prs.leanprover_lnsym.open-->LNSym#267<!--/n-->). LNSym#267 (2026-11-27) proves five `sorry`s in `sha512_block_armv8_loop_2` with one helper lemma. Not draft, branch not behind. Code owner was requested automatically. CI is in `action_required`, so the build has not run, and there is no review or comment yet.

## Typical rounds

Unmeasured for outsiders. The one outside PR merged in the sample (LNSym#221, 2024-10) got a first review in about a day. Since then the repo has been bursty: a batch of core-developer merges on 2026-11-06, and three other outside PRs (#264, #265, #266) also sit unreviewed with CI awaiting approval.

## Do / don't

- Do: expect CI to wait for a maintainer to approve the workflow on a first fork PR; say so in the PR if the build was run locally (observed: #264, #265, #266, #267).
- Do: one code owner is requested for you; you do not need to ask (documented: .github/CODEOWNERS; observed: #267).
- Do: keep the template's Testing and License sections; state whether cosim ran (documented: pull_request_template.md).
- Do: put the copyright header on any new `.lean` file; CI rejects files without it (documented: ci.yml).
- Don't: leave a nonterminal `simp` or add a dependency (documented: CONTRIBUTING.md).
- Don't: count on a fast reply; the contributing page says review "may take some time" (documented: CONTRIBUTING.md).
