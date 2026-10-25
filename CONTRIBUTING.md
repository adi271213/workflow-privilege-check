# Contributing

Thanks for your interest. This is a small, deterministic tool; contributions that
keep it focused, well-tested, and honest about its limits are very welcome.

## Development

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
python scripts/validate.py        # full suite (synthetic acceptance + integration)
python -m unittest discover -s tests
```

CI runs the suite on Python 3.11–3.14 for every pull request.

## Guidelines

- **Scope:** the tool reports the base→head *privilege delta* in GitHub Actions
  config (triggers, token scopes, secret references, runners and environments). It is not a general linter —
  broad static checks belong in tools like zizmor.
- **Determinism:** no network or code execution during analysis; same input, same
  output. Keep it that way.
- **Honesty:** a finding is a review prompt, not a vulnerability claim. Don't let
  messages overstate what is verified.
- **Tests first:** every rule or parser change needs a regression test. Add cases
  to `tests/` (see `tests/cases.json`).

## Reporting security issues

See [SECURITY.md](SECURITY.md). Please do not open public issues for vulnerabilities.

See VALIDATION.md for offline Action tests and benchmarks/README.md for the
hash-pinned historical replay. Runtime dependency updates must preserve vendor
provenance, license and disconnected-network validation.
