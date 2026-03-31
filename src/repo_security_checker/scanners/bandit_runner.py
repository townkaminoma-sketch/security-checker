from __future__ import annotations

import logging

from .base import ScanResult

logger = logging.getLogger(__name__)


def scan_code(target_dir: str = ".") -> ScanResult:
    """Run bandit to scan code for security issues (stub)."""
    logger.info("bandit scan is not yet implemented (stub)")
    return ScanResult(tool="bandit", findings=[])
