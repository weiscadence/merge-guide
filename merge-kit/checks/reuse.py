"""reuse: for each new declaration (and each long `have`), list same-shape or near-name
declarations already in local Mathlib + the repo, with file:line.

Score = idf-weighted overlap of conclusion identifiers (binder names dropped, local defs unfolded
one level) + 0.6 x idf-weighted overlap of name tokens. Severity:
  ask   : normalised conclusion text identical, or score >= HIGH
  maybe : score >= LOW (top 3 listed)
Rubric: reuse (TauCeti rubric "Reuse and duplication"; Q1/Q2 of the quality pass).
"""
import math, re
from mergekit import lean
from mergekit.context import finding

NAME = "reuse"
RUBRIC = "reuse"
HIGH, LOW = 0.80, 0.45
VAR_RE = re.compile(r"^([a-zα-ωA-Z𝕜𝔽]|h\w*)[₀-₉'0-9]*$")
HAVE_RE = re.compile(r"\bhave\s+([\w'₀-₉]*)\s*:\s*(.+?)\s*:=", re.S)


def ident_tokens(text):
    # raw tokens (not lean.sig_tokens: `(f : T)` ascriptions in a conclusion are not binders)
    toks = [t for t in lean.TOK_RE.findall(text) if t not in lean.LEAN_KW]
    return {t.split(".")[-1] for t in toks if t[0].isalpha() and len(t) > 1 and not VAR_RE.match(t)} | \
           {t for t in toks if "." in t and t[0].isupper()}


def norm_concl(text):
    """Statement text up to renaming of variables and of the concrete base field."""
    s = re.sub(r"\s+", " ", text).strip()
    s = re.sub(r"(?<![\w.])([a-zα-ωA-Z𝕜]|h\w*)[₀-₉'0-9]*(?![\w])", "_", s)
    s = re.sub(r"[ℚℝℂ]", "_", s)
    s = s.replace("( ", "(").replace(" )", ")")
    return s


_EXACT = {}


def exact_table(idx):
    """norm_concl(conclusion) -> row ids, built once per index (statements >= 8 chars)."""
    key = id(idx)
    if key not in _EXACT:
        t = {}
        for i, r in enumerate(idx.rows):
            if len(r[4]) >= 8:
                t.setdefault(norm_concl(r[4]), []).append(i)
        _EXACT[key] = t
    return _EXACT[key]


def exact_hits(idx, stmt, exclude_names, exclude_files, row_ok):
    out = []
    for i in exact_table(idx).get(norm_concl(stmt), [])[:20]:
        r = idx.rows[i]
        if r[0] in exclude_names or r[1] in exclude_files or r[6] or (row_ok and not row_ok(r)):
            continue
        out.append((1.0, r))
    return out[:3]


def expand(tokens, local_defs):
    out = set(tokens)
    for t in tokens:
        if t in local_defs:
            out.discard(t)
            val = local_defs[t].split(":=", 1)[-1]
            out |= ident_tokens(val[:400])
    return out - {"noncomputable", "private", "protected"}


def candidates(idx, ctoks, ntoks, exclude_names, exclude_files, limit=3, row_ok=None):
    if idx is None:
        return []
    N = idx.ndocs
    def idf(table, t):
        return math.log(1 + N / (1 + len(table.get(t, ()))))
    # candidate pool: rows sharing the 3 rarest conclusion tokens or the 2 rarest name tokens
    pool = set()
    rare_c = sorted((t for t in ctoks if t in idx.by_ctok), key=lambda t: len(idx.by_ctok[t]))[:3]
    rare_n = sorted((t for t in ntoks if t in idx.by_tok), key=lambda t: len(idx.by_tok[t]))[:2]
    for t in rare_c:
        if len(idx.by_ctok[t]) < 20000: pool.update(idx.by_ctok[t])
    for t in rare_n:
        if len(idx.by_tok[t]) < 20000: pool.update(idx.by_tok[t])
    ctoks = {t for t in ctoks if t in idx.by_ctok}   # local-only names cannot match anything
    ntoks = {t for t in ntoks if t in idx.by_tok}
    wc = sum(idf(idx.by_ctok, t) for t in ctoks) or 1.0
    wn = sum(idf(idx.by_tok, t) for t in ntoks) or 1.0
    scored = []
    for i in pool:
        r = idx.rows[i]
        if r[0] in exclude_names or r[1] in exclude_files or r[6]:
            continue
        rc = ident_tokens(r[4])
        rn = set(lean.name_tokens(r[0]))
        shared = (ctoks & rc) | (ntoks & rn)
        if not any(len(idx.by_ctok.get(t, ())) < 3000 or len(idx.by_tok.get(t, ())) < 3000 for t in shared):
            continue  # only very common tokens in common: not evidence
        oc = sum(idf(idx.by_ctok, t) for t in ctoks & rc)
        on = sum(idf(idx.by_tok, t) for t in ntoks & rn)
        # mostly query coverage (does the candidate contain what we state?), a little cosine
        sc = 0.75 * oc / wc + 0.25 * oc / math.sqrt(wc * (sum(idf(idx.by_ctok, t) for t in rc) or 1.0))
        sn = 0.75 * on / wn + 0.25 * on / math.sqrt(wn * (sum(idf(idx.by_tok, t) for t in rn) or 1.0))
        s = (sc + 0.6 * sn) / 1.6 if ctoks else sn
        scored.append((s, r))
    scored.sort(key=lambda x: -x[0])
    if row_ok is None:
        return scored[:limit]
    out = []
    for s, r in scored[:limit * 6]:
        if row_ok(r):
            out.append((s, r))
            if len(out) == limit:
                break
    return out


