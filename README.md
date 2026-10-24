# Workflow Privilege Check — experimental alpha

A deterministic, offline analysis engine that explains supported GitHub Actions
configuration changes between exact snapshots. It reports token scope increases,
new pull_request_target/workflow_run event names, and new per-job secret references.
It does not establish runtime access, maliciousness, cloud trust, or PR safety.

Version 0.2.0 adds explicit Action outcomes and an advisory installation. The
scanner rules and CLI exit behavior are unchanged from v0.1.1.

Read [PILOT.md](PILOT.md) for the result contract, installation and removal.
The consumer template is [examples/github-action-template.yml](examples/github-action-template.yml).
Always pin the Action to a reviewed full commit SHA. Keep pilot checks outside
required merge rules; a green workflow is not authorization to merge.

## Evidence

81 local tests pass. Earlier scanner versions were replayed on 74 public PRs and
v0.1.1 passed six hosted branch/fork cases, including approval and rendered summaries:
[hosted test repository](https://github.com/adi271213/workflow-privilege-check-smoke-20261024).
The new 0.2.0 public-output installation is being tested in a fresh consumer repo.
Corpus labels need independent human review; maintainer value is unvalidated.

## Local use

Requires Python 3.11+ and PyYAML 6.0.3. Install with `python -m pip install .`, then:

```sh
workflow-privilege-check scan --dirs examples/base examples/head --format markdown
workflow-privilege-check scan --repo /path/to/repo --base BASE_SHA --head HEAD_SHA
```

The CLI exits 0 for complete reports, including findings; incomplete/error reports
exit 2. Unknown defaults remain unknown when a comparison needs their values.
Unchanged inherited permissions for matched jobs compare symbolically under a
fixed-external-defaults assumption. Dynamic secret selection and YAML aliases
are unsupported; unavailable/invalid inputs never establish a clean result.

## Input limits and ownership

Only immediate .github/workflows/*.yml and *.yaml files are analyzed. Limits:
200 workflows/4 MiB per snapshot, 256 KiB per file, 60,000 YAML tokens and 50
nesting levels. Symlinks, duplicate keys, aliases, merge keys, and unknown scopes
are rejected. Proposed scripts, remote action bodies, environment protections,
cloud IAM policies, and existing-trigger filter expansions are outside coverage.

The Action is tested on Linux GitHub-hosted runners. It requests no writes,
comments, cloud calls, or telemetry. PyYAML installation uses hash-verified wheels.
Reports may include workflow paths and secret names; they do not contain secret
values discovered from GitHub. See [SECURITY.md](SECURITY.md) and [LICENSE](LICENSE).
