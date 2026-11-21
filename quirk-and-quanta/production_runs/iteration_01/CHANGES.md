# Production Run 01: Changes
## Milestone: Production Preflight, Container Verification & Security Audit
**Iteration**: 1 of 8  
**Gates Addressed**: P01, P04  

### 1. Code Changes
1. **`rag/server.py`**:
   - Added `host="0.0.0.0"` support and dynamic `PORT` environment variable resolution.
   - Added instant `/healthz` and `/health` probe endpoint (lat < 1ms).
   - Hardened `QuirkHTTPRequestHandler.translate_path` to prevent path traversal outside `SITE_DIR`.
   - Enhanced `/api/rag/status` with honest chunking classification metadata (`"Structural / Heading-Based Section Splitting"`).
2. **`deploy/Dockerfile`**:
   - Changed default `PORT` to `8080` (Cloud Run standard).
   - Changed `EXPOSE 8080 8000`.
   - Updated `HEALTHCHECK` to query `/healthz` via dynamic `PORT`.
   - Changed `CMD ["python3", "rag/server.py"]` to allow runtime port injection.
3. **`scripts/production_smoke_test.py`**:
   - Created comprehensive deployment smoke tester testing startup latency, memory footprint, `/healthz`, `/api/rag/status`, static asset integrity, path traversal isolation, and retrieval pipeline.
