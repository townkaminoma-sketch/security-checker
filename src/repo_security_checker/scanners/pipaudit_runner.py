from __future__ import annotations

import json
import logging
import subprocess

from ..models import Finding
from .base import ScanResult

logger = logging.getLogger(__name__)


def scan_dependencies(target_dir: str = ".") -> ScanResult:
    """Run pip-audit to find vulnerable dependencies."""
    try:
        result = subprocess.run(
            ["pip-audit", "--format", "json"],
            capture_output=True,
            text=True,
            cwd=target_dir,
        )
        data = json.loads(result.stdout) if result.stdout.strip() else {}
    except FileNotFoundError:
        logger.warning("pip-audit is not installed; skipping dependency scan")
        return ScanResult(tool="pip-audit", findings=[])
    except json.JSONDecodeError:
        logger.warning("Failed to parse pip-audit JSON output")
        return ScanResult(tool="pip-audit", findings=[])

    findings: list[Finding] = []
    for dep in data.get("dependencies", []):
        dep_name = dep.get("name", "unknown")
        for vuln in dep.get("vulns", []):
            findings.append(
                Finding(
                    tool="pip-audit",
                    severity="high",
                    title=f"{dep_name} {vuln.get('id', 'unknown')}",
                    detail=vuln.get("description", "")[:500],
                    file=None,
                    line=None,
                )
            )

    return ScanResult(tool="pip-audit", findings=findings)
