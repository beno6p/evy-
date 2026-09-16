# Rule reference

| Rule | Severity | Meaning |
|---|---|---|
| OG-DOC-001 | error/pass | README documentation should exist |
| OG-LIC-001 | warn/pass | A license file should exist |
| OG-SEC-003 | warn/pass | A security policy is recommended |
| OG-DEP-001 | warn/pass | A dependency manifest is expected for dependency-based projects |
| OG-CI-001 | warn/pass | GitHub Actions CI is detected |
| OG-TEST-001 | warn/pass | A conventional test directory is detected |
| OG-SEC-001 | error | A high-confidence token-like assignment requires review |
| OG-SEC-002 | error | A private-key header requires review |
| OG-SEC-004 | pass | No high-confidence secret pattern was detected |

Findings are deliberately conservative. A match is not proof that a credential is valid or exposed. Never commit real secrets to test fixtures.
