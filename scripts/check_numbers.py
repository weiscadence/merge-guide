#!/usr/bin/env python3
"""Refuse to build docs from a ledger whose totals do not add up.

Reads data/numbers.json (written by collect_numbers.py) and checks that every stamped family of counts
partitions its total. `make docs` runs this before stamp.py, so a broken ledger never reaches a README.

  check_numbers.py          prints each check; exit 1 if any fails

Checks:
  buckets        obs.prs_landed + obs.prs_open + obs.prs_closed = obs.prs_total
  by repo        the per-repo rows sum to the same total, and each row's buckets sum to its n
  threads        the per-repo rubric threads sum to obs.threads_total; each repo's rubrics sum to its threads
  profile        every thread-derived profile count equals the observatory count for that rubric
  PR lists       the PR numbers listed per repo and bucket match that bucket's count
  claims         three sentences the docs state in words ("all", "none") still hold in the data
  logins         rows keyed by a reviewer login carry the pseudonym, never the login
  date           obs.asof is a date
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = json.load(open(os.path.join(HERE, "data", "numbers.json")))
res = []


def check(name, ok, detail):
    res.append(ok); print(f"  check {name}: {'PASS' if ok else 'FAIL'}  ({detail})")


def group(prefix):
    """{row: {field: value}} for keys prefix.<row>.<field>"""
    g = {}
    for k, v in N.items():
        if k.startswith(prefix + "."):
            row, _, field = k[len(prefix) + 1:].partition(".")
            if field and "." not in field:
                g.setdefault(row, {})[field] = v
    return g


t = N["obs.prs_total"]
parts = [N["obs.prs_landed"], N["obs.prs_open"], N["obs.prs_closed"]]
check("landed+open+closed=total", sum(parts) == t, f"{'+'.join(map(str, parts))} vs {t}")

rows = group("obs.t.by_repo")
check("by-repo rows sum to total", sum(r["n"] for r in rows.values()) == t, f"{sum(r['n'] for r in rows.values())} vs {t}")
bad = [k for k, r in rows.items() if r["landed"] + r["open"] + r["closed"] != r["n"]]
check("each repo's buckets sum to its n", not bad, f"{len(rows)} repos" + (f", off: {bad}" if bad else ""))

rub = {}
for k, v in N.items():
    m = re.fullmatch(r"obs\.rubric\.([a-z0-9_]+)\.([a-z0-9_]+)", k)
    if m:
        rub.setdefault(m.group(1), {})[m.group(2)] = v
tot = sum(r["threads"] for r in rub.values())
check("rubric threads sum to threads_total", tot == N["obs.threads_total"], f"{tot} vs {N['obs.threads_total']}")
bad = [k for k, r in rub.items() if sum(v for f, v in r.items() if f not in ("threads", "prs")) != r["threads"]]
check("each repo's rubrics sum to its threads", not bad, f"{len(rub)} repo(s)" + (f", off: {bad}" if bad else ""))

for repo, r in sorted(rub.items()):
    want = {f: v for f, v in r.items() if f not in ("threads", "prs")}
    have = {k[len(f"profile.{repo}."):]: v for k, v in N.items() if k.startswith(f"profile.{repo}.")}
    check(f"profile.{repo} = observatory threads", have == want,
          f"{len(want)} rubrics" + ("" if have == want else f"; profile {have} vs threads {want}"))

lists = group("obs.prs")
bad = [f"{k}.{b}" for k, r in lists.items() for b in ("landed", "closed", "open")
       if r[b + "_n"] != rows[k][b] or r[b + "_n"] != (0 if r[b] == "none" else r[b].count("#"))]
check("PR lists match the per-repo counts", set(lists) == set(rows) and not bad, f"{len(lists)} repos" + (f", off: {bad}" if bad else ""))
check("repos_total = per-repo rows", N["obs.repos_total"] == len(rows), f"{N['obs.repos_total']} vs {len(rows)}")
hc = {k.rsplit(".", 1)[1]: v for k, v in N.items() if k.startswith("obs.comments_human_by_repo.")}
check("human comments per repo sum to comments_human", sum(hc.values()) == N["obs.comments_human"], f"{sum(hc.values())} vs {N['obs.comments_human']}")

# Sentences in the notes that say "all" or "none". The docs state them in words, so they are checked here:
# if the data stops supporting one, the build stops and the sentence has to be rewritten by hand.
tc, abx = "taucetiproject_tauceti", "artblocks_abx"
check("claim: every TauCeti landing was bot-merged", lists[tc]["landed_bot"] == rows[tc]["landed"],
      f"{lists[tc]['landed_bot']} of {rows[tc]['landed']}")
check("claim: no comment without an AI marker on our TauCeti PRs", hc[tc] == 0, f"{hc[tc]}")
check("claim: every abx landing was merged by a person", lists[abx]["landed_human"] == rows[abx]["landed"],
      f"{lists[abx]['landed_human']} of {rows[abx]['landed']}")

names = {k.split(".")[3] for k in N if k.startswith("obs.t.rubric_by_login.")}
leak = sorted(n for n in names if not re.fullmatch(r"user_[0-9a-f]{10}|weiscadence|jiggy_cadence|.*_bot", n))
check("login-keyed rows are pseudonymised", not leak, f"{len(names)} rows" + (f", {len(leak)} raw" if leak else ""))

check("asof is a date", bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(N.get("obs.asof")))), N.get("obs.asof"))
print(f"numbers: {sum(res)}/{len(res)} checks pass")
sys.exit(0 if all(res) else 1)
