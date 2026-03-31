from __future__ import annotations

import json
from unittest.mock import patch, MagicMock

from src.repo_security_checker.scanners.gitleaks_runner import scan_secrets
from src.repo_security_checker.scanners.base import ScanResult


GITLEAKS_FIXTURE = [
    {
        "Description": "AWS Access Key",
        "File": "config.py",
        "StartLine": 10,
        "Match": "AKIA...redacted",
    },
    {
        "Description": "Generic API Key",
        "File": "src/app.py",
        "StartLine": 25,
        "Match": "api_key=abc123",
    },
]


class TestScanSecretsParses:
    @patch("src.repo_security_checker.scanners.gitleaks_runner.subprocess.run")
    @patch("src.repo_security_checker.scanners.gitleaks_runner.Path")
    @patch("src.repo_security_checker.scanners.gitleaks_runner.tempfile.NamedTemporaryFile")
    def test_scan_secrets_parses_findings(
        self, mock_tmpfile, mock_path_cls, mock_run
    ):
        # Set up temp file mock
        tmp_ctx = MagicMock()
        tmp_ctx.__enter__ = MagicMock(return_value=MagicMock(name="tmp_report.json"))
        tmp_ctx.__enter__.return_value.name = "tmp_report.json"
        tmp_ctx.__exit__ = MagicMock(return_value=False)
        mock_tmpfile.return_value = tmp_ctx

        # gitleaks exit code 1 means leaks found
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")

        # Path(...).read_text() returns fixture JSON
        mock_path_instance = MagicMock()
        mock_path_instance.read_text.return_value = json.dumps(GITLEAKS_FIXTURE)
        mock_path_instance.unlink = MagicMock()
        mock_path_cls.return_value = mock_path_instance

        result = scan_secrets("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "gitleaks"
        assert len(result.findings) == 2

        f0 = result.findings[0]
        assert f0.tool == "gitleaks"
        assert f0.severity == "high"
        assert f0.title == "AWS Access Key"
        assert f0.file == "config.py"
        assert f0.line == 10

        f1 = result.findings[1]
        assert f1.title == "Generic API Key"
        assert f1.file == "src/app.py"
        assert f1.line == 25


class TestScanSecretsNoLeaks:
    @patch("src.repo_security_checker.scanners.gitleaks_runner.subprocess.run")
    @patch("src.repo_security_checker.scanners.gitleaks_runner.Path")
    @patch("src.repo_security_checker.scanners.gitleaks_runner.tempfile.NamedTemporaryFile")
    def test_scan_secrets_no_leaks(self, mock_tmpfile, mock_path_cls, mock_run):
        tmp_ctx = MagicMock()
        tmp_ctx.__enter__ = MagicMock(return_value=MagicMock(name="tmp.json"))
        tmp_ctx.__enter__.return_value.name = "tmp.json"
        tmp_ctx.__exit__ = MagicMock(return_value=False)
        mock_tmpfile.return_value = tmp_ctx

        # Exit code 0 = no leaks
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        mock_path_instance = MagicMock()
        mock_path_instance.unlink = MagicMock()
        mock_path_cls.return_value = mock_path_instance

        result = scan_secrets("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "gitleaks"
        assert len(result.findings) == 0


class TestScanSecretsToolNotFound:
    @patch("src.repo_security_checker.scanners.gitleaks_runner.tempfile.NamedTemporaryFile")
    @patch("src.repo_security_checker.scanners.gitleaks_runner.subprocess.run")
    def test_scan_secrets_tool_not_found(self, mock_run, mock_tmpfile):
        tmp_ctx = MagicMock()
        tmp_ctx.__enter__ = MagicMock(return_value=MagicMock(name="tmp.json"))
        tmp_ctx.__enter__.return_value.name = "tmp.json"
        tmp_ctx.__exit__ = MagicMock(return_value=False)
        mock_tmpfile.return_value = tmp_ctx

        mock_run.side_effect = FileNotFoundError("gitleaks not found")

        result = scan_secrets("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "gitleaks"
        assert len(result.findings) == 0
