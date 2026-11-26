#!/usr/bin/env python3
"""Fail if any shipped file carries a local path, a credential, or an internal agent/operator name.

Public GitHub logins (including our own PR-author accounts) are allowed: they are already public
on every PR. Scans every text file under the repo except .git/ and this script; .gz files are
decompressed first.

  privacy_check.py          exit 1 on any hit, printing file:line and the pattern name
"""
import gzip, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERNS = {
    "local path": re.compile(r"/home/\w+|/Users/\w+|~/[\w.-]+|\.openclaw|/tmp/[\w.-]+"),
    "credential": re.compile(r"\b(sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bp]-[\w-]{10,})"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "email": re.compile(r"[\w.+-]+@(gmail|outlook|hotmail|proton)\.\w+"),
    # internal agent / operator names (the public login `weiscadence` is fine: lookbehind skips it)
    "internal name": re.compile(r"(?<![\w-])(Cadence|Jiggy|Lodestone|Aperture)(?![\w-])"),
    "agent harness": re.compile(r"\b(sessions_(spawn|history|search|yield)|subagent-reports|HEARTBEAT|MEMORY\.md|HANDOFF\.md|brain-nodes)\b"),
}
SKIP_DIRS = {".git", "__pycache__", "cache", ".merge-kit", "rubrics"}
SELF = os.path.abspath(__file__)
COPYRIGHT_OK = {"LICENSE"}  # holder name is intentional here


def lines(path):
    if path.endswith(".gz"):
        with gzip.open(path, "rt", errors="replace") as f:
            yield from f
        return
    with open(path, "rb") as f:
        head = f.read(4096)
    if b"\0" in head:
        return
    with open(path, errors="replace") as f:
        yield from f


def main():
    hits = 0
    for root, dirs, files in os.walk(HERE):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for fn in sorted(files):
            p = os.path.join(root, fn)
            if os.path.abspath(p) == SELF or fn.endswith(".pyc") or (root == HERE and fn in COPYRIGHT_OK):
                continue
            for i, line in enumerate(lines(p), 1):
                for name, rx in PATTERNS.items():
                    m = rx.search(line)
                    if m:
                        hits += 1
                        if hits <= 200:
                            print(f"  {os.path.relpath(p, HERE)}:{i}: {name}: {m.group(0)!r}")
    # per-person rows in the ledger must carry the observatory's pseudonyms, never a GitHub login
    import json
    for key in json.load(open(os.path.join(HERE, "data", "numbers.json"))):
        m = re.search(r"_by_login\.([a-z0-9_]+?)\.(human_typed|other|rubric)$", key)
        if m and not re.fullmatch(r"user_[0-9a-f]{10}(_to_[a-z0-9_]+)?|(weiscadence|jiggy_cadence)(_to_[a-z0-9_]+)?", m.group(1)):
            hits += 1
            print(f"  data/numbers.json: login in ledger key: {key.split('.')[2]}.<login>.{m.group(2)}")
    print(f"privacy: {hits} hit(s)")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
