# Known release limitations

## Runner matrix combinations in 0.0.1 (fixed in 0.0.2)

WF005 in 0.0.1 compares the combined labels and groups across matrix rows. It can
miss a change that rearranges combinations while keeping those combined values
the same. For example, changing these pairs:

```text
base: (prod, x64), (test, arm64)
head: (prod, arm64), (test, x64)
```

changes the runner selection when `runs-on` uses both `${{ matrix.pool }}` and
`${{ matrix.arch }}`. Version 0.0.1 can report `complete / none` for this change.
The same problem affects combinations of a runner group and label. Review these
changes manually when using the 0.0.1 tag or its published full-SHA installation.

Version 0.0.2 preserves each row's label/group combination and
includes the changed targets in WF005 findings. It does not query runner
inventory or prove that a newly selected runner exists or has more authority.
The published 0.0.1 tag remains unchanged.

## Runner/environment associations in 0.0.2 (fix unreleased)

The published 0.0.2 version compares runner and environment selections
independently. It can miss swapping `production` and `staging` between
`ubuntu-latest` and `self-hosted` when both individual sets remain unchanged.

The unreleased WF008 compares resolved runner/environment pairs within supported
static matrix rows. See the [reproduction and boundaries](ASSOCIATION-ANALYSIS.md).
It does not trace secret delivery, inspect remote environment policy or establish
actual runtime access. The published tags and installation pin remain unchanged.

For the broader supported scope, see [README](../README.md#coverage),
[runner/environment policy](CONTEXT-POLICY.md) and [YAML policy](YAML-POLICY.md).
