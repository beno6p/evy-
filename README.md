# OpenSource Guardian

OpenSource Guardian is a local-first repository audit toolkit for open-source maintainers. It produces deterministic reports about documentation, testing, dependency manifests, common secret patterns, licensing, and GitHub Actions hygiene.

The project runs locally and does not require GitHub credentials or upload repository contents.

## Features

- Human-readable and JSON reports
- Documentation and maintainer-readiness checks
- Test and CI discovery
- Dependency manifest discovery
- Conservative secret-pattern scanning
- License and security-policy checks
- GitHub Actions workflow checks
- CI-friendly exit codes
- Python 3.10+ with a small runtime footprint

## Quick start

```bash
python -m pip install -e '.[dev]'
opensource-guardian .
opensource-guardian . --format json
opensource-guardian . --fail-on error
pytest -q
```

## Design principles

1. Local first: repository contents stay on the machine running the tool.
2. Conservative findings: suspicious patterns are reported as findings, not declared secrets.
3. Reproducible output: JSON is stable enough for CI and downstream tooling.
4. Explainable checks: findings include a rule ID, severity, message, and path when applicable.
5. Open-source friendly: contribution guidance, security reporting, tests, and CI are included.

## Roadmap

- Pluggable rule packs
- SARIF output for code-scanning workflows
- SPDX-aware license expression checks
- Dependency lockfile consistency checks
- Configurable policy files for organizations

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/rules.md](docs/rules.md).

## License

MIT. See [LICENSE](LICENSE).
