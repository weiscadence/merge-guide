"""Declaration index over local Mathlib + TauCeti sources (grep-level, cached).

Cache key = (root path, git HEAD of root, git HEAD of mathlib package). Stored as gzipped JSONL
under merge-kit/cache/. One row per declaration:
  [full_name, rel_file, line, kind, conclusion_text(<=300), source]  source = "mathlib"|"local"
"""
import gzip, hashlib, json, os, subprocess, sys
from collections import defaultdict
from . import lean

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(HERE, "cache")


def _head(d):
    try:
        return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        return "nogit"


def roots_for(repo_dir, src_dirs=None):
    """(label, dir, prefix) for the library sources to index."""
    out = []
    mathlib = os.path.join(repo_dir, ".lake/packages/mathlib")
    if os.path.isdir(os.path.join(mathlib, "Mathlib")):
        out.append(("mathlib", mathlib, "Mathlib"))
    for s in (src_dirs or []):
        if os.path.isdir(os.path.join(repo_dir, s)):
            out.append(("local", repo_dir, s))
    return out


def build(roots, verbose=True):
    rows = []
    for label, base, prefix in roots:
        top = os.path.join(base, prefix)
        n = 0
        for dp, _, fs in os.walk(top):
            for f in fs:
                if not f.endswith(".lean"):
                    continue
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, base)
                try:
                    txt = open(p, encoding="utf-8", errors="replace").read()
                except OSError:
                    continue
                for d in lean.parse_decls(txt, rel):
                    if not d["full"]:
                        continue
                    rows.append([d["full"], rel, d["line"], d["kind"], lean.conclusion(d["sig"])[:300], label,
                                 int(d["private"])])
                n += 1
        if verbose:
            print(f"[index] {label}:{prefix} {n} files", file=sys.stderr)
    return rows


def load(repo_dir, src_dirs=None, rebuild=False):
    roots = roots_for(repo_dir, src_dirs)
    key = hashlib.sha1(json.dumps([(l, os.path.realpath(b), p, _head(b)) for l, b, p in roots]).encode()).hexdigest()[:16]
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"index-{key}.jsonl.gz")
    if os.path.exists(path) and not rebuild:
        with gzip.open(path, "rt") as fh:
            rows = [json.loads(l) for l in fh]
    else:
        rows = build(roots)
        with gzip.open(path + ".tmp", "wt") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(path + ".tmp", path)
    return Index(rows, path)


class Index:
    def __init__(self, rows, path=""):
        self.rows, self.path = rows, path
        self.by_tok = defaultdict(list)     # name token -> row ids
        self.by_ctok = defaultdict(list)    # conclusion identifier -> row ids
        self.by_last = defaultdict(list)    # last name component -> row ids
        self.by_file = defaultdict(list)
        for i, r in enumerate(rows):
            for t in set(lean.name_tokens(r[0])):
                self.by_tok[t].append(i)
            for t in set(x for x in lean.sig_tokens(r[4]) if len(x) > 2 and x[0].isalpha()):
                self.by_ctok[t].append(i)
            self.by_last[r[0].split(".")[-1]].append(i)
            self.by_file[r[1]].append(i)
        self.ndocs = max(1, len(rows))

    def df(self, tok, table):
        return len(table.get(tok, ()))
