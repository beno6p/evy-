# Contributing

Contributions are welcome. Please keep pull requests focused and explain the user-facing or maintainer-facing problem they solve.

## Development

```bash
python -m pip install -e '.[dev]'
pytest -q
```

For a new rule, include tests covering both the expected positive case and an important false-positive case where practical. Avoid sending repository contents to external services.

## Pull requests

Use a descriptive title, include tests for behavior changes, and update documentation when the CLI or rule set changes.
