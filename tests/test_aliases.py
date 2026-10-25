import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from privilege_check.scan import compare
from privilege_check.sources import Snapshot

WF = ".github/workflows/ci.yml"


def _run(base_text, head_text):
    base = Snapshot("b", {WF: base_text})
    head = Snapshot("h", {WF: head_text})
    r = compare(base, head)
    return r["analysis"], sorted({f["rule"] for f in r["findings"]})


class AliasTests(unittest.TestCase):
    def test_anchor_workflow_is_analyzed_and_grant_detected(self):
        base = ("on: push\npermissions: {contents: read}\n"
                "jobs:\n  a: &base\n    runs-on: x\n    steps: [{run: make}]\n  b: *base\n")
        head = ("on: push\npermissions: {contents: read, id-token: write}\n"
                "jobs:\n  a: &base\n    runs-on: x\n    steps: [{run: make}]\n  b: *base\n")
        analysis, rules = _run(base, head)
        self.assertEqual(analysis, "complete")
        self.assertIn("WF001", rules)

    def test_unchanged_anchors_are_neutral(self):
        wf = ("on: push\npermissions: {contents: read}\n"
              "jobs:\n  a: &base\n    runs-on: x\n    steps: [{run: make}]\n  b: *base\n")
        analysis, rules = _run(wf, wf.replace("run: make", "run: build"))
        self.assertEqual(analysis, "complete")
        self.assertEqual(rules, [])

    def test_alias_expansion_bomb_is_bounded_not_hanging(self):
        bomb = (
            "on: push\npermissions: {contents: read}\n"
            "l0: &l0 [z,z,z,z,z,z,z,z,z,z]\n"
            "l1: &l1 [*l0,*l0,*l0,*l0,*l0,*l0,*l0,*l0,*l0,*l0]\n"
            "l2: &l2 [*l1,*l1,*l1,*l1,*l1,*l1,*l1,*l1,*l1,*l1]\n"
            "l3: &l3 [*l2,*l2,*l2,*l2,*l2,*l2,*l2,*l2,*l2,*l2]\n"
            "l4: &l4 [*l3,*l3,*l3,*l3,*l3,*l3,*l3,*l3,*l3,*l3]\n"
            "l5: &l5 [*l4,*l4,*l4,*l4,*l4,*l4,*l4,*l4,*l4,*l4]\n"
            "l6: &l6 [*l5,*l5,*l5,*l5,*l5,*l5,*l5,*l5,*l5,*l5]\n"
            "jobs:\n  a:\n    runs-on: x\n    steps:\n      - run: echo\n        env:\n          BOMB: *l6\n")
        head = bomb.replace("contents: read}", "contents: read, id-token: write}")
        analysis, _ = _run(bomb, head)
        # must terminate with an explicit error, not hang or crash
        self.assertEqual(analysis, "error")


if __name__ == "__main__":
    unittest.main()
