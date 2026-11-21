# Iteration 3 Changes

## Files Created & Updated
1. `.firebaserc`:
   - Configured default GCP project: `idc-rag-proj`.
2. `firebase.json`:
   - Configured `public: "site"`.
   - Reverse proxy rewrite: `{"source": "/api/**", "run": {"serviceId": "quirk-quanta-rag", "region": "asia-south1"}}`.
   - Security headers: `nosniff`, `SAMEORIGIN`, `strict-origin-when-cross-origin`.
   - Asset cache policy: 1-year immutable (`max-age=31536000, immutable`) on images, styles, scripts, fonts.
   - HTML cache policy: 300s (`max-age=300, must-revalidate`).
   - Catalog data cache policy: 3600s (`max-age=3600, stale-while-revalidate=86400`).
   - Dynamic API cache policy: `no-store, no-cache, must-revalidate` for `/api/**`.
3. `deploy/deploy_firebase.sh`:
   - Deployment automation supporting both native `firebase` CLI and `npx firebase-tools`.
4. `scripts/verify_firebase_routing.py`:
   - Automated test suite validating Firebase configuration, cache policies, reverse proxy headers, API routing, and traversal prevention.
