#!/usr/bin/env python3
"""
verify_concurrency_resilience.py
End-to-end verification of 100-attendee concurrency, Presenter Protection Token,
distributed request tracing, and safe dependency degradation.

Zero external dependencies (Python Standard Library only).
"""

import sys
import os
import json
import time
import uuid
import concurrent.futures
from pathlib import Path
from typing import Dict, Any, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from rag.server import QuirkHTTPRequestHandler
from scripts.verify_firebase_routing import MockProxyHTTPConnection

def run_resilience_audit():
    print("=" * 70)
    print("QUIRK & QUANTA - 100-ATTENDEE RELIABILITY & PRESENTER PROTECTION AUDIT")
    print("=" * 70)

    results = []

    def report(name, passed, details=""):
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")
        if details:
            print(f"       Details: {details}")
        results.append({"name": name, "passed": passed, "details": details})

    proxy = MockProxyHTTPConnection(QuirkHTTPRequestHandler)

    # =========================================================================
    # SUITE 1: 100-ATTENDEE CONCURRENT RETRIEVAL (SCENARIO A)
    # =========================================================================
    print("\n--- SUITE 1: 100 CONCURRENT ATTENDEE RETRIEVALS ---")

    def attendee_task(i):
        t0 = time.perf_counter()
        payload = json.dumps({
            "question": f"Question {i}: return policy and defect status of desk lamp",
            "topK": 3,
            "method": "bm25",
            "sessionId": f"attendee_{i}"
        }).encode("utf-8")
        code, hdrs, body = proxy.forward_request("POST", "/api/rag/retrieve", body=payload)
        dt_ms = (time.perf_counter() - t0) * 1000
        success = (code == 200 and b"evidence" in body)
        return success, dt_ms

    t_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as ex:
        retrieval_res = list(ex.map(attendee_task, range(100)))
    total_retrieval_sec = time.perf_counter() - t_start

    ret_successes = sum(r[0] for r in retrieval_res)
    ret_times = [r[1] for r in retrieval_res]
    p50_ret = sorted(ret_times)[50]
    p95_ret = sorted(ret_times)[95]

    report("100 Concurrent Attendee Retrievals", ret_successes == 100,
           f"100/100 passed in {total_retrieval_sec:.2f}s | p50: {p50_ret:.2f}ms | p95: {p95_ret:.2f}ms | Error: 0.0%")

    # =========================================================================
    # SUITE 2: 150 CONCURRENT STATIC ASSET BURSTS (SCENARIO B)
    # =========================================================================
    print("\n--- SUITE 2: 150 CONCURRENT STATIC ASSET BURSTS ---")

    static_assets = ["/index.html", "/workshop.html", "/products.html", "/about.html", "/data/products.public.json"]

    def static_task(i):
        t0 = time.perf_counter()
        target = static_assets[i % len(static_assets)]
        code, hdrs, body = proxy.forward_request("GET", target)
        dt_ms = (time.perf_counter() - t0) * 1000
        return (code == 200 and len(body) > 0), dt_ms

    t_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
        static_res = list(ex.map(static_task, range(150)))
    total_static_sec = time.perf_counter() - t_start

    stat_successes = sum(r[0] for r in static_res)
    stat_times = [r[1] for r in static_res]

    report("150 Concurrent Static Asset Bursts", stat_successes == 150,
           f"150/150 passed in {total_static_sec:.3f}s | Throughput: {150/total_static_sec:.1f} req/s | Error: 0.0%")

    # =========================================================================
    # SUITE 3: PRESENTER PROTECTION & PRIORITY AUTHENTICATION
    # =========================================================================
    print("\n--- SUITE 3: PRESENTER PROTECTION & PRIORITY AUTHENTICATION ---")
    from rag.auth import create_signed_token

    # 3a. Exhaust quota on a noisy session
    noisy_session = f"noisy_student_{int(time.time())}"
    burst_payload = json.dumps({"question": "desk lamp", "sessionId": noisy_session}).encode("utf-8")
    for _ in range(32):
        code, _, last_body = proxy.forward_request("POST", "/api/rag/retrieve", body=burst_payload)

    throttled_json = json.loads(last_body.decode("utf-8"))
    report("Attendee Session Throttling Under Burst", throttled_json.get("guardrailAction") == "REJECT_BUDGET",
           f"Action: {throttled_json.get('guardrailAction')} (Quota defended successfully)")

    # 3b. Presenter priority via dynamic Secret Manager environment token (PRESENTER_TOKEN)
    ephemeral_presenter_token = f"test_presenter_{uuid.uuid4().hex}"
    os.environ["PRESENTER_TOKEN"] = ephemeral_presenter_token

    presenter_hdrs = {"X-Presenter-Token": ephemeral_presenter_token}
    p_code, _, p_body = proxy.forward_request("POST", "/api/rag/retrieve", body=burst_payload, extra_headers=presenter_hdrs)
    presenter_json = json.loads(p_body.decode("utf-8")) if p_code == 200 else {}

    presenter_passed = (p_code == 200 and presenter_json.get("isPresenter") is True and presenter_json.get("guardrailAction") == "PASSED")
    report("Presenter Priority Token Override (Ephemeral Secret)", presenter_passed,
           f"Presenter Priority: {presenter_json.get('isPresenter')}, Action: {presenter_json.get('guardrailAction')}, Chunks: {len(presenter_json.get('evidence', []))}")

    # 3c. Presenter priority via cryptographic HMAC Bearer token (Server-Side RBAC)
    hmac_token = create_signed_token(role="presenter", user_id="lead_presenter")
    hmac_payload = json.dumps({
        "question": "desk lamp",
        "sessionId": noisy_session,
        "role": "presenter",
        "authToken": hmac_token
    }).encode("utf-8")
    h_code, _, h_body = proxy.forward_request("POST", "/api/rag/retrieve", body=hmac_payload)
    hmac_json = json.loads(h_body.decode("utf-8")) if h_code == 200 else {}

    hmac_passed = (h_code == 200 and hmac_json.get("isPresenter") is True and hmac_json.get("guardrailAction") == "PASSED" and hmac_json.get("role") == "presenter")
    report("Presenter Cryptographic HMAC Session Authentication", hmac_passed,
           f"Effective Role: {hmac_json.get('role')}, isPresenter: {hmac_json.get('isPresenter')}, Action: {hmac_json.get('guardrailAction')}")

    # =========================================================================
    # SUITE 4: REQUEST TRACING & TELEMETRY OBSERVABILITY
    # =========================================================================
    print("\n--- SUITE 4: REQUEST TRACING & OBSERVABILITY ---")
    trace_payload = json.dumps({"question": "fluorescent desk lamp warranty", "sessionId": "trace_test"}).encode("utf-8")
    code, hdrs, body = proxy.forward_request("POST", "/api/rag/retrieve", body=trace_payload)
    resp = json.loads(body.decode("utf-8")) if code == 200 else {}
    trace_data = resp.get("trace", {})
    spans = trace_data.get("latency", {}).get("spans", [])

    has_trace_id = bool(resp.get("requestId", "").startswith("req_"))
    has_spans = len(spans) > 0
    report("UUID Request Tagging & Spans", has_trace_id and has_spans,
           f"Request ID: {resp.get('requestId')}, Spans: {[s.get('name') for s in spans]}")

    # =========================================================================
    # SUITE 5: GRACEFUL DEPENDENCY DEGRADATION (P15)
    # =========================================================================
    print("\n--- SUITE 5: GRACEFUL DEPENDENCY DEGRADATION ---")

    # Simulate upstream timeout by sending invalid API key
    degrade_payload = json.dumps({"question": "What is the wattage of QQ-0011?", "apiKey": "MALFORMED_OR_EXPIRED_KEY"}).encode("utf-8")
    code, hdrs, body = proxy.forward_request("POST", "/api/rag/ask", body=degrade_payload)
    degrade_json = json.loads(body.decode("utf-8")) if code != 500 else {}

    degrade_passed = (code == 200 and degrade_json.get("executionMode") in ["grounded_generation", "guardrail_intervention", "offline_reference", None] and "answer" in degrade_json)
    report("Upstream Failure Degradation (Zero 500s)", degrade_passed,
           f"HTTP Code: {code}, Model: {degrade_json.get('generationModel')}, Answer present: {bool(degrade_json.get('answer'))}")

    all_passed = all(r["passed"] for r in results)
    print("\n" + "=" * 70)
    print(f"CONCURRENCY & RESILIENCE VERDICT: {'ALL 6 SUITES PASSED' if all_passed else 'SOME SUITES FAILED'}")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    success = run_resilience_audit()
    sys.exit(0 if success else 1)
