#!/usr/bin/env python3
"""
Quirk & Quanta - 100-Attendee Concurrency & Load Stress Harness
Zero external dependencies (uses standard library threading, urllib.request, and json).

Simulates 100 concurrent attendees in the IDC Workshop:
1. Scenario A: 100 Concurrent Retrieval Queries (POST /api/rag/retrieve)
2. Scenario B: 150 Concurrent Static Asset Bursts (GET /index.html, /workshop.html)
3. Scenario C: Mixed Workshop Traffic (Concurrent API + Static)

Computes empirical p50, p95, p99 latency, throughput (req/sec), and error rate.
Outputs: engineering_runs/run_07/load_test_results.json
"""

import os
import sys
import time
import json
import math
import random
import threading
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Tuple, Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.server import create_server

RUN_07_DIR = os.path.join(ROOT_DIR, "engineering_runs", "run_07")
OUTPUT_FILE = os.path.join(RUN_07_DIR, "load_test_results.json")

SAMPLE_QUESTIONS = [
    "What is the return policy for opened physics kits?",
    "Do you sell quantum levitation desk toys?",
    "Why is my Atomic Orbit Desk Lamp flickering?",
    "Tell me about the Train Schedule Precision Chronometer.",
    "Which products are affected by voltage regulator defects?",
    "What are the specifications of the Borosilicate Beaker Mug?",
    "Is international shipping available for fragile glassware?",
    "Show me products in the Quantum Computing category."
]

SAMPLE_ASSETS = [
    "/index.html",
    "/products.html",
    "/product.html",
    "/about.html",
    "/workshop.html",
    "/css/styles.css",
    "/css/components.css",
    "/js/app.js",
    "/js/catalog.js",
    "/data/products.public.json"
]

def percentile(data: List[float], p: float) -> float:
    if not data:
        return 0.0
    sorted_data = sorted(data)
    idx = (len(sorted_data) - 1) * p
    lower = math.floor(idx)
    upper = math.ceil(idx)
    if lower == upper:
        return sorted_data[int(idx)]
    d0 = sorted_data[int(lower)] * (upper - idx)
    d1 = sorted_data[int(upper)] * (idx - lower)
    return round(d0 + d1, 2)

def compute_stats(latencies_ms: List[float], errors: int, total_time_sec: float) -> Dict[str, Any]:
    total_reqs = len(latencies_ms) + errors
    if not latencies_ms:
        return {
            "totalRequests": total_reqs,
            "successfulRequests": 0,
            "failedRequests": errors,
            "errorRatePercent": 100.0 if total_reqs > 0 else 0.0,
            "throughputReqPerSec": 0.0,
            "latencyMs": {"min": 0, "max": 0, "mean": 0, "p50": 0, "p95": 0, "p99": 0}
        }

    return {
        "totalRequests": total_reqs,
        "successfulRequests": len(latencies_ms),
        "failedRequests": errors,
        "errorRatePercent": round((errors / total_reqs) * 100.0, 2),
        "totalDurationSec": round(total_time_sec, 3),
        "throughputReqPerSec": round(total_reqs / total_time_sec, 2) if total_time_sec > 0 else 0.0,
        "latencyMs": {
            "min": round(min(latencies_ms), 2),
            "max": round(max(latencies_ms), 2),
            "mean": round(sum(latencies_ms) / len(latencies_ms), 2),
            "p50": percentile(latencies_ms, 0.50),
            "p95": percentile(latencies_ms, 0.95),
            "p99": percentile(latencies_ms, 0.99)
        }
    }

SITE_DIR = os.path.join(ROOT_DIR, "site")

from rag.pipeline import RAGPipeline
_shared_pipeline = None

def get_shared_pipeline():
    global _shared_pipeline
    if _shared_pipeline is None:
        _shared_pipeline = RAGPipeline(default_strategy="semantic")
    return _shared_pipeline

def detect_transport(port: int = 8888) -> Tuple[str, Any, str]:
    """
    Detects whether HTTP socket connections are permitted in the current environment.
    Falls back gracefully to in-process concurrent pipeline dispatch if sandboxed.
    """
    base_url = f"http://127.0.0.1:{port}"
    try:
        req = urllib.request.Request(f"{base_url}/api/rag/status", method="GET")
        with urllib.request.urlopen(req, timeout=0.5) as resp:
            if resp.status == 200:
                return "http", None, base_url
    except urllib.error.URLError as e:
        if "Operation not permitted" in str(e) or "Permission denied" in str(e):
            return "in_process", None, "in-process-concurrent"
    except Exception:
        pass

    try:
        server = create_server(port=port)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        time.sleep(0.3)
        req = urllib.request.Request(f"{base_url}/api/rag/status", method="GET")
        with urllib.request.urlopen(req, timeout=0.5) as resp:
            if resp.status == 200:
                return "http", server, base_url
    except Exception:
        pass

    return "in_process", None, "in-process-concurrent"

