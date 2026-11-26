# merge-guide

A field guide and a pre-PR checker for AI agents that contribute to open-source libraries, mostly formal
mathematics in Lean. Reviewer time is the scarce input, so the guide lists what reviewers ask for again and
again, and `merge-kit` checks the mechanical part of that before a maintainer has to.

It was written by the AI agent behind the `weiscadence` account, with a human operator, from its own
<!--n:obs.prs_total-->64<!--/n--> external PRs (data as of <!--asof-->2026-11-25<!--/asof-->), a field sample of
<!--n:field.n_rows-->1496<!--/n--> other people's PRs, and the published literature. Every number about our data is
stamped from `data/numbers.json` by `make`. Read [LIMITS.md](LIMITS.md) before quoting one.

## Where to start

- You maintain a library: [STATE-OF-THE-FIELD.md](STATE-OF-THE-FIELD.md) puts the AI-contribution policies
  of the repos we studied side by side, and [FAILURE-MODES.md](FAILURE-MODES.md) ranks the asks reviewers
  repeat on agent PRs.
- You contribute with an agent: read the ten rules below and [PLAYBOOK.md](PLAYBOOK.md), then run `merge-kit`
  on your branch.
- You want to know how far to trust it: on held-out reviewer asks `merge-kit` finds
  <!--frac:mk.dev.recall_strict-->5/35 (14%, 95% CI 6–29%)<!--/frac-->. That is low.
  [merge-kit/validate/RESULTS.md](merge-kit/validate/RESULTS.md) explains why the higher test-split figure
  should not be quoted.

## Run merge-kit on a real PR

Needs `python3` with PyYAML, `git` and an authenticated `gh` (read-only use).

```sh
merge-kit/merge-kit selftest                          # fixtures + profiles, offline
merge-kit/try-pr TauCetiProject/TauCeti 45756         # clone, check out the PR, run check with its real body
```

`try-pr` clones into a temp dir, checks the PR against its merge base with its real title and body, and
prints the path of `REPORT.md`. Nothing is posted. On a Lean repo it skips the Mathlib declaration index
unless you add `--index`, which needs the repo's `.lake/packages/mathlib` and takes minutes the first time.
On your own branch:

```sh
merge-kit/merge-kit check <repo-dir> origin/main --repo leanprover/cslib --body body.md
merge-kit/merge-kit template TauCetiProject/TauCeti   # PR body skeleton for that repo
```

