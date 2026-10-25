# Evidence & limitations

This is an **experimental** review aid for GitHub Actions privilege *changes*. It
does not certify PR safety, detect arbitrary malicious workflow code, or enforce a
merge boundary.

## The honest caveat (read this first)

The implementation, the original benchmark labels, and a second "reviewer-agent"
re-adjudication were all produced by **the same AI assistant**. This is **not**
independent human review, a blinded evaluation, or a production precision/recall
measurement. Maintainer usefulness is unmeasured. Treat the signal as a review
prompt, never as proof of a vulnerability or of expanded runtime authority.

## What has been checked

- **Local suite:** `python scripts/validate.py` — synthetic acceptance matrix plus
  parser, source-reader, CLI, and Action-entry integration tests. Green on Python
  3.11–3.14 in [CI](../../.github/workflows/ci.yml). No network or credentials.
- **Frozen replay (regression, not accuracy):** a selected, correlated 2021–2026
  sample of **74 PRs**. See [benchmark-replay-summary.json](benchmark-replay-summary.json):
  all **45** expected finding facts preserved, 62 complete / 12 incomplete, label
  classes 20 configured-signal / 47 no-signal / 7 unresolved. This is a guard that
  behavior hasn't regressed — **not** a precision or recall estimate, and the sample
  is small and self-labeled.
- Two hardening fixes verified by regression tests: Git replacement refs could
  substitute workflow bytes under a recorded commit ID (now ignored); an unresolved
  head secret selector suppressed provable literal additions (now reported).

The raw per-PR label dumps and agent-adjudication artifacts from earlier passes
were removed from the tree to keep the repo focused; they remain in Git history.

## Known gaps / future work

- **YAML aliases/merge keys** are rejected as an explicit `error`; anchor-using
  workflows need a separate bounded alias expansion before they can be analyzed.
- **No read/write severity tiering** yet — read-scope increases are reported the
  same as write; a tier would reduce review noise.
- **No independent validation.** The next real step is a hosted-consumer pilot and
  an outside reviewer; until then, keep this advisory and out of required checks.
- Out of scope by design: template injection, untrusted checkout, unpinned actions,
  malicious scripts, upstream-action compromise (use zizmor / pinning / Socket).
