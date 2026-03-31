from __future__ import annotations

import json
from unittest.mock import patch, MagicMock

from src.repo_security_checker.scanners.bandit_runner import scan_code
from src.repo_security_checker.scanners.base import ScanResult


BANDIT_FIXTURE = {
    "results": [
        {
            "test_id": "B101",
            "test_name": "assert_used",
            "issue_text": "Use of assert detected.",
            "issue_severity": "LOW",
            "issue_confidence": "HIGH",
            "filename": "src/app.py",
            "line_number": 15,
        },
        {
            "test_id": "B105",
            "test_name": "hardcoded_password_string",
            "issue_text": "Possible hardcoded password.",
            "issue_severity": "HIGH",
            "issue_confidence": "MEDIUM",
            "filename": "src/config.py",
            "line_number": 8,
        },
    ]
}


class TestScanCodeParses:
    @patch("src.repo_security_checker.scanners.bandit_runner.subprocess.run")
    def test_scan_code_parses_findings(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout=json.dumps(BANDIT_FIXTURE),
            stderr="",
        )

        result = scan_code("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "bandit"
        assert len(result.findings) == 2

        f0 = result.findings[0]
        assert f0.tool == "bandit"
        assert f0.severity == "low"
        assert f0.title == "B101 assert_used"
        assert f0.detail == "Use of assert detected."
        assert f0.file == "src/app.py"
        assert f0.line == 15

        f1 = result.findings[1]
        assert f1.severity == "high"
        assert f1.title == "B105 hardcoded_password_string"
        assert f1.file == "src/config.py"
        assert f1.line == 8


class TestScanCodeNoIssues:
    @patch("src.repo_security_checker.scanners.bandit_runner.subprocess.run")
    def test_scan_code_no_issues(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"results": []}),
            stderr="",
        )

        result = scan_code("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "bandit"
        assert len(result.findings) == 0


class TestScanCodeToolNotFound:
    @patch("src.repo_security_checker.scanners.bandit_runner.subprocess.run")
    def test_scan_code_tool_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError("bandit not found")

        result = scan_code("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "bandit"
        assert len(result.findings) == 0