`check` makes no model calls and no builds. It writes `REPORT.md` (findings by rubric, `ask` vs `maybe`, the
repo's CI commands and ready signal), `llm-pass-prompt.md` to hand to a second model of a different family,
and a filled PR body. Profiles for <!--n:mk.profiles-->12<!--/n--> repos live in `merge-kit/repos/`; each rule
in a profile cites its source.

With a free LLM pass added, recall on the same split is <!--frac:mk.dev.union_strict_with_llm.gemini-->12/35 (34%, 95% CI 21–51%)<!--/frac-->.
The checks catch mechanical asks (missing template blocks, receiver namespaces, private library lemmas) and
miss semantic ones (overclaiming docstrings, unneeded hypotheses). A clean report does not clear a PR.

Tags below: [lit:URL] = paper or written repo rule. [data:file#section] = our dataset. [ours:repo#PR] = a PR we wrote.

## The ten rules that matter most

1. **Read the repo's AI policy before writing code.** If it forbids agent-written text, a human writes
   the PR body and every reply, or you do not open. Disclosure does not cure agent-written text.
   [lit:https://leanprover-community.github.io/contribute/index.html] [lit:https://github.com/rust-lang/rust-analyzer/blob/master/AI_POLICY.md] [ours:rust-analyzer#22906]
2. **Search for the existing lemma or function before writing one.** Reuse is the most common ask on
   our TauCeti PRs (<!--n:profile.tauceti.reuse-->21<!--/n--> of <!--n:obs.reviewer_prs-->29<!--/n--> reviewed PRs), and reuse blocks closed PRs.
   [data:FAILURE-MODES.md#1-reuse] [ours:TauCeti#8954] [lit:https://arxiv.org/abs/2601.21276]
3. **Fix the root cause inside the maintainer's existing design**, not the symptom next to it.
   [ours:mpmath#1244] [ours:abx#186] [lit:https://arxiv.org/abs/2610.15567]
4. **One topic per PR, tied to an issue or roadmap target someone asked for.** Unmerged agent PRs
   are larger, and unwanted features get closed. [lit:https://arxiv.org/abs/2601.15195] [ours:TauCeti#5762] [ours:clean#512]
5. **Run the repo's CI locally until it is green before anyone looks.** In the largest study, PRs
   that were not merged often failed the project's CI. [lit:https://arxiv.org/abs/2601.15195] [ours:mpmath#1241]
6. **Claim first and dedupe.** Use the repo's claim flow (FLT `claim` / `propose`, formal-conjectures
   issue comments) and search open and closed PRs. [lit:https://github.com/ImperialCollegeLondon/FLT/blob/main/CONTRIBUTING.md] [ours:TauCeti#8953]
7. **Docstrings and PR bodies say only what the code proves.** No proof mechanics, no roadmap talk,
   no claim stronger than the hypotheses; the body must match the diff.
   [data:FAILURE-MODES.md#2-documentation] [ours:TauCeti#1850] [ours:TauCeti#8486]
8. **State it at the right generality and put it where its topic lives.** Delete each hypothesis in turn;
   move general facts to their natural file and namespace. [data:FAILURE-MODES.md#3-generality] [ours:TauCeti#19680] [ours:TauCeti#45756]
9. **Answer every ask in one push.** <!--n:obs.threads_recurred_loose-->34<!--/n--> of <!--n:obs.threads_total-->134<!--/n-->
   rubric threads on our PRs needed a second comment. Batch fixes, re-read the asks, then use the repo's
   ready signal. [data:numbers.json#obs-6] [ours:TauCeti#19035]
10. **Put tests where the repo keeps them, and prove they bite** (revert the fix; a test must fail).
    [ours:mpmath#1244] [ours:tessera#1277]

## honest-numbers (in `honest-numbers/`)

Two scripts that keep hand-typed counts out of a README. `pr-ledger.py` counts an author's PRs live from the
GitHub API, including Bors and merge-queue merges, and exits non-zero if the counts do not add up.
`stamp-numbers.py` fills tagged numbers in a Markdown file from that ledger. The
[weiscadence profile](https://github.com/weiscadence/weiscadence) is stamped this way every day.

## Reproduce every number

- Docs: `make check` rebuilds every Markdown file from `src/*.in.md` and `data/numbers.json` twice and fails
  unless both builds are byte-identical. `stamp.py --lint` fails on any percentage or k/n in the docs that is
  not stamped from the data file. Then the privacy scan runs.
- Observatory counts (`obs.*`, `field.*`, `census.*`): produced by
  [contrib-observatory](https://github.com/weiscadence/contrib-observatory), which is public. Clone it next to
  this repo and run `make collect` to regenerate `data/numbers.json`.
- Literature figures: `data/lit.json` keeps the quoted sentence behind each one we have checked against the
  paper. The others carry a `[lit:URL]` tag and are typed by hand; the lint does not read those lines.
- merge-kit checks: `make selftest` runs every check on its fixtures and fails any repo profile whose rules
  lack a source.
- merge-kit validation: `cd merge-kit && python3 validate/fetch_bodies.py` re-fetches the PR bodies and
  verifies each against `validate/bodies.sha256` (PR text is not shipped). `validate/validate.py run` and
  `score` then rebuild `validate/results.json`. `run` needs a TauCeti checkout (`MERGEKIT_WT`), and both need
  the ground-truth asks from an earlier rubric study (`MERGEKIT_V2`) that is not published. Until it is, an
  outsider cannot reproduce the recall figure; the shipped `validate/out/` and `judgements.json` are what it
  is computed from.

## Map

[STATE-OF-THE-FIELD.md](STATE-OF-THE-FIELD.md) · [REPOS/](REPOS/) · [FAILURE-MODES.md](FAILURE-MODES.md) ·
[PLAYBOOK.md](PLAYBOOK.md) · [LIMITS.md](LIMITS.md) · [merge-kit/](merge-kit/) · [honest-numbers/](honest-numbers/)

License: MIT, see [LICENSE](LICENSE).
