from __future__ import annotations

from src.repo_security_checker.scanners.bandit_runner import scan_code
from src.repo_security_checker.scanners.base import ScanResult


class TestScanCode:
    def test_scan_code_returns_empty(self):
        result = scan_code("/fake/dir")

        assert isinstance(result, ScanResult)
        assert result.tool == "bandit"
        assert len(result.findings) == 0
