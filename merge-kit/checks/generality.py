"""generality (HEURISTIC; every finding is `maybe`): patterns that often signal an
over-specialised statement. Mirrors quality-pass Q3 (TauCeti PR template) and the generality
rubric. It cannot decide whether the statement is false without the hypothesis.

  G1 `0 < t` hypothesis where `t` occurs in the conclusion only under `⁻¹`, `/`, `^ (-...)`,
     `≠ 0` contexts -> `t ≠ 0` may suffice.
  G2 typeclass stronger than the visible operations: `[Field K]`/`[DivisionRing K]` with no
     `⁻¹`, `/`, `inv`, `div` in statement+proof -> CommRing/Ring may do; `[RCLike 𝕜]` with no
     inner product / conj / re / im / `RCLike.` use -> a normed field or ring may do (TauCeti#1202).
     Applies to section `variable` lines too (reported at the first new decl that uses it).
  G3 concrete base field: a library function applied to `ℚ`/`ℝ`/`ℂ` as its base ring
     (`minpoly ℚ`, `IntermediateField ℚ`, `Algebra ℚ`, `ℚ⟮`) in a theorem not named after that
     type -> generalise to a field `K` (TauCeti#19002).
  G4 explicit hypothesis whose name is never used in the proof body (unusedArguments will
     flag it in CI anyway; cheap to catch locally).
"""
import re
from mergekit import lean
from mergekit.context import finding

NAME = "generality"
RUBRIC = "generality"
CLASS_USES = {
    "Field": r"⁻¹|/|\binv\b|\bdiv\b|Inv|Div|field_simp|Field",
    "DivisionRing": r"⁻¹|/|\binv\b|\bdiv\b|Inv|Div|field_simp",
    "RCLike": r"⟪|inner|\bconj\b|starRingEnd|\.re\b|\.im\b|RCLike\.|IsROrC|InnerProduct|\bre\b|\bim\b",
    "LinearOrderedField": r"⁻¹|/|\binv\b|\bdiv\b",
}
BASE_RE = re.compile(r"\b(minpoly|IntermediateField|Algebra|Module|FiniteDimensional|finrank|adjoin|Polynomial\.aeval|aeval|IsAlgebraic|IsIntegral)\s+(ℚ|ℝ|ℂ)\b|(ℚ|ℝ|ℂ)⟮")


def run(ctx):
    out = []
    for f in ctx.lean_files():
        var_classes = []  # (class, binder, line)
        for i, line in enumerate(f.lines, 1):
            if line.startswith("variable"):
                for m in re.finditer(r"\[\s*(Field|DivisionRing|RCLike|LinearOrderedField)\s+([^\]\s]+)\s*\]", line):
                    var_classes.append((m.group(1), m.group(2), i))
        reported_var = set()
        for d in f.new_decls():
            if d["kind"] not in ("theorem", "lemma", "def", "abbrev"):
                continue
            sig, body = d["sig"], d["body"]
            concl = lean.conclusion(sig)
            L = lambda msg: out.append(finding(NAME, RUBRIC, f.name, d["line"], msg, "maybe", decl=d["full"], heuristic=True))
            # G1
            for m in re.finditer(r"\((\w+)\s*:\s*0\s*<\s*([\w']+)\s*\)", sig):
                hname, t = m.groups()
                occ = [mm.start() for mm in re.finditer(r"(?<![\w'])" + re.escape(t) + r"(?![\w'])", concl)]
                inverted = any(re.match(r"\s*(⁻¹|/|≠\s*0)", concl[o + len(t):o + len(t) + 4]) or concl[max(0, o - 2):o].endswith("/ ") for o in occ)
                ordered = re.search(r"<|≤|sqrt|log|rpow|\^ *\(|‖|\|", concl)
                if occ and inverted and not ordered:
                    L(f"`{hname} : 0 < {t}`: {t} only appears inverted/divided in the conclusion; `{t} ≠ 0` may suffice")
            # G2 (binders of this decl and enclosing variable lines)
            classes = [(m.group(1), m.group(2)) for m in re.finditer(r"\[\s*(Field|DivisionRing|RCLike|LinearOrderedField)\s+([^\]\s]+)\s*\]", sig)]
            for c, b in classes:
                if not re.search(CLASS_USES[c], concl + "\n" + body.replace(f"[{c} {b}]", "")):
                    L(f"`[{c} {b}]` but no {c}-specific operation appears in `{d['name']}`; a weaker class may do")
            for c, b, ln in var_classes:
                if (c, b) in reported_var or ln > d["line"] or b not in sig + body:
                    continue
                if not re.search(CLASS_USES[c], sig + "\n" + body):
                    reported_var.add((c, b))
                    L(f"section `variable [{c} {b}]` (line {ln}) but `{d['name']}` uses nothing {c}-specific; put such decls in a section with a weaker class")
            # G3
            m = BASE_RE.search(sig + " " + body[:2000])
            if m:
                ty = m.group(2) or m.group(3)
                tyname = {"ℚ": "rat", "ℝ": "real", "ℂ": "complex"}[ty]
                if tyname not in d["name"].lower() and BASE_RE.search(sig):
                    L(f"statement fixes the base field to {ty} (`{m.group(0)}`); check whether any field `K` works")
            # G4
            for m in re.finditer(r"\(([\w' ]+?)\s*:\s*[^()]*\)", sig):
                for h in m.group(1).split():
                    if h.startswith("h") and h != "_" and not re.search(r"(?<![\w'.])" + re.escape(h) + r"(?![\w'])", body) \
                            and ":= by" not in sig and "fun" not in body[:0] and body.strip():
                        if re.search(r"\b(simp|omega|positivity|linarith|nlinarith|aesop|grind|tauto|decide|norm_num|assumption|exact\?|field_simp|bound|gcongr|fun_prop|measurability|continuity|polyrith)\b", body):
                            continue  # tactics can use hypotheses anonymously
                        L(f"hypothesis `{h}` is never referenced by name in the proof; drop it if the statement holds without it")
    return out


def selftest():
    from mergekit.context import Context, File
    src = open(__file__.replace("generality.py", "fixtures/generality.lean")).read()
    fs = run(Context("t/t", {}, [File("T/G.lean", "added", "", src)]))
    msgs = " | ".join(x["msg"] for x in fs)
    assert "`t ≠ 0` may suffice" in msgs and "[Field K]" in msgs and "base field to ℚ" in msgs and "variable [RCLike" in msgs, msgs
    assert "keeps_field" not in msgs, msgs
    return "ok"
