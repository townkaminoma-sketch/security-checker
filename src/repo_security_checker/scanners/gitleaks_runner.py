from __future__ import annotations

import json
import logging
import subprocess
import tempfile
from pathlib import Path

from ..models import Finding
from .base import ScanResult

logger = logging.getLogger(__name__)


def scan_secrets(target_dir: str = ".") -> ScanResult:
    """Run gitleaks to detect secrets in the target directory."""
    try:
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".json", delete=False
        ) as tmp:
            tmp_path = tmp.name

        result = subprocess.run(
            [
                "gitleaks",
                "detect",
                "--source",
                target_dir,
                "--report-format",
                "json",
                "--report-path",
                tmp_path,
                "--no-banner",
            ],
            capture_output=True,
            text=True,
        )

        # Exit code 0 means no leaks found
        if result.returncode == 0:
            Path(tmp_path).unlink(missing_ok=True)
            return ScanResult(tool="gitleaks", findings=[])

        try:
            raw = Path(tmp_path).read_text(encoding="utf-8")
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        items = json.loads(raw) if raw.strip() else []

    except FileNotFoundError:
        logger.warning("gitleaks is not installed; skipping secret scan")
        return ScanResult(tool="gitleaks", findings=[])
    except json.JSONDecodeError:
        logger.warning("Failed to parse gitleaks JSON output")
        return ScanResult(tool="gitleaks", findings=[])

    findings: list[Finding] = []
    for item in items:
        findings.append(
            Finding(
                tool="gitleaks",
                severity="high",
                title=item.get("Description", "Secret detected"),
                detail=item.get("Match", "")[:200],
                file=item.get("File"),
                line=item.get("StartLine"),
            )
        )

    return ScanResult(tool="gitleaks", findings=findings)
