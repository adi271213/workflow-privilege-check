# Workflow Privilege Check

[![CI](https://github.com/adi271213/workflow-privilege-check/actions/workflows/ci.yml/badge.svg)](https://github.com/adi271213/workflow-privilege-check/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Catch pull requests that **escalate your GitHub Actions privileges** — a newly
added `pull_request_target`, a token widened to `write`, an `id-token`/OIDC grant,
or a newly referenced secret — and route them to a human. Capability-neutral
workflow PRs pass automatically.

It is deterministic, read-only, and runs no workflow code. Unlike static linters,
which audit the *current* state of your files, it reports the **base→head diff**:
what a pull request *adds*. A pre-existing `pull_request_target` is normal; a PR
that introduces one is worth a look.

## How it fits with your other tools

Run [zizmor](https://github.com/zizmorcore/zizmor) for broad static analysis —
template injection, untrusted checkout, unpinned actions, and more. This tool is a
**complement**, not a replacement: it answers the one question a state linter can't
— *did this PR make the pipeline more privileged than before?* — which is exactly
what you want for review routing and safe auto-merge. It does **not** detect
template injection, malicious scripts, or compromised upstream actions.

## Usage

Add an advisory check to pull requests. It writes a job summary and sets a status;
it never blocks a merge on its own and requests only `contents: read`.

```yaml
- uses: adi271213/workflow-privilege-check@v0.3.0
  with:
    mode: advisory   # non-blocking; omit to fail the step on incomplete/error
```

The Action needs both the base and head commits available in the checkout. See
[`examples/github-action-template.yml`](examples/github-action-template.yml) for the
complete, hardened workflow (it checks out the trusted base and fetches the PR head
as data). To **enforce**, make the Action's status a required check in branch
protection — a report-only workflow is intentionally not a self-enforcing gate.

### Example report

```markdown
## Review suggested

| Rule  | Workflow   | Job     | Change |
|-------|------------|---------|--------|
| WF003 | release.yml| —       | Privileged trigger `pull_request_target` introduced. |
| WF001 | release.yml| publish | Job `publish` newly requests an OIDC identity token. |
| WF001 | release.yml| publish | Job `publish` newly uses `packages: write`.          |
| WF004 | release.yml| publish | Job `publish` adds a reference to secret `PUBLISH_TOKEN`. |
```

## Command line

Requires Python 3.11+ and Git. Install from source:

```sh
pip install -e .
# Compare two directories:
workflow-privilege-check scan --dirs examples/base examples/head --format markdown
# Compare exact commits in a local repo (no checkout, no network):
workflow-privilege-check scan --repo /path/to/repo --base BASE_SHA --head HEAD_SHA
```

For jobs that inherit token defaults, pass the trusted defaults to resolve
otherwise-incomplete comparisons:
`--default-permissions '{"contents":"read"}'`.

## What it reports

| Rule | Flags when a PR… | Does not establish |
|------|------------------|--------------------|
| **WF001** | increases a per-job token scope (`contents: write`, `id-token: write`, …), including read increases | runtime token privileges, fork restrictions, cloud authorization |
| **WF003** | adds a review-sensitive trigger (`pull_request_target`, `workflow_run`, `issue_comment`, `issues`, `discussion`, `discussion_comment`) | exploitability, actor checks, or filter changes on an existing trigger — see [trigger policy](docs/TRIGGER-POLICY.md) |
| **WF004** | adds a secret reference, workflow-env reference, or `secrets: inherit` forwarding | whether the secret exists, is available, or is actually used |

A new trigger does not automatically grant write access; findings are review
prompts, not vulnerability claims.

**Result contract:** `complete` with no findings → exit 0 (no increase detected);
`complete` with findings → exit 0 (review suggested); `incomplete` or `error` →
exit 2. A zero exit is not a statement that a PR is safe.

## Scope & limitations

- Reads only `.github/workflows/*.yml|*.yaml`; bounds of 200 files / 4 MiB per
  snapshot and 256 KiB per file; analysis is offline and never executes PR code.
- YAML anchors/merge keys are not yet supported and produce an explicit `error`
  rather than a silent pass.
- Scripts, action internals, reusable-workflow bodies, cloud trust policies, and
  existing-trigger filter changes are out of scope.
- **Early project.** Tested by a synthetic acceptance suite (run `python
  scripts/validate.py`; CI covers Python 3.11–3.14) and a 74-PR regression replay.
  It has not yet been validated in production — real-world PRs and feedback welcome.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and pull requests are welcome.

## License

[MIT](LICENSE) · Security policy: [SECURITY.md](SECURITY.md)