def run(ctx):
    out = []
    idx = ctx.index
    if idx is None:
        return [finding(NAME, RUBRIC, "", 0, "no declaration index (no .lake/packages/mathlib?); reuse search skipped", "info")]
    excl_files = set(ctx.changed_names) | getattr(ctx, 'exclude_files', set())
    for f in ctx.lean_files():
        local_defs = {d["name"].split(".")[-1]: d["body"] for d in f.decls if d["kind"] in ("def", "abbrev", "noncomputable")}
        names_here = {d["full"] for d in f.decls}
        for d in f.new_decls():
            if d["kind"] in ("instance", "structure", "class", "inductive"):
                continue
            if d["kind"] in ("theorem", "lemma"):
                concl = lean.conclusion(d["sig"])
            else:  # def/abbrev: its type and (the start of) its value
                concl = lean.conclusion(d["sig"]) + " " + d["body"].split(":=", 1)[-1][:300]
            ctoks = expand(ident_tokens(concl), local_defs)
            ntoks = set(lean.name_tokens(d["full"]))
            for cls in re.findall(r"\[\s*([A-Z][\w.]*)", d["sig"]):   # [Module.Flat ℤ V] -> module, flat
                ntoks |= set(lean.name_tokens(cls.replace(".", "_")))
            row_ok = getattr(ctx, 'row_ok', None)
            exact = exact_hits(idx, concl, names_here, excl_files, row_ok) if d["kind"] in ("theorem", "lemma") and len(norm_concl(concl)) >= 12 else []
            cands = exact + [c for c in candidates(idx, ctoks, ntoks, names_here, excl_files, limit=5, row_ok=row_ok)
                             if c[1] not in [e[1] for e in exact]]
            if not cands:
                continue
            best = cands[0][0]
            sev = "ask" if exact or best >= HIGH else ("maybe" if best >= LOW else None)
            if not sev:
                continue
            ev = [f"{r[0]}  {r[1]}:{r[2]}  ({s:.2f})  : {r[4][:120]}" for s, r in cands if s >= LOW * 0.8]
            out.append(finding(NAME, RUBRIC, f.name, d["line"],
                               f"`{d['name']}` may duplicate an existing declaration; check the candidates and use them if one replaces it",
                               sev, decl=d["full"], evidence=ev))
            # long `have` steps inside the proof
            for m in HAVE_RE.finditer(d["body"]):
                stmt = " ".join(m.group(2).split())
                ex = exact_hits(idx, stmt, names_here, excl_files, row_ok) if len(norm_concl(stmt)) >= 8 else []
                if ex:
                    line = d["body_line"] + d["body"][:m.start()].count("\n")
                    out.append(finding(NAME, RUBRIC, f.name, line,
                                       f"`have {m.group(1) or '_'} : {stmt[:60]}` inside `{d['name']}` has the same statement as an existing lemma",
                                       "ask", decl=d["full"], evidence=[f"{r[0]}  {r[1]}:{r[2]} : {r[4][:120]}" for s, r in ex]))
                    continue
                if len(stmt) < 25:
                    continue
                ht = expand(ident_tokens(stmt), local_defs)
                if len(ht) < 2:
                    continue
                hc = candidates(idx, ht, set(), names_here, excl_files, limit=2, row_ok=getattr(ctx, 'row_ok', None))
                if hc and hc[0][0] >= HIGH:
                    line = d["body_line"] + d["body"][:m.start()].count("\n")
                    out.append(finding(NAME, RUBRIC, f.name, line,
                                       f"`have {m.group(1) or '_'}` inside `{d['name']}` may restate an existing lemma",
                                       "maybe", decl=d["full"],
                                       evidence=[f"{r[0]}  {r[1]}:{r[2]}  ({s:.2f}) : {r[4][:120]}" for s, r in hc]))
    return out


def selftest():
    from mergekit.index import Index
    from mergekit.context import Context, File
    rows = [["Module.Flat.tensorProduct_mk_injective", "Mathlib/RingTheory/Flat/Basic.lean", 259, "lemma",
             "Function.Injective (TensorProduct.mk R S M 1)", "mathlib", 0],
            ["Nat.succ_le_iff", "Mathlib/Order/Basic.lean", 1, "theorem", "succ m ≤ n ↔ m < n", "mathlib", 0]]
    rows += [[f"Foo.bar{i}", "Mathlib/X.lean", i, "theorem", f"Foo.baz{i} x = 0", "mathlib", 0] for i in range(50)]
    idx = Index(rows)
    src = open(__file__.replace("reuse.py", "fixtures/reuse.lean")).read()
    ctx = Context("t/t", {}, [File("T/Rat.lean", "added", "", src)], index=idx)
    fs = run(ctx)
    assert any(x["decl"] == "rationalificationMap_injective" and "tensorProduct_mk_injective" in " ".join(x["evidence"]) for x in fs), fs
    assert not any(x["decl"] == "unrelated_thing" for x in fs), fs
    return "ok"
