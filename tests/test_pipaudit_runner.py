from __future__ import annotations

import json
from unittest.mock import patch, MagicMock

from src.repo_security_checker.scanners.pipaudit_runner import scan_dependencies
from src.repo_security_checker.scanners.base import ScanResult


PIPAUDIT_FIXTURE = {
    "dependencies": [
        {
            "name": "requests",
            "version": "2.25.0",
            "vulns": [
                {
                    "id": "PYSEC-2023-001",
                    "description": "SSRF vulnerability",
                    "fix_versions": ["2.31.0"],
                }
            ],
        }
    ]
}


class TestScanDependenciesParses:
    @patch("src.repo_security_checker.scanners.pipaudit_runner.subprocess.run")
    def test_scan_dependencies_parses_vulns(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(PIPAUDIT_FIXTURE),
            stderr="",
        )

        result = scan_dependencies("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "pip-audit"
        assert len(result.findings) == 1

        f0 = result.findings[0]
        assert f0.tool == "pip-audit"
        assert f0.severity == "high"
        assert f0.title == "requests PYSEC-2023-001"
        assert f0.detail == "SSRF vulnerability"
        assert f0.file is None
        assert f0.line is None


class TestScanDependenciesNoVulns:
    @patch("src.repo_security_checker.scanners.pipaudit_runner.subprocess.run")
    def test_scan_dependencies_no_vulns(self, mock_run):
        no_vulns = {"dependencies": [{"name": "requests", "version": "2.31.0", "vulns": []}]}
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(no_vulns),
            stderr="",
        )

        result = scan_dependencies("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "pip-audit"
        assert len(result.findings) == 0


class TestScanDependenciesToolNotFound:
    @patch("src.repo_security_checker.scanners.pipaudit_runner.subprocess.run")
    def test_scan_dependencies_tool_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError("pip-audit not found")

        result = scan_dependencies("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "pip-audit"
        assert len(result.findings) == 0
