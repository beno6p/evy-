from dataclasses import asdict, dataclass
from typing import Optional

@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    message: str
    path: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Report:
    findings: list[Finding]

    @property
    def counts(self) -> dict[str, int]:
        return {level: sum(f.severity == level for f in self.findings) for level in ("pass", "warn", "error")}

    def to_dict(self) -> dict:
        return {"findings": [f.to_dict() for f in self.findings], "summary": self.counts}
