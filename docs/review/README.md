# Evidence and limits for the advisory pilot

This is an experimental configured-change review aid. It does not certify PR
safety, detect arbitrary malicious workflow code, or enforce a merge boundary.

The [current pilot pin and hosted results](#current-pilot-trigger-extension)
are recorded below. Earlier sections retain their original revision boundaries.

## Implementation and label review

The v0.2.1 review reproduced and fixed two issues: Git replacement refs could
substitute workflow content under recorded commit identities; an unresolved head
secret selector suppressed separate provable literal additions. Git environment
redirections are also ignored. Neither issue establishes an ordinary fork-PR
exploit against the tested installation. Regression tests cover both fixes.

The same assistant wrote the implementation and original benchmark labels, and
performed this second pass. This is **not independent human review**, a blinded
evaluation, or a new holdout. Maintainer usefulness remains unmeasured.

[Reviewed labels](labels-reviewed.json) include 74 PR URLs, immutable source links,
file hashes, exact expected rule/workflow/job/before/after facts, uncertainty,
validity caveats, and usefulness notes. The frozen historical label classes remain
20 configured-change positives, 47 with no supported signal, and 7 unresolved.
No label claims maliciousness or demonstrated expanded runtime authority.

- Django #21077: corrected rationale; scripts-tests inherits explicit contents
  read. It is not an unknown-default job.
- FastAPI #14592: a boolean availability expression is weak value evidence, not
  proof of newly available plaintext credentials or a uniquely found vulnerability.
- pandas #65089: base has invalid step-level permissions. Its declaration change
  is useful as a regression but cannot establish a valid runtime before/after pair.
- Read additions during hardening and PAT-to-OIDC migrations are positive
  component deltas; they can coexist with reduced overall risk.

[Replay summary](benchmark-replay-summary.json): 74 PRs, all 45 exact expected
finding facts preserved, 62 complete and 12 incomplete results. These are a small,
selected, correlated 2021–2026 sample. They are not production precision or recall.
No independently adjudicated malicious-PR corpus was tested.

The original 50-case comparator run showed related-category signals on 15/15
configured positives for this tool, 14/15 for Actions Permission Diff Ledger 0.2.0,
6/15 for zizmor 1.31.1 regular and 13/15 auditor using simple baseline subtraction.
A related category is not the same exact grant. Competitors were not rerun for
v0.2.1. This does not support a superiority claim or an unoccupied category.

## Hosted evidence before v0.2.1

The v0.2.0 clean public-repository pilot passed 11 PR runs, including four genuine
fork PRs with contributor approval, and eight mode/failure contract jobs.

- [Consumer repository](https://github.com/adi271213/workflow-privilege-check-pilot-20261024)
- [Fork incomplete example](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40110499653)
- [Fork error example](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40110549481)
- [Original eight contract jobs](https://github.com/adi271213/workflow-privilege-check/actions/runs/40110530848)

Those runs used b0fc6b639749c78ebc5e7be37942ef6ecef86446. They do not by themselves
validate the v0.2.1 revision; its hosted replay is documented separately below.

## Separate agent review and pilot readiness

At the user's request, a [separate reviewer agent](separate-agent/REPORT.md)
reviewed PR #1 at `97c83338c0100b5998729770465d3bd72e19a0a2`, the surrounding
implementation and Action trust boundary, and all 38 selected cases: all 20
positives, all 12 incomplete cases, and ten routine negatives, deduplicated.
It found no blocking security/correctness issue, agreed with all 45 exact facts,
and verified the 85 local tests and retained hosted evidence. The original
history/labels were available; this was not blinded or human validation.

The reviewer requested one P3 correction: make the README opening identify the
current pin and 18 + 10 hosted counts instead of mixing historical revisions.
That documentation correction is applied and the [reviewer confirmed closure](separate-agent/FOLLOWUP.md). The tested functional code is unchanged.
See [case adjudications](separate-agent/case-review.csv) and
[verification summary](separate-agent/verification-summary.json).

No reproduced engineering issue remains open before a small public-repository
advisory pilot. Human review can add assurance but has not been performed. Start
with about three maintainers and keep the workflow outside required checks;
success is whether the explanations are useful enough to keep. Maintainer
usefulness and production precision remain unmeasured.

## Hosted v0.2.1 candidate replay

All 18 [contract jobs](https://github.com/adi271213/workflow-privilege-check/actions/runs/40113060308)
and 10 updated consumer PR runs (four genuine forks) passed against functional pin
`50bc69f8d1772a67129635e0814097da6f8d8c11`. The retained log verifier checks the
downloaded Action SHA, exact inputs, output states, read-only permissions and
failure-mode behavior. [Machine-readable results](hosted-results.json).

[Updated fork error example](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40124655019)
shows error/unknown without presenting advisory success as a clean analysis.
The first reopened consumer runs still used the old pin and are excluded from
these counts; the PR branches were explicitly updated before this verified replay.
The fixes merged in [PR #1](https://github.com/adi271213/workflow-privilege-check/pull/1),
with the separate agent review recorded above. The [pilot setup guide](../../PILOT.md)
used the then-current hosted-tested Action pin. The newer trigger-extension pin
is documented below. No maintainer invitations or merge enforcement changes.

## Current pilot trigger extension

The evaluated Action pin is `b3a6401e90f873e192c9d423ece5a44bc22ed44e`, introduced by
[PR #3](https://github.com/adi271213/workflow-privilege-check/pull/3). It adds the
four issue/discussion events in [the trigger policy](../TRIGGER-POLICY.md) and
renders Markdown syntax in untrusted names literally. Later setup/evidence
commits retain identical scanner/runtime bytes; package version remains 0.2.1,
with no new tagged release.

- All 93 tests passed across Python 3.11–3.14 in [PR CI](https://github.com/adi271213/workflow-privilege-check/actions/runs/40199391256).
- Ten same-repository consumer PR runs passed: [machine-readable results](pr3-consumer-results.json).
- Eighteen hosted contract jobs passed across advisory/require-complete modes:
  [run](https://github.com/adi271213/workflow-privilege-check/actions/runs/40200633642) and [verified results](pr3-contract-results.json).
- The frozen 74-PR replay preserved all 45 exact facts and 62 complete / 12
  incomplete outcomes: [replay summary](pr3-replay-summary.json). It produced no
  additional trigger findings and does not measure the new policy's usefulness.

| Consumer case | Expected analysis / review / findings | Hosted run |
|---|---|---|
| neutral | complete / none / 0 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200492528) |
| issue-comment | complete / suggested / 1 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200495553) |
| issues | complete / suggested / 1 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200498279) |
| discussion | complete / suggested / 1 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200502249) |
| discussion-comment | complete / suggested / 1 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200507148) |
| incomplete | incomplete / unknown / 0 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200509964) |
| mixed | incomplete / suggested / 1 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200513720) |
| alias-error | error / unknown / 0 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200517973) |
| syntax-error | error / unknown / 0 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200521310) |
| markdown-name | complete / suggested / 1 | [run](https://github.com/adi271213/workflow-privilege-check-pilot-20261024/actions/runs/40200524136) |

The consumer checked exact event base/head SHAs, read-only token permissions,
report consistency and uncertainty warnings using the public template. Alias and
malformed YAML cases passed by reporting error/unknown. The intentionally malformed
fixture also caused GitHub's own workflow validation failure; that fixture run is
not the consumer check being counted. No fixture workflow was dispatched or merged.
The Markdown-name consumer case verified JSON evidence; escaping is covered by
unit tests, without a new rendered-UI assertion.

These are synthetic same-repository runs. Four genuine fork tests and a separate
agent's 38-case assessment remain evidence for the older pin only; neither was
repeated for this extension. No human security review, production precision/recall,
new independent malicious-PR corpus, or maintainer-usefulness result is claimed.
No maintainer invitations have been sent.
