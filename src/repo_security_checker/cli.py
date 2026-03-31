from __future__ import annotations

import sys
from pathlib import Path

import click

from .models import SecurityReport
from .report import write_report
from .scanners import scan_code, scan_dependencies, scan_secrets


@click.group()
def main() -> None:
    """repo-security-checker: aggregate security scanning tool."""


@main.command()
@click.option("--target-dir", default=".", help="Directory to scan")
@click.option("--output", default="security-report.json", help="Output report path")
def scan(target_dir: str, output: str) -> None:
    """Run all security scanners and generate a report."""
    click.echo(f"Scanning {target_dir} ...")

    secrets = scan_secrets(target_dir)
    deps = scan_dependencies(target_dir)
    code = scan_code(target_dir)

    all_findings = secrets.findings + deps.findings + code.findings

    report = SecurityReport(findings=all_findings)
    output_path = Path(output)
    write_report(report, output_path)

    click.echo(f"Report written to {output_path}")
    click.echo(f"Findings: {len(all_findings)} total")

    if report.exit_code != 0:
        click.echo("FAIL: high/critical findings detected", err=True)
        sys.exit(1)
    else:
        click.echo("PASS: no high/critical findings")
