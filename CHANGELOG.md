# Changes

## 0.2.0 — 2026-10-24

- Expose explicit analysis/review outcomes, counts, exact commits, and report paths
  as composite Action outputs.
- Keep require-complete as the default; add explicit advisory mode for an
  observational pilot. The CLI and scanner rules remain unchanged.
- Report bootstrap/process failures as error/unknown outcomes, with warnings and
  retained reports. Publishing failures remain failing Action steps.
- Add a clean consumer workflow and seven focused Action outcome tests.
- Verify published PyYAML wheel hashes during Action dependency installation.

## 0.1.1 — 2026-10-24

- Compare unchanged unknown inherited token permissions symbolically for matched
  existing job IDs, assuming unchanged external defaults. Record compared jobs
  and the assumption in JSON; disclose it in Markdown.
- Keep new inherited jobs, job renames, and inherited/explicit transitions
  incomplete. Do not assume read-only defaults or suppress other rule findings.
- Add eight regression tests, including an 18-map concrete-default enumeration;
  update fixture P09's expected result. All 74 local tests pass.
- Preserve every finding fact on the original 50 PRs and 24 unseen PRs while
  reducing incomplete results. See the sibling inherited-default benchmark.
