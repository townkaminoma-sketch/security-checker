from __future__ import annotations

import dataclasses
import json
from pathlib import Path

from .models import SecurityReport


def write_report(report: SecurityReport, output_path: Path) -> None:
    data = dataclasses.asdict(report)
    data["exit_code"] = report.exit_code
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
