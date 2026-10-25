# Workflow Privilege Check

[![CI](https://github.com/adi271213/workflow-privilege-check/actions/workflows/ci.yml/badge.svg)](https://github.com/adi271213/workflow-privilege-check/actions/workflows/ci.yml)

**An advisory PR check that flags when a change to your GitHub Actions config
*increases* privilege** — a newly added privileged trigger, a widened workflow
token, or a new secret reference. It compares the pull request's base and head and
reports only what the change *added*, so capability-neutral workflow PRs can be
fast-pathed and the few that expand privilege get a human.

> **Status:** experimental alpha. Advisory only — do not make it a required merge
> check or auto-merge authorizer yet. Validation to date is author-run, not
> independent (see [Evidence](docs/review/README.md)).

## Why this exists (and how it differs from zizmor)

Static linters like [zizmor](https://github.com/zizmorcore/zizmor) are excellent
and **broader than this tool** — they audit the *current state* of your workflows
for many issue classes (template injection, untrusted checkout, unpinned actions,
excessive permissions, and more). Run zizmor; most teams should.

This tool answers a different, narrow question a state linter structurally can't:

> **Did *this PR* make the pipeline more privileged than before?**

A pre-existing `pull_request_target` is normal; a PR that *adds* one is a signal.
Because the check is a base→head **diff**, it stays quiet on accepted existing
config and fires only on the delta — which makes it usable for **review routing**
and safely fast-pathing the capability-neutral majority of workflow PRs.

It is a **complement, not a replacement**. It does **not** detect template
injection, untrusted-checkout exploits, unpinned actions, malicious `run:` scripts,
or compromised upstream actions. Use zizmor (and pinning/Socket) for those.

## Try it

Requires Python 3.11+ and Git.

```sh
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -e .
workflow-privilege-check scan --dirs examples/base examples/head --format markdown
```

The bundled example adds package publishing, an OIDC token request, a privileged
trigger, and a secret reference — all reported as suggestions for human review.

Compare exact Git commits without a checkout (objects must already exist locally):

```sh
workflow-privilege-check scan --repo /path/to/repo --base BASE_SHA --head HEAD_SHA
```

## Supported rules

| Rule | Flags when a PR… | Does **not** establish |
|---|---|---|
| **WF001** | increases a per-job token scope (e.g. `contents: write`, `id-token: write`), incl. read increases | runtime token privileges, fork restrictions, cloud authorization |
| **WF003** | adds a review-sensitive trigger (`pull_request_target`, `workflow_run`, `issue_comment`, `issues`, `discussion`, `discussion_comment`) | exploitability, actor checks, or filter changes on an existing trigger — see [trigger policy](docs/TRIGGER-POLICY.md) |
| **WF004** | adds a secret reference, workflow-env reference, or `secrets: inherit` forwarding | whether the secret exists, is available, or is actually used |

A new trigger does not automatically grant write access; these are **review
prompts**, not vulnerability claims.

## Result contract

| Analysis | Meaning | Exit |
|---|---|---|
| `complete`, no findings | no supported privilege increase detected | 0 |
| `complete`, findings | human review suggested | 0 |
| `incomplete` | required context unavailable (e.g. inherited defaults unknown) | 2 |
| `error` | input invalid, unsupported, or over budget | 2 |

A zero exit is **not** a statement that a PR is safe. For jobs that inherit token
defaults, pass `--default-permissions '{"contents":"read"}'` (a trusted operator
assertion) to resolve otherwise-incomplete comparisons.

## GitHub Action

`action.yml` is a read-only Linux composite wrapper: it reads the PR base/head
SHAs, writes a job summary, requests no write permissions, and posts no comments.
See [`examples/github-action-template.yml`](examples/github-action-template.yml)
and [PILOT.md](PILOT.md). Pin it to a full commit SHA; never run `uses: ./` from an
untrusted PR checkout. A report-only workflow is not an unbypassable gate.

## Limitations & trust boundary

- Reads only `.github/workflows/*.yml|*.yaml`. Bounds: 200 files / 4 MiB per
  snapshot, 256 KiB per file; YAML capped at 60k tokens / 50 levels.
- **YAML aliases and merge keys are unsupported** and produce an explicit `error`
  (not a silent pass) — anchor-using workflows aren't analyzed yet. Duplicate keys,
  custom tags, invalid UTF-8, and symlinked inputs are rejected.
- Analysis is offline and never executes workflow code; the Action's dependency
  install step uses PyPI. Errors never echo workflow source or secret values.
- Scripts, action internals, reusable-workflow bodies, cloud trust policies,
  environment protection rules, and existing-trigger filter changes are out of scope.
- Run from a trusted install, never from PR-modifiable source during analysis.

## Validation & evidence

Honest status: the implementation, benchmark labels, and a second "reviewer-agent"
pass were all produced by the same assistant — this is **not** independent human
review or a production precision/recall estimate. A frozen 74-PR replay preserves
all expected findings as a regression guard. Details, boundaries, and known gaps:
[docs/review/README.md](docs/review/README.md).

Run the local suite (synthetic acceptance + parser/reader/CLI/Action-entry tests,
no network or credentials):

```sh
python scripts/validate.py
```

CI runs it on Python 3.11–3.14 for pushes to `main` and pull requests.

## License

[MIT](LICENSE). Security policy: [SECURITY.md](SECURITY.md).
