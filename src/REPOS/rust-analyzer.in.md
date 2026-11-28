# rust-analyzer

`rust-lang/rust-analyzer` · profile: `merge-kit/repos/rust-lang__rust-analyzer.yaml`

## AI policy

> "AI should not be used to generate comments when communicating with maintainers." · "We do not allow autonomous agents to be used to open pull requests or issues to our projects." · "AI should not be used to author code for E-easy+E-has-instructions issues."
> [lit:https://github.com/rust-lang/rust-analyzer/blob/master/AI_POLICY.md]

- **Stance:** RESTRICT: no autonomous agents
- **Who may write PR text and replies:** humans only: 'AI should not be used to generate comments when communicating with maintainers'; PR body and replies in your own words; 'We do not allow autonomous agents to be used to open pull requests or issues to our projects'
- **Disclosure:** 'we kindly ask you to disclose usage of AI tools'; AI context only inside a quote block; citation required for AI-authored changes to analysis code
- **Forbidden content:** AI-authored code on E-easy+E-has-instructions issues; new ide-assists during the feature freeze
- **Verdict for agents:** DO NOT OPEN unless a human author writes the body and every reply
- Source: https://github.com/rust-lang/rust-analyzer/blob/master/AI_POLICY.md lines 1-35 (fetched 2026-11-25); rust-analyzer#22906

## Ready signal

link the issue; non-draft (source: rust-analyzer CONTRIBUTING.md 'Fixing a bug or improving a feature')

Open-PR cap: not stated (source: rust-analyzer CONTRIBUTING.md (none stated))

## CI to run locally

```sh
cargo test
cargo fmt --check
cargo clippy
```
Note: squash commits before merge (maintainer ask, rust-analyzer#22906)
Source: rust-analyzer CONTRIBUTING.md; maintainer notes

## PR body skeleton

```
<Must be written by a human, in their own words (AI_POLICY.md).>
```

## What reviewers here actually ask for (our data)

Review style: human maintainers; 2-3 days between rounds

| class | asks / threads in our data |
|---|---|
| policy | <!--n:profile.rust_analyzer.policy--><!--/n--> |
| root-cause | <!--n:profile.rust_analyzer.root_cause--><!--/n--> |
| scope | <!--n:profile.rust_analyzer.scope--><!--/n--> |

Source: FAILURE-MODES.md (review-harvest counts), general classes; maintainer notes

## Our PRs here

<!--n:obs.t.by_repo.rust_lang_rust_analyzer.closed--><!--/n--> closed (<!--n:obs.prs.rust_lang_rust_analyzer.closed--><!--/n-->). rust-analyzer#22906 is the cautionary case: an agent opened it and wrote the body, both against the written policy. The code review itself was constructive (restore `#[deprecated]` rather than delete it; a lint sweep belongs in a separate PR).

## Typical rounds

Two to three days between rounds; scope ambiguity cost one round.

## Do / don't

- Don't: open here with an agent. A human must open the PR, write the body and every reply.
- Do (human author): disclose AI use; quote any AI-produced context in a quote block; squash before merge.
