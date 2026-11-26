#!/usr/bin/env python3
"""Live PR ledger: every number derived from the GitHub API, with the PRs behind it.

Why: README counts went stale (dated 2026-11-22) and a plain is:merged filter misses Bors
merges (Bors pushes the commit, then CLOSES the PR with a "[Merged by Bors]" title).

landed  = merged_at set  OR  closed with title "[Merged by Bors]"
merger  = merged_by login (bors-closed -> closed_by of the issue event); [bot] suffix = bot
own     = repos under weiscadence/ or jiggy-cadence/ (excluded, as in the README)

Usage: pr-ledger.py [--json out.json]   Prints counts + the PR list for every count.
Self-check: the buckets must partition the total, or it exits 1.
"""
import json, subprocess, sys, datetime

AUTHORS = ["weiscadence", "jiggy-cadence"]
OWN = {a.lower() for a in AUTHORS}

def gh(*args):
    r = subprocess.run(["gh", "api", *args], capture_output=True, text=True, check=True)
    return json.loads(r.stdout) if r.stdout.strip() else None

def search(author):
    out, page = [], 1
    while True:
        d = gh("-X", "GET", "search/issues", "-f", f"q=is:pr author:{author}",
               "-f", "per_page=100", "-f", f"page={page}")
        out += d["items"]
        if len(d["items"]) < 100: return out
        page += 1

prs = []
for a in AUTHORS:
    for it in search(a):
        owner, repo = it["repository_url"].split("/")[-2:]
        p = dict(repo=f"{owner}/{repo}", num=it["number"], author=a, state=it["state"],
                 title=it["title"], url=it["html_url"], own=owner.lower() in OWN)
        bors = it["title"].startswith("[Merged by Bors]")
        p["merged_at"] = it["pull_request"].get("merged_at")
        if p["merged_at"]:
            p["landed"], p["via"] = True, "merged"
            p["merger"] = (gh(f"repos/{p['repo']}/pulls/{p['num']}").get("merged_by") or {}).get("login")
            if not p["merger"]:  # merge queues leave merged_by null; the merged/closed event has the actor
                ev = [e for e in gh(f"repos/{p['repo']}/issues/{p['num']}/events", "--paginate")
                      if e["event"] in ("merged", "closed") and e.get("actor")]
                if ev: p["merger"] = ev[-1]["actor"]["login"]
        elif bors and p["state"] == "closed":
            p["landed"], p["via"] = True, "bors"
            p["merger"] = (gh(f"repos/{p['repo']}/issues/{p['num']}").get("closed_by") or {}).get("login")
        else:
            p["landed"], p["via"], p["merger"] = False, None, None
        p["bucket"] = ("landed" if p["landed"] else "open" if p["state"] == "open" else "closed_unmerged")
        p["by_bot"] = bool(p["merger"] and p["merger"].endswith("[bot]"))
        prs.append(p)

ext = [p for p in prs if not p["own"]]
def n(f): return [p for p in ext if f(p)]
tc = lambda p: p["repo"] == "TauCetiProject/TauCeti"
C = {
  "total": n(lambda p: True),
  "landed": n(lambda p: p["landed"]),
  "closed_unmerged": n(lambda p: p["bucket"] == "closed_unmerged"),
  "open": n(lambda p: p["bucket"] == "open"),
  "landed_human": n(lambda p: p["landed"] and p["merger"] and not p["by_bot"]),
  "landed_merger_unknown": n(lambda p: p["landed"] and not p["merger"]),
  "landed_bot": n(lambda p: p["landed"] and p["by_bot"]),
  "landed_bors": n(lambda p: p["via"] == "bors"),
  "tauceti_total": n(tc), "tauceti_landed": n(lambda p: tc(p) and p["landed"]),
  "tauceti_open": n(lambda p: tc(p) and p["bucket"] == "open"),
  "tauceti_closed_unmerged": n(lambda p: tc(p) and p["bucket"] == "closed_unmerged"),
  "tauceti_merged_plain": n(lambda p: tc(p) and p["via"] == "merged"),
  "tauceti_bors": n(lambda p: tc(p) and p["via"] == "bors"),
  "roadmap_landed": n(lambda p: p["repo"] == "TauCetiProject/TauCetiRoadmap" and p["landed"]),
  "outside_total": n(lambda p: not tc(p)), "outside_landed": n(lambda p: not tc(p) and p["landed"]),
  "outside_open": n(lambda p: not tc(p) and p["bucket"] == "open"),
  "outside_closed_unmerged": n(lambda p: not tc(p) and p["bucket"] == "closed_unmerged"),
}
for p in ext:  # per-repo human merges, keyed human@owner/repo
    if p["landed"] and p["merger"] and not p["by_bot"]:
        C.setdefault(f"human@{p['repo']}", []).append(p)
# invariants: buckets partition the total; human+bot = landed; inside+outside = total
L = lambda k: len(C[k])
checks = {
  "landed+closed+open=total": L("landed") + L("closed_unmerged") + L("open") == L("total"),
  "human+bot+unknown=landed": L("landed_human") + L("landed_bot") + L("landed_merger_unknown") == L("landed"),
  "tauceti+outside=total": L("tauceti_total") + L("outside_total") == L("total"),
  "tauceti buckets": L("tauceti_landed") + L("tauceti_open") + L("tauceti_closed_unmerged") == L("tauceti_total"),
  "outside buckets": L("outside_landed") + L("outside_open") + L("outside_closed_unmerged") == L("outside_total"),
}
resolved = L("landed") + L("closed_unmerged")
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%MZ")
print(f"PR ledger @ {now}  (external repos only; own repos excluded: {len(prs)-len(ext)})")
for k, v in C.items():
    print(f"  {k:26} {len(v):3}   " + " ".join(f"{p['repo'].split('/')[1]}#{p['num']}" for p in v)[:160])
print(f"  resolved rate: {L('landed')}/{resolved} = {100*L('landed')/max(resolved,1):.0f}%")
for k, ok in checks.items(): print(f"  check {k}: {'PASS' if ok else 'FAIL'}")
if "--json" in sys.argv:
    out = sys.argv[sys.argv.index("--json") + 1]
    json.dump({"generated": now, "counts": {k: len(v) for k, v in C.items()},
               "evidence": {k: [p["url"] for p in v] for k, v in C.items()}, "prs": prs},
              open(out, "w"), indent=1)
    print(f"  wrote {out}")
sys.exit(0 if all(checks.values()) else 1)
