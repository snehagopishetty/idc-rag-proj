#!/usr/bin/env python3
"""
verify_public_security_gate.py
Explicit verification harness for the Quirk & Quanta Public Access Security Gate.

Tests:
1. Public users cannot mint privileged HMAC sessions (/api/rag/auth/demo-token blocked with 403).
2. Authenticated presenter CAN mint privileged HMAC sessions when presenting valid PRESENTER_TOKEN.
3. Anonymous users cannot access internal procurement records via /api/rag/doc.
4. Anonymous users attempting role escalation (role='admin' or 'procurement') are downgraded to customer.
5. Public client cannot activate genuinely vulnerable security modes (hardened=False cannot bypass IDOR/RBAC).
6. Directory traversal attempts on docId are blocked.
7. Anonymous inference requests are bound by per-session rate limits (30 req/min).
8. Presenter bypass cannot disable global spending safeguards.
"""

import os
import sys
import json
import uuid
import hmac
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from rag.server import QuirkHTTPRequestHandler
from scripts.verify_firebase_routing import MockProxyHTTPConnection
from rag.auth import create_signed_token, resolve_effective_role, check_resource_access
from rag.guardrails import GuardrailsEngine

def run_gate_audit():
    print("=" * 75)
    print("QUIRK & QUANTA - PUBLIC ACCESS SECURITY GATE AUDIT")
    print("=" * 75)

    proxy = MockProxyHTTPConnection(QuirkHTTPRequestHandler)
    ephemeral_secret = f"gate_secret_{uuid.uuid4().hex}"
    os.environ["PRESENTER_TOKEN"] = ephemeral_secret

    passed_count = 0
    total_count = 8

    def report(num, name, condition, details=""):
        nonlocal passed_count
        status = "PASS" if condition else "FAIL"
        if condition:
            passed_count += 1
        print(f"[{status}] Check {num}: {name}")
        if details:
            print(f"       Details: {details}")

    # 1. Public users cannot mint privileged HMAC sessions
    code, _, body = proxy.forward_request("GET", "/api/rag/auth/demo-token")
    resp = json.loads(body.decode("utf-8")) if code != 500 else {}
    report(1, "Public Cannot Mint Privileged HMAC Sessions", code == 403 and resp.get("status") == 403,
           f"HTTP Status: {code}, Message: {resp.get('message')}")

    # 2. Presenter with Secret Manager token CAN mint token
    pres_hdrs = {"X-Presenter-Token": ephemeral_secret}
    p_code, _, p_body = proxy.forward_request("GET", "/api/rag/auth/demo-token", extra_headers=pres_hdrs)
    p_resp = json.loads(p_body.decode("utf-8")) if p_code == 200 else {}
    report(2, "Authorized Presenter Token Minting", p_code == 200 and p_resp.get("role") == "admin" and "token" in p_resp,
           f"HTTP Status: {p_code}, Issued Role: {p_resp.get('role')}, User: {p_resp.get('userId')}")

    # 3. Anonymous users cannot access internal procurement records
    doc_payload = json.dumps({"docId": "PROC-QQ-0011", "role": "customer"}).encode("utf-8")
    d_code, _, d_body = proxy.forward_request("POST", "/api/rag/doc", body=doc_payload)
    d_resp = json.loads(d_body.decode("utf-8")) if d_code != 500 else {}
    report(3, "Anonymous Access to Internal Procurement Blocked", d_code == 403 and d_resp.get("effectiveRole") == "customer",
           f"HTTP Status: {d_code}, Alert: {d_resp.get('securityAlert')}")

    # 4. Role escalation without valid token demoted to customer
    tamper_payload = json.dumps({"docId": "PROC-QQ-0011", "role": "admin"}).encode("utf-8")
    t_code, _, t_body = proxy.forward_request("POST", "/api/rag/doc", body=tamper_payload)
    t_resp = json.loads(t_body.decode("utf-8")) if t_code != 500 else {}
    report(4, "Role Escalation Downgraded to Customer", t_code == 403 and t_resp.get("wasTampered") is True and t_resp.get("effectiveRole") == "customer",
           f"HTTP Status: {t_code}, wasTampered: {t_resp.get('wasTampered')}, effectiveRole: {t_resp.get('effectiveRole')}")

    # 5. Public client cannot activate genuinely vulnerable security modes
    vuln_payload = json.dumps({"docId": "PROC-QQ-0011", "role": "admin", "hardened": False}).encode("utf-8")
    v_code, _, v_body = proxy.forward_request("POST", "/api/rag/doc", body=vuln_payload)
    v_resp = json.loads(v_body.decode("utf-8")) if v_code != 500 else {}
    report(5, "Unhardened Flag Cannot Bypass Security Boundary", v_code == 403 and v_resp.get("wasTampered") is True,
           f"HTTP Status: {v_code}, wasTampered: {v_resp.get('wasTampered')}, effectiveRole: {v_resp.get('effectiveRole')}")

    # 6. Path traversal in docId is blocked
    trav_payload = json.dumps({"docId": "../../../data/internal/suppliers", "role": "admin"}).encode("utf-8")
    tr_code, _, tr_body = proxy.forward_request("POST", "/api/rag/doc", body=trav_payload)
    report(6, "Directory Traversal in docId Blocked", tr_code in [403, 404],
           f"HTTP Status: {tr_code} (Directory traversal prevented)")

    # 7. Anonymous inference requests bound by rate limits
    noisy_sess = f"noisy_anon_{uuid.uuid4().hex[:8]}"
    burst = json.dumps({"question": "desk lamp warranty", "sessionId": noisy_sess}).encode("utf-8")
    for _ in range(32):
        proxy.forward_request("POST", "/api/rag/retrieve", body=burst)
    l_code, _, l_body = proxy.forward_request("POST", "/api/rag/retrieve", body=burst)
    l_resp = json.loads(l_body.decode("utf-8"))
    report(7, "Anonymous Session Rate Limiting Enforced", l_resp.get("guardrailAction") == "REJECT_BUDGET",
           f"Action: {l_resp.get('guardrailAction')}, Reason: {l_resp.get('reason')}")

    # 8. Presenter bypass cannot disable global spending safeguards
    guard = GuardrailsEngine()
    guard.global_tokens_total = guard.max_global_tokens + 1  # Simulate global spending ceiling reached
    pres_allowed, pres_err = guard.check_presenter_budget("test_presenter")
    report(8, "Presenter Bounded by Global Spending Safeguard", pres_allowed is False and "Global service spending safeguard" in pres_err,
           f"Presenter Allowed: {pres_allowed}, Safeguard: {pres_err}")

    print("=" * 75)
    print(f"SECURITY GATE VERDICT: {passed_count}/{total_count} CHECKS PASSED")
    print("=" * 75)
    return passed_count == total_count

if __name__ == "__main__":
    success = run_gate_audit()
    sys.exit(0 if success else 1)
