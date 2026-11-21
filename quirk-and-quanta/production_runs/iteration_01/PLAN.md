# Production Run 01: Plan
## Milestone: Production Preflight, Container Verification & Security Audit
**Iteration**: 1 of 8  
**Gates Targeted**: P01 (Reproducible Container Build), P04 (All Storefront Pages and Assets Functional)

### 1. Action 1: Inspect
- Baseline commit: `0c83696`
- Container file: `deploy/Dockerfile`
- Server startup: `rag/server.py`
- Discovered risks:
  - `Dockerfile` hardcoded `"8000"` in CMD, which breaks Cloud Run's dynamic `$PORT` injection.
  - Server did not bind explicitly to `0.0.0.0` or read `PORT` env var.
  - Static file handler needed explicit directory boundary enforcement to prevent path traversal into `data/internal/`.
  - Fast liveness probe (`/healthz`) was absent.

### 2. Action 2: Decide
- Update `rag/server.py` to:
  - Dynamically read `PORT` from environment (`PORT=8080` default for Cloud Run).
  - Bind to `0.0.0.0`.
  - Add `/healthz` fast liveness probe endpoint (< 2ms).
  - Harden `QuirkHTTPRequestHandler.translate_path` to strictly restrict files to `SITE_DIR`.
  - Add honest chunking labeling for structural vs semantic splitting.
- Update `deploy/Dockerfile` to remove hardcoded port from `CMD`, expose `8080 8000`, and set `/healthz` healthcheck.
- Build and execute `scripts/production_smoke_test.py`.
