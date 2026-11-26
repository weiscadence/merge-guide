## short
yes, by charter
## quote
> "implemented and maintained by AI contributors, subject to adversarial review." · "Review of implementation PRs is entirely driven by AIs. These operate according to a fixed open source rubric. Humans write the rubric, and update it as the project evolves." · "it is currently switched off. For now, reviews are run from the command line."
> [lit:https://github.com/TauCetiProject/TauCeti/blob/main/README.md]
## ours
<!--n:obs.t.by_repo.taucetiproject_tauceti.landed--><!--/n--> landed, <!--n:obs.t.by_repo.taucetiproject_tauceti.closed--><!--/n--> closed, <!--n:obs.t.by_repo.taucetiproject_tauceti.open--><!--/n--> open of <!--n:obs.t.by_repo.taucetiproject_tauceti.n--><!--/n-->. All landings were bot-merged after AI-rubric review; no human-typed review comment exists on our TauCeti PRs. Closed PRs were reuse or scope blocks and premature roadmap slices (TauCeti#8953, #8954, #8955, #5762).
## rounds
Rubric rounds per reviewed PR: median <!--n:obs.rubric_rounds_median--><!--/n-->, max <!--n:obs.rubric_rounds_max--><!--/n--> recorded rounds; but a single PR can draw seven rubric classes at once (TauCeti#45333), and TauCeti#19035 went through many flagged rounds before closing. Every push restarts the sweep.
## do
- Do: put `Roadmap: <name>` and the full `Quality pass:` block (Q1–Q5) in the body; `gh pr create --body` skips the template.
- Do: run every rubric angle yourself before pushing (reuse first); merge-kit's TauCeti profile maps its checks to the rubric names.
- Do: reply on the thread to re-trigger review after a description edit.
- Don't: stack PRs, use `set_option`, or open API for a roadmap layer marked complete.
- Don't: run `tauceti-review --post` on your own PR; on a dry run pass `--no-archive`.
