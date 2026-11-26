"""proof-shape (proof-quality rubric; quality-pass Q5). Deterministic:
  Q1 proof longer than profile.lean.max_proof_lines (TauCeti: 50) -> ask
  Q2 `rw [...]` chain with >= 6 rewrites -> maybe (brittle positional chain; TauCeti#19035)
  Q3 `show` with no comment on the line or the line above -> maybe (TauCeti#45354)
"""
import re
from mergekit.context import finding

NAME = "proof-shape"
RUBRIC = "proof-quality"


def run(ctx):
    out = []
    mx = (ctx.profile.get("lean") or {}).get("max_proof_lines")
    for f in ctx.lean_files():
        for d in f.new_decls():
            if d["kind"] not in ("theorem", "lemma", "def", "instance"):
                continue
            if mx and d["proof_lines"] > mx:
                out.append(finding(NAME, RUBRIC, f.name, d["line"], f"`{d['name']}` proof is {d['proof_lines']} lines > {mx}: split it at natural stages", "ask", decl=d["full"]))
            for i, line in enumerate(d["body"].splitlines()):
                ln = d["body_line"] + i
                m = re.search(r"\brw\s*\[([^\]]*)\]", line)
                if m and m.group(1).count(",") >= 5:
                    out.append(finding(NAME, RUBRIC, f.name, ln, f"{m.group(1).count(',') + 1}-step `rw` chain in `{d['name']}`: brittle; try `simp only`/`field_simp`/a named lemma", "maybe", decl=d["full"], heuristic=True))
                if re.search(r"(^|[\s(;·])show\s", line) and "--" not in line:
                    prev = d["body"].splitlines()[i - 1] if i else ""
                    if "--" not in prev:
                        out.append(finding(NAME, RUBRIC, f.name, ln, f"undocumented `show` in `{d['name']}`", "maybe", decl=d["full"], heuristic=True))
    return out


def selftest():
    from mergekit.context import Context, File
    body = "theorem t (a b : ℕ) : a + b = b + a := by\n  show a + b = b + a\n  rw [Nat.add_comm, h1, h2, h3, h4, h5]\n" + "  skip\n" * 55
    fs = run(Context("t/t", {"lean": {"max_proof_lines": 50}}, [File("T/P.lean", "added", "", body)]))
    msgs = " | ".join(x["msg"] for x in fs)
    assert "> 50" in msgs and "6-step" in msgs and "show" in msgs, msgs
    return "ok"
