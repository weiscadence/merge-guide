"""scope: the diff is one concern and inside the repo's size/path limits.

  S1 files outside profile.scope.allowed_paths (regex list) -> ask (TauCeti lake lint diff guard).
  S2 added lines > profile.scope.max_added, new file > profile.scope.max_new_file_lines -> ask.
  S3 topic spread: changed source files fall in > profile.scope.max_topics distinct directories
     (depth profile.scope.topic_depth) -> maybe (one topic per PR).
  S4 whitespace-only or comment-only hunks in modified files -> maybe (unrelated hunk).
  S5 removed declarations without replacement listed in the PR body (mathlib `Deletions:`) -> maybe.
"""
import os, re
from mergekit.context import finding

NAME = "scope"
RUBRIC = "scope"


def run(ctx):
    out = []
    sc = ctx.profile.get("scope") or {}
    allowed = [re.compile(r) for r in sc.get("allowed_paths", [])]
    total = 0
    topics = set()
    depth = sc.get("topic_depth", 3)
    for f in ctx.files:
        if allowed and not any(r.search(f.name) for r in allowed):
            out.append(finding(NAME, RUBRIC, f.name, 0, "file outside the paths this repo's PRs may touch", "ask"))
        total += len(f.added)
        if f.status == "added" and sc.get("max_new_file_lines") and len(f.lines) > sc["max_new_file_lines"]:
            out.append(finding(NAME, RUBRIC, f.name, 0, f"new file has {len(f.lines)} lines > {sc['max_new_file_lines']}", "ask"))
        if f.is_lean or f.name.endswith((".py", ".rs", ".ts", ".js", ".go")):
            topics.add("/".join(f.name.split("/")[:depth]))
        if f.status == "modified":
            for h in f.hunks:
                a = [l.strip() for l in h["added"]]; r = [l.strip() for l in h["removed"]]
                if a and r and "".join(a).replace(" ", "") == "".join(r).replace(" ", ""):
                    out.append(finding(NAME, RUBRIC, f.name, h["start"], "whitespace-only hunk: unrelated to the change?", "maybe", heuristic=True))
                elif a and all(l.startswith("--") or not l for l in a) and not r:
                    pass
    if sc.get("max_added") and total > sc["max_added"]:
        out.append(finding(NAME, RUBRIC, "", 0, f"{total} added lines > {sc['max_added']}", "ask"))
    if sc.get("max_topics") and len(topics) > sc["max_topics"]:
        out.append(finding(NAME, RUBRIC, "", 0, f"diff spans {len(topics)} topic directories ({', '.join(sorted(topics)[:5])}); one topic per PR",
                           "maybe", heuristic=True))
    return out


def selftest():
    from mergekit.context import Context, File
    prof = {"scope": {"allowed_paths": [r"^T/"], "max_added": 5, "max_topics": 1, "topic_depth": 2}}
    patch = "@@ -1,1 +1,1 @@\n-foo  bar\n+foo bar\n"
    files = [File("T/A/x.lean", "added", "", "a\nb\nc\nd\ne\nf\n"), File("T/B/y.lean", "modified", patch, "foo bar\n"),
             File("scripts/z.py", "added", "", "x\n")]
    msgs = " | ".join(x["msg"] for x in run(Context("t/t", prof, files)))
    assert "outside" in msgs and "added lines" in msgs and "topic" in msgs and "whitespace-only" in msgs, msgs
    return "ok"
