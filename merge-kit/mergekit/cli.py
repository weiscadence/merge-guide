"""merge-kit CLI.

  merge-kit check <repo-dir> <base-ref> [--repo owner/name] [--body FILE] [--title T] [--out DIR]
                  [--no-index] [--rebuild-index] [--lake-lint]
  merge-kit selftest
  merge-kit template <owner/name>
"""
import argparse, glob, importlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from mergekit import context, index as mkindex  # noqa: E402
import yaml  # noqa: E402

CHECKS = ["reuse", "placement", "naming", "docs", "generality", "attribution", "scope", "hygiene", "proof_shape"]
RUBRIC_ORDER = ["reuse", "api-design", "generality", "documentation", "naming", "placement", "proof-quality",
                "attribution", "scope", "correctness", "policy", "hygiene"]


def load_profile(repo):
    p = os.path.join(HERE, "repos", repo.replace("/", "__") + ".yaml")
    if not os.path.exists(p):
        return {"repo": repo}
    return yaml.safe_load(open(p))


def guess_repo(repo_dir):
    out = subprocess.run(["git", "-C", repo_dir, "remote", "-v"], capture_output=True, text=True).stdout
    names = [p[:-len(".yaml")].replace("__", "/") for p in os.listdir(os.path.join(HERE, "repos"))]
    for n in names:  # prefer upstream-looking remotes
        if re.search(r"[:/]" + re.escape(n) + r"(\.git)?\s", out):
            return n
    for n in names:
        if n.split("/")[1].lower() in out.lower():
            return n
    return None


def run_checks(ctx, lake_lint=False, only=None):
    fs = []
    for name in CHECKS:
        if only and name not in only:
            continue
        mod = importlib.import_module(f"checks.{name}")
        try:
            fs += mod.run(ctx, lake_lint=lake_lint) if name == "hygiene" else mod.run(ctx)
        except Exception as e:  # a broken check must not hide the others
            fs.append(context.finding(name, "hygiene", "", 0, f"check crashed: {e!r}", "info"))
    return fs


def render_report(ctx, findings, profile):
    L = [f"# merge-kit report: {profile.get('repo', '?')}", ""]
    asks = [f for f in findings if f["severity"] == "ask"]
    maybes = [f for f in findings if f["severity"] == "maybe"]
    L.append(f"{len(asks)} ask, {len(maybes)} maybe, {len(findings) - len(asks) - len(maybes)} info. "
             f"Files: {len(ctx.files)}; new declarations: {sum(len(f.new_decls()) for f in ctx.lean_files())}.")
    L.append("`ask` = the rule is mechanical and fired; `maybe` = heuristic or a candidate list to review by hand.")
    L.append("A clean report does NOT clear the PR: see README 'What it does not catch'.\n")
    rev = profile.get("review") or {}
    if rev.get("recurring"):
        L.append("Recurring asks in this repo (our data): " + ", ".join(f"{k} {v}" for k, v in rev["recurring"].items()) + "\n")
    by = {}
    for f in findings:
        by.setdefault(f["rubric"], []).append(f)
    for rub in RUBRIC_ORDER + sorted(set(by) - set(RUBRIC_ORDER)):
        if rub not in by:
            continue
        L.append(f"## {rub}")
        for f in sorted(by[rub], key=lambda x: ({"ask": 0, "maybe": 1}.get(x["severity"], 2), x["file"], x["line"])):
            loc = f"{f['file']}:{f['line']}" if f["file"] else "(PR)"
            L.append(f"- **{f['severity']}** [{f['check']}{', heuristic' if f['heuristic'] else ''}] `{loc}` {f['msg']}")
            for e in f["evidence"][:5]:
                L.append(f"    - {e}")
        L.append("")
    ready = profile.get("ready_signal")
    if ready:
        L.append(f"## Before asking for review\n- Ready signal: {ready.get('how')} ({ready.get('source')})")
        mx = profile.get("max_open_prs")
        if mx:
            L.append(f"- Max open PRs: {mx.get('value')} ({mx.get('source')})")
        for c in (profile.get("ci") or {}).get("local", []):
            L.append(f"- CI locally: `{c}`")
    return "\n".join(L) + "\n"


