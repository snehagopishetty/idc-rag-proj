#!/usr/bin/env python3
"""
Quirk & Quanta - Security, RBAC & IDOR Test Suite
Tests HMAC session token generation, verification, client role tampering prevention,
confidential cost leakage mitigation, and IDOR protection.
"""

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.auth import (
    create_signed_token,
    verify_token,
    resolve_effective_role,
    check_resource_access
)
from rag.pipeline import RAGPipeline

class TestSecurityAndRBAC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = RAGPipeline(default_strategy="semantic")

    def test_hmac_token_lifecycle(self):
        token = create_signed_token(role="admin", user_id="test_admin", expiry_seconds=300)
        self.assertIn(".", token)
        payload = verify_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["role"], "admin")
        self.assertEqual(payload["userId"], "test_admin")

    def test_forged_token_rejected(self):
        valid_token = create_signed_token(role="admin", user_id="test_admin")
        parts = valid_token.split(".")
        # Tamper with the signature
        tampered_token = f"{parts[0]}.deadbeef00112233"
        self.assertIsNone(verify_token(tampered_token))

    def test_client_role_tampering_downgraded_in_hardened_mode(self):
        # Client claims role='admin' without a signed token
        role, was_tampered, msg = resolve_effective_role(
            requested_role="admin",
            auth_token=None,
            hardened=True
        )
        self.assertEqual(role, "customer")
        self.assertTrue(was_tampered)
        self.assertIn("SECURITY ROLE TAMPERING DETECTED", msg)

    def test_authenticated_admin_accepted_in_hardened_mode(self):
        token = create_signed_token(role="admin", user_id="dr_arthur")
        role, was_tampered, msg = resolve_effective_role(
            requested_role="admin",
            auth_token=token,
            hardened=True
        )
        self.assertEqual(role, "admin")
        self.assertFalse(was_tampered)
        self.assertIn("dr_arthur", msg)

    def test_vulnerable_mode_accepts_unverified_role(self):
        # In vulnerable demonstration mode, unauthenticated escalation succeeds
        role, was_tampered, msg = resolve_effective_role(
            requested_role="admin",
            auth_token=None,
            hardened=False
        )
        self.assertEqual(role, "admin")
        self.assertFalse(was_tampered)
        self.assertIn("VULNERABLE MODE ACTIVE", msg)

    def test_confidential_cost_leakage_prevented_for_customer(self):
        cost_query = "What is the supplier acquisition cost and profit margin for QQ-0001?"
        # Run as customer without token
        res = self.pipeline.ask(cost_query, role="customer", hardened=True)
        # Check that no evidence has accessLevel != 'public'
        for chunk in res["evidence"]:
            self.assertEqual(chunk["accessLevel"], "public")
            self.assertNotIn("wholesale acquisition cost", chunk["text"].lower())

    def test_confidential_cost_accessible_to_authenticated_admin(self):
        cost_query = "What is the supplier acquisition cost and profit margin for QQ-0001?"
        admin_token = create_signed_token(role="admin", user_id="dr_arthur")
        res = self.pipeline.ask(cost_query, role="admin", auth_token=admin_token, hardened=True)
        internal_found = any(c.get("accessLevel") != "public" for c in res["evidence"])
        self.assertTrue(internal_found, "Authenticated admin should retrieve internal procurement records")

    def test_idor_direct_access_control(self):
        # Customer trying to access internal procurement doc
        allowed_cust, msg_cust = check_resource_access(
            doc_id="PROC-QQ-0001",
            role="customer",
            doc_access_level="internal_procurement"
        )
        self.assertFalse(allowed_cust)
        self.assertIn("IDOR ACCESS VIOLATION", msg_cust)

        # Admin granted access
        allowed_admin, msg_admin = check_resource_access(
            doc_id="PROC-QQ-0001",
            role="admin",
            doc_access_level="internal_procurement"
        )
        self.assertTrue(allowed_admin)

if __name__ == "__main__":
    unittest.main()
