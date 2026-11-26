"""docs: module docstring and declaration docstrings, plus docstring-content red flags.

  D1 every new/modified substantive .lean file has a `/-! ... -/` module docstring (ask).
  D2 public def/abbrev/structure/class/inductive without `/-- -/` (ask); theorems too when the
     profile says `docs.theorems: required`; otherwise main theorems (>15 proof lines) -> maybe.
  D3 docstring red flags (ask): roadmap/process commentary (`roadmap`, `Suggested.lean`, `TODO`,
     `this PR`, `status`), proof mechanics (`by induction`, `the proof`, `we use`, `rewrite`).
     TauCeti documentation rubric: "describe the object or result, not the proof"; TauCeti#8954.
"""
import re
from mergekit.context import finding

NAME = "docs"
RUBRIC = "documentation"
FLAG_ROADMAP = re.compile(r"\b(roadmap|Suggested\.lean|TODO|this PR|this pull request|status:|work in progress|WIP)\b", re.I)
FLAG_PROOF = re.compile(r"\b(the proof (?:uses|goes|is by)|we (?:use|apply|rewrite|unfold)|by induction on|proof sketch|by `?simp`?|`rw`|is proved by)\b", re.I)
DOC_RE = re.compile(r"/--(.*?)-/", re.S)
MODDOC_RE = re.compile(r"/-!(.*?)-/", re.S)


def run(ctx):
    out = []
    thm_req = (ctx.profile.get("docs") or {}).get("theorems", "main")
    for f in ctx.lean_files():
        if not f.text.strip():
            continue
        substantive = len(f.decls) > 0
        if substantive and not MODDOC_RE.search(f.text):
            out.append(finding(NAME, RUBRIC, f.name, 1, "file has no module docstring `/-! ... -/`", "ask"))
        for d in f.new_decls():
            if d["private"] or d["kind"] == "instance":
                continue
            if not d["doc"]:
                if d["kind"] in ("def", "abbrev", "structure", "class", "inductive", "opaque"):
                    out.append(finding(NAME, RUBRIC, f.name, d["line"], f"public {d['kind']} `{d['name']}` has no docstring", "ask", decl=d["full"]))
                elif thm_req == "required":
                    out.append(finding(NAME, RUBRIC, f.name, d["line"], f"theorem `{d['name']}` has no docstring (repo requires one)", "ask", decl=d["full"]))
                elif d["proof_lines"] > 15:
                    out.append(finding(NAME, RUBRIC, f.name, d["line"], f"main theorem `{d['name']}` ({d['proof_lines']} lines) has no docstring", "maybe", decl=d["full"]))
        # D3 over docstrings touching added lines
        for rx, kind in ((DOC_RE, "decl"), (MODDOC_RE, "module")):
            for m in rx.finditer(f.text):
                start = f.text[:m.start()].count("\n") + 1
                end = start + m.group(0).count("\n")
                if not any(l in f.added for l in range(start, end + 1)):
                    continue
                body = m.group(1)
                for flag, what in ((FLAG_ROADMAP, "roadmap/process commentary"), (FLAG_PROOF, "proof mechanics")):
                    mm = flag.search(body)
                    if mm:
                        line = start + body[:mm.start()].count("\n")
                        out.append(finding(NAME, RUBRIC, f.name, line,
                                           f"{kind} docstring contains {what} (`{mm.group(0)}`): docstrings describe the result, not the process or proof",
                                           "ask" if what.startswith("roadmap") else "maybe", heuristic=what.startswith("proof")))
    return out


def selftest():
    from mergekit.context import Context, File
    src = open(__file__.replace("docs.py", "fixtures/docs.lean")).read()
    fs = run(Context("t/t", {}, [File("T/D.lean", "added", "", src)]))
    msgs = " | ".join(x["msg"] for x in fs)
    assert "no module docstring" in msgs and "`undocumented`" in msgs and "roadmap" in msgs, msgs
    assert "`documented`" not in msgs, msgs
    return "ok"
