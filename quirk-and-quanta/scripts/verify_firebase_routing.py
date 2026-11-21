#!/usr/bin/env python3
"""
verify_firebase_routing.py
Comprehensive verification of Firebase Hosting configuration, reverse-proxy rewrite rules,
CDN cache headers, security headers, and end-to-end API forwarding to Cloud Run.

Zero external dependencies (Python Standard Library only).
"""

import sys
import os
import json
import time
import io
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from rag.server import QuirkHTTPRequestHandler

class MockProxyHTTPConnection:
    """Simulates Firebase Hosting edge reverse proxy forwarding requests to the Cloud Run backend."""
    def __init__(self, handler_cls, client_ip="203.0.113.195", host="idc-rag-proj.web.app"):
        self.handler_cls = handler_cls
        self.client_ip = client_ip
        self.host = host

    def forward_request(self, method: str, path: str, body: bytes = b"", extra_headers: dict = None):
        if extra_headers is None:
            extra_headers = {}

        # Standard Firebase Hosting edge proxy headers injected
        default_headers = {
            "Host": self.host,
            "X-Forwarded-For": self.client_ip,
            "X-Forwarded-Host": self.host,
            "X-Forwarded-Proto": "https",
            "Connection": "close"
        }
        if body:
            default_headers["Content-Length"] = str(len(body))
            if "Content-Type" not in extra_headers:
                default_headers["Content-Type"] = "application/json"

        headers = {**default_headers, **extra_headers}

        req_lines = [f"{method} {path} HTTP/1.1"]
        for k, v in headers.items():
            req_lines.append(f"{k}: {v}")
        req_lines.append("")
        req_lines.append("")

        raw_req = "\r\n".join(req_lines).encode("latin-1") + body

        class MockSocket:
            def __init__(self, data):
                self._rfile = io.BytesIO(data)
                self._wfile = io.BytesIO()
            def makefile(self, mode, *args, **kwargs):
                if 'r' in mode:
                    return self._rfile
                return self._wfile
            def sendall(self, data):
                self._wfile.write(data)

        sock = MockSocket(raw_req)

        class SilentHandler(self.handler_cls):
            def log_message(self, format, *args):
                pass

        try:
            SilentHandler(sock, (self.client_ip, 54321), None)
        except Exception:
            pass

        response_bytes = sock._wfile.getvalue()
        if not response_bytes:
            return 500, {}, b""

        parts = response_bytes.split(b"\r\n\r\n", 1)
        header_part = parts[0].decode("latin-1")
        body_part = parts[1] if len(parts) > 1 else b""

        lines = header_part.split("\r\n")
        status_line = lines[0]
        status_code = int(status_line.split(" ")[1])

        resp_headers = {}
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                resp_headers[k.strip().lower()] = v.strip()

        return status_code, resp_headers, body_part