def llm_prompt(ctx, findings, profile, max_diff=60000):
    # TauCetiReview's open rubrics: set MERGEKIT_RUBRICS, or `make rubrics` fetches them into rubrics/
    rub_dir = os.environ.get("MERGEKIT_RUBRICS") or os.path.join(HERE, "rubrics")
    L = ["# LLM review pass (prepared by merge-kit; run with a Claude subagent, no paid API)", "",
         "You are reviewing a pull request before it is opened. Apply each rubric below to the diff.",
         "Output JSON lines: {rubric, file, line, decl, ask, fix, evidence}. Only asks you would bet the",
         "repo's reviewer raises in the FIRST round. For reuse, name the replacement (candidates below were",
         "found by grep over local Mathlib + the repo; verify them, do not trust them).", ""]
    if (profile.get("review") or {}).get("rubric_files") and os.path.isdir(rub_dir):
        L.append("## Rubrics")
        for r in profile["review"]["rubric_files"]:
            p = os.path.join(rub_dir, r)
            if os.path.exists(p):
                L.append(f"### {r}\n" + open(p).read())
    elif (profile.get("review") or {}).get("rubric_files"):
        L.append("## Rubrics\n(not found: run `make rubrics` or set MERGEKIT_RUBRICS to a TauCetiReview rubrics/ dir)")
    else:
        L.append("## Review style\n" + yaml.safe_dump(profile.get("review") or {}, allow_unicode=True))
    L.append("## Deterministic findings already raised (do not repeat; confirm or refute the `maybe`s)")
    for f in findings:
        if f["severity"] in ("ask", "maybe"):
            L.append(f"- {f['severity']} {f['rubric']} {f['file']}:{f['line']} {f['msg']}")
            for e in f["evidence"][:5]:
                L.append(f"    - {e}")
    if ctx.pr_body is not None:
        L.append("## PR description\n" + ctx.pr_body)
    L.append("## Diff")
    budget = max_diff
    for f in ctx.files:
        chunk = f"### {f.name} ({f.status})\n```\n" + (f.text if f.status == "added" else f.patch) + "\n```\n"
        if len(chunk) > budget:
            chunk = chunk[:budget] + "\n...(truncated)\n```\n"
        budget -= len(chunk)
        L.append(chunk)
        if budget <= 0:
            L.append("(diff budget exhausted)")
            break
    return "\n".join(L)


def cmd_check(a):
    repo = a.repo or guess_repo(a.repo_dir)
    profile = load_profile(repo or "unknown/unknown")
    profile.setdefault("repo", repo)
    idx = None
    if not a.no_index:
        src = (profile.get("lean") or {}).get("src_dirs", [])
        if os.path.isdir(os.path.join(a.repo_dir, ".lake/packages/mathlib")) or src:
            os.nice(19) if hasattr(os, "nice") else None
            idx = mkindex.load(a.repo_dir, src, rebuild=a.rebuild_index)
    body = open(a.body).read() if a.body else None
    ctx = context.from_git(a.repo_dir, a.base, profile, pr_body=body, index=idx, title=a.title)
    findings = run_checks(ctx, lake_lint=a.lake_lint)
    out = a.out or os.path.join(a.repo_dir, ".merge-kit")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "REPORT.md"), "w").write(render_report(ctx, findings, profile))
    open(os.path.join(out, "llm-pass-prompt.md"), "w").write(llm_prompt(ctx, findings, profile))
    open(os.path.join(out, "findings.json"), "w").write(json.dumps(findings, indent=1, ensure_ascii=False))
    from checks import attribution
    open(os.path.join(out, "pr-body-template.md"), "w").write(attribution.template(profile, ctx))
    n_ask = sum(f["severity"] == "ask" for f in findings)
    print(f"merge-kit: {n_ask} ask, {sum(f['severity'] == 'maybe' for f in findings)} maybe -> {out}/REPORT.md")
    return 1 if n_ask else 0


def cmd_selftest(_a):
    bad = 0
    for name in CHECKS:
        mod = importlib.import_module(f"checks.{name}")
        try:
            print(f"{name}: {mod.selftest()}")
        except AssertionError as e:
            bad += 1; print(f"{name}: FAIL {str(e)[:500]}")
    for p in sorted(glob.glob(os.path.join(HERE, "repos", "*.yaml"))):
        y = yaml.safe_load(open(p))
        missing = [k for k in ("repo", "ai_policy", "ci", "pr", "placement", "review", "max_open_prs", "ready_signal") if k not in y]
        unsourced = _unsourced(y)
        status = "ok" if not missing and not unsourced else f"FAIL missing={missing} unsourced={unsourced[:5]}"
        bad += status != "ok"
        print(f"profile {os.path.basename(p)}: {status}")
    return 1 if bad else 0


def _unsourced(y, path=""):
    """Every top-level section that is a mapping must carry a `source` (or `sources`)."""
    out = []
    for k, v in y.items():
        if k in ("repo", "name", "lean", "scope", "naming", "docs"):
            continue
        if isinstance(v, dict) and not ({"source", "sources"} & set(v)):
            out.append(k)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="merge-kit")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("repo_dir"); c.add_argument("base")
    c.add_argument("--repo"); c.add_argument("--body"); c.add_argument("--title"); c.add_argument("--out")
    c.add_argument("--no-index", action="store_true"); c.add_argument("--rebuild-index", action="store_true")
    c.add_argument("--lake-lint", action="store_true")
    sub.add_parser("selftest")
    t = sub.add_parser("template"); t.add_argument("repo")
    a = ap.parse_args(argv)
    if a.cmd == "check":
        return cmd_check(a)
    if a.cmd == "selftest":
        return cmd_selftest(a)
    if a.cmd == "template":
        from checks import attribution
        print(attribution.template(load_profile(a.repo)))
        return 0


if __name__ == "__main__":
    sys.exit(main())
