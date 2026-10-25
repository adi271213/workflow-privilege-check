# Separate reviewer-agent review of PR #1

**Recommendation: suitable for a small advisory pilot after the documentation correction below. No new blocking security/correctness issue reproduced.** This is a separate agent's review, not independent human validation or a blinded benchmark.

Reviewed PR branch HEAD `97c8333` against `main` (`4923197`), including the full code diff, the surrounding scanner/Git reader/controller/report/CLI, the pinned public consumer recipe, and the source-side hosted contract workflow. The evaluated functional Action pin is `50bc69f8d1772a67129635e0814097da6f8d8c11`.

## Findings

### P3 — README presents historical hosted counts without identifying their revision

`README.md:7–20` calls the product v0.2.1 but says “all six hosted Action cases” and “11 consumer PR runs ... eight ... contract jobs.” These are historical results. The linked `docs/review/README.md:66–77` correctly records the current candidate's 18 contract jobs and 10 consumer runs against `50bc69f...`. A reader can reasonably associate the opening counts with the current version or mix the different runs.

**Requested correction:** state the current candidate's exact pin and 18 + 10 counts in the opening status/pilot section, including four genuine fork runs. Identify older counts as historical in the evidence document only. Continue saying incomplete/error cases passed their expected outcome contract; they did not become clean analyses.

No P0/P1/P2 finding was established in this bounded review. Absence of a reproduced issue is not a security certification.

## Implementation conclusions

- The Git fix disables replacement object interpretation for every read and removes inherited `GIT_*` redirection/config variables. It covers both replaced commits and replaced workflow blobs without changing the recorded commit identities. The fix does not claim that the host Git executable or installation can be untrusted.
- The secret fix preserves a newly added literal reference when only the head also contains a dynamic selector. The result remains incomplete. A dynamic base could already select the head name, so suppressing directional additions there is justified. Existing whole-context forwarding is correctly treated as covering all literal names.
- Permission handling resolves job overrides before workflow settings, treats unspecified keys in explicit maps as none, distinguishes unknown defaults from explicit empty maps, and confines symbolic inherited equality to matched job IDs with unchanged inherited declarations. Known scope changes survive unrelated uncertainty.
- Parsing remains deliberately narrower than the full Actions schema. Aliases/merges and unsupported inputs produce an explicit error. This is a disclosed coverage limitation. Existing-trigger filter expansion, action/script behavior, reusable-workflow internals, guards/cloud trust, and same-job secret redistribution remain outside coverage.
- The supplied consumer checks out base code, fetches head as data, and invokes a pinned Action. It requests read-only permissions and does not load proposed policy/code. Its calling workflow is PR-modifiable and is appropriately disclosed as advisory; this is not an unbypassable gate or an auto-merge authorization.
- The controller separates analysis state from review state, retains outputs/files for expected analysis errors, and fails visibly if reporting itself fails. The default mode requires complete analysis; findings alone are not a failure. Bootstrap/reporting tests and the hosted matrix cover those intended semantics.

## Benchmark re-adjudication

Read the raw frozen base/head diffs for **all 38 selected cases**, then checked surrounding source and an independent YAML BaseLoader declaration inventory. For the large Pydantic hardening change, inspected the entire changed permission/job inventory and the diff's supported-declaration/reference changes. The review script does not import the scanner. Permission/event facts are derived separately; the eight secret-reference facts were manually transcribed from source.

The packet contains every configured-signal case, every incomplete case, and ten routine negatives after deduplication. The result is **45 exact configured facts, with zero disagreements** against the reviewed facts, narrow label classes, or the scanner's expected analysis states. See `case-adjudications.json` and `case-review.csv` for per-case reasoning, exact facts, unknown comparisons, source paths/hashes and explicit caveats. Prior labels and parent history were available, so this is not a blinded evaluation. The other 36 benchmark cases were not separately adjudicated in this review.

Several correct labels still provide weak evidence of product value:

- **pandas #65089:** invalid step-level `permissions` in the base. Useful declaration regression, unsuitable evidence of a valid runtime privilege transition.
- **FastAPI #14592:** only an aggregation job gains workflow-env reference evidence from a secret-availability boolean. No newly available plaintext credential is shown. This is not a uniquely detected vulnerability.
- **Pydantic #13039 and uv #21298/#16797:** read additions can occur during hardening, including removal of stronger scopes. A positive component delta does not measure increased net risk.
- **Ruff OIDC migrations:** new OIDC declarations coexist with static PAT removal; broker URL references are not proof of new credentials. Ruff #28830 also adds `--admin` script behavior that requires ordinary code review and is outside these rules.
- **Werkzeug #3150:** source proves nonincreases/equivalence, while the scanner remains conservatively incomplete. This is a coverage/usability cost, not a missed increasing component.
- Unknown inherited defaults are genuinely unresolved for the seven unresolved labels; the author describing a change as hardening does not establish the missing settings.

The sample does not establish production precision, attack recall, maliciousness, expanded runtime authority, or superiority over existing tools. Maintainer usefulness remains unmeasured and should be the purpose of the advisory pilot.

## Verification performed by this reviewer

- Re-ran the full local unittest suite from the PR checkout: **85 tests passed**.
- Independently checked SHA-256 hashes of all **18 contract logs and 10 consumer logs**, including four forks, against retained result metadata, and confirmed every log names the evaluated Action SHA.
- Compared functional source hashes from the PR checkout and `git show` at `50bc69f...` with the recorded tested-source manifest: match.
- Inspected raw hosted workflow construction and assertions, including both modes, missing/error/incomplete states, partial secret evidence, unknown base selectors, replaced commits/blobs and Git redirection.
- This was an offline review of retained hosted evidence, not a new GitHub execution or fresh API attestation. Existing success evidence supports the exact tested functional revision; it does not automatically validate later functional changes.

## Pilot readiness

Correct the README's revision/count ambiguity, preserve the documented limits, and incorporate this agent review into the evidence record. There is no newly reproduced engineering issue requiring another functional change before a small public-repository advisory pilot. A human security review can still add assurance, but it should not be claimed as completed by this agent review. No maintainer outreach, merge enforcement, or publication was performed by this reviewer.
