from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .models import Report
from .rules import audit_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit an open-source repository locally.")
    parser.add_argument("repo", nargs="?", default=".", help="Repository path")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--fail-on", choices=("warn", "error"), default=None, help="Return exit code 1 at this severity or above")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def render_text(report: Report, repo: Path) -> str:
    lines = [f"OpenSource Guardian {__version__}", f"Repository: {repo}", ""]
    for finding in report.findings:
        label = finding.severity.upper()
        location = f" [{finding.path}]" if finding.path else ""
        lines.append(f"{finding.rule_id:<12} {label:<5} {finding.message}{location}")
    c = report.counts
    lines.extend(["", f"Summary: {c['pass']} passed, {c['warn']} warnings, {c['error']} errors"])
    return "\n".join(lines)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo = Path(args.repo).expanduser().resolve()
    if not (repo / ".git").is_dir():
        parser.error(f"not a Git repository: {repo}")
    report = Report(audit_repository(repo))
    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(render_text(report, repo))
    if args.fail_on == "error" and report.counts["error"]:
        return 1
    if args.fail_on == "warn" and (report.counts["error"] or report.counts["warn"]):
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
