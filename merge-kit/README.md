# merge-kit: pre-PR gate (deterministic, no paid API)

    merge-kit/merge-kit check <repo-dir> <base-ref> [--repo owner/name] [--body pr-body.md] [--title "feat: ..."]
    merge-kit/merge-kit selftest          # every check's fixture + every profile has sources
    merge-kit/merge-kit template TauCetiProject/TauCeti   # PR body skeleton
    merge-kit/try-pr owner/name PR-NUMBER [--index]       # run check on an existing GitHub PR (read-only)

`check` writes to `<repo-dir>/.merge-kit/` (override with `--out`):
- `REPORT.md`: findings grouped by the repo's rubric names, `ask` (a mechanical rule fired) vs
  `maybe` (heuristic, or a candidate list to review by hand), plus CI commands and the ready signal.
- `llm-pass-prompt.md`: rubric text + diff + the deterministic findings and reuse candidates. Hand it
  to a Claude subagent (subscription, free); merge-kit never calls a model.
- `findings.json`, `pr-body-template.md`.
Exit code 1 if any `ask` fired. Runs under `nice -n 19`; no builds (`--lake-lint` opts into `lake lint`).

First run on a Lean repo builds a declaration index of `.lake/packages/mathlib` + the repo's
sources (TauCeti + Mathlib: 815k declarations, about 4 min, about 650 MB RAM, cached in `cache/` by git HEAD).

## Layout
- `repos/<owner>__<repo>.yaml`: one profile per repo (TauCeti, mathlib4, cslib, formal-conjectures, FLT,
  physlib, mpmath, abx, anchor, clean, rust-analyzer, tessera). Fields: `ai_policy`, `ci.local`, `pr` (title regex, body
  required/forbidden regexes, disclosure, template), `placement`, `review` (style, recurring asks
  with counts from our data), `max_open_prs`, `ready_signal`, `lean` (sorry/set_option/line rules).
  Every section has a `source:` (URL, repo file + line, or repo#PR); `selftest` fails a profile
  that lacks one.
- `checks/*.py`: one module per check, each with `run(ctx)` and `selftest()` on `checks/fixtures/`.
- `mergekit/`: Lean parsing (`lean.py`), index (`index.py`), git/ctx loading (`context.py`), CLI.
- `validate/`: evaluation on rubric-prereview v2's ground truth (see "Validation").

## Checks -> rubric names -> observatory taxonomy (kw-v1)
| check | what fires | rubric (TauCeti) | observatory class |
|---|---|---|---|
| reuse | same-shape / near-name decls in local Mathlib + repo, with file:line; long `have`s | reuse | reuse |
| placement P1-P3 | prefix-sharing sibling files; redundant import (transitive); `import Mathlib` | placement | placement |
| placement P4 | nearest neighbours by name live in another file of the same area (heuristic) | placement | placement |
| placement P5 | `private` theorem about library notions only (heuristic) | api-design + placement | api-design, placement |
| naming | UpperCamel theorems, snake structures/defs, `_iff` without `↔`, `coe`→`coeFn`, receiver namespace, `lemma` keyword | naming | naming |
| docs | module docstring, public def docstrings, roadmap/proof-mechanics wording | documentation | docs |
| generality | `0 < t` vs `t ≠ 0`, Field/RCLike unused, fixed ℚ base field, unused named hyps (all heuristic) | generality | generality |
| attribution | PR body regexes (`Roadmap:`, Quality pass Q1-Q5, disclosure), title regex, `Authors:` header | attribution, quality-pass, policy | attribution, docs (Q-blocks), policy |
| scope | allowed paths, size caps, topic spread, whitespace-only hunks | scope | scope |
| hygiene | sorry/admit, set_option, native_decide, debug commands, line length | (CI) | ci |
| proof-shape | proof > 50 lines, ≥6-step `rw`, undocumented `show` | proof-quality | proof-quality |
Not covered by any check: observatory `correctness`, `root-cause`, `tests` (no deterministic signal;
leave to the LLM pass and to the human).

## Validation (honest numbers: see validate/RESULTS.md)
Same ground truth and split as rubric-prereview v2 (first-round bot asks from original comment
versions; test = sha256 split). **Contamination warning:** the test asks were read before the
checks were written (the brief points at v2's report), and four fixtures mirror test asks
(1202, 8954, 19002, 44204). Test recall is therefore optimistic. The dev split's ask texts were
not read while writing the rules, only review-lessons' summaries; dev is the more honest number.

## What it does not catch
api-design asks for missing lemmas (`piHilbertBasis_apply`), correctness, proof-plan reuse that
needs semantic matching (a `have` restating an existing lemma under different notation), the
"is this hypothesis needed" judgement, and anything that needs the roadmap. A clean report does
not clear the PR.
