"""Unit tests for repo_security_checker.models."""

from __future__ import annotations

from src.repo_security_checker.models import Finding, SecurityReport


class TestFinding:
    def test_creation_all_fields(self) -> None:
        f = Finding(
            tool="gitleaks",
            severity="high",
            title="Hardcoded secret",
            detail="AWS key found",
            file="src/config.py",
            line=42,
        )
        assert f.tool == "gitleaks"
        assert f.severity == "high"
        assert f.title == "Hardcoded secret"
        assert f.detail == "AWS key found"
        assert f.file == "src/config.py"
        assert f.line == 42

    def test_creation_optional_fields_none(self) -> None:
        f = Finding(
            tool="bandit",
            severity="medium",
            title="Insecure function",
            detail="Use of eval()",
        )
        assert f.file is None
        assert f.line is None


class TestSecurityReport:
    def test_exit_code_high(self) -> None:
        report = SecurityReport(
            findings=[
                Finding(tool="gitleaks", severity="high", title="t", detail="d"),
            ]
        )
        assert report.exit_code == 1

    def test_exit_code_critical(self) -> None:
        report = SecurityReport(
            findings=[
                Finding(tool="bandit", severity="critical", title="t", detail="d"),
            ]
        )
        assert report.exit_code == 1

    def test_exit_code_medium_low_info(self) -> None:
        report = SecurityReport(
            findings=[
                Finding(tool="pip-audit", severity="medium", title="t", detail="d"),
                Finding(tool="bandit", severity="low", title="t", detail="d"),
                Finding(tool="gitleaks", severity="info", title="t", detail="d"),
            ]
        )
        assert report.exit_code == 0

    def test_exit_code_no_findings(self) -> None:
        report = SecurityReport(findings=[])
        assert report.exit_code == 0
