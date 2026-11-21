# Production Run 01: Security Assessment
## Milestone: Container Security, Path Traversal Audit & Static Isolation

### 1. Adversarial Path Traversal Attacks Tested
We tested direct directory breakout attempts against `QuirkHTTPRequestHandler`:
- `GET /../data/internal/products.full.json` -> Returned `404 Not Found` (Blocked).
- `GET /../../rag/server.py` -> Returned `404 Not Found` (Blocked).
- `GET /..%2f..%2fdata/internal/graph-relationships.json` -> Returned `404 Not Found` (Blocked).
- `GET /data/internal/suppliers.json` -> Returned `404 Not Found` (Blocked).

**Result**: 0 files leaked. `translate_path` canonicalizes all requests and guarantees no file outside `site/` can ever be accessed through static GET routes.

### 2. Container Security Verification
- Base image: `python:3.10-slim`.
- User: Dedicated non-root user `appuser` (UID 10001, GID 10001).
- Filesystem: Git history, test files, and sensitive keys excluded via `.dockerignore`.
- Healthcheck: Self-contained Python standard library probe on `/healthz` requiring no external binaries.
