#!/usr/bin/env python3
"""Render src/*.in.md into the published docs, filling every number from data/numbers.json.

Same idea as the observatory's stamp-numbers.py: no number about our data is typed by hand.

Tags (invisible in rendered markdown; kept in the output so a reader can see each number's key):
  <!--n:EXPR-->...<!--/n-->     EXPR over ledger keys (dotted), + - * / ( ); trailing % = percent of a ratio
  <!--frac:KEY-->...<!--/frac--> "k/n (p%, 95% CI lo–hi%)" from KEY.k, KEY.n, KEY.pct, KEY.lo, KEY.hi
  <!--asof-->...<!--/asof-->    observatory generation date
A key under `census.` that is missing renders as "(census pending)" and is listed; any other
missing key is an error (exit 1). `--lint` also fails on an untagged ratio or percentage outside
a line that carries a [lit:...] tag, a code block, or a URL: those are hand-typed numbers.

  stamp.py [--lint] [--strict]      (--strict: pending census keys are an error too)
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = json.load(open(os.path.join(HERE, "data", "numbers.json")))
PENDING = "(census pending)"
NAME = re.compile(r"[a-z_][a-z0-9_]*(?:\.[a-z0-9_]+)+|[a-z_][a-z0-9_]*")
pending, bad = set(), []


class Pending(Exception):
    pass


def get(k):
    if k in N and N[k] is not None:
        return N[k]
    if k.startswith("census."):
        pending.add(k); raise Pending(k)
    raise KeyError(k)


def num(x):
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, float):
        return str(int(x)) if x.is_integer() else f"{x:.2f}".rstrip("0").rstrip(".")
    return str(x)


def value(expr):
    pct = expr.endswith("%"); e = expr[:-1] if pct else expr
    names = {}
    def sub(m):
        v = f"_v{len(names)}"; names[v] = get(m.group(0)); return v
    py = NAME.sub(sub, e)
    if not re.fullmatch(r"[\s\w+\-*/().]*", py):
        raise ValueError(expr)
    if len(names) == 1 and py.strip() == "_v0" and not pct:
        return num(names["_v0"])
    x = eval(py, {"__builtins__": {}}, names)
    return f"{round(100 * x)}%" if pct else num(x)


def frac(key):
    k, n = get(key + ".k"), get(key + ".n")
    if not n:
        return f"{k}/{n}"
    return f"{k}/{n} ({get(key + '.pct')}%, 95% CI {get(key + '.lo')}–{get(key + '.hi')}%)"


def render(src):
    def rep(fn):
        def r(m):
            try:
                new = fn(m.group(1))
            except Pending:
                new = PENDING
            except (KeyError, ValueError, ZeroDivisionError) as e:
                bad.append(f"{m.group(1)} ({type(e).__name__}: {e})"); return m.group(0)
            return m.group(0)[: m.start(2) - m.start(0)] + new + m.group(0)[m.end(2) - m.start(0):]
        return r
    out = re.sub(r"<!--n:(.+?)-->(.*?)<!--/n-->", rep(value), src)
    out = re.sub(r"<!--frac:(.+?)-->(.*?)<!--/frac-->", rep(frac), out)
    out = re.sub(r"<!--asof()-->(.*?)<!--/asof-->", rep(lambda _: str(N["obs.asof"])), out)
    return out


UNTAGGED = re.compile(r"(?<![\w.#/-])\d+(?:\.\d+)?\s?%|(?<![\w.#/-])\d+/\d+(?![\w/])")


def lint(path, text):
    errs, fence = [], False
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            fence = not fence; continue
        if fence or "[lit:" in line:
            continue
        bare = re.sub(r"<!--(n|frac|asof)(:.+?)?-->.*?<!--/\1-->", "", line)
        bare = re.sub(r"https?://\S+|`[^`]*`|<!--.*?-->", "", bare)
        bare = re.sub(r"(Wilson )?95% (CI|interval)|Wilson 95%", "", bare)  # the interval's level, not a datum
        for m in UNTAGGED.finditer(bare):
            errs.append(f"{os.path.relpath(path, HERE)}:{i}: untagged number {m.group(0)!r}")
    return errs


def main():
    a = sys.argv[1:]
    errs = []
    for src in sorted(glob.glob(os.path.join(HERE, "src", "**", "*.in.md"), recursive=True)):
        rel = os.path.relpath(src, os.path.join(HERE, "src"))[: -len(".in.md")] + ".md"
        dst = os.path.join(HERE, rel)
        out = render(open(src).read())
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst) or open(dst).read() != out:
            open(dst, "w").write(out)
        if "--lint" in a:
            errs += lint(dst, out)
    for b in bad:
        print("  UNKNOWN", b)
    for p in sorted(pending):
        print("  PENDING", p)
    for e in errs:
        print("  LINT", e)
    print(f"stamp: {len(bad)} unknown, {len(pending)} pending census key(s), {len(errs)} lint error(s)")
    if bad or errs or ("--strict" in a and pending):
        sys.exit(1)


if __name__ == "__main__":
    main()
