# Install the three-maintainer advisory pilot

This is an experimental review aid for public GitHub repositories. It compares
configured token scopes, newly added `pull_request_target` / `workflow_run` event
names, and secret references between two snapshots. It does not establish runtime
credential access or PR safety. Keep your existing review process and scanners.

The reviewed fixes merged in [PR #1](https://github.com/adi271213/workflow-privilege-check/pull/1).
Use the already-tested Action pin below throughout the pilot:

```text
adi271213/workflow-privilege-check@50bc69f8d1772a67129635e0814097da6f8d8c11
```

This is a full commit pin, not a moving branch or release tag. It is part of the
merged history. The later merge/documentation commits do not change the tested
functional code.

## 1. Choose one public repository

Choose a repository you maintain that already uses GitHub Actions and is likely
to receive workflow edits during the next two weeks. Installation uses an Ubuntu
GitHub-hosted runner, read-only `contents` permission and public Git fetch access.
It needs no repository secrets, cloud credentials, write token or external account.
The Action installs hash-pinned PyYAML wheels from PyPI during setup.

This recipe has not been validated for private repositories or self-hosted runners.
If your existing Actions policy blocks it, record the reason rather than broadening
permissions just to join the pilot.

## 2. Install the workflow

Copy the provided `workflow-privilege-review.yml` to:

```text
.github/workflows/workflow-privilege-review.yml
```

The exact hosted-tested template is also available in the
[merged source](https://github.com/adi271213/workflow-privilege-check/blob/dba670946280694448ebb3f9582c76a9325e2094/examples/github-action-template.yml).
From your repository root, this downloads that fixed template:

```sh
mkdir -p .github/workflows
curl --fail --silent --show-error --location \
  https://raw.githubusercontent.com/adi271213/workflow-privilege-check/dba670946280694448ebb3f9582c76a9325e2094/examples/github-action-template.yml \
  --output .github/workflows/workflow-privilege-review.yml
```

The Action pin is already filled in. Keep `mode: advisory`, `contents: read`, the
trusted-base checkout, explicit head fetch and the result-explanation step.
The workflow analyzes proposed files as Git objects; it does not execute the
proposed workflow code. It emits a job summary and outputs, with no PR comments,
telemetry or external reporting backend. Reports remain in your GitHub workflow
logs/summary and job-local files.

Open an installation PR and merge it through your normal process. Keep this
workflow outside required merge checks and auto-merge authorization. The check
is report-only and can itself be changed by a PR; it is not an enforcement boundary.
GitHub's normal fork-workflow approval requirements still apply.

## 3. Run two onboarding checks

After installation reaches the default branch:

1. Open a PR changing only a README sentence. Expected: `analysis: complete`,
   `review: none`, zero findings and analysis exit 0. Read the job summary.
2. In a separate test PR, add the following unused manual workflow as
   `.github/workflows/pilot-read-grant.yml`. Expected: `analysis: complete`,
   `review: suggested`, one WF001 finding for the new job's `contents: read`,
   and analysis exit 0. Do not dispatch it or merge the test fixture. Close the
   test PR after inspection. No write grant, real secret or privileged trigger
   is needed to check that findings appear.

```yaml
name: Pilot read-grant fixture
on: workflow_dispatch
permissions: {}
jobs:
  fixture:
    permissions:
      contents: read
    runs-on: ubuntu-latest
    steps:
      - run: echo "Manual pilot fixture"
```

Record the installation PR and both check-run URLs. If the outputs differ, capture
the summary and ask us to investigate. Do not invent default permissions or add
write access to force a successful result. The installation itself introduces
read access for its checker job, so a finding on the installation PR can be expected.

## 4. Interpret each result

| Analysis / review | What to do |
|---|---|
| complete / none | No supported configured increase detected. Continue ordinary review. |
| complete / suggested | Read the exact workflow/job change and decide whether it is intended. |
| incomplete / unknown | Required context is missing; zero findings is not a clean conclusion. |
| incomplete or error / suggested | Review the known findings and the unresolved part. |
| error / unknown | Analysis failed or input is unsupported; inspect the diagnostic. |
| failed Action step or missing outputs | Installation/execution/reporting did not finish; inspect the failed step. |

In advisory mode, incomplete/error analysis can coexist with a successful Action
step. The explicit outputs and summary are what matter. Examples of correct
uncertainty reporting are available in the
[fork incomplete run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40124634136)
and [fork error run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40124655019).

Secret references do not prove a secret exists or that plaintext is delivered.
An OIDC migration or a new read scope can be a legitimate improvement. Dynamic
selectors and unknown inherited-default transitions can remain incomplete.
Aliases are currently unsupported. Scripts/action behavior, reusable-workflow
internals, cloud trust, environment guards, existing-trigger filters and secret
redistribution within an existing job are outside this version's coverage.

## 5. Give brief feedback and remove if needed

For each real workflow PR, share its public URL, summary outcome and whether the
explanation was useful, accurate but low-value, incorrect or unclear. Record
incomplete/error outcomes separately. Flag any supported change you expected it
to catch but it missed. Do not send secret values, credentials or private logs.

At the end of two weeks, answer: would you keep it, what caused extra work, and
what single improvement would make it more useful? Removal is deleting
`.github/workflows/workflow-privilege-review.yml` through your normal process.
There is no hosted account, cloud resource or credential to revoke for this tool.

## Evidence and limits

The tested pin passed 85 local tests, 18 hosted contract jobs and 10 consumer PR
runs, including four genuine forks. A separate reviewer agent re-adjudicated the
38-case packet and agreed with 45 configured facts. These are engineering checks
on selected examples, not production precision/recall or human security validation.
See the [evidence index](https://github.com/adi271213/workflow-privilege-check/blob/main/docs/review/README.md).

## Output reference

| Output | Meaning |
|---|---|
| analysis-status | complete, incomplete or error |
| review-status | none, suggested or unknown |
| finding-count | Decimal count; zero is inconclusive if analysis is incomplete/error |
| analysis-exit-code | 0 for complete, 2 for incomplete/error, independent of advisory mode |
| report-path / summary-path | Absolute JSON/Markdown paths available to later steps in the same job |
| base-sha / head-sha | Exact resolved commits; empty if resolution failed |

JSON reports include an additive `action` object with mode, reviewStatus and
analysisExitCode. Reports are not automatically uploaded as artifacts. Reporting
failures or invalid mode fail the Action; advisory success does not authorize merging.
