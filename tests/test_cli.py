from pathlib import Path

from opensource_guardian.cli import render_text
from opensource_guardian.models import Finding, Report


def test_text_output_contains_summary(tmp_path: Path):
    report = Report([Finding("OG-TEST-001", "pass", "Test directory detected")])
    output = render_text(report, tmp_path)
    assert "OpenSource Guardian" in output
    assert "Summary:" in output
    assert "1 passed" in output
