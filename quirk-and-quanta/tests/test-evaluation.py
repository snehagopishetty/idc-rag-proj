#!/usr/bin/env python3
"""
Quirk & Quanta - Golden Dataset & Evaluation Integrity Test Suite
Validates dataset completeness, unique IDs, entity references, schema compliance,
and comparative metric computations (Dr. Boon's Evaluation Benchmark).
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

EVAL_DIR = os.path.join(ROOT_DIR, "data", "evaluation")

class TestGoldenDatasetIntegrity(unittest.TestCase):
    def setUp(self):
        self.dataset_path = os.path.join(EVAL_DIR, "golden_dataset.json")
        self.baseline_path = os.path.join(EVAL_DIR, "golden_dataset_baseline_v1.json")
        self.assertTrue(os.path.exists(self.dataset_path), "golden_dataset.json must exist")
        self.assertTrue(os.path.exists(self.baseline_path), "golden_dataset_baseline_v1.json must exist")

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            self.cases = json.load(f)
        with open(self.baseline_path, "r", encoding="utf-8") as f:
            self.baseline_cases = json.load(f)

    def test_baseline_cases_frozen_and_preserved(self):
        self.assertEqual(len(self.baseline_cases), 22, "Baseline v1 dataset must retain exact 22 test cases")
        # Check that first 22 cases in current dataset match baseline IDs
        for i in range(22):
            self.assertEqual(self.cases[i]["id"], self.baseline_cases[i]["id"])
            self.assertEqual(self.cases[i]["question"], self.baseline_cases[i]["question"])

    def test_target_dataset_size(self):
        # Section H requirement: Target at least 40 total curated cases
        self.assertGreaterEqual(len(self.cases), 40, f"Dataset must contain >= 40 cases, found {len(self.cases)}")

    def test_unique_test_ids(self):
        ids = [c["id"] for c in self.cases]
        self.assertEqual(len(ids), len(set(ids)), "All test case IDs must be unique")

    def test_schema_compliance_and_required_fields(self):
        required_fields = ["id", "family", "question", "expectedBehavior", "expectedAnswer", "authorizedRoles"]
        for c in self.cases:
            for field in required_fields:
                self.assertIn(field, c, f"Test case {c.get('id')} missing required field: {field}")
            self.assertGreater(len(c["question"].strip()), 5, f"Question for {c['id']} is too short")
            self.assertGreater(len(c["expectedAnswer"].strip()), 5, f"Expected answer for {c['id']} is too short")

    def test_film_defect_cases_present(self):
        # Check presence of EVAL-023
        case_23 = next((c for c in self.cases if c["id"] == "EVAL-023"), None)
        self.assertIsNotNone(case_23)
        self.assertIn("QQ-0011", case_23["question"])
        self.assertIn("QQ-0074", case_23["question"])
        self.assertIn("QQ-0049", case_23["question"])
        self.assertIn("COMP-025", case_23["expectedEntities"])
        self.assertIn("REC-VREG-01", case_23["expectedEntities"])

    def test_security_cases_present(self):
        families = set(c["family"] for c in self.cases)
        self.assertIn("pirate_direct_injection", families)
        self.assertIn("scope_boundary_coding", families)
        self.assertIn("confidential_cost_leakage", families)
        self.assertIn("client_role_tampering", families)
        self.assertIn("idor_resource_access", families)
        self.assertIn("grounded_abstention", families)

if __name__ == "__main__":
    unittest.main()
