"""Unit tests for scripts/check_pr_invariants.py (loaded by path)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
_SCRIPT = _ROOT / "scripts" / "check_pr_invariants.py"


@pytest.fixture(scope="module")
def cpi():
    spec = importlib.util.spec_from_file_location("check_pr_invariants", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("[docs-only] add guide", "docs-only"),
        ("  [WORKFLOW-only] ci", "workflow-only"),
        ("[config-only] bump", "config-only"),
        ("chore: no tag", None),
        ("docs-only] missing bracket", None),
    ],
)
def test_parse_tag(cpi, title, expected):
    assert cpi.parse_tag(title) == expected


def test_outputs_violations(cpi):
    assert cpi.outputs_violations(["docs/a.md", "src/x.py"]) == []
    assert cpi.outputs_violations(["outputs/x.csv"]) == ["outputs/x.csv"]
    assert cpi.outputs_violations(["outputs"]) == ["outputs"]


def test_docs_only_violations(cpi):
    assert cpi.docs_only_violations(["docs/a.md"]) == []
    assert cpi.docs_only_violations(["docs/a.md", "README.md"]) == ["README.md"]


def test_workflow_only_violations(cpi):
    assert cpi.workflow_only_violations([".github/workflows/ci.yml"]) == []
    assert cpi.workflow_only_violations([".github/workflows/ci.yml", "src/x.py"]) == ["src/x.py"]


def test_config_only_violations(cpi):
    assert cpi.config_only_violations(["pyproject.toml"]) == []
    assert cpi.config_only_violations(["pyproject.toml", "src/x.py"]) == ["src/x.py"]


def test_draft_issue_doc_violations(cpi):
    assert cpi.draft_issue_doc_violations(["docs/guide.md"]) == []
    assert cpi.draft_issue_doc_violations(["docs/draft_issue_editorconfig.md"]) == [
        "docs/draft_issue_editorconfig.md",
    ]
    assert cpi.draft_issue_doc_violations(["docs/draft_issue_x.txt"]) == []
