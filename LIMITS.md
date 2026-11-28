# Limits: read before quoting anything here

1. **Single operator, single agent.** All <!--n:obs.prs_total-->85<!--/n--> of "our" PRs come from one AI agent run by
   one person, across two GitHub accounts. Habits of that operator (which repos, which tasks, how fast
   replies went out) are baked into every "ours" number. Nothing here is a sample of agents in general.
2. **Small n.** Outside TauCeti we have <!--n:obs.prs_total-obs.t.by_repo.taucetiproject_tauceti.n-obs.t.by_repo.taucetiproject_taucetiroadmap.n-->45<!--/n-->
   PRs spread over <!--n:obs.repos_total-2-->22<!--/n--> repos, and only <!--n:obs.comments_human-->43<!--/n--> review comments with no AI marker.
   Per-repo rows with fewer than about 20 resolved PRs have intervals too wide to rank. The hand-typed
   human classes (root cause, tests, policy) rest on one or two PRs each.
3. **AI review is edited in place.** TauCeti's rubric comments are overwritten to "✅ now passing" when
   fixed. The original ask survives only in the comment's edit history (merge-kit's validation set uses
   it); the observatory counts use current bodies. So "approve" means "passes now", early texts are
   under-represented, and classes that get fixed quickly look rarer than they were.
4. **Date confounds.** Author model, reviewer model, rubric set and repo mix all change by month. The
   July cohort is almost all one reviewer model and unknown authors; November is newer models and more
   open PRs. Month-to-month merge-rate differences mostly overlap; the one non-overlapping pair
   (July <!--n:obs.t.trend.2026_07.rate-->88<!--/n-->% vs September <!--n:obs.t.trend.2026_09.rate-->20<!--/n-->%, n = <!--n:obs.t.trend.2026_07.n-->17<!--/n--> and <!--n:obs.t.trend.2026_09.n-->5<!--/n-->) coincides with a change in which repos we targeted. [data:numbers.json#obs-7]
5. **Classifier agreement has one rater.** The finding classifier agrees with the gold labels on
   <!--n:obs.gold_agree-->29<!--/n--> of <!--n:obs.gold_n-->40<!--/n--> (CI <!--n:obs.gold_lo-->57<!--/n-->–<!--n:obs.gold_hi-->84<!--/n-->%), but the gold labels were made by
   the same person who wrote the classifier, and the rules were tuned on overlapping data. A blind packet
   for a second rater exists in the observatory (`gold/blind-packet.md`); it has not been labelled yet.
6. **merge-kit validation is not blind.** The checks' author judged the matches. The test split is
   contaminated (its asks were read before the rules were written), so only the dev split is quoted:
   <!--frac:mk.dev.recall_strict-->5/35 (14%, 95% CI 6–29%)<!--/frac--> strict over <!--n:mk.dev.n_prs-->14<!--/n--> PRs. Precision is low.
7. **"Human" means "no AI marker".** Outside TauCeti no marker exists, so AI-written comments that do not
   say so are counted as human. The AI share of review is therefore a floor there.
8. **Field detection has unknown recall.** A PR counts as declared only if it names a tool; a seeded audit
   found 39 of 40 declared rows genuine, but undeclared AI PRs are invisible. Keyword samples follow
   GitHub search order, so only the baseline sample is unselected. [data:numbers.json#obs-detection]
9. **Census scope.** The full-window census covers TauCeti, formal-conjectures and mathlib4 (mathlib4 only
   since the `LLM-generated` label appeared). Comment bodies are sampled, not complete. If the census output
   is missing when the guide is rebuilt, its cells read "(census pending)" instead of a number.
10. **Policies move.** Each policy quote was fetched once, on the date its profile records (`source:` in `merge-kit/repos/*.yaml`). The daily number refresh does not refetch them. Re-read the repo's file before relying on it.
11. **What the lint covers.** `make check` fails on any untagged ratio or percentage outside a line that
    cites the literature. Plain counts in prose (for example "one operator") are not linted.

## Known corrections made while building this guide
- merge-kit's TauCeti profile said review "runs automatically on push". The TauCeti README says automatic
  review is switched off and reviews are run from the command line. The profile is fixed.
- The observatory's prose said physlib's CI is not a `sorry` gate; its own table (and a later check of the
  workflow: `--iofail` fails on the `sorry` warning, and the cited `sorry` lines sit in a block comment)
  say it is. This guide uses the table.
- An earlier internal note said a `tauceti-review` dry run "posts nothing". True for the PR, but by default
  it also tries to archive the run to the project's data repo and take a review lease. Use `--no-archive`.
