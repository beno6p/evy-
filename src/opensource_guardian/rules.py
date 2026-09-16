from pathlib import Path
import re

from .models import Finding

SECRET_PATTERNS = {
    "OG-SEC-001": re.compile(r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*[\"'][A-Za-z0-9_\-]{20,}[\"']"),
    "OG-SEC-002": re.compile(r"(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def _exists(root: Path, *names: str) -> bool:
    return any((root / n).exists() for n in names)


def audit_repository(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    if _exists(root, "README.md", "README.rst", "README.txt"):
        findings.append(Finding("OG-DOC-001", "pass", "README documentation detected"))
    else:
        findings.append(Finding("OG-DOC-001", "error", "README documentation is missing", "README.md"))

    if _exists(root, "LICENSE", "LICENSE.md", "LICENSE.txt"):
        findings.append(Finding("OG-LIC-001", "pass", "License file detected"))
    else:
        findings.append(Finding("OG-LIC-001", "warn", "License file is missing", "LICENSE"))

    if _exists(root, "SECURITY.md", ".github/SECURITY.md"):
        findings.append(Finding("OG-SEC-003", "pass", "Security policy detected"))
    else:
        findings.append(Finding("OG-SEC-003", "warn", "SECURITY.md is missing", "SECURITY.md"))

    manifests = ("pyproject.toml", "package.json", "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "requirements.txt")
    if _exists(root, *manifests):
        findings.append(Finding("OG-DEP-001", "pass", "Dependency manifest detected"))
    else:
        findings.append(Finding("OG-DEP-001", "warn", "No common dependency manifest detected"))

    workflow_dir = root / ".github" / "workflows"
    if workflow_dir.is_dir() and any(workflow_dir.glob("*.y*ml")):
        findings.append(Finding("OG-CI-001", "pass", "GitHub Actions workflow detected", ".github/workflows"))
    else:
        findings.append(Finding("OG-CI-001", "warn", "No GitHub Actions workflow detected", ".github/workflows"))

    test_markers = ("tests", "test", "spec")
    if any((root / marker).exists() for marker in test_markers):
        findings.append(Finding("OG-TEST-001", "pass", "Test directory detected"))
    else:
        findings.append(Finding("OG-TEST-001", "warn", "No conventional test directory detected"))

    candidates = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or any(p.startswith(".") for p in path.parts if p != "."):
            continue
        if path.stat().st_size > 1_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for rule_id, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                candidates.append(Finding(rule_id, "error", "Potential secret pattern detected; review manually", str(path.relative_to(root))))

    findings.extend(candidates or [Finding("OG-SEC-004", "pass", "No high-confidence secret patterns detected")])
    return findings
