# Bundled Action dependency

The Action uses the unmodified pure-Python files of PyYAML 6.0.3 in `pyyaml/`.
Its MIT license and per-file SHA-256 manifest are included. The manifest records
the published upstream wheel URL and verified SHA-256. The optional compiled
extension is omitted; the scanner already uses Python SafeLoader subclasses.

The pinned Action verifies these files before starting the isolated scanner. It
creates no venv and invokes no pip, dependency index, installer or download.
Python 3.11+ and Git must exist on the runner. Downloading the Action and fetching
Git objects are installation operations and can still require network access.

To refresh the current bundle, run `python scripts/vendor_pyyaml.py`. Updating the
dependency version requires selecting and reviewing the upstream release and
published wheel digest, updating the script's source pin, then reviewing the new
license/manifest and running the full Python matrix and offline smoke test.
No constant startup-time promise is made.
