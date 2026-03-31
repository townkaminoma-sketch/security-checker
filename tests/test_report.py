"""Unit tests for repo_security_checker.report."""

from __future__ import annotations

import json
from pathlib import Path

from src.repo_security_checker.models import Finding, SecurityReport
from src.repo_security_checker.report import write_report


class TestWriteReport:
    def test_creates_json_file(self, tmp_path: Path) -> None:
        report = SecurityReport(findings=[])
        out = tmp_path / "report.json"
        write_report(report, out)
        assert out.exists()

    def test_json_structure(self, tmp_path: Path) -> None:
        report = SecurityReport(
            findings=[
                Finding(tool="gitleaks", severity="high", title="t", detail="d"),
            ]
        )
        out = tmp_path / "report.json"
        write_report(report, out)
        data = json.loads(out.read_text())
        assert "findings" in data
        assert "scanned_at" in data
        assert "exit_code" in data
        assert isinstance(data["findings"], list)
        assert len(data["findings"]) == 1

    def test_exit_code_matches(self, tmp_path: Path) -> None:
        report = SecurityReport(
            findings=[
                Finding(tool="bandit", severity="critical", title="t", detail="d"),
            ]
        )
        out = tmp_path / "report.json"
        write_report(report, out)
        data = json.loads(out.read_text())
        assert data["exit_code"] == report.exit_code
        assert data["exit_code"] == 1

    def test_findings_serialized(self, tmp_path: Path) -> None:
        report = SecurityReport(
            findings=[
                Finding(
                    tool="pip-audit",
                    severity="medium",
                    title="Vuln",
                    detail="CVE-123",
                    file="requirements.txt",
                    line=5,
                ),
            ]
        )
        out = tmp_path / "report.json"
        write_report(report, out)
        data = json.loads(out.read_text())
        f = data["findings"][0]
        assert f["tool"] == "pip-audit"
        assert f["severity"] == "medium"
        assert f["title"] == "Vuln"
        assert f["detail"] == "CVE-123"
        assert f["file"] == "requirements.txt"
        assert f["line"] == 5
