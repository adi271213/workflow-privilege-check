# Evidence and limits for the advisory pilot

This is an experimental configured-change review aid. It does not certify PR
safety, detect arbitrary malicious workflow code, or enforce a merge boundary.

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

## Before invitations

Obtain a different engineer's review of the Git reader, expression handling,
Action trust boundary, and benchmark judgments. Start with all 20 positives,
all 12 incomplete cases, and ten routine negatives (deduplicate overlap).
Use exact source evidence and record disagreements and usefulness separately.
Start any subsequent pilot in advisory mode outside required checks; success is
whether maintainers find the explanations useful enough to keep.
