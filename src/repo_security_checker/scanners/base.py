from __future__ import annotations

import dataclasses

from ..models import Finding


@dataclasses.dataclass
class ScanResult:
    tool: str
    findings: list[Finding]
