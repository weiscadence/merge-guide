"""Cheap Lean 4 source parsing: declarations, namespaces, docstrings, imports.

No elaboration. Regex + a line scanner, good enough for grep-level checks.
"""
import re

DECL_KW = r"(theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque|axiom)"
MODS = r"((?:@\[[^\]]*\]\s*)*)((?:(?:private|protected|noncomputable|nonrec|partial|unsafe|public|meta)\s+)*)"
DECL_RE = re.compile(r"^" + MODS + DECL_KW + r"\b\s*([^\s:(\[{]*)")
NS_RE = re.compile(r"^\s*(namespace|section|end)\b\s*([\w.'?!₀-₉]*)")
IMPORT_RE = re.compile(r"^\s*(?:public\s+|meta\s+)*import\s+([\w.']+)")
OPEN_RE = re.compile(r"^\s*open\s+(.*)")

LEAN_KW = set("""fun λ ∀ ∃ forall exists let have show from by at with in if then else match do
theorem lemma def Type Prop Sort _ := : ( ) [ ] { } ⦃ ⦄ , → ↔ ∧ ∨ ¬ = ≠ ≤ < ≥ > . · ∘""".split())


def strip_comments(text):
    """Remove -- line comments and /- -/ block comments (keeping newlines)."""
    out, i, n, depth = [], 0, len(text), 0
    while i < n:
        if text.startswith("/-", i):
            depth += 1; i += 2; continue
        if depth and text.startswith("-/", i):
            depth -= 1; i += 2; continue
        c = text[i]
        if depth:
            if c == "\n": out.append(c)
            i += 1; continue
        if text.startswith("--", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        out.append(c); i += 1
    return "".join(out)


def imports(text):
    return [m.group(1) for line in text.splitlines() if (m := IMPORT_RE.match(line))]


def has_module_doc(text):
    return re.search(r"^/-!", text, re.M) is not None


def parse_decls(text, path=""):
    """Return a list of dicts: name, full, kind, line (1-based), sig, body, doc, private,
    attrs, ns (current namespace)."""
    lines = text.splitlines()
    decls, ns_stack = [], []
    # track comment state so we don't match inside block comments
    in_block, doc_buf, doc_end_line = 0, False, -10
    i = 0
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        # block comment tracking (approximate: counts /- and -/ on the line)
        if in_block:
            in_block += raw.count("/-") - raw.count("-/")
            if in_block <= 0:
                in_block = 0
                if doc_buf: doc_end_line = i
            i += 1; continue
        if s.startswith("/--") or s.startswith("/-"):
            is_doc = s.startswith("/--")
            depth = raw.count("/-") - raw.count("-/")
            if depth > 0:
                in_block, doc_buf = depth, is_doc
            elif is_doc:
                doc_end_line = i
            i += 1; continue
        m = NS_RE.match(raw)
        if m and not raw.startswith(" "):
            kw, nm = m.groups()
            if kw == "namespace":
                ns_stack.append(("ns", nm))
            elif kw == "section":
                ns_stack.append(("sec", nm))
            elif kw == "end" and ns_stack:
                ns_stack.pop()
            i += 1; continue
        m = DECL_RE.match(raw)
        if m:
            attrs, mods, kind, name = m.group(1), m.group(2), m.group(3), m.group(4)
            # gather the signature up to ':=' / 'where' / '|' at depth 0 (max 40 lines)
            sig_lines, j = [raw], i
            joined = raw
            while ":=" not in joined and " where" not in joined and j + 1 < len(lines) and j - i < 40:
                nxt = lines[j + 1]
                if DECL_RE.match(nxt) or (nxt.strip() == "" and kind in ("structure", "class", "inductive")):
                    break
                j += 1; sig_lines.append(nxt); joined = " ".join(sig_lines)
            sig = joined[m.end():].split(":=")[0].split(" where")[0]
            # body: following lines until next top-level decl (bounded)
            k = j + 1
            while k < len(lines) and k - j < 400:
                t = lines[k]
                if t and not t[0].isspace() and (DECL_RE.match(t) or NS_RE.match(t) or t.startswith("/-") or t.startswith("@[")):
                    break
                k += 1
            body = "\n".join(lines[j:k])
            nss = ".".join(n for t, n in ns_stack if t == "ns" and n)
            full = name if name.startswith("_root_.") or not nss else f"{nss}.{name}"
            if not name:
                full = ""
            decls.append(dict(
                name=name, full=full.replace("_root_.", ""), kind=kind, line=i + 1, end=k,
                sig=" ".join(sig.split()), body=body, ns=nss,
                doc=(doc_end_line >= i - 1 - _attr_lines_above(lines, i)),
                private="private" in mods, protected="protected" in mods,
                attrs=attrs.strip(), path=path,
                proof_lines=k - j, body_line=j + 1,
            ))
            i = j + 1; continue
        i += 1
    return decls


def _attr_lines_above(lines, i):
    """Count `@[...]` lines directly above line i (docstring sits above them)."""
    c, k = 0, i - 1
    while k >= 0 and lines[k].strip().startswith("@["):
        c += 1; k -= 1
    return c


TOK_RE = re.compile(r"[A-Za-z_][\w'.₀-₉]*|[^\sA-Za-z_0-9]")


def sig_tokens(sig):
    """Identifier tokens of a signature, with binder names alpha-renamed away.

    Binder names = identifiers immediately followed by ':' inside (), {}, [], ⦃⦄; they are dropped
    so that `(x : α) : f x = 0` and `(y : β) : f y = 0` compare equal up to type names."""
    binders = set(re.findall(r"[({⦃\[]\s*([\w'₀-₉ ]+?)\s*:", sig))
    bnames = set()
    for b in binders:
        bnames.update(b.split())
    toks = []
    for t in TOK_RE.findall(sig):
        if t in bnames or t in LEAN_KW:
            continue
        toks.append(t)
    return toks


def name_tokens(name):
    """`foo_bar_iff` -> {foo, bar, iff}; `Foo.barBaz` -> {foo, bar, baz}. Namespace components
    count too (`Module.Flat.x` -> module, flat), except the project root `TauCeti`."""
    comps = [c for c in name.split(".") if c not in ("TauCeti", "_root_")]
    parts = re.split(r"[_.]", ".".join(comps))
    out = []
    for p in parts:
        out += [w.lower() for w in re.findall(r"[A-Z]?[a-z0-9'₀-₉]+|[A-Z]+(?![a-z])", p)]
    return [t for t in out if t]


def conclusion(sig):
    """Text after the last top-level ':' of a signature (the statement's type)."""
    depth, last = 0, -1
    for idx, c in enumerate(sig):
        if c in "([{⦃": depth += 1
        elif c in ")]}⦄": depth -= 1
        elif c == ":" and depth == 0 and not sig.startswith(":=", idx):
            last = idx
    return sig[last + 1:].strip() if last >= 0 else ""


def hypotheses(sig):
    """List of (binder-text, kind) for explicit/implicit/instance binders before the conclusion."""
    out = []
    for m in re.finditer(r"(\(|\{|\[|⦃)([^()\[\]{}⦃⦄]*?)(\)|\}|\]|⦄)", sig):
        out.append((m.group(2).strip(), m.group(1)))
    return out
