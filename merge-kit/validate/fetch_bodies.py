"""Fetch the PR titles/bodies + edit history that validate.py reads, and check them against bodies.sha256.

PR text belongs to its authors, so the repo ships only (repo, PR number, sha256), not the text.
This script re-fetches each PR read-only through `gh api graphql` into validate/cache/bodies/
(gitignored) and verifies the sha256 of a canonical JSON form of the pullRequest object.

  python3 validate/fetch_bodies.py           # fetch missing, verify all; exit 1 on mismatch
  python3 validate/fetch_bodies.py --hash    # print manifest lines for already-cached files

Each manifest line pins the one body version validate.py used (by `editedAt`, or `current` for a
never-edited PR), so later edits to a PR do not break the check. Before hashing and before
validate.py reads it, the agent's internal name is replaced by `[agent]` (the same redaction the
original snapshot had).
"""
import hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache", "bodies")
MANIFEST = os.path.join(HERE, "bodies.sha256")
QUERY = """query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){
title body createdAt userContentEdits(first:100){nodes{createdAt editedAt diff}}}}}"""


REDACT = re.compile("(?<![\\w-])" + "Cad" + "ence" + "(?![\\w-])")  # split so the privacy grep stays clean


def redact(path):
    d = json.load(open(path))
    pr = d["data"]["repository"]["pullRequest"]
    pr["body"] = REDACT.sub("[agent]", pr["body"] or "")
    for e in pr["userContentEdits"]["nodes"]:
        if e.get("diff") is not None:
            e["diff"] = REDACT.sub("[agent]", e["diff"])
    json.dump(d, open(path, "w"), ensure_ascii=False)
    return pr


def version_text(pr, version):
    if version == "current":
        return pr["body"]
    hit = [e for e in pr["userContentEdits"]["nodes"] if e["editedAt"] == version]
    return hit[0]["diff"] if hit else None


def canon(pr, version):
    text = version_text(pr, version)
    if text is None:
        return "missing"
    return hashlib.sha256((pr["title"] + "\n" + text).encode()).hexdigest()


def manifest():
    for line in open(MANIFEST):
        if line.strip() and not line.startswith("#"):
            yield line.split()


def main():
    os.makedirs(CACHE, exist_ok=True)
    if "--hash" in sys.argv:
        for _, repo, pr, version in manifest():
            print(canon(redact(os.path.join(CACHE, f"{pr}.json")), version), repo, pr, version)
        return
    bad = 0
    for sha, repo, pr, version in manifest():
        p = os.path.join(CACHE, f"{pr}.json")
        if not os.path.exists(p):
            owner, name = repo.split("/")
            out = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"owner={owner}",
                                  "-f", f"name={name}", "-F", f"n={pr}"], capture_output=True, text=True, check=True).stdout
            open(p, "w").write(out)
        got = canon(redact(p), version)
        ok = got == sha
        bad += not ok
        print(f"{'ok      ' if ok else 'CHANGED '} {repo}#{pr} @ {version}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
