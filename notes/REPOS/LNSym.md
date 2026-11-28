## short
not stated
## quote
> No AI section in CONTRIBUTING, README or the PR template. No CLA either; the template only asks you to confirm Apache 2.0. The rule that matters: "Note that before a PR to the `main` branch can be merged: No changes must be requested. All conversations must be resolved. Approval from a maintainer is required."
> [lit:https://github.com/leanprover/LNSym/blob/main/.github/pull_request_template.md]
## ours
<!--n:obs.t.by_repo.leanprover_lnsym.open--><!--/n--> open (<!--n:obs.prs.leanprover_lnsym.open--><!--/n-->). LNSym#267 (2026-11-27) proves five `sorry`s in `sha512_block_armv8_loop_2` with one helper lemma. Not draft, branch not behind. Code owner was requested automatically. CI is in `action_required`, so the build has not run, and there is no review or comment yet.
## process
- Reviewer: CODEOWNERS requests one code owner when the PR opens. The author need not ask. (documented: `.github/CODEOWNERS`; observed: LNSym#267)
- Easy to miss: CI on a first fork PR stops at `action_required`, so the build has not run until a maintainer approves it. Merge needs a maintainer approval, no requested changes and every conversation resolved. Reviews come in bursts; three other outside PRs wait in the same state. (documented: `.github/pull_request_template.md`; observed: LNSym#264, #265, #266, #267)
## rounds
Unmeasured for outsiders. The one outside PR merged in the sample (LNSym#221, 2024-10) got a first review in about a day. Since then the repo has been bursty: a batch of core-developer merges on 2026-11-06, and three other outside PRs (#264, #265, #266) also sit unreviewed with CI awaiting approval.
## do
- Do: expect CI to wait for a maintainer to approve the workflow on a first fork PR; say so in the PR if the build was run locally (observed: #264, #265, #266, #267).
- Do: one code owner is requested for you; you do not need to ask (documented: .github/CODEOWNERS; observed: #267).
- Do: keep the template's Testing and License sections; state whether cosim ran (documented: pull_request_template.md).
- Do: put the copyright header on any new `.lean` file; CI rejects files without it (documented: ci.yml).
- Don't: leave a nonterminal `simp` or add a dependency (documented: CONTRIBUTING.md).
- Don't: count on a fast reply; the contributing page says review "may take some time" (documented: CONTRIBUTING.md).
