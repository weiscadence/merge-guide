# honest-numbers

Stale counts in READMEs, grant applications and handoffs are a quiet way to be wrong. This folder has two scripts so that no number gets typed by hand.

- **`pr-ledger.py`** counts an author's PRs live from the GitHub API (needs `gh` auth). A PR counts as **landed** if GitHub shows it merged, or if it was closed with a `[Merged by Bors]` title. Bors pushes the commit itself and then closes the PR, so a plain `is:merged` search misses it. For each landed PR it records who merged it: `merged_by`, or the actor on the merged/closed event when a merge queue leaves `merged_by` empty. The merger is labelled human, bot or unknown. Every count is saved with the list of PRs behind it. The script **exits 1 if the counts don't add up**: landed + closed unmerged + open = total, human + bot + unknown = landed, and inside + outside = total.
- **`stamp-numbers.py`** fills tagged numbers in a markdown file from that ledger:
  - `<!--n:landed/(landed+closed_unmerged)%-->71%<!--/n-->` holds a sum or percentage over named counts
  - `<!--list:tauceti_bors--><!--/list-->` becomes a list of links to the PRs
  - `<!--asof--><!--/asof-->` becomes the date the ledger was made

  The tags don't show when the markdown renders. If a tag names a count that doesn't exist, the script stops instead of guessing, and running it a second time changes nothing.

```
python3 pr-ledger.py --json ledger.json
python3 stamp-numbers.py ledger.json README.md          # dry run: show what would change; exits 2 if anything would
python3 stamp-numbers.py ledger.json README.md --write
```
Run both on a daily schedule and commit only when the diff isn't empty. To track a different author, edit `AUTHORS`. Live example: [weiscadence profile README](https://github.com/weiscadence/weiscadence).

These scripts were first published as `weiscadence/honest-numbers` and then `weiscadence/agent-tools`; both now point here.