def send_retrieval_request(transport: str, base_url: str, query: str, method: str = "vector", session_id: str = "default_session") -> Tuple[bool, float, Optional[str]]:
    t0 = time.perf_counter()
    if transport == "in_process":
        try:
            pipeline = get_shared_pipeline()
            res = pipeline.ask(question=query, method=method, retrieval_only=True, top_k=5, strategy="semantic", session_id=session_id)
            latency = (time.perf_counter() - t0) * 1000.0
            if res and "evidence" in res:
                return True, latency, None
            return False, latency, "Invalid retrieval payload"
        except Exception as e:
            latency = (time.perf_counter() - t0) * 1000.0
            return False, latency, str(e)

    # HTTP transport
    url = f"{base_url}/api/rag/retrieve"
    payload = json.dumps({
        "question": query,
        "method": method,
        "topK": 5,
        "strategy": "semantic",
        "sessionId": session_id
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            data = resp.read()
            latency = (time.perf_counter() - t0) * 1000.0
            if resp.status == 200:
                return True, latency, None
            return False, latency, f"HTTP {resp.status}"
    except Exception as e:
        latency = (time.perf_counter() - t0) * 1000.0
        return False, latency, str(e)

def send_static_request(transport: str, base_url: str, asset_path: str) -> Tuple[bool, float, Optional[str]]:
    t0 = time.perf_counter()
    if transport == "in_process":
        try:
            rel_path = asset_path.lstrip("/")
            file_path = os.path.join(SITE_DIR, rel_path)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    _ = f.read()
                latency = (time.perf_counter() - t0) * 1000.0
                return True, latency, None
            latency = (time.perf_counter() - t0) * 1000.0
            return False, latency, f"File not found: {asset_path}"
        except Exception as e:
            latency = (time.perf_counter() - t0) * 1000.0
            return False, latency, str(e)

    # HTTP transport
    url = f"{base_url}{asset_path}"
    req = urllib.request.Request(url, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            data = resp.read()
            latency = (time.perf_counter() - t0) * 1000.0
            if resp.status == 200:
                return True, latency, None
            return False, latency, f"HTTP {resp.status}"
    except Exception as e:
        latency = (time.perf_counter() - t0) * 1000.0
        return False, latency, str(e)

def run_load_test(port: int = 8888, concurrency_rag: int = 100, concurrency_static: int = 150) -> Dict[str, Any]:
    print("=" * 70)
    print("QUIRK & QUANTA - 100-ATTENDEE LOAD TEST HARNESS (GATE G17)")
    print("=" * 70)

    transport, server_inst, base_url = detect_transport(port=port)
    print(f"Transport Mode:     {transport.upper()}")
    print(f"Target Server URL:  {base_url}")
    print(f"Testing Concurrency: {concurrency_rag} RAG requests | {concurrency_static} Static requests\n")

    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "transportMode": transport,
        "targetUrl": base_url,
        "scenarios": {}
    }

    # -------------------------------------------------------------
    # Scenario A: 100 Concurrent Retrieval Queries
    # -------------------------------------------------------------
    print(f"--> [1/3] Executing Scenario A: {concurrency_rag} Concurrent RAG Retrievals...")
    methods = ["vector", "bm25", "hybrid"]
    tasks_a = []
    for i in range(concurrency_rag):
        q = SAMPLE_QUESTIONS[i % len(SAMPLE_QUESTIONS)]
        m = methods[i % len(methods)]
        sid = f"attendee_a_{i:03d}"
        tasks_a.append((q, m, sid))

    t_start = time.perf_counter()
    latencies_a = []
    errors_a = 0
    with ThreadPoolExecutor(max_workers=concurrency_rag) as executor:
        futures = [executor.submit(send_retrieval_request, transport, base_url, q, m, sid) for q, m, sid in tasks_a]
        for f in as_completed(futures):
            ok, lat, err = f.result()
            if ok:
                latencies_a.append(lat)
            else:
                errors_a += 1
                if errors_a <= 3:
                    print(f"    [Error sample]: {err}")

    t_elapsed_a = time.perf_counter() - t_start
    stats_a = compute_stats(latencies_a, errors_a, t_elapsed_a)
    results["scenarios"]["scenario_a_concurrent_retrieval"] = {
        "description": "100 concurrent attendees issuing retrieval queries across Vector, BM25, and Hybrid RRF",
        "concurrency": concurrency_rag,
        **stats_a
    }
    print(f"    Completed in {t_elapsed_a:.2f}s | Success: {stats_a['successfulRequests']}/{concurrency_rag} | "
          f"p50: {stats_a['latencyMs']['p50']}ms | p95: {stats_a['latencyMs']['p95']}ms | "
          f"Throughput: {stats_a['throughputReqPerSec']} req/s | Error Rate: {stats_a['errorRatePercent']}%\n")

    # -------------------------------------------------------------
    # Scenario B: 150 Static Asset Burst
    # -------------------------------------------------------------
    print(f"--> [2/3] Executing Scenario B: {concurrency_static} Concurrent Static Asset Bursts...")
    tasks_b = [SAMPLE_ASSETS[i % len(SAMPLE_ASSETS)] for i in range(concurrency_static)]

    t_start_b = time.perf_counter()
    latencies_b = []
    errors_b = 0
    with ThreadPoolExecutor(max_workers=concurrency_static) as executor:
        futures = [executor.submit(send_static_request, transport, base_url, asset) for asset in tasks_b]
        for f in as_completed(futures):
            ok, lat, err = f.result()
            if ok:
                latencies_b.append(lat)
            else:
                errors_b += 1

    t_elapsed_b = time.perf_counter() - t_start_b
    stats_b = compute_stats(latencies_b, errors_b, t_elapsed_b)
    results["scenarios"]["scenario_b_static_assets_burst"] = {
        "description": "150 concurrent attendees loading storefront pages, styles, scripts, and JSON catalog",
        "concurrency": concurrency_static,
        **stats_b
    }
    print(f"    Completed in {t_elapsed_b:.2f}s | Success: {stats_b['successfulRequests']}/{concurrency_static} | "
          f"p50: {stats_b['latencyMs']['p50']}ms | p95: {stats_b['latencyMs']['p95']}ms | "
          f"Throughput: {stats_b['throughputReqPerSec']} req/s | Error Rate: {stats_b['errorRatePercent']}%\n")

    # -------------------------------------------------------------
    # Scenario C: Mixed Traffic (50 API + 50 Static concurrently)
    # -------------------------------------------------------------
    print("--> [3/3] Executing Scenario C: Mixed Workshop Traffic (50 RAG + 50 Static concurrently)...")
    tasks_c = []
    for i in range(50):
        tasks_c.append(("rag", SAMPLE_QUESTIONS[i % len(SAMPLE_QUESTIONS)], "hybrid", f"attendee_c_{i:03d}"))
        tasks_c.append(("static", SAMPLE_ASSETS[i % len(SAMPLE_ASSETS)], None, None))

    random.shuffle(tasks_c)
    t_start_c = time.perf_counter()
    latencies_c = []
    errors_c = 0
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_req = []
        for req_type, arg1, arg2, arg3 in tasks_c:
            if req_type == "rag":
                future_to_req.append(executor.submit(send_retrieval_request, transport, base_url, arg1, arg2, arg3))
            else:
                future_to_req.append(executor.submit(send_static_request, transport, base_url, arg1))
        for f in as_completed(future_to_req):
            ok, lat, err = f.result()
            if ok:
                latencies_c.append(lat)
            else:
                errors_c += 1

    t_elapsed_c = time.perf_counter() - t_start_c
    stats_c = compute_stats(latencies_c, errors_c, t_elapsed_c)
    results["scenarios"]["scenario_c_mixed_traffic"] = {
        "description": "100 concurrent requests mixing live hybrid retrieval and static assets",
        "concurrency": 100,
        **stats_c
    }
    print(f"    Completed in {t_elapsed_c:.2f}s | Success: {stats_c['successfulRequests']}/100 | "
          f"p50: {stats_c['latencyMs']['p50']}ms | p95: {stats_c['latencyMs']['p95']}ms | "
          f"Throughput: {stats_c['throughputReqPerSec']} req/s | Error Rate: {stats_c['errorRatePercent']}%\n")

    # Overall Summary
    total_reqs = stats_a["totalRequests"] + stats_b["totalRequests"] + stats_c["totalRequests"]
    total_fails = stats_a["failedRequests"] + stats_b["failedRequests"] + stats_c["failedRequests"]
    results["summary"] = {
        "totalWorkshopRequestsExecuted": total_reqs,
        "totalFailures": total_fails,
        "overallErrorRatePercent": round((total_fails / total_reqs) * 100.0, 2),
        "staticP95Ms": stats_b["latencyMs"]["p95"],
        "retrievalP95Ms": stats_a["latencyMs"]["p95"],
        "verdict": "PASS" if total_fails == 0 and stats_b["latencyMs"]["p95"] < 200.0 and stats_a["latencyMs"]["p95"] < 3500.0 else "FAIL"
    }

    os.makedirs(RUN_07_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("=" * 70)
    print(f"LOAD TEST VERDICT: {results['summary']['verdict']}")
    print(f"Total Requests: {total_reqs} | Total Failures: {total_fails} | Error Rate: {results['summary']['overallErrorRatePercent']}%")
    print(f"Results saved to: {OUTPUT_FILE}")
    print("=" * 70)

    if server_inst:
        server_inst.shutdown()

    return results

if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    run_load_test(port=port_arg)
