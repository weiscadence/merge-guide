"""naming: Mathlib naming conventions, mechanically checkable subset.

Source: https://leanprover-community.github.io/contribute/naming.html (capitalisation rules,
`_iff`, `_of_`, `coe`/`coeFn`), TauCeti naming rubric (name must not overstate the statement;
wrong namespace for the receiver), FAILURE-MODES.md (review-harvest counts) §2a row 5.
  N1 theorem/lemma (Prop-valued) names: last component snake_case/lowerCamel, not UpperCamel
     (exception: components that are type names, e.g. `IsOpen.inter` is fine as `inter`).
  N2 structure/class/inductive: UpperCamelCase, no `_`.
  N3 def: lowerCamelCase (no `_`) unless it returns Prop/Type/Sort (then UpperCamelCase).
  N4 `_iff` without `↔` in the conclusion; `_eq` / `eq_` with no `=` (overstated name).
  N5 `coe_` name whose statement uses `⇑` -> `coeFn_` (TauCeti#1283).
  N6 namespace receiver: decl in namespace `X` (Nat, Int, Polynomial, Real, ...) whose signature
     never mentions `X` -> the namespace is probably wrong (TauCeti#19680 `Nat.`, review-lessons).
  N7 `lemma` keyword where the repo profile forbids it.
"""
import re
from mergekit import lean
from mergekit.context import finding

NAME = "naming"
RUBRIC = "naming"
RECEIVERS = {"Nat": ["ℕ", "Nat"], "Int": ["ℤ", "Int"], "Rat": ["ℚ", "Rat"], "Real": ["ℝ", "Real"],
             "Complex": ["ℂ", "Complex"], "Polynomial": ["Polynomial", "[X]", "X]"], "Finset": ["Finset"],
             "List": ["List"], "Multiset": ["Multiset"], "Set": ["Set"], "Matrix": ["Matrix"]}


def run(ctx):
    out = []
    forbid_lemma = (ctx.profile.get("naming") or {}).get("forbid_lemma_keyword", False)
    for f in ctx.lean_files():
        for d in f.new_decls():
            last = d["name"].split(".")[-1]
            if not last or last.startswith("_"):
                continue
            concl = lean.conclusion(d["sig"])
            k = d["kind"]
            L = lambda msg, sev="ask", heur=False: out.append(
                finding(NAME, RUBRIC, f.name, d["line"], msg, sev, decl=d["full"], heuristic=heur))
            if k in ("theorem", "lemma"):
                if last[0].isupper() and "_" not in last and not re.match(r"^[A-Z][a-z]+$", last):
                    L(f"theorem `{last}` is UpperCamelCase; Prop-valued declarations are snake_case")
                elif re.search(r"[a-z][A-Z]", last.split("_")[0]) and "_" in last and False:
                    pass
                if re.search(r"(^|_)iff($|_)", last) and "↔" not in concl:
                    L(f"`{last}` says `iff` but the statement has no `↔`")
                if re.search(r"(^|_)eq($|_)", last) and "=" not in concl and "↔" not in concl and "≃" not in concl and concl:
                    L(f"`{last}` says `eq` but the statement has no `=`", "maybe", True)
                if re.search(r"(^|_)coe(_|$)", last) and "⇑" in d["sig"]:
                    L(f"`{last}`: function coercions `⇑` are named `coeFn`, not `coe`")
            elif k in ("structure", "class", "inductive"):
                if not last[0].isupper() or "_" in last:
                    L(f"{k} `{last}` should be UpperCamelCase")
            elif k in ("def", "abbrev"):
                typ = lean.conclusion(d["sig"])
                returns_sort = bool(re.match(r"^(Prop|Type|Sort)\b", typ.strip()))
                if returns_sort and last[0].islower():
                    L(f"`{last}` returns {typ.split()[0]}: name it UpperCamelCase")
                elif not returns_sort and "_" in last and typ and not typ.strip().startswith("Prop"):
                    L(f"def `{last}` uses snake_case; data-valued defs are lowerCamelCase", "maybe", True)
            # N6 receiver namespace
            ns_parts = d["full"].split(".")[:-1]
            if ns_parts:
                recv = ns_parts[-1]
                if recv in RECEIVERS and not any(s in d["sig"] for s in RECEIVERS[recv]) and k in ("theorem", "lemma", "def"):
                    L(f"`{d['full']}` lives in namespace `{recv}` but its signature never mentions {recv}: name it in the argument type's namespace", "maybe", True)
            if forbid_lemma and k == "lemma":
                L("`lemma` keyword: this repo writes `theorem`")
    return out


def selftest():
    from mergekit.context import Context, File
    src = open(__file__.replace("naming.py", "fixtures/naming.lean")).read()
    fs = run(Context("t/t", {"naming": {"forbid_lemma_keyword": True}}, [File("T/N.lean", "added", "", src)]))
    msgs = " | ".join(x["msg"] for x in fs)
    for want in ("FooBarBaz", "says `iff`", "coeFn", "namespace `Polynomial`", "`lemma` keyword", "should be UpperCamelCase"):
        assert want in msgs, (want, msgs)
    assert "good_name" not in msgs, msgs
    return "ok"
