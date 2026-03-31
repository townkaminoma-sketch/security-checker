from __future__ import annotations

import json
import logging
import subprocess

from ..models import Finding
from .base import ScanResult

logger = logging.getLogger(__name__)

SEVERITY_MAP = {
    "HIGH": "high",
    "MEDIUM": "medium",
    "LOW": "low",
}


def scan_code(target_dir: str = ".") -> ScanResult:
    """Run bandit to scan Python code for security issues."""
    try:
        result = subprocess.run(
            [
                "bandit", "-r", target_dir, "-f", "json", "-q",
                "--exclude", ".venv,.tox,node_modules,.git",
            ],
            capture_output=True,
            text=True,
        )
        if not result.stdout.strip():
            if result.stderr.strip():
                logger.warning("bandit produced no JSON output: %s", result.stderr.strip()[:200])
            return ScanResult(tool="bandit", findings=[])
        data = json.loads(result.stdout)
    except FileNotFoundError:
        logger.warning("bandit is not installed; skipping code scan")
        return ScanResult(tool="bandit", findings=[])
    except json.JSONDecodeError:
        logger.warning("Failed to parse bandit JSON output")
        return ScanResult(tool="bandit", findings=[])

    findings: list[Finding] = []
    for item in data.get("results", []):
        findings.append(
            Finding(
                tool="bandit",
                severity=SEVERITY_MAP.get(item.get("issue_severity", ""), "info"),
                title=f"{item.get('test_id', '')} {item.get('test_name', '')}".strip(),
                detail=item.get("issue_text", ""),
                file=item.get("filename"),
                line=item.get("line_number"),
            )
        )

    return ScanResult(tool="bandit", findings=findings)
