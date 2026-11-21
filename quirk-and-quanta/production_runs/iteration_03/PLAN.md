# Iteration 3 Plan: Firebase Hosting Integration, Reverse Proxy Routing & CDN Caching (Gates P03, P05)

## 1. Objectives
- Establish Firebase Hosting integration as the unified public-facing origin for the Quirk & Quanta storefront and workshop dashboard.
- Route all `/api/**` endpoints to Cloud Run backend `quirk-quanta-rag` in `asia-south1`.
- Configure CDN caching rules: 1-year immutable for static assets (`assets/`, `css/`, `js/`), short TTL (300s) for HTML pages, and `no-store` for dynamic RAG API routes.
- Enforce strict security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`.
- Implement `scripts/verify_firebase_routing.py` to validate configuration, proxy headers injection, and end-to-end API forwarding.

## 2. Acceptance Criteria
- `firebase.json` and `.firebaserc` pass programmatic validation.
- All 6-point checks in `scripts/verify_firebase_routing.py` pass.
- Simulated reverse proxy verifies `/healthz`, `/api/rag/status`, `/api/rag/questions`, `/api/rag/retrieve`, and `/api/rag/compare`.
- Path traversal and unauthorized access to `/data/internal/` return 404 through proxy.
