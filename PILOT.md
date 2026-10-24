# Advisory pilot installation

The Action exposes analysis and review as separate outcomes. Neither a green
workflow nor an empty finding list establishes that a PR is safe.

| Analysis | Review output | Meaning |
|---|---|---|
| complete | none | No supported configured-capability increases detected |
| complete | suggested | Known changes need human review |
| incomplete | unknown | Missing context prevents a clean conclusion |
| incomplete/error | suggested | Known changes were found; analysis also has limitations |
| error | unknown | Analysis did not succeed; inspect the summary/logs |

`mode: require-complete` is the default: complete analysis exits 0, while
incomplete/error exits 2. Findings alone do not fail the step.

`mode: advisory` reports all these states without failing the Action solely for
an analysis result. The `analysis-exit-code` output remains 0 or 2, and incomplete
or error analysis creates a warning. A reporting failure or invalid mode still
fails the step. Keep the pilot workflow outside required merge checks.

## Install

Copy `examples/github-action-template.yml` into
`.github/workflows/workflow-privilege-review.yml` in the pilot repository. Use the
reviewed full commit SHA of this Action. The example checks out the trusted base,
fetches the proposed head as Git objects, runs the pinned Action in advisory mode,
and explains its public outputs. It does not execute PR code or load proposed
suppression/default-policy files. No test harness, summary-capture hook, or
vendored scanner is needed in the consumer repository.

The calling workflow can itself be changed or removed by a PR. This installation
is a review aid and does not enforce an unbypassable approval boundary. It is not
an authorization mechanism for auto-merge.

## Public outputs

| Output | Values |
|---|---|
| analysis-status | complete, incomplete, error |
| review-status | none, suggested, unknown |
| finding-count | Decimal count; zero is not a clean result when analysis is incomplete/error |
| analysis-exit-code | 0 for complete, 2 for incomplete/error, independent of Action mode |
| report-path | Absolute JSON file path in runner temp |
| summary-path | Absolute Markdown file path in runner temp |
| base-sha / head-sha | Exact resolved commits; empty when resolution failed |

The report files remain available to subsequent steps in the same job. They are
not automatically uploaded or transmitted to an external service. JSON includes
an `action` object with mode, reviewStatus, and analysisExitCode. The CLI retains
its existing exit codes and report schema; these Action fields are additive.

The stdlib-only controller can report setup failures before PyYAML is installed.
Dependency installation uses version-pinned, hash-verified wheels. The tested
environment is a Linux GitHub-hosted runner with Python 3 available.

## Read and remove

Read the job summary first, especially the analysis status, diagnostic reasons,
and exact commit identities. A finding can describe a legitimate hardening change
such as replacing static credentials with OIDC. Secret-reference findings do not
prove credential availability or plaintext delivery.

To remove the pilot, delete its calling workflow. The Action creates no comments,
remote state, telemetry, cloud resources, or persistent credentials. Read-only
comparisons do not need cloud credentials or repository secrets.
