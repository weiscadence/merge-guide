#!/usr/bin/env python3
"""Build src/REPOS/<repo>.in.md from merge-kit/repos/<profile>.yaml + notes/REPOS/<repo>.md.

The profile is the single source for AI rule, CI commands, ready signal and recurring asks, so the
guide and merge-kit cannot disagree. The notes file adds the verbatim policy quote, the reviewer/author process, rounds, do/don't.
Recurring-ask counts are emitted as stamp tags (profile.<repo>.<class>) so stamp.py fills them.
"""
import glob, os, re, sys
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json
NUM = json.load(open(os.path.join(HERE, "data", "numbers.json")))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")


def obs_slug(repo):
    return slug(repo)


def page(y, notes):
    repo = y["repo"]; name = repo.split("/")[1]; s = slug(name)
    ai, ci, pr, rv, rd, mx = (y.get(k) or {} for k in ("ai_policy", "ci", "pr", "review", "ready_signal", "max_open_prs"))
    L = [f"# {name}", "", f"`{repo}` · profile: `merge-kit/repos/{os.path.basename(y['_path'])}`", ""]
    L += ["## AI policy", "", notes.get("quote", "").strip(), "",
          f"- **Stance:** {ai.get('stance')}", f"- **Who may write PR text and replies:** {ai.get('who_may_write_text')}",
          f"- **Disclosure:** {ai.get('disclosure')}"]
    for k in ("cla", "forbidden_content", "consequence", "verdict_for_agents"):
        if ai.get(k):
            L.append(f"- **{k.replace('_', ' ').capitalize()}:** {ai[k]}")
    L += [f"- Source: {ai.get('source')}", "", "## Ready signal", "", f"{rd.get('how')} (source: {rd.get('source')})", ""]
    if mx:
        L += [f"Open-PR cap: {mx.get('value')} (source: {mx.get('source')})", ""]
    L += ["## CI to run locally", "", "```sh"] + list(ci.get("local") or ["(none recorded)"]) + ["```"]
    if ci.get("notes"):
        L.append(f"Note: {ci['notes']}")
    L += [f"Source: {ci.get('source')}", ""]
    if pr.get("body_template"):
        L += ["## PR body skeleton", "", "```", pr["body_template"].rstrip(), "```", ""]
    L += ["## What reviewers here actually ask for (our data)", "", f"Review style: {rv.get('style')}", ""]
    rec = rv.get("recurring") or {}
    if rec:
        L += ["| class | asks / threads in our data |", "|---|---|"]
        L += [f"| {c} | <!--n:profile.{s}.{slug(c)}--><!--/n--> |" for c in sorted(rec, key=lambda c: (-rec[c], c))]
        L.append("")
    else:
        L += [f"None recorded: {rv.get('recurring_note', 'no review in our data')}.", ""]
    L += [f"Source: {rv.get('source')}", ""]
    if notes.get("process"):
        L += ["## How a PR gets a reviewer, and what the author must do", "", notes["process"].strip(), ""]
    if notes.get("ours"):
        L += ["## Our PRs here", "", notes["ours"].strip(), ""]
    if notes.get("rounds"):
        L += ["## Typical rounds", "", notes["rounds"].strip(), ""]
    if notes.get("do"):
        L += ["## Do / don't", "", notes["do"].strip(), ""]
    if y.get("corrected") or rd.get("corrected"):
        L += ["## Profile corrections", "", f"- {rd.get('corrected') or y.get('corrected')}", ""]
    return "\n".join(L).rstrip() + "\n"


def read_notes(p):
    if not os.path.exists(p):
        return {}
    out, cur = {}, None
    for line in open(p):
        m = re.match(r"^## (\w+)\s*$", line)
        if m:
            cur = m.group(1); out[cur] = ""; continue
        if cur:
            out[cur] += line
    return out


def main():
    os.makedirs(os.path.join(HERE, "src", "REPOS"), exist_ok=True)
    index = ["# Repos", "", "One page per repo, generated from the merge-kit profile plus a short note.", "",
             "| repo | agent-written text allowed? | our PRs (landed / closed / open) |", "|---|---|---|"]
    for p in sorted(glob.glob(os.path.join(HERE, "merge-kit", "repos", "*.yaml"))):
        y = yaml.safe_load(open(p)); y["_path"] = p
        name = y["repo"].split("/")[1]
        notes = read_notes(os.path.join(HERE, "notes", "REPOS", f"{name}.md"))
        open(os.path.join(HERE, "src", "REPOS", f"{name}.in.md"), "w").write(page(y, notes))
        o = f"obs.t.by_repo.{obs_slug(y['repo'])}"
        has = o + ".n" in NUM
        who = (notes.get("short") or "").strip() or str((y.get("ai_policy") or {}).get("who_may_write_text"))[:60]
        cnt = f"<!--n:{o}.landed--><!--/n--> / <!--n:{o}.closed--><!--/n--> / <!--n:{o}.open--><!--/n-->" if has else "not in snapshot"
        index.append(f"| [{name}]({name}.md) | {who} | {cnt} |")
    index += ["", "Counts are from the observatory snapshot of <!--asof--><!--/asof-->; a repo where we have no PR in it reads "
              "\"not in snapshot\"; its page says what we did there instead. See [../LIMITS.md](../LIMITS.md)."]
    open(os.path.join(HERE, "src", "REPOS", "README.in.md"), "w").write("\n".join(index) + "\n")


if __name__ == "__main__":
    main()
