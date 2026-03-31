"""Opt-in PR path checks for tagged checkpoint titles (pull_request CI only).

Title prefix (leading whitespace allowed, case-insensitive):
  [docs-only]      -> only paths under docs/
  [workflow-only]  -> only under .github/workflows/
  [config-only]    -> only known config-like root files (see CONFIG_ONLY_FILES)

Always: block changes under top-level outputs/ (generated artifacts).
Always: block adds/changes to docs/draft_issue_*.md (local draft-issue scaffolding; see docs/checkpoint_machine_check_items.md).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys


TAG_PATTERN = re.compile(
    r"^\s*\[(docs-only|workflow-only|config-only)\]",
    re.IGNORECASE,
)

# Extend only when a new "config-only" checkpoint explicitly needs it.
CONFIG_ONLY_FILES: frozenset[str] = frozenset(
    {
        ".editorconfig",
        ".pre-commit-config.yaml",
        ".python-version",
        "pyproject.toml",
        "uv.lock",
        "ruff.toml",
        "pytest.ini",
        ".codex/config.toml",
    }
)


def parse_tag(title: str) -> str | None:
    m = TAG_PATTERN.match(title.strip() if title else "")
    if not m:
        return None
    return m.group(1).lower()


def git_changed_files(base_sha: str, head_sha: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{base_sha}...{head_sha}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("[invariants] git diff failed:", proc.stderr.strip(), file=sys.stderr)
        sys.exit(1)
    lines = [ln.strip().replace("\\", "/") for ln in proc.stdout.splitlines() if ln.strip()]
    return lines


def outputs_violations(paths: list[str]) -> list[str]:
    bad: list[str] = []
    for p in paths:
        if p == "outputs" or p.startswith("outputs/"):
            bad.append(p)
    return bad


def draft_issue_doc_violations(paths: list[str]) -> list[str]:
    """Paths under docs/ that look like draft issue scratch files (keep out of PRs)."""
    bad: list[str] = []
    for p in paths:
        if p.startswith("docs/draft_issue_") and p.endswith(".md"):
            bad.append(p)
    return bad


def docs_only_violations(paths: list[str]) -> list[str]:
    return [p for p in paths if not p.startswith("docs/")]


def workflow_only_violations(paths: list[str]) -> list[str]:
    prefix = ".github/workflows/"
    return [p for p in paths if not p.startswith(prefix)]


def config_only_violations(paths: list[str]) -> list[str]:
    return [p for p in paths if p not in CONFIG_ONLY_FILES]


def main() -> None:
    title = os.environ.get("PR_TITLE", "")
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")

    if not base or not head:
        print("[invariants] skip: BASE_SHA/HEAD_SHA unset (not a PR CI run)")
        sys.exit(0)

    tag = parse_tag(title)
    paths = git_changed_files(base, head)

    violations: list[tuple[str, list[str]]] = []

    out_bad = outputs_violations(paths)
    if out_bad:
        violations.append(
            (
                "Changes touch top-level outputs/ (generated artifacts; keep out of PRs):\n"
                + "\n".join(f"  - {p}" for p in out_bad),
                out_bad,
            )
        )

    draft_bad = draft_issue_doc_violations(paths)
    if draft_bad:
        violations.append(
            (
                "Changes include docs/draft_issue_*.md (local draft-issue scaffolding; keep out of PRs):\n"
                + "\n".join(f"  - {p}" for p in draft_bad)
                + "\n\nSee docs/checkpoint_machine_check_items.md (item 2).",
                draft_bad,
            )
        )

    if tag == "docs-only":
        d_bad = docs_only_violations(paths)
        if d_bad:
            violations.append(
                (
                    "PR title has [docs-only] but non-docs paths changed:\n"
                    + "\n".join(f"  - {p}" for p in d_bad),
                    d_bad,
                ),
            )
    elif tag == "workflow-only":
        w_bad = workflow_only_violations(paths)
        if w_bad:
            violations.append(
                (
                    "PR title has [workflow-only] but paths outside .github/workflows/ changed:\n"
                    + "\n".join(f"  - {p}" for p in w_bad),
                    w_bad,
                ),
            )
    elif tag == "config-only":
        c_bad = config_only_violations(paths)
        if c_bad:
            violations.append(
                (
                    "PR title has [config-only] but paths outside the allow-list changed:\n"
                    + "\n".join(f"  - {p}" for p in c_bad)
                    + "\n\nAllow-list (extend in scripts/check_pr_invariants.py if needed):\n"
                    + "\n".join(f"  - {p}" for p in sorted(CONFIG_ONLY_FILES)),
                    c_bad,
                ),
            )

    if violations:
        print("[invariants] FAILED", file=sys.stderr)
        for msg, _ in violations:
            print(msg, file=sys.stderr)
            print(file=sys.stderr)
        sys.exit(1)

    if tag:
        print(f"[invariants] OK (tag={tag}, {len(paths)} paths checked)")
    else:
        print("[invariants] OK (no opt-in tag; only outputs/ guard ran)")


if __name__ == "__main__":
    main()
