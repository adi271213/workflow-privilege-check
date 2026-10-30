# 0.0.4 release checks

Evaluated runtime: `ff12d9b482a55777815dd5a1391e058986259320`.
Package and module versions agree at 0.0.4.

Candidate validation is in progress. Publication waits for Python CI, the
self-contained hosted contract, fresh consumer/fork cases, package installation
checks and the frozen historical replay. Results will be recorded before merge.

This patch fixes expression identifier boundaries that could invent whole-secret
access and hide a real new literal secret reference. It resolves hyphenated direct
matrix fields without evaluating expressions. Findings remain advisory and do not
establish runtime access or PR safety. See the known release limitations for older
installations; earlier tags remain unchanged.
