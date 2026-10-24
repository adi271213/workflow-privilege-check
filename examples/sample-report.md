## Review suggested

Base: `directory:sha256:0f74f59804637bf5b8e855153fe7e0b703189d1d7a1699c0b1be09596f22c93f`
Head: `directory:sha256:c6f3b69a45ca538e6bd23a33274aafa8d39d1848c251e566c6ac49cf50a36386`

| Rule | Workflow | Job | Change |
|---|---|---|---|
| WF003 | .github/workflows/release.yml | — | Privileged trigger pull_request_target introduced. Review untrusted-input handling. |
| WF001 | .github/workflows/release.yml | publish | Job publish is newly configured to request an OIDC identity token. Runtime access is not verified. |
| WF001 | .github/workflows/release.yml | publish | Job publish is newly configured to use packages: write. Runtime access is not verified. |
| WF004 | .github/workflows/release.yml | publish | Job publish adds a reference or forwarding path to PUBLISH_TOKEN. Availability and actual access are not verified. |


Scope: configured capability changes only. This report does not establish PR safety.
