from __future__ import annotations

import dataclasses
from datetime import datetime, timezone

SEVERITY_ORDER = ["critical", "high", "medium", "low", "info"]


@dataclasses.dataclass
class Finding:
    tool: str  # "gitleaks" | "pip-audit" | "bandit"
    severity: str  # one of SEVERITY_ORDER
    title: str
    detail: str
    file: str | None = None
    line: int | None = None


@dataclasses.dataclass
class SecurityReport:
    findings: list[Finding]
    scanned_at: str = dataclasses.field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def exit_code(self) -> int:
        """Return 1 if any finding is high or critical, else 0."""
        return 1 if any(f.severity in ("critical", "high") for f in self.findings) else 0
