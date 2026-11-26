"""placement: does each new file / declaration sit where similar material lives?

Deterministic rules:
  P1 prefix-sharing siblings (TauCeti placement rubric): a new file `D/Foo.lean` or `D/FooBar.lean`
     next to `D/Foo/` or another `D/Foo*.lean` -> ask to make `D/Foo/` a directory.
  P2 redundant import: file imports A and B where B (transitively, depth<=4, via local sources)
     already imports A -> ask (placement rubric "Imports").
  P3 broad `import Mathlib` -> ask.
Heuristic (marked):
  P4 nearest neighbours: >=4 of a public new decl's 8 nearest local-repo neighbours (name tokens)
     live in one other file -> maybe "move next to <file>".
  P5 general helper hidden as private: a `private` theorem whose statement mentions no
     declaration defined in this repo -> maybe (also an api-design ask).
"""
import math, os, re
from collections import Counter
from mergekit import lean
from mergekit.context import finding

NAME = "placement"
RUBRIC = "placement"


def camel_lead(stem):
    m = re.match(r"[A-Z0-9][a-z0-9']*|[A-Z]+(?=[A-Z][a-z]|$)", stem)
    return m.group(0) if m else stem


def mod_to_path(mod):
    return mod.replace(".", "/") + ".lean"


def import_closure(ctx, mod, depth=4, seen=None):
    seen = set() if seen is None else seen
    if depth == 0 or mod in seen:
        return seen
    seen.add(mod)
    txt = ctx.read_repo_file(mod_to_path(mod))
    if txt:
        for m in lean.imports(txt):
            import_closure(ctx, m, depth - 1, seen)
    return seen


def run(ctx):
    out = []
    tree = ctx.tree()
    for f in ctx.lean_files():
        d, base = os.path.split(f.name)
        stem = base[:-5]
        # P1 (only for added files)
        if f.status == "added" and tree:
            lead = camel_lead(stem)
            sibs = sorted(p for p in tree if os.path.dirname(p) == d and p != f.name and p.endswith(".lean")
                          and camel_lead(os.path.basename(p)[:-5]) == lead)
            # directory named like the parent of the new file, with a flat prefix-sharing sibling
            pdir, pname = os.path.split(d)
            flat = sorted(p for p in tree if os.path.dirname(p) == pdir and p.endswith(".lean")
                          and os.path.basename(p)[:-5] != pname and os.path.basename(p).startswith(pname)
                          and camel_lead(os.path.basename(p)[:-5]) == camel_lead(pname))
            if sibs:
                out.append(finding(NAME, RUBRIC, f.name, 1,
                                   f"new file shares the leading component `{lead}` with {', '.join(sibs[:3])}: make `{os.path.join(d, lead)}/` a directory in this PR",
                                   "ask", evidence=sibs))
            if flat:
                out.append(finding(NAME, RUBRIC, f.name, 1,
                                   f"new file under `{d}/` while flat prefix-sharing sibling(s) {', '.join(flat[:3])} remain: move them into `{d}/`",
                                   "ask", evidence=flat))
        # P2/P3 imports (new or touched import lines)
        imps = lean.imports(f.text)
        for i, line in enumerate(f.lines[:80], 1):
            if re.match(r"^\s*(public\s+)?import\s+Mathlib\s*$", line):
                out.append(finding(NAME, RUBRIC, f.name, i, "broad `import Mathlib`: import the specific modules", "ask"))
        if ctx.repo_dir or len(ctx.files) > 0:
            closures = {m: import_closure(ctx, m) - {m} for m in imps}
            for a in imps:
                via = [b for b in imps if b != a and a in closures.get(b, ())]
                if via:
                    line = next((i for i, l in enumerate(f.lines, 1) if re.search(r"import\s+" + re.escape(a) + r"\s*$", l)), 1)
                    if line in f.added or f.status == "added":
                        out.append(finding(NAME, RUBRIC, f.name, line,
                                           f"import `{a}` is redundant: already imported by `{via[0]}`", "ask", evidence=via))
        # P4/P5 neighbours
        idx = ctx.index
        local_names = set()
        if idx is not None:
            for dd in f.new_decls():
                if dd["kind"] not in ("theorem", "lemma", "def", "abbrev"):
                    continue
                ntoks = [t for t in set(lean.name_tokens(dd["full"])) if t in idx.by_tok and len(idx.by_tok[t]) < 5000]
                if dd["private"]:
                    concl_ids = {t for t in lean.sig_tokens(dd["sig"]) if t[:1].isalpha() and len(t) > 2}
                    lib_defined = [t for t in concl_ids if any(idx.rows[i][5] == "mathlib" for i in idx.by_last.get(t.split(".")[-1], ()))]
                    repo_defined = [t for t in concl_ids if t not in lib_defined and any(idx.rows[i][5] == "local" for i in idx.by_last.get(t.split(".")[-1], ()))]
                    if not repo_defined and len(lib_defined) >= 2 and dd["kind"] in ("theorem", "lemma"):
                        out.append(finding(NAME, "api-design", f.name, dd["line"],
                                           f"private `{dd['name']}` states a fact about library notions only ({', '.join(sorted(lib_defined)[:4])}); general infrastructure should be public in its natural home",
                                           "maybe", decl=dd["full"], heuristic=True))
                        out.append(finding(NAME, RUBRIC, f.name, dd["line"],
                                           f"`{dd['name']}` looks like general material living in a feature file; consider the topic file for {', '.join(sorted(lib_defined)[:3])}",
                                           "maybe", decl=dd["full"], heuristic=True))
                    continue
                if len(ntoks) < 2:
                    continue
                N = idx.ndocs
                score = Counter()
                for t in ntoks:
                    w = math.log(1 + N / (1 + len(idx.by_tok[t])))
                    for i in idx.by_tok[t]:
                        r = idx.rows[i]
                        if r[5] == "local" and r[1] not in ctx.changed_names and r[1] not in ctx.exclude_files:
                            score[i] += w
                area = "/".join(f.name.split("/")[:2])
                row_ok = getattr(ctx, "row_ok", None)
                top = [idx.rows[i] for i, _ in score.most_common(40) if idx.rows[i][1].startswith(area + "/")]
                if row_ok:
                    top = [r for r in top[:16] if row_ok(r)]
                top = top[:8]
                files = Counter(r[1] for r in top)
                if files:
                    tf, n = files.most_common(1)[0]
                    if n >= 4 and tf != f.name:
                        out.append(finding(NAME, RUBRIC, f.name, dd["line"],
                                           f"{n}/8 nearest neighbours of `{dd['name']}` live in `{tf}`; check whether it belongs there",
                                           "maybe", decl=dd["full"], heuristic=True,
                                           evidence=[f"{r[0]} {r[1]}:{r[2]}" for r in top[:5]]))
    return out


def selftest():
    from mergekit.context import Context, File
    a = File("T/A/L2/Pi.lean", "added", "", "import T.A.B\nimport T.A.C\n\ntheorem x : True := trivial\n")
    b = File("T/A/B.lean", "added", "", "import T.A.C\n")
    c = File("T/A/C.lean", "added", "", "\n")
    l2p = File("T/A/L2Product.lean", "added", "", "\n")
    ctx = Context("t/t", {}, [a, b, c, l2p])
    ctx._tree = {"T/A/L2/Pi.lean", "T/A/B.lean", "T/A/C.lean", "T/A/L2Product.lean"}
    fs = run(ctx)
    assert any("L2Product" in x["msg"] for x in fs), fs
    assert any("redundant" in x["msg"] and "T.A.C" in x["msg"] for x in fs), fs
    return "ok"
