#!/usr/bin/env python3
"""Fill tagged numbers in a doc from a ledger JSON, so no number is ever typed by hand.

Tags (invisible in rendered markdown):
  <!--n:EXPR-->47<!--/n-->        EXPR over ledger count names, e.g. landed, landed/(landed+closed_unmerged)%
                                  trailing % = percent, rounded. Per-repo names: human@owner/repo.
  <!--list:KEY-->...<!--/list-->  comma list of [repo#N](url) links for count KEY
  <!--asof-->2026-11-22<!--/asof-->  ledger generation time

Usage: stamp-numbers.py LEDGER.json DOC.md [--write]   (default: dry run, prints diffs)
Exit 1 if a tag names an unknown count (refuses to guess). Exit 2 = numbers changed (dry run).
"""
import json, re, sys

led = json.load(open(sys.argv[1])); doc = sys.argv[2]; write = "--write" in sys.argv
counts, ev = led["counts"], led["evidence"]
prs = {p["url"]: p for p in led["prs"]}
NAME = re.compile(r"[A-Za-z_]\w*(?:@[\w.\-]+/[\w.\-]+)?")  # '/' only inside human@owner/repo

def value(expr):
    pct = expr.endswith("%"); e = expr[:-1] if pct else expr
    names = {}
    def sub(m):
        k = m.group(0)
        if k not in counts: raise KeyError(k)
        v = f"_v{len(names)}"; names[v] = counts[k]; return v
    py = NAME.sub(sub, e)
    if not re.fullmatch(r"[\s\w+\-*/()]*", py): raise ValueError(expr)
    x = eval(py, {"__builtins__": {}}, names)
    return f"{round(100 * x)}%" if pct else (str(int(x)) if float(x).is_integer() else f"{x:.2f}")

def links(key):
    if key not in ev: raise KeyError(key)
    return ", ".join(f"[{prs[u]['repo'].split('/')[1]}#{prs[u]['num']}]({u})" for u in ev[key])

src = open(doc).read(); changes = []; bad = []
def rep(kind, fn):
    def r(m):
        try: new = fn(m.group(1))
        except (KeyError, ValueError) as e: bad.append(f"{kind}:{m.group(1)} ({e})"); return m.group(0)
        if new != m.group(2): changes.append(f"{kind}:{m.group(1)}  {m.group(2)!r} -> {new!r}")
        return m.group(0).replace(m.group(2), new, 1) if m.group(2) else m.group(0).replace("-->", "-->" + new, 1)
    return r
out = re.sub(r"<!--n:(.+?)-->(.*?)<!--/n-->", rep("n", value), src)
out = re.sub(r"<!--list:(.+?)-->(.*?)<!--/list-->", rep("list", links), out, flags=re.S)
out = re.sub(r"<!--asof()-->(.*?)<!--/asof-->", rep("asof", lambda _: led["generated"][:10]), out)
for c in changes: print("  CHANGE", c)
for b in bad: print("  UNKNOWN", b)
if bad: sys.exit(1)
if write and out != src: open(doc, "w").write(out); print(f"wrote {doc}")
print(f"{len(changes)} change(s)")
sys.exit(2 if changes and not write else 0)
