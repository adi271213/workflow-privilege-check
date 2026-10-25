import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from privilege_check.scan import compare
from privilege_check.sources import Snapshot
WF = ".github/workflows/ci.yml"

def _run(b, h):
    r = compare(Snapshot("b", {WF: b}), Snapshot("h", {WF: h}))
    return r, sorted({(f["rule"], f["severity"]) for f in r["findings"]})

class SeverityTests(unittest.TestCase):
    def test_read_increase_is_info_not_review(self):
        r, f = _run("on: push\npermissions: {issues: none}\njobs:\n  a: {runs-on: x, steps: [{run: m}]}\n",
                    "on: push\npermissions: {issues: read}\njobs:\n  a: {runs-on: x, steps: [{run: m}]}\n")
        self.assertEqual(r["analysis"], "complete")
        self.assertIn(("WF001", "info"), f)
        self.assertEqual(r["review"], "none")   # read increase does not force review

    def test_write_increase_is_review(self):
        r, f = _run("on: push\npermissions: {contents: read}\njobs:\n  a: {runs-on: x, steps: [{run: m}]}\n",
                    "on: push\npermissions: {contents: write}\njobs:\n  a: {runs-on: x, steps: [{run: m}]}\n")
        self.assertIn(("WF001", "review"), f)
        self.assertEqual(r["review"], "suggested")

    def test_id_token_is_review(self):
        r, f = _run("on: push\npermissions: {contents: read}\njobs:\n  a: {runs-on: x, steps: [{run: m}]}\n",
                    "on: push\npermissions: {contents: read, id-token: write}\njobs:\n  a: {runs-on: x, steps: [{run: m}]}\n")
        self.assertIn(("WF001", "review"), f)
        self.assertEqual(r["review"], "suggested")

if __name__ == "__main__":
    unittest.main()