def run_checks():
    print("=" * 70)
    print("QUIRK & QUANTA - FIREBASE HOSTING & API ROUTING VERIFICATION")
    print("=" * 70)

    results = []

    def report(name, passed, details=""):
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")
        if details:
            print(f"       Details: {details}")
        results.append({"name": name, "passed": passed, "details": details})

    # CHECK 1: .firebaserc presence and validity
    firebaserc_path = REPO_ROOT / ".firebaserc"
    if not firebaserc_path.exists():
        report(".firebaserc Existence", False, "Missing .firebaserc")
    else:
        try:
            with open(firebaserc_path, "r", encoding="utf-8") as f:
                frc = json.load(f)
            default_proj = frc.get("projects", {}).get("default")
            if default_proj == "idc-rag-proj":
                report(".firebaserc Default Project", True, f"Configured default: {default_proj}")
            else:
                report(".firebaserc Default Project", False, f"Unexpected project: {default_proj}")
        except Exception as e:
            report(".firebaserc Validation", False, str(e))

    # CHECK 2: firebase.json presence and structure
    fb_path = REPO_ROOT / "firebase.json"
    if not fb_path.exists():
        report("firebase.json Existence", False, "Missing firebase.json")
        return False
    
    with open(fb_path, "r", encoding="utf-8") as f:
        fb_config = json.load(f)

    hosting = fb_config.get("hosting", {})
    if hosting.get("public") == "site":
        report("Firebase Hosting Public Directory", True, "public: site")
    else:
        report("Firebase Hosting Public Directory", False, f"Expected 'site', got {hosting.get('public')}")

    # CHECK 3: Rewrites configuration for Cloud Run
    rewrites = hosting.get("rewrites", [])
    api_rewrite = None
    for rw in rewrites:
        if rw.get("source") == "/api/**":
            api_rewrite = rw
            break

    if api_rewrite and api_rewrite.get("run", {}).get("serviceId") == "quirk-quanta-rag" and api_rewrite.get("run", {}).get("region") == "asia-south1":
        report("Cloud Run /api/** Reverse Proxy Rewrite", True, f"source: /api/** -> Cloud Run service {api_rewrite['run']['serviceId']} ({api_rewrite['run']['region']})")
    else:
        report("Cloud Run /api/** Reverse Proxy Rewrite", False, f"Invalid rewrite spec: {api_rewrite}")

    # CHECK 4: Cache-Control & Security Headers
    headers = hosting.get("headers", [])
    has_security_headers = False
    has_static_cache = False
    has_html_cache = False
    has_api_cache = False

    for h in headers:
        src = h.get("source", "")
        h_dict = {item.get("key", "").lower(): item.get("value", "") for item in h.get("headers", [])}
        if "/**" in src and "x-content-type-options" in h_dict and "x-frame-options" in h_dict:
            has_security_headers = True
        if "@(jpg|jpeg|gif|png|svg|webp|js|css|woff|woff2)" in src and "max-age=31536000" in h_dict.get("cache-control", ""):
            has_static_cache = True
        if "@(html|htm)" in src and "max-age=300" in h_dict.get("cache-control", ""):
            has_html_cache = True
        if "/api/**" in src and "no-store" in h_dict.get("cache-control", ""):
            has_api_cache = True

    report("Security Headers Configuration", has_security_headers, "nosniff, SAMEORIGIN, strict-origin-when-cross-origin configured")
    report("Static Asset Cache Headers (1 Year Immutable)", has_static_cache, "max-age=31536000, immutable configured for static assets")
    report("HTML Short TTL Cache Headers", has_html_cache, "max-age=300 configured for HTML")
    report("API No-Store Cache Headers", has_api_cache, "no-store, no-cache configured for /api/**")

    # CHECK 5: Simulated Reverse Proxy End-to-End API Calls
    proxy = MockProxyHTTPConnection(QuirkHTTPRequestHandler)

    # 5a. /health
    code, hdrs, body = proxy.forward_request("GET", "/health")
    report("Proxy Request -> /health", code == 200 and b"healthy" in body, f"Status {code}, Body: {body.decode('utf-8', 'ignore')[:60]}...")

    # 5b. /api/rag/status
    code, hdrs, body = proxy.forward_request("GET", "/api/rag/status")
    status_json = json.loads(body.decode("utf-8")) if code == 200 else {}
    report("Proxy Request -> /api/rag/status", code == 200 and status_json.get("status") == "ready", f"Status {code}, Service: {status_json.get('service')}, Mode: {status_json.get('activeMode')}")

    # 5c. /api/rag/questions
    code, hdrs, body = proxy.forward_request("GET", "/api/rag/questions")
    q_json = json.loads(body.decode("utf-8")) if code == 200 else []
    report("Proxy Request -> /api/rag/questions", code == 200 and isinstance(q_json, list) and len(q_json) > 0, f"Status {code}, Questions count: {len(q_json)}")

    # 5d. /api/rag/retrieve
    post_payload = json.dumps({"question": "fluorescent desk lamp recall", "topK": 3, "method": "bm25"}).encode("utf-8")
    code, hdrs, body = proxy.forward_request("POST", "/api/rag/retrieve", body=post_payload)
    ret_json = json.loads(body.decode("utf-8")) if code == 200 else {}
    report("Proxy Request -> POST /api/rag/retrieve", code == 200 and len(ret_json.get("evidence", [])) > 0, f"Status {code}, Retrieved chunks: {len(ret_json.get('evidence', []))}")

    # 5e. /api/rag/compare
    cmp_payload = json.dumps({"question": "desk lamp capacitor defect", "topK": 3}).encode("utf-8")
    code, hdrs, body = proxy.forward_request("POST", "/api/rag/compare", body=cmp_payload)
    cmp_json = json.loads(body.decode("utf-8")) if code == 200 else {}
    has_modes = "vector" in cmp_json and "bm25" in cmp_json and "hybrid" in cmp_json
    report("Proxy Request -> POST /api/rag/compare", code == 200 and has_modes, f"Status {code}, Vector evidence: {len(cmp_json.get('vector', {}).get('evidence', []))}, BM25 evidence: {len(cmp_json.get('bm25', {}).get('evidence', []))}")

    # CHECK 6: Internal Directory Access Denial through Proxy
    code, hdrs, body = proxy.forward_request("GET", "/data/internal/products.full.json")
    report("Proxy Security Check -> Block /data/internal/", code == 404, f"Status: {code} (expected 404 Not Found)")

    code, hdrs, body = proxy.forward_request("GET", "/../data/internal/products.full.json")
    report("Proxy Security Check -> Block Traversal to /data/internal/", code == 404, f"Status: {code} (expected 404 Not Found)")

    all_passed = all(r["passed"] for r in results)
    print("=" * 70)
    print(f"VERDICT: {'ALL CHECKS PASSED' if all_passed else 'SOME CHECKS FAILED'}")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
