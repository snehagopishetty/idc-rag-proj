# Iteration 3 Operations Report

## Firebase Edge Proxy and CDN Architecture
- **Unified Domain**: `https://idc-rag-proj.web.app` serves as the single public entry point for the workshop.
- **Cache Policy**:
  - High cache hit ratio for static assets (`.svg`, `.js`, `.css`) with 1-year immutable caching (`max-age=31536000, immutable`).
  - Catalog JSON cached at edge for 1 hour with 24-hour background revalidation (`stale-while-revalidate=86400`).
  - Dynamic API queries explicitly bypass edge caches with `Cache-Control: no-store, no-cache, must-revalidate`.
- **Zero-Touch Script**: `deploy/deploy_firebase.sh` automates deployment via either `firebase` or `npx firebase-tools`.
