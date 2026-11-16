"""Reject policy bypasses and unverifiable inventory declarations."""
import copy
import json
from pathlib import Path
import unittest

from protocol_compatibility import validate_inventory

ROOT = Path(__file__).resolve().parent.parent
REPOSITORIES = {"true-line/agent-bot-hq", "true-line/soul-contracts"}


class InventoryGateTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "registry/protocol-compatibility.json").read_text())

    def test_reviewed_inventory_requires_an_accepted_decision(self):
        self.assertEqual(validate_inventory(self.data, "Accepted", REPOSITORIES), [])
        for status in [None, "Proposed", "Superseded"]:
            with self.subTest(status=status):
                self.assertTrue(validate_inventory(self.data, status, REPOSITORIES))

    def test_bootstrap_approval_cannot_authorize_other_version_histories(self):
        for versions in [dict(current_major=2),
                         dict(first_supported_major=2, current_major=2),
                         dict(previous_supported_major=0),
                         dict(current_major=True), dict(first_supported_major=True)]:
            with self.subTest(versions=versions):
                data = copy.deepcopy(self.data)
                data["protocols"]["hq"].update(versions)
                self.assertTrue(validate_inventory(data, "Accepted", REPOSITORIES))

    def test_unverifiable_or_redirected_evidence_refuses(self):
        for field, value in [("repository", "other/repo"), ("commit", "main"),
                             ("sha256", ""), ("path", ""), ("path", "."),
                             ("path", "../secret"), ("path", "/etc/passwd"),
                             ("path", "sdk/file.mjs?ref=other"), ("path", "sdk/file.mjs#fragment"),
                             ("path", "sdk/%2e%2e/file.mjs"), ("path", "sdk/file name.mjs"),
                             ("path", "sdk/../file.mjs"), ("path", "sdk\\file.mjs")]:
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data)
                data["protocols"]["wire"]["evidence"][0][field] = value
                self.assertTrue(validate_inventory(data, "Accepted", REPOSITORIES))

    def test_missing_family_or_source_does_not_imply_inapplicability(self):
        for mutation in [lambda d: d["protocols"].pop("hq"),
                         lambda d: d["protocols"]["hq"].update(evidence=[]),
                         lambda d: d.update(decision_path="docs/other.md")]:
            data = copy.deepcopy(self.data)
            mutation(data)
            self.assertTrue(validate_inventory(data, "Accepted", REPOSITORIES))
