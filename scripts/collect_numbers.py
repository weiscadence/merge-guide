#!/usr/bin/env python3
"""Flatten the observatory and merge-kit outputs into one ledger: data/numbers.json.

  collect_numbers.py [--obs DIR]     (default: $OBSERVATORY or ../contrib-observatory)

Sources (all read-only):
  obs.*        contrib-observatory out/metrics.json `counts`         (our 64 PRs, 334 comments)
  obs.t.*      contrib-observatory out/tables.json                    (rendered tables of the same data)
  field.*      contrib-observatory field/stats.json                   (1496-PR field sample)
  census.*     contrib-observatory field/census/stats.json            (full census; may be absent)
  mk.*         merge-kit/validate/results.json                        (merge-kit recall/precision)
  profile.*    merge-kit/repos/*.yaml review.recurring                (asks per class, our data)

Keys are lower-case, non-alphanumerics folded to `_`. Fractions "k/n" become .k, .n, .pct, .lo, .hi
(Wilson 95%, percent, rounded). Output is sorted, so the same inputs give the same bytes.
If the observatory directory is missing, the existing data/numbers.json is kept (offline build).
"""
import glob, json, math, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "data", "numbers.json")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")


def wilson(k, n, z=1.96):
    if not n:
        return None, None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return round(100 * (c - h) / d), round(100 * (c + h) / d)


def put_frac(N, key, k, n):
    lo, hi = wilson(k, n)
    N[key + ".k"], N[key + ".n"] = k, n
    if n:
        N[key + ".pct"] = round(100 * k / n); N[key + ".lo"] = lo; N[key + ".hi"] = hi


def flat(N, prefix, v):
    if isinstance(v, dict):
        for k, x in v.items():
            flat(N, f"{prefix}.{slug(k)}", x)
    elif isinstance(v, list) and len(v) == 2 and all(isinstance(x, (int, float)) or x is None for x in v):
        N[prefix + ".lo"], N[prefix + ".hi"] = v
    elif isinstance(v, str) and re.fullmatch(r"\d+/\d+ strict, \d+/\d+ lenient", v):
        a, b = re.findall(r"\d+/\d+", v)
        flat(N, prefix + ".strict", a); flat(N, prefix + ".lenient", b)
    elif isinstance(v, str) and re.fullmatch(r"\d+/\d+", v):
        k, n = map(int, v.split("/")); put_frac(N, prefix, k, n)
    elif isinstance(v, (int, float, str, bool)) or v is None:
        N[prefix] = v


ROWKEY = ("group", "cls", "repo", "month", "model", "key", "who")


def flat_table(N, prefix, rows):
    if isinstance(rows, dict):
        return  # matrix tables (model_rubric, author_classes) are not stamped
    for r in rows:
        if not isinstance(r, dict):
            continue
        name = next((r[k] for k in ROWKEY if k in r), None)
        if name is None:
            continue
        if "month" in r and "group" in r:
            name = f"{r['group']}_{r['month']}"
        for k, x in r.items():
            if k not in ROWKEY:
                flat(N, f"{prefix}.{slug(name)}.{slug(k)}", x)


def collect_obs(N, obs, m):
    met = json.load(open(m))
    for k, v in met["counts"].items():
        flat(N, "obs." + slug(k), v)
    N["obs.asof"] = met["generated"][:10]
    for t, rows in sorted(json.load(open(os.path.join(obs, "out", "tables.json"))).items()):
        flat_table(N, "obs.t." + slug(t), rows)
    fs = os.path.join(obs, "field", "stats.json")
    if os.path.exists(fs):
        flat(N, "field", json.load(open(fs)))
        for sec in ("baseline_by_repo", "baseline_pooled", "by_family", "by_repo"):
            for name, r in json.load(open(fs))[sec].items():
                if r.get("resolved_n"):
                    put_frac(N, f"field.{sec}.{slug(name)}.rate", r["landed"], r["resolved_n"])
    cs = os.path.join(obs, "field", "census", "stats.json")
    N["census.available"] = os.path.exists(cs)
    if os.path.exists(cs):
        flat(N, "census", json.load(open(cs)))


def main():
    a = sys.argv[1:]
    obs = a[a.index("--obs") + 1] if "--obs" in a else os.environ.get("OBSERVATORY", os.path.join(HERE, "..", "contrib-observatory"))
    old = json.load(open(OUT)) if os.path.exists(OUT) else {}
    N = {}
    m = os.path.join(obs, "out", "metrics.json")
    if os.path.exists(m):
        collect_obs(N, obs, m)
    else:
        print(f"collect: no observatory outputs at {obs}; keeping obs/field/census keys from the existing ledger")
        N.update({k: v for k, v in old.items() if k.split(".")[0] in ("obs", "field", "census")})
    flat(N, "mk", json.load(open(os.path.join(HERE, "merge-kit", "validate", "results.json"))))
    try:
        import yaml
        N["mk.profiles"] = len(glob.glob(os.path.join(HERE, "merge-kit", "repos", "*.yaml")))
        for p in sorted(glob.glob(os.path.join(HERE, "merge-kit", "repos", "*.yaml"))):
            y = yaml.safe_load(open(p))
            name = slug(y["repo"].split("/")[1])
            for cls, n in sorted(((y.get("review") or {}).get("recurring") or {}).items()):
                N[f"profile.{name}.{slug(cls)}"] = n
    except ImportError:
        print("collect: PyYAML missing; profile.* keys not refreshed")
        N.update({k: v for k, v in old.items() if k.startswith("profile.")})
    for key in [k[:-2] for k in N if k.endswith(".k")]:
        if key + ".n" in N and key + ".pct" not in N and isinstance(N[key + ".n"], int):
            put_frac(N, key, N[key + ".k"], N[key + ".n"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    s = json.dumps(dict(sorted(N.items())), indent=0, ensure_ascii=False, sort_keys=True) + "\n"
    open(OUT, "w").write(s)
    print(f"collect: {len(N)} keys -> {os.path.relpath(OUT, HERE)} (census {'present' if N['census.available'] else 'absent: placeholders stay'})")


if __name__ == "__main__":
    main()
