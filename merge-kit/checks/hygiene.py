"""hygiene: forbidden tokens in added lines (comments stripped).

  H1 `sorry` / `admit` (unless profile.lean.sorry_allowed) -> ask
  H2 `set_option maxHeartbeats` without a comment on the same or previous line -> ask; any
     `set_option` when profile.lean.forbid_set_option (TauCeti AGENTS.md) -> ask
  H3 `native_decide`, `axiom` when profile.lean.forbid_native_decide -> ask
  H4 `#eval`/`#check`/`#print`/`#exit` left in library code -> ask
  H5 lines > profile.lean.max_line (Mathlib style linter: 100) -> ask
  H6 optional: `lake lint` (only with --lake-lint; not run by default on a busy box)
"""
import re, subprocess
from mergekit import lean
from mergekit.context import finding

NAME = "hygiene"
RUBRIC = "hygiene"


def run(ctx, lake_lint=False):
    out = []
    lp = ctx.profile.get("lean") or {}
    for f in ctx.lean_files():
        clean = lean.strip_comments(f.text).splitlines()
        for ln in sorted(f.added):
            if ln - 1 >= len(clean):
                continue
            c, raw = clean[ln - 1], f.lines[ln - 1] if ln - 1 < len(f.lines) else ""
            prev = f.lines[ln - 2] if ln >= 2 else ""
            L = lambda msg: out.append(finding(NAME, RUBRIC, f.name, ln, msg, "ask"))
            if re.search(r"(?<![\w'.])(sorry|admit)(?![\w'])", c) and not lp.get("sorry_allowed"):
                L("`sorry`/`admit` in added code")
            if re.search(r"\bset_option\b", c):
                if lp.get("forbid_set_option"):
                    L("`set_option` is forbidden in library code in this repo")
                elif "maxHeartbeats" in c and "--" not in raw and not prev.strip().startswith("--"):
                    L("`set_option maxHeartbeats` without a comment saying why")
            if lp.get("forbid_native_decide", True) and re.search(r"\bnative_decide\b|^\s*axiom\b", c):
                L("`native_decide`/`axiom` in added code")
            if re.search(r"^\s*#(eval|check|print|exit|reduce)\b", c):
                L(f"debug command `{c.strip().split()[0]}` left in library code")
            ml = lp.get("max_line")
            if ml and len(raw) > ml and not re.search(r"https?://", raw):
                L(f"line is {len(raw)} chars > {ml}")
    if lake_lint and ctx.repo_dir:
        r = subprocess.run(["nice", "-n", "19", "lake", "lint"], cwd=ctx.repo_dir, capture_output=True, text=True, timeout=900)
        if r.returncode != 0:
            out.append(finding(NAME, RUBRIC, "", 0, "`lake lint` failed: " + (r.stdout + r.stderr)[-400:], "ask"))
    return out


def selftest():
    from mergekit.context import Context, File
    src = open(__file__.replace("hygiene.py", "fixtures/hygiene.lean")).read()
    fs = run(Context("t/t", {"lean": {"max_line": 100}}, [File("T/H.lean", "added", "", src)]))
    msgs = " | ".join(x["msg"] for x in fs)
    assert "sorry" in msgs and "maxHeartbeats" in msgs and "#eval" in msgs and "chars" in msgs, msgs
    assert sum("sorry" in x["msg"] for x in fs) == 1, fs  # the one in a comment does not count
    return "ok"
