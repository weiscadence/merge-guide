"""Check context: changed files, added lines, new declarations, profile, PR body, index."""
import os, re, subprocess
from . import lean

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def added_lines(patch):
    """Set of 1-based new-file line numbers added by a unified-diff patch, plus hunk list."""
    added, hunks, cur = set(), [], None
    ln = 0
    for line in (patch or "").splitlines():
        m = HUNK_RE.match(line)
        if m:
            ln = int(m.group(3)); cur = dict(start=ln, added=[], removed=[]); hunks.append(cur); continue
        if cur is None:
            continue
        if line.startswith("+") and not line.startswith("+++"):
            added.add(ln); cur["added"].append(line[1:]); ln += 1
        elif line.startswith("-") and not line.startswith("---"):
            cur["removed"].append(line[1:])
        else:
            ln += 1
    return added, hunks


class File:
    def __init__(self, name, status, patch, text, base_text=None):
        self.name, self.status, self.patch, self.text = name, status, patch or "", text or ""
        self.base_text = base_text
        self.added, self.hunks = added_lines(self.patch)
        if status == "added" and not self.added and self.text:
            self.added = set(range(1, self.text.count("\n") + 2))
        self.is_lean = name.endswith(".lean")
        self.decls = lean.parse_decls(self.text, name) if self.is_lean else []
        self.lines = self.text.splitlines()

    def new_decls(self):
        """Declarations whose header line is added (new or rewritten statements)."""
        return [d for d in self.decls if d["line"] in self.added and d["full"]]


class Context:
    def __init__(self, repo, profile, files, pr_body=None, repo_dir=None, index=None, title=None):
        self.repo, self.profile, self.files = repo, profile, files
        self.pr_body, self.title = pr_body, title
        self.repo_dir, self.index = repo_dir, index
        self.changed_names = {f.name for f in files}
        self.exclude_files = set()  # validation: library files that did not exist yet
        self.row_ok = None        # validation: drop index rows that did not exist yet
        self.tree_ref = None      # git ref whose tree is "the repo before this PR"
        self._tree = None
        self.by_name = {f.name: f for f in files}

    def tree(self):
        """Paths in the repo at tree_ref (or the working tree), plus the PR's added files."""
        if self._tree is None:
            paths = set()
            if self.repo_dir:
                ref = self.tree_ref or "HEAD"
                out = subprocess.run(["git", "-C", self.repo_dir, "ls-tree", "-r", "--name-only", ref],
                                     capture_output=True, text=True).stdout
                paths = set(out.split())
            paths |= {f.name for f in self.files if f.status != "removed"}
            paths -= {f.name for f in self.files if f.status == "removed"}
            self._tree = paths
        return self._tree

    def lean_files(self):
        return [f for f in self.files if f.is_lean]

    def read_repo_file(self, rel):
        """Read a file from the working tree or Mathlib package (for import graphs)."""
        if rel in self.by_name and self.by_name[rel].text:
            return self.by_name[rel].text
        if not self.repo_dir:
            return None
        if self.tree_ref and not rel.startswith("Mathlib/"):
            r = subprocess.run(["git", "-C", self.repo_dir, "show", f"{self.tree_ref}:{rel}"], capture_output=True, text=True)
            if r.returncode == 0:
                return r.stdout
        for base in (self.repo_dir, os.path.join(self.repo_dir, ".lake/packages/mathlib")):
            p = os.path.join(base, rel)
            if os.path.exists(p):
                try:
                    return open(p, encoding="utf-8", errors="replace").read()
                except OSError:
                    return None
        return None


def from_git(repo_dir, base, profile, pr_body=None, index=None, title=None):
    def git(*a):
        return subprocess.run(["git", "-C", repo_dir, *a], capture_output=True, text=True).stdout
    mb = git("merge-base", base, "HEAD").strip() or base
    files = []
    for line in git("diff", "--name-status", "-M", mb, "HEAD").splitlines():
        parts = line.split("\t")
        st, name = parts[0], parts[-1]
        status = {"A": "added", "D": "removed", "M": "modified"}.get(st[0], "renamed" if st[0] == "R" else "modified")
        if status == "removed":
            files.append(File(name, status, "", "")); continue
        patch = git("diff", "-U0", mb, "HEAD", "--", name)
        text = git("show", f"HEAD:{name}")
        base_text = git("show", f"{mb}:{name}") if status != "added" else None
        files.append(File(name, status, patch, text, base_text))
    c = Context(profile.get("repo"), profile, files, pr_body, repo_dir, index, title)
    c.tree_ref = mb
    return c


def from_ctx_json(c, profile, pr_body=None, index=None, repo_dir=None, title=None):
    """Build from a rubric-prereview v2 ctx/<pr>.json (validation path)."""
    files = [File(f["name"], f["status"], f.get("patch"), f.get("full") or "") for f in c["files"]]
    return Context(profile.get("repo"), profile, files, pr_body, repo_dir, index, title)


def finding(check, rubric, file, line, msg, severity="ask", decl=None, heuristic=False, evidence=None):
    return dict(check=check, rubric=rubric, file=file, line=line, decl=decl, msg=msg,
                severity=severity, heuristic=heuristic, evidence=evidence or [])
