# Workflow Privilege Check — experimental Action

A report-only tool that explains supported GitHub Actions configuration changes
between two snapshots. Built from scratch; no historical scanner implementation
is included.

**Status:** experimental alpha, v0.2.1 candidate. The tested functional Action pin
is `50bc69f8d1772a67129635e0814097da6f8d8c11`: **18 hosted contract jobs and
10 consumer PR runs passed, including four genuine fork PRs**. Expected
incomplete/error cases passed by reporting uncertainty; they are not clean
analyses. See [evidence and limitations](docs/review/README.md) for exact revisions,
run links, historical results, and the 74-PR benchmark.

A [separate reviewer agent](docs/review/separate-agent/REPORT.md) found no blocking
issue and agreed with the 45 configured facts in the 38-case review packet.
This is not human validation or a production precision estimate. Do not require
this check for merging or use its result to authorize auto-merge during evaluation.

## Advisory pilot

See [PILOT.md](PILOT.md) for explicit outcomes and the ready-to-copy public
repository installation used by the tested consumer runs. The consumer contains
no scanner or internal test hooks. Keep this workflow outside required merge checks.

The Action exports analysis-status, review-status, finding-count,
analysis-exit-code, report-path, summary-path, base-sha and head-sha. Review is
unknown when analysis is incomplete/error without known findings. The default
require-complete mode retains the previous exit behavior; advisory mode makes
analysis outcomes nonblocking while preserving warnings and explicit status.
Reporting failures and invalid mode still fail the Action. The CLI is unchanged.

## Try it locally

Requires Python 3.11+ and Git for commit comparisons.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
workflow-privilege-check scan --dirs examples/base examples/head --format markdown
```

The included example introduces package publishing, an OIDC token request, a
privileged trigger, and a secret reference. All findings are suggestions for human
review; they do not establish maliciousness.

Compare exact Git snapshots without checkout:

```sh
workflow-privilege-check scan --repo /path/to/repository --base BASE_SHA --head HEAD_SHA
```

Branch names are accepted by the CLI and resolved to exact commits in the report.
The supplied base is compared directly; the tool does not substitute a merge base.
Git replacement refs and caller-provided Git environment overrides are ignored,
so recorded object IDs identify the workflow bytes being read.
It does not fetch missing objects or execute scripts, actions, install hooks, or
other code from the analyzed repository.

For an existing job with the same job ID, unchanged inherited permissions compare
symbolically: `D -> D` has no configured increase for any fixed default map `D`.
The report lists these jobs in `inheritedComparisons` and discloses the assumption
that external repository/organization defaults remain fixed. It does not discover
their values or verify runtime access. Trigger and secret checks still run.

A new inherited job, a renamed inherited job, or a transition between inherited and explicit
permissions remains incomplete. Supply explicit defaults from a trusted source
to resolve those comparisons:

```sh
workflow-privilege-check scan --dirs examples/base examples/head \
  --default-permissions '{"contents":"read","packages":"read"}'
