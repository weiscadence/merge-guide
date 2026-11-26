# abx

`ArtBlocks/abx` · profile: `merge-kit/repos/ArtBlocks__abx.yaml`

## AI policy

> No AI section in CONTRIBUTING. Content rule: "Do not add planning, strategy, research notebooks, review transcripts, or private triage records."
> [lit:https://github.com/ArtBlocks/abx/blob/main/CONTRIBUTING.md]

- **Stance:** no AI section in CONTRIBUTING.md
- **Who may write PR text and replies:** not stated
- **Disclosure:** not stated; disclose anyway
- **Forbidden content:** Do not add planning, strategy, research notebooks, review transcripts, or private triage records
- Source: https://github.com/ArtBlocks/abx/blob/main/CONTRIBUTING.md lines 37-46 (gh api 2026-11-25)

## Ready signal

fork workflow runs need maintainer approval on each push; ask once CI is approved and green (source: abx CONTRIBUTING.md lines 66-69)

Open-PR cap: no written cap; our default 2 (source: abx CONTRIBUTING.md (none stated))

## CI to run locally

```sh
corepack enable
pnpm install --frozen-lockfile
pnpm build
pnpm test
cd contracts && forge soldeer install && forge test
```
Note: do not raise code-size test limits to make a change pass
Source: abx CONTRIBUTING.md lines 12-35, 53-60

## PR body skeleton

```
<Behaviour changed.>

Verified: <commands run>
Affects: contracts / deployed addresses / package APIs / CLI / public docs: <which, or none>
```

## What reviewers here actually ask for (our data)

Review style: human maintainer; superseded our abx#152 and #186 with own PRs (#177, #197)

| class | asks / threads in our data |
|---|---|
| root-cause | <!--n:profile.abx.root_cause--><!--/n--> |

Source: FAILURE-MODES.md (review-harvest counts), general classes 'Superseded without merge'

## Our PRs here

<!--n:obs.t.by_repo.artblocks_abx.landed--><!--/n--> landed, <!--n:obs.t.by_repo.artblocks_abx.closed--><!--/n--> closed, <!--n:obs.t.by_repo.artblocks_abx.open--><!--/n--> open; all landings human-merged. Two closed PRs (abx#152, #186) were superseded by the maintainer's own PRs, with credit, that extended the shared script preparation instead.

## Typical rounds

Usually none: the maintainer merges or reimplements.

## Do / don't

- Do: say how the change was verified (`pnpm test`, `forge test`); fork CI needs maintainer approval on each push.
- Do: extend the shared mechanism rather than adding a branch.
- Don't: raise code-size test limits to make a change pass.
