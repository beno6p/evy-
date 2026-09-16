from pathlib import Path

from opensource_guardian.rules import audit_repository


def test_healthy_repo_has_documentation_license_and_tests(tmp_path: Path):
    (tmp_path / ".git").mkdir()
    (tmp_path / "README.md").write_text("# Demo\n")
    (tmp_path / "LICENSE").write_text("MIT\n")
    (tmp_path / "SECURITY.md").write_text("Report issues privately.\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n")
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: CI\n")
    findings = audit_repository(tmp_path)
    assert all(f.severity != "error" for f in findings)


def test_private_key_is_reported(tmp_path: Path):
    (tmp_path / ".git").mkdir()
    (tmp_path / "README.md").write_text("# Demo\n")
    (tmp_path / "example.txt").write_text("-----BEGIN PRIVATE KEY-----\n")
    findings = audit_repository(tmp_path)
    assert any(f.rule_id == "OG-SEC-002" and f.severity == "error" for f in findings)
