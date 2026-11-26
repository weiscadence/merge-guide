"""Validate merge-kit's deterministic checks on rubric-prereview v2's ground truth and split.

Inputs (read-only): rubric-prereview/v2/{gt_v3.json, prs_v3.json, ctx/<pr>.json, judged-*.json},
validate/cache/bodies/<pr>.json (PR title/body + edit history): run `python3 validate/fetch_bodies.py`
first; it fetches read-only via gh GraphQL and checks each against validate/bodies.sha256.
Index: local Mathlib + TauCeti from $MERGEKIT_WT (a TauCeti checkout) (current, NOT as of each PR: see README).
Tree for placement/imports: `git ls-tree <merge_base_sha>` of each PR in that worktree.

  python3 validate/validate.py run            # run checks, write validate/out/<pr>.json + pairs.md
  python3 validate/validate.py score          # read validate/judgements.json, print + write results.json
"""
import json, os, re, sys, subprocess
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from mergekit import context, index as mkindex  # noqa: E402
from mergekit.cli import run_checks, load_profile  # noqa: E402

V2 = os.environ.get("MERGEKIT_V2", os.path.join(HERE, "validate", "v2"))  # rubric-prereview v2 ground truth
OUT = os.path.join(HERE, "validate", "out")
WT = os.environ.get("MERGEKIT_WT", "tauceti")


def body_at(pr, ts):
    p = os.path.join(HERE, "validate", "cache", "bodies", f"{pr}.json")
    d = json.load(open(p))["data"]["repository"]["pullRequest"]
    # each edit node is one version; `editedAt` is that version's time (the original has
    # editedAt == PR createdAt), `createdAt` is when GitHub recorded the edit
    edits = sorted(d["userContentEdits"]["nodes"], key=lambda e: e["editedAt"])
    if not edits:
        return d["title"], d["body"], "current (never edited)"
    before = [e for e in edits if e["editedAt"] <= ts and e.get("diff") is not None]
    if before:
        return d["title"], before[-1]["diff"], f"version of {before[-1]['editedAt']}"
    return d["title"], edits[0]["diff"] or d["body"], f"earliest version {edits[0]['editedAt']}"


def file_added_ts():
    import gzip
    out, ts = {}, None
    for line in gzip.open(os.path.join(HERE, "validate", "tauceti-file-added.txt.gz"), "rt"):
        line = line.strip()
        if line.startswith("@"):
            ts = int(line[1:])
        elif line:
            out[line] = min(ts, out.get(line, ts))
    return out


_SHOW = {}


def make_row_ok(base):
    """A TauCeti row is usable only if its name already occurs in that file at the PR's merge base
    (`git show <base>:<file>`, cached). Removes candidates the PR itself (or later work) added."""
    def ok(r):
        if r[5] != "local":
            return True
        key = (base, r[1])
        if key not in _SHOW:
            p = subprocess.run(["git", "-C", WT, "show", f"{base}:{r[1]}"], capture_output=True, text=True)
            _SHOW[key] = p.stdout if p.returncode == 0 else ""
        return re.search(r"(?<![\w'.])" + re.escape(r[0].split(".")[-1]) + r"(?![\w'])", _SHOW[key]) is not None
    return ok


def ask_items(body):
    return re.findall(r"^- (.*)$", body, re.M)


