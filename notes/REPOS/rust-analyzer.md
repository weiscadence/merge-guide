## short
NO; no autonomous agents
## quote
> "AI should not be used to generate comments when communicating with maintainers." · "We do not allow autonomous agents to be used to open pull requests or issues to our projects." · "AI should not be used to author code for E-easy+E-has-instructions issues."
> [lit:https://github.com/rust-lang/rust-analyzer/blob/master/AI_POLICY.md]
## ours
<!--n:obs.t.by_repo.rust_lang_rust_analyzer.closed--><!--/n--> closed (rust-analyzer#22906). The cautionary case: an agent opened it and wrote the body, both against the written policy. The code review itself was constructive (restore `#[deprecated]` rather than delete it; a lint sweep belongs in a separate PR).
## rounds
Two to three days between rounds; scope ambiguity cost one round.
## do
- Don't: open here with an agent. A human must open the PR, write the body and every reply.
- Do (human author): disclose AI use; quote any AI-produced context in a quote block; squash before merge.
