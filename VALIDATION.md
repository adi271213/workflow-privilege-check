# Validation and limits

Three different checks answer different questions:

1. `python scripts/validate.py` runs synthetic acceptance, parser, source-reader,
   rule, CLI and Action-controller tests. It writes ignored
   `validation-results.json` with runtime versions and source hashes. It performs
   no hosted Action run or public-PR benchmark.
2. CI runs that suite on Python 3.11–3.14, plus
   `python scripts/offline_smoke.py --network-namespace`. The latter runs the
   actual controller as an unprivileged process in a disconnected Linux network
   namespace, in both modes, against local Git fixtures. It validates outputs and
   token/runner/environment findings without pip or external site packages in
   the controller. `python scripts/offline_smoke.py` provides a local smoke test
   without the Linux-only isolation assertion.
3. [The 74-PR replay](benchmarks/README.md) verifies frozen public workflow hashes
   and exact legacy configured facts. It is selected, correlated and self-labeled,
   and not a production accuracy measurement. New context findings are separate.

A hosted consumer test additionally exercises the public pinned composite Action,
trusted-base checkout, exact head fetch and result interpretation. The published
0.0.0 setup is selected only after candidate consumer tests, both mode contracts
and CI pass. Current run links are retained in [release verification notes](docs/RELEASE-VALIDATION.md).
Earlier fork runs belong to earlier revisions and are not claimed as new-version
fork validation. No human security audit or maintainer usefulness result is claimed.

Known limitations include unsupported YAML aliases/merge keys, edited-rename
noise, no execution analysis, no cloud authorization or remote environment-policy
inspection, and bounded expression/matrix support. See the policies linked from
README. An incomplete/error outcome is not a clean analysis even when advisory
execution succeeds. Findings alone do not block merges.
