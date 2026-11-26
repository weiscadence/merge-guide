"""attribution / PR body: the description carries what the repo profile requires.

Profile keys used (repos/<owner>__<repo>.yaml -> pr.body):
  required:   list of {id, regex, msg, rubric}   each regex must match (multiline) -> ask
  forbidden:  list of {id, regex, msg, rubric}   must not match -> ask
  disclosure: {regex, msg}                       AI-use disclosure line -> ask when missing
  title_regex: PR title must match -> ask
Also: file header `Authors:` line present in new Lean files when profile.lean.authors_header.
With no PR body supplied, emits one `info` finding and the generated template (see template()).
"""
import re
from mergekit.context import finding

NAME = "attribution"
RUBRIC = "attribution"


def run(ctx):
    out = []
    pr = (ctx.profile.get("pr") or {})
    body_rules = pr.get("body") or {}
    if ctx.pr_body is None:
        out.append(finding(NAME, RUBRIC, "", 0, "no PR body given (--body FILE); body checks skipped. A template is in pr-body-template.md", "info"))
    else:
        b = ctx.pr_body
        for r in body_rules.get("required", []):
            if not re.search(r["regex"], b, re.M):
                out.append(finding(NAME, r.get("rubric", RUBRIC), "", 0, f"PR body: {r['msg']}", "ask"))
        for r in body_rules.get("forbidden", []):
            m = re.search(r["regex"], b, re.M)
            if m:
                out.append(finding(NAME, r.get("rubric", RUBRIC), "", 0, f"PR body: {r['msg']} (`{m.group(0)[:60]}`)", "ask"))
        disc = body_rules.get("disclosure")
        if disc and not re.search(disc["regex"], b, re.M | re.I):
            out.append(finding(NAME, "policy", "", 0, f"PR body: {disc['msg']}", "ask"))
    tr = pr.get("title_regex")
    if tr and ctx.title is not None and not re.search(tr, ctx.title):
        out.append(finding(NAME, "policy", "", 0, f"PR title `{ctx.title}` does not match `{tr}`", "ask"))
    if (ctx.profile.get("lean") or {}).get("authors_header"):
        for f in ctx.lean_files():
            if f.status == "added" and f.text and not re.search(r"^Authors?:", f.text[:800], re.M):
                out.append(finding(NAME, RUBRIC, f.name, 1, "new file has no copyright header with `Authors:`", "ask"))
    return out


def template(profile, ctx=None):
    """Markdown PR body skeleton from the profile (filled with changed decls when ctx is given)."""
    pr = profile.get("pr") or {}
    t = pr.get("body_template") or "## Summary\n\n<what and why>\n"
    if ctx is not None:
        decls = [f"- `{d['full']}` ({f.name}:{d['line']})" for f in ctx.lean_files() for d in f.new_decls()]
        t = t.replace("{{decls}}", "\n".join(decls) or "- (none)")
    return t


def selftest():
    from mergekit.context import Context, File
    prof = {"pr": {"body": {"required": [{"id": "roadmap", "regex": r"^Roadmap: \S+", "msg": "missing `Roadmap:` line"}],
                            "forbidden": [{"id": "qp", "regex": r"^- Q\d .*…", "msg": "unfilled quality pass"}],
                            "disclosure": {"regex": r"AI|Claude", "msg": "no AI disclosure"}}},
            "lean": {"authors_header": True}}
    fs = run(Context("t/t", prof, [File("T/A.lean", "added", "", "theorem x : True := trivial\n")],
                     pr_body="Adds x.\n\nQuality pass:\n- Q1 Mathlib duplicates: …\n"))
    msgs = " | ".join(x["msg"] for x in fs)
    assert "Roadmap" in msgs and "unfilled" in msgs and "disclosure" in msgs and "Authors" in msgs, msgs
    fs = run(Context("t/t", prof, [], pr_body="Roadmap: Foo\nWritten with Claude.\n"))
    assert not fs, fs
    return "ok"
