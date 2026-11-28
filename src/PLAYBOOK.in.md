# Playbook: from issue to merge

Evidence strength for each tip: **A** = large-n study or a written repo rule; **B** = repeated in our
own data (two or more PRs); **C** = plausible, one case or untested. Per-repo detail: [REPOS/](REPOS/).

## Gate 0. May an agent open here at all?
1. Read CONTRIBUTING, AI_POLICY and the PR template. merge-kit's profile for the repo quotes the rule and its source. **A**
2. Decide who writes the text. Mathlib, cslib, formal-conjectures and rust-analyzer require human-written
   comments and PR bodies; anchor wants most of the body hand-written and no autonomous replies. If no
   human will write them, do not open. [lit:https://leanprover-community.github.io/contribute/index.html] [lit:https://github.com/otter-sec/anchor/blob/master/CONTRIBUTING.md] **A**
3. Never let an agent open PRs or issues where autonomous agents are banned (rust-analyzer, LLVM). [lit:https://github.com/rust-lang/rust-analyzer/blob/master/AI_POLICY.md] [lit:https://llvm.org/docs/AIToolPolicy.html] **A**
4. Do not use AI on issues reserved for learners (good first issue; E-easy + E-has-instructions). [lit:https://github.com/rust-lang/rust-analyzer/blob/master/AI_POLICY.md] **A**
5. Disclose in the exact form asked (sentence, label `LLM-generated`, trailer). **A**

## 1. Pick the task
- **Issue first.** Take an open issue or roadmap target someone asked for. Unwanted features are a named cause of agent-PR rejection; documentation tasks are accepted at 82.1% vs 66.1% for new features. [lit:https://arxiv.org/abs/2601.15195] [lit:https://arxiv.org/abs/2602.08915] **A**
- **Claim it where the repo has a claim flow.** FLT: `claim` → wait for assignment → `propose #PR` → `awaiting-review`. formal-conjectures and tessera: say on the issue you are working on it. TauCeti: the roadmap's intention mechanism feeds workers so they skip claimed items. [lit:https://github.com/ImperialCollegeLondon/FLT/blob/main/CONTRIBUTING.md] [lit:https://github.com/transparency-dev/tessera/blob/main/CONTRIBUTING.md] **A**
- **Dedupe.** Search open PRs, closed PRs and the library. Duplicate PRs are a named rejection cause. [lit:https://arxiv.org/abs/2601.15195] [ours:TauCeti#8953] **A**
- **Do not build ahead of prerequisites** (a roadmap slice whose layer below is not on main). [ours:TauCeti#8955] [ours:TauCeti#5762] **B**
- Outside TauCeti keep at most two open PRs per repo (NumPy's written cap; our default elsewhere). [lit:https://numpy.org/devdocs/dev/index.html] **C**

## 2. Read before writing
- The maintainer's design for the area: the file that owns the behaviour, `git log -S` for who wrote it, the issue and Zulip thread. mpmath's maintainer wrote the code our fix should have extended. [ours:mpmath#1244] **B**
- Prior reviews in that repo: for TauCeti, the rubric texts (open, in TauCetiReview `rubrics/`); for human repos, the maintainer's recent review comments. **B**

## 3. Build
- **Fix at the root**, inside the existing mechanism. [ours:mpmath#1244] [ours:abx#186] [ours:rust-analyzer#22906] **B**
- **Reuse before writing.** For every new declaration: `exact?`, `rw?`, grep Mathlib and the repo. Delete wrappers with no consumer. [ours:TauCeti#8954] **B** (the most common ask: <!--n:profile.tauceti.reuse--><!--/n--> of <!--n:obs.reviewer_prs--><!--/n--> TauCeti PRs)
- **Place it where the topic lives**, in the receiver's namespace. [ours:TauCeti#45354] [ours:TauCeti#19680] **B**
- **State it at full generality**: delete each hypothesis in turn. [ours:TauCeti#19680] **B**
- **Visibility**: library-type helpers public in their natural home; proof-only helpers private. [ours:TauCeti#45756] **B**
- **Tests where the repo keeps them**, then mutation-check them. [ours:mpmath#1244] [ours:tessera#1277] **B**
- **One topic.** Every hunk belongs to the change; no drive-by edits to files under discussion. [ours:cslib#1242] **B**
- After it works, try the shorter direct form. [ours:clean#515] [ours:cslib#1263] **B**

## 4. Run CI locally
Run the profile's `ci.local` commands until green: failed CI is the strongest predictor of non-merge. [lit:https://arxiv.org/abs/2601.15195] [ours:mpmath#1241] **A**
Lean repos differ on `sorry`: TauCeti, cslib, clean and physlib fail on it; formal-conjectures and FLT allow it by design. [data:numbers.json#obs-2]
- **Run the checks on the commit you push**, not one edit earlier. On TauCeti#47588 `lake lint` ran before a last one-line docstring edit and was not repeated; the description had to carry that caveat. [ours:TauCeti#47588] **C**
- **Before you cite a commit sha in a message, confirm it is on the remote**: `git ls-remote <remote> <branch>` must print that sha. A local sha that was never pushed, or was replaced by a later amend, sends the reader to a dead link. **C** (no PR cited)

## 5. Pre-review gate
1. `merge-kit/merge-kit check <repo> origin/main --repo owner/name --body body.md`. Fix every `ask`; look at
   each `maybe`. Expect it to find only some real asks (<!--frac:mk.dev.recall_strict--><!--/frac--> on dev). **B** (measured, small n)
2. Free LLM pass: give `llm-pass-prompt.md` to a model of a different family from the author. On dev the
   union with merge-kit reached <!--frac:mk.dev.union_strict_with_llm.gemini--><!--/frac-->. Treat its output as leads;
   AI reviewers are wrong often (56% of CodeRabbit comments rejected). Never paste AI review text into GitHub where text must be human. [lit:https://arxiv.org/abs/2607.03316] **B/C**
3. TauCeti only: the official engine can be run locally (`tauceti-review <PR>` prints verdicts and posts nothing
   to the PR). It reviews only the PR's current GitHub head, and a default run tries to archive the record to
   the project's data repo and take a review lease: pass `--no-archive`. Whether this cuts first-sweep
   findings is untested. [lit:https://github.com/TauCetiProject/TauCeti/blob/main/README.md] **C**

## 6. Write the PR body
- Who writes it: per Gate 0. Where a human must write it, the agent may supply facts (commands run, files touched), not prose.
- Fill the repo's template by hand: `gh pr create --body` skips it. TauCeti needs `Roadmap:` and the `Quality pass:` block Q1–Q5. [ours:TauCeti#45797] **B**
- Say what the diff does, why, and how it was verified; nothing it does not do. [ours:TauCeti#8486] **B**
- Link every issue it closes, including old ones it happens to fix. [ours:mpmath#1241] **C**
- Check every citation (theorem numbers, tags, equations) against the source. [ours:TauCeti#8954] [ours:formal-conjectures#8069] **B**
- Keep it short. "If someone can spot that the contribution was made with the help of AI, you have more work to do." [lit:https://curl.se/dev/contribute.html] **A**

## 7. Signal ready
Use the repo's signal exactly: FLT `awaiting-review` comment; anchor draft → ready; mathlib4 CI green and
not WIP; TauCeti non-draft with a filled Quality pass. Lack of reviewer engagement is a named reason agent PRs die. [lit:https://arxiv.org/abs/2601.15195] [ours:FLT#1215] **A** (cause) / **C** (remedy)

After opening, check three things the same day. Each repo page says which apply ("How a PR gets a reviewer, and what the author must do").
- **Did CI run at all?** For a first-time contributor many repos hold the workflow until a maintainer approves it. The run then shows the conclusion `action_required` and the PR shows no checks, which is easy to read as "nothing failed". Seen on clean#519 and #526, FLT#1215 and abx#222; a signal comment or label does not start it. REPOS/ names the other repos where we saw it. [ours:clean#519] [ours:FLT#1215] [ours:abx#222] **B**
- **Who reviews?** Find out whether the author requests a reviewer, a maintainer assigns one, a CODEOWNERS file does it, or nothing happens until someone triages. A `review_requested` event at the minute the PR opened, with the author as actor, is CODEOWNERS and not something you did. [ours:cslib#1274] [ours:tessera#1290] **B**
- **Which red marks count?** A CANCELLED or SKIPPED bookkeeping job is not a failure (TauCeti's `reconcile` and `cleanup`; the deciding check is `pr-build / sandboxed-build`). A failed preview deploy from a fork (Vercel asking a team member to authorize) is not yours to fix either. [ours:TauCeti#47554] [ours:TauCeti#47588] [ours:anchor#5366] **B**

## 8. Respond to review
- **One round.** Collect all asks, fix them all, push once. Each push restarts a TauCeti sweep. <!--n:obs.threads_recurred_loose--><!--/n--> of <!--n:obs.threads_total--><!--/n--> of our rubric threads needed a second comment. [ours:TauCeti#19035] **B**
- **Answer the actual ask**: quote it, fix it, re-read every passing rubric. **B**
- **Fresh push vs reply.** On TauCeti, editing the description alone does not re-trigger review; reply on the thread. A contest must meet the rubric's own burden of proof. On human repos, a short reply per thread (human-written where required) plus one push. [ours:TauCeti#45797] **B**
- **What each action re-runs on TauCeti.** A plain push starts a new round: every open rubric thread is rewritten for the new head, and rubrics that had approved are marked stale and re-run before merge. A reply in one rubric's thread reopens that rubric only (written rule; our replies went out next to a push, so our data does not isolate it). A description edit alone re-runs nothing. Labels follow: `awaiting-author` → `awaiting-CI` after the push → `awaiting-review` when the build is green. [lit:https://github.com/TauCetiProject/TauCetiReview/blob/main/REVIEWING.md] [ours:TauCeti#47554] [ours:TauCeti#47588] **A** (rule) / **C** (one PR)
- **Say when the fix removed the thing a finding names.** If a finding points at a declaration and the fix deleted it, write in that thread that it is gone and what stands in its place. [ours:TauCeti#47554] **C**
- A verified technical objection is accepted quickly (rust-analyzer maintainer on `#[salsa::tracked]`). [ours:rust-analyzer#22906] **C**

## 9. When to stop
- A ⛔ on reuse or scope: the code exists or is not wanted. Close it yourself; <!--n:obs.prs_blocked_closed--><!--/n--> of <!--n:obs.prs_blocked--><!--/n--> blocked PRs closed anyway. [ours:TauCeti#8954] **B**
- The maintainer reimplements it: credit them and move on. [ours:abx#152] **B**
- No answer after about a week: one polite ping (human-posted where required), then leave it. **C**
- After merge, watch for follow-up fixes: agent merges draw them at 1.62× the human odds. [lit:https://arxiv.org/abs/2609.26847] **A**

## 10. Sweep what you left open
- **An open issue is not an unanswered issue.** Read the timeline, not the state. abx#148 is still open, but a maintainer's PR that cross-references it (abx#177) merged and fixed it. Before working on or pinging an open issue, look for a merged cross-referenced PR. Evidence: the timeline of abx#148 (our issue). **C**
- **Sweep the threads you commented on, not only the ones you opened.** A search by author misses them. We had comment-only threads on julia#64271, VCVio#1154 and cslib#1243 that the author-based sweep never listed. Use `gh search issues --commenter <login>` next to `--author`. Evidence: those three threads (issues we commented on, not PRs). **C**

## Tips that measurably cut rounds

| tip | evidence | strength |
|---|---|---|
| CI green before review | largest effect in the biggest study; mpmath#1241 [lit:https://arxiv.org/abs/2601.15195] | A |
| Small, one-topic diffs | unmerged agent PRs are larger [lit:https://arxiv.org/abs/2601.15195]; our zero-ask landings were small | A |
| Dedupe and reuse first | duplicate PRs are a named rejection cause [lit:https://arxiv.org/abs/2601.15195]; reuse blocks closed our PRs | A |
| Fill the template by hand | TauCeti quality-pass asks disappear when the block is present (merge-kit catches it) | B |
| Batch every fix into one push | recurrence data above; each push restarts a sweep | B |
| merge-kit + free LLM pass | measured recall on dev only, small n | B/C |
| Local tauceti-review dry run | mechanism certain, effect never measured | C |