```

That map is an assertion by the operator, not a discovered repository setting.
No policy or suppression files are loaded from the proposed tree.

## Supported rules

| Rule | What is compared | What is not established |
|---|---|---|
| WF001 | Per-job token scope increases, including read increases; workflow settings and job overrides | Runtime token privileges, fork restrictions, cloud authorization |
| WF003 | New `pull_request_target` and `workflow_run` event names | Exploitability or changes to filters on an existing trigger |
| WF004 | New per-job literal secret references, workflow-level env references, and whole-secret forwarding | Whether secrets exist, are available, or are actually accessed |

Job identities are their job IDs. A permission copied to another existing job is
a new finding. Job renames may conservatively appear as new jobs. Exact-content
workflow file renames are recognized in both directory and Git modes; renames
combined with edits are conservatively treated as removal plus addition.

Secret names are compared case-insensitively. Literal dot and bracket references
are supported; dynamic selection is incomplete. Known literal additions are still
reported when only the head has an unresolved selector. An unresolved selector in
the base prevents establishing secret additions. Expression string literals are
ignored. References to `secrets.GITHUB_TOKEN` alone are ignored because the token
is implicitly available; its configured scopes are covered by WF001.

Workflow-level environment expressions are counted as reference evidence for each
job. The scanner does not prove data flow or account for every environment-variable
shadowing case. Changes within the same job that give another step an existing
secret are outside coverage.

## Result contract

| Analysis | Meaning | Exit |
|---|---|---|
| complete, no findings | No supported expansions detected | 0 |
| complete, findings | Human review suggested | 0 |
| incomplete | Required context is unavailable | 2 |
| error | Inputs are unavailable, invalid, unsupported, or over budget | 2 |

Findings may coexist with incomplete analysis. Inspect `analysis` before relying
on a report. A zero exit code is not a statement that a PR is safe.

JSON includes exact Git SHAs or directory content fingerprints, per-job evidence,
renames, diagnostics, symbolic inheritance evidence, assumptions, and permanent
coverage limitations. Use `--output report.json`
to save JSON, or `--format markdown`. `--summary PATH` explicitly appends Markdown.
The CLI does not implicitly write GitHub environment files.

## Input and trust boundaries

- Only immediate `.github/workflows/*.yml` and `*.yaml` files are read.
- Limit: 200 workflows and 4 MiB per snapshot; 256 KiB per file.
- YAML: at most 60,000 tokens and 50 nesting levels. Aliases and merge keys are
  explicitly unsupported. Duplicate keys, custom tags, invalid UTF-8, and symlinked
  workflow inputs are rejected.
- Errors do not echo workflow source lines or secret values.
- Analysis is offline. The Action's separate dependency-install step uses PyPI.
- Read-only comparisons do not enforce approvals or prevent bypass by a PR that
  removes or changes the calling workflow. Enforcement is a future feature.
- Scripts, action source, reusable-workflow internals, cloud trust policies,
  environment protection rules, and existing-trigger filter expansion are not analyzed.
- The permission vocabulary is explicit and versioned in source; unknown scopes
  produce an error rather than silently disappearing.

Use a trusted interpreter and installation outside an untrusted checkout. Never
install or run this scanner from PR-modifiable source during privileged analysis.

## GitHub Action wrapper

`action.yml` and `scripts/run-action.sh` provide a Linux composite wrapper. It
uses an isolated Python environment, reads PR base/head SHAs, and writes a job
summary. Both Git objects must already exist locally. It does not post comments
or request write permissions.

The tested v0.2.1 pin passed the hosted tests documented above, covering
neutral edits, known grants, incomplete defaults and analysis errors. Dependency
bootstrap, contributor approval, read-only token context, event SHA delivery,
summary content and signed-in rendering, and exit handling passed. The tests use
Linux GitHub-hosted runners and synthetic fixtures; they do not establish universal
integration safety.

See `examples/github-action-template.yml`. Select the evaluated full commit SHA
for the version being tested. Do not use `uses: ./` from an untrusted PR
checkout. A pinned Action protects the scanner version, but a report-only calling
workflow is not an unbypassable security gate.

## Run validation

```sh
python scripts/validate.py
```

This runs the synthetic acceptance matrix plus parser, source-reader, CLI, and local
Action-entry integration tests. It saves `validation-results.json` with outcomes,
runtime versions, and source hashes. It requires no cloud credentials or network.

## Next experiment

The initial public-PR comparison found substantial overlap with existing tools.
The v0.1.1 update reduced incomplete results from 15/50 to 4/50 on that sample and
from 13/24 to 8/24 on unseen PRs, preserving all 45 finding facts across both
samples. The original labels came from the implementing assistant; a separate
reviewer agent re-adjudicated the 38-case packet without disagreement. These are
regression and usability observations, not production recall estimates.
See `VALIDATION.md`. Adoption and production precision remain unvalidated.

The v0.2.1 implementation audit and separate label addendum are in
[evidence and limitations](docs/review/README.md), alongside the subsequent separate
agent review. Neither review is human adjudication or a blinded evaluation.
Historical labels and benchmark artifacts remain frozen. A configured-change
signal must not be counted as a vulnerability or proof of expanded runtime authority.

Technical references:
[workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax),
[secret naming](https://docs.github.com/en/actions/reference/security/secrets),
[context availability](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts).