def run():
    gt = json.load(open(os.path.join(V2, "gt_v3.json")))
    prs = json.load(open(os.path.join(V2, "prs_v3.json")))
    profile = load_profile("TauCetiProject/TauCeti")
    idx = mkindex.load(WT, ["TauCeti"])
    os.makedirs(OUT, exist_ok=True)
    pr_list = sorted({a["pr"] for a in gt})
    added = file_added_ts()
    pairs = ["# Candidate pairs (same rubric + same file, or PR-level), for hand judgement", ""]
    for pr in pr_list:
        cpath = os.path.join(V2, "ctx", f"{pr}.json")
        if not os.path.exists(cpath):
            continue
        meta = prs[str(pr)]
        title, body, which = body_at(pr, meta["ts"])
        ctx = context.from_ctx_json(json.load(open(cpath)), profile, pr_body=body, index=idx, repo_dir=WT, title=title)
        ctx.tree_ref = meta["base"]
        import datetime
        cut = datetime.datetime.fromisoformat(meta["ts"].replace("Z", "+00:00")).timestamp()
        ctx.exclude_files = {f for f, t in added.items() if t > cut}
        ctx.row_ok = make_row_ok(meta["base"])
        fs = run_checks(ctx)
        for i, f in enumerate(fs):
            f["id"] = f"{pr}:{i}"
        json.dump(dict(pr=pr, test=meta["test"], body_version=which, findings=fs), open(os.path.join(OUT, f"{pr}.json"), "w"), indent=1, ensure_ascii=False)
        asks = [a for a in gt if a["pr"] == pr]
        pairs.append(f"## PR {pr} ({'test' if meta['test'] else 'dev'}); body: {which}; findings {len(fs)}")
        for k, a in enumerate(asks):
            key = f"{pr}:{a['rubric']}:{a['file'].split('/')[-1]}"
            pairs.append(f"### REAL {key}")
            for it in ask_items(a["body"]):
                pairs.append(f"    > {it[:400]}")
            rub = a["rubric"]
            files = {a["file"]} | set(re.findall(r"`(TauCeti/[^`:]+\.lean)", a["body"]))
            cands = [f for f in fs if f["severity"] in ("ask", "maybe") and
                     (f["rubric"] == rub or (rub == "quality-pass" and f["rubric"] == "quality-pass")) and
                     (f["file"] == "" or f["file"] in files)]
            for f in cands:
                pairs.append(f"  - PRED {f['id']} {f['severity']} [{f['check']}] {f['file'].split('/')[-1]}:{f['line']} {f['msg'][:220]}")
                for e in f["evidence"][:3]:
                    pairs.append(f"        {e[:200]}")
            other = [f for f in fs if f["severity"] in ("ask", "maybe") and (f["file"] == "" or f["file"] in files) and f not in cands]
            if other:
                pairs.append(f"  (other-rubric findings on this file: " + "; ".join(f"{f['id']} {f['rubric']}:{f['line']} {f['msg'][:80]}" for f in other[:12]) + ")")
        pairs.append("")
        print(pr, len(fs), file=sys.stderr)
    open(os.path.join(HERE, "validate", "pairs.md"), "w").write("\n".join(pairs))


def score():
    gt = json.load(open(os.path.join(V2, "gt_v3.json")))
    prs = json.load(open(os.path.join(V2, "prs_v3.json")))
    J = json.load(open(os.path.join(HERE, "validate", "judgements.json")))
    llm = {}
    for split, tag in (("test", "test1"), ("dev", "dev3")):
        for kind in ("mimic", "gemini"):
            p = os.path.join(V2, f"judged-{split}-{tag if kind == 'mimic' or split == 'test' else 'dev2'}-{kind}.json")
            if os.path.exists(p):
                for r in json.load(open(p)):
                    if r.get("src") == "model" and r.get("same"):
                        llm.setdefault((kind, r["pr"], r["rubric"], r["file"]), True)
    res = {}
    for split in ("dev", "test"):
        asks = [a for a in gt if prs[str(a["pr"])]["test"] == (split == "test") and a["pr"] not in (8486, 1256)
                and os.path.exists(os.path.join(OUT, f"{a['pr']}.json"))]
        fs = [f for a_pr in sorted({a["pr"] for a in asks}) for f in json.load(open(os.path.join(OUT, f"{a_pr}.json")))["findings"] if f["severity"] in ("ask", "maybe")]
        hit_ids = set()
        rec = {"strict": 0, "lenient": 0}
        per_rubric = {}
        both = {"mimic": 0, "gemini": 0}
        llm_only = {"mimic": 0, "gemini": 0}
        for a in asks:
            key = f"{a['pr']}:{a['rubric']}:{a['file'].split('/')[-1]}"
            j = J.get(key, {})
            s = bool(j.get("strict")); l = s or bool(j.get("lenient"))
            hit_ids.update(j.get("strict", []) or []); hit_ids.update(j.get("lenient", []) or [])
            rec["strict"] += s; rec["lenient"] += l
            pr_ = per_rubric.setdefault(a["rubric"], [0, 0, 0]); pr_[0] += 1; pr_[1] += s; pr_[2] += l
            for kind in ("mimic", "gemini"):
                m = (kind, a["pr"], a["rubric"], a["file"]) in llm
                both[kind] += (m or s)
                llm_only[kind] += m
        n_ask_findings = sum(f["severity"] == "ask" for f in fs)
        res[split] = dict(n_prs=len({a["pr"] for a in asks}), n_real=len(asks), recall_strict=f"{rec['strict']}/{len(asks)}",
                          recall_lenient=f"{rec['lenient']}/{len(asks)}", n_findings=len(fs), n_ask_findings=n_ask_findings,
                          precision_findings=f"{len([f for f in fs if f['id'] in hit_ids])}/{len(fs)}",
                          precision_ask_only=f"{len([f for f in fs if f['id'] in hit_ids and f['severity'] == 'ask'])}/{n_ask_findings}",
                          per_rubric={k: f"{v[1]}/{v[0]} strict, {v[2]}/{v[0]} lenient" for k, v in sorted(per_rubric.items())},
                          llm_recall={k: f"{v}/{len(asks)}" for k, v in llm_only.items()},
                          union_strict_with_llm={k: f"{v}/{len(asks)}" for k, v in both.items()})
    json.dump(res, open(os.path.join(HERE, "validate", "results.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    {"run": run, "score": score}[sys.argv[1]]()
