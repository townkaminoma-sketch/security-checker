from __future__ import annotations

from unittest.mock import patch

from click.testing import CliRunner

from src.repo_security_checker.cli import main
from src.repo_security_checker.models import Finding
from src.repo_security_checker.scanners.base import ScanResult


class TestCliScan:
    def _empty_result(self, tool: str) -> ScanResult:
        return ScanResult(tool=tool, findings=[])

    @patch("src.repo_security_checker.cli.scan_code")
    @patch("src.repo_security_checker.cli.scan_dependencies")
    @patch("src.repo_security_checker.cli.scan_secrets")
    def test_scan_no_findings(self, mock_secrets, mock_deps, mock_code, tmp_path):
        mock_secrets.return_value = self._empty_result("gitleaks")
        mock_deps.return_value = self._empty_result("pip-audit")
        mock_code.return_value = self._empty_result("bandit")

        out_file = tmp_path / "report.json"
        runner = CliRunner()
        result = runner.invoke(main, ["scan", "--output", str(out_file)])

        assert result.exit_code == 0
        assert "PASS" in result.output
        assert out_file.exists()

    @patch("src.repo_security_checker.cli.scan_code")
    @patch("src.repo_security_checker.cli.scan_dependencies")
    @patch("src.repo_security_checker.cli.scan_secrets")
    def test_scan_high_finding_exits_1(self, mock_secrets, mock_deps, mock_code, tmp_path):
        mock_secrets.return_value = ScanResult(
            tool="gitleaks",
            findings=[Finding(tool="gitleaks", severity="high", title="Leak", detail="d")],
        )
        mock_deps.return_value = self._empty_result("pip-audit")
        mock_code.return_value = self._empty_result("bandit")

        out_file = tmp_path / "report.json"
        runner = CliRunner()
        result = runner.invoke(main, ["scan", "--output", str(out_file)])

        assert result.exit_code == 1
        assert "FAIL" in result.output

    @patch("src.repo_security_checker.cli.scan_code")
    @patch("src.repo_security_checker.cli.scan_dependencies")
    @patch("src.repo_security_checker.cli.scan_secrets")
    def test_scan_custom_target_dir(self, mock_secrets, mock_deps, mock_code, tmp_path):
        mock_secrets.return_value = self._empty_result("gitleaks")
        mock_deps.return_value = self._empty_result("pip-audit")
        mock_code.return_value = self._empty_result("bandit")

        out_file = tmp_path / "report.json"
        runner = CliRunner()
        result = runner.invoke(
            main, ["scan", "--target-dir", "/some/path", "--output", str(out_file)]
        )

        assert result.exit_code == 0
        mock_secrets.assert_called_once_with("/some/path")

    @patch("src.repo_security_checker.cli.scan_code")
    @patch("src.repo_security_checker.cli.scan_dependencies")
    @patch("src.repo_security_checker.cli.scan_secrets")
    def test_scan_aggregates_all_findings(self, mock_secrets, mock_deps, mock_code, tmp_path):
        mock_secrets.return_value = ScanResult(
            tool="gitleaks",
            findings=[Finding(tool="gitleaks", severity="medium", title="t1", detail="d")],
        )
        mock_deps.return_value = ScanResult(
            tool="pip-audit",
            findings=[Finding(tool="pip-audit", severity="low", title="t2", detail="d")],
        )
        mock_code.return_value = self._empty_result("bandit")

        out_file = tmp_path / "report.json"
        runner = CliRunner()
        result = runner.invoke(main, ["scan", "--output", str(out_file)])

        assert result.exit_code == 0
        assert "2 total" in result.output
