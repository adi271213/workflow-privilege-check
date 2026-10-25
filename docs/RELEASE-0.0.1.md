# 0.0.1 release checks

Evaluated runtime: `ed5248238b1f88d06cb76e9bfa6427e09567f743`. Package and module versions are 0.0.1.
Release validation covers the full Python matrix, disconnected-network Action
smoke tests, built-package installation, the frozen 74-PR regression replay,
both hosted outcome modes, and installation through the released tag.

The [alias validation packet](ALIAS-VALIDATION.md) separately records 21 consumer
PR cases / 42 mode outcomes and the whole-graph checks. The release retains those
rules and bounds, and read increases continue to suggest review.

Release evidence links are added after the candidate checks finish. The
historical benchmark remains selected and self-labeled; it is not production
precision/recall. No new fork or independent human security audit is claimed.
