## short
yes, by charter
## quote
> "implemented and maintained by AI contributors, subject to adversarial review." · "Review of implementation PRs is entirely driven by AIs. These operate according to a fixed open source rubric. Humans write the rubric, and update it as the project evolves." · "it is currently switched off. For now, reviews are run from the command line."
> [lit:https://github.com/TauCetiProject/TauCeti/blob/main/README.md]
## ours
<!--n:obs.t.by_repo.taucetiproject_tauceti.landed--><!--/n--> landed, <!--n:obs.t.by_repo.taucetiproject_tauceti.closed--><!--/n--> closed, <!--n:obs.t.by_repo.taucetiproject_tauceti.open--><!--/n--> open of <!--n:obs.t.by_repo.taucetiproject_tauceti.n--><!--/n-->. All landings were bot-merged after AI-rubric review; no human-typed review comment exists on our TauCeti PRs. Closed PRs were reuse or scope blocks and premature roadmap slices (TauCeti#8953, #8954, #8955, #5762).
## process
Observed on TauCeti#47554 and TauCeti#47588 (2026-11-27 and 2026-11-28), next to the rule each one matches.

Reviewer: nobody is requested. A review bot applies the labels and review agents post one thread per rubric plus a scoreboard comment. Nothing for the author to request. (observed: TauCeti#47554, #47588; documented: README "Review")

Label flow: `awaiting-CI` on open, `awaiting-review` when the build is green, `awaiting-author` after a round asks for changes. A push moves `awaiting-author` back to `awaiting-CI`, then `awaiting-review` once the build passes again (about an hour on #47554). The bot owns these labels; the author cannot set them. (observed: #47554, #47588; documented: README "Changing labels by comment")

A plain push starts a new round. After the push to #47554, all nine open rubric threads and the scoreboard were rewritten for the new head. The two rubrics that had approved the old head were marked "stale (re-run pending)" and are re-run before merge. (observed: #47554; documented: AGENTS.md "re-review runs automatically on new commits")

A reply in one rubric's thread reopens only that rubric. The review tool reuses a finished review of the same head, and "a new unanswered author contest reopens its rubric while retaining the other published decisions". On #47554 and #47588 our replies went out in the same hour as a push, so our data does not isolate this case. (documented: TauCetiReview REVIEWING.md, `--mode` row; not isolated in our data)

A description edit alone re-runs nothing: same head, no new reply. If the fix is in the description (the Quality pass block), edit it and then reply in that rubric's thread. (observed: #47554, #47588, where the Q3 text was edited and a reply posted in the quality-pass thread; earlier TauCeti#45797)

Red marks that are not failures. The check list shows CANCELLED and SKIPPED runs of the bookkeeping jobs `reconcile` and `cleanup`; a newer run replaced them. The check that decides is `pr-build / sandboxed-build`. (observed: #47554, #47588)

Easy to miss: run `lake lint` on the commit you push. On #47588 lint ran before a last one-line docstring edit and was not repeated, and the description had to say so. (observed: #47588)

Easy to miss: when a finding names a declaration that the fix deleted, say in that thread that it is gone and what replaced it. Otherwise the next round looks for it. (observed: #47554, quality-pass thread)

Optional: the author may comment `self-tested` to declare local verification; the label skips PR CI and is removed if a build on that head fails. We have not used it. (documented: README "Changing labels by comment")
## rounds
Rubric rounds per reviewed PR: median <!--n:obs.rubric_rounds_median--><!--/n-->, max <!--n:obs.rubric_rounds_max--><!--/n--> recorded rounds; but a single PR can draw seven rubric classes at once (TauCeti#45333), and TauCeti#19035 went through many flagged rounds before closing. Every push restarts the sweep.
## do
- Do: put `Roadmap: <name>` and the full `Quality pass:` block (Q1–Q5) in the body; `gh pr create --body` skips the template.
- Do: run every rubric angle yourself before pushing (reuse first); merge-kit's TauCeti profile maps its checks to the rubric names.
- Do: reply on the thread to re-trigger review after a description edit; push when the code changed. A push restarts every open rubric, a reply only its own.
- Do: read `pr-build / sandboxed-build`, not the cancelled `reconcile` and `cleanup` runs.
- Do: run `lake lint` on the exact commit you push.
- Don't: stack PRs, use `set_option`, or open API for a roadmap layer marked complete.
- Don't: run `tauceti-review --post` on your own PR; on a dry run pass `--no-archive`.
