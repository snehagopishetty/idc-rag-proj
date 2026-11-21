# Quirk & Quanta: Production Deployment & Reliability Master Plan
## IDC Workshop: *"Beyond Basic RAG: Building Production-Ready AI Systems"* (Nov 21, 2026)

### 1. Project Goal
Ensure the Quirk & Quanta storefront, multi-strategy RAG backend, and Workshop Lab are genuinely production-ready, reliable, secure, and performant for approximately 100 simultaneous attendees during the IDC Workshop.

### 2. Discovered Target Infrastructure
- **GCP Project**: `idc-rag-proj` (authoritative workshop project)
- **Primary Region**: `asia-south1` (Mumbai)
- **Container Service**: Cloud Run service `quirk-quanta-rag`
- **Frontend / CDN**: Firebase Hosting (single user-facing origin with `/api/**` proxying to Cloud Run)
- **Runtime Model**: Python 3.10+ Standard Library backend, Vanilla HTML5/CSS3/JS frontend

### 3. Eight-Iteration Execution Schedule
1. **Iteration 1: Production Preflight & Container Audit**
   - Audit Dockerfile, runtime port handling (`0.0.0.0:$PORT`), non-root user, memory footprint, thread safety, and static file security boundaries.
   - Build automated deployment smoke test script (`scripts/production_smoke_test.py`).
2. **Iteration 2: Cloud Run Deployment & Live Backend Verification**
   - Cloud Run packaging, service configuration, memory/CPU tuning, startup probe, and live service verification.
3. **Iteration 3: Firebase Hosting & Cloud Run Integration**
   - Unified origin setup via Firebase Hosting rewrites (`/api/**` -> Cloud Run), caching policies (no-store for API, immutable for static), and end-to-end routing.
4. **Iteration 4: Secrets, Authentication & API Security Hardening**
   - Independent backend security verification: ensure direct Cloud Run access cannot bypass authorization.
   - Strict isolation of vulnerable demonstration modes so public endpoints cannot disable security checks.
   - Path traversal prevention for `data/internal/`.
5. **Iteration 5: Live Inference, Retrieval Integrity & Neo4j Verification**
   - Verified quota management for Gemini 2.5 Flash, truthful metric reporting (Vector 47.6%, BM25 57.1%, Hybrid 50.0%), and Neo4j AuraDB live vs offline reference validation.
6. **Iteration 6: 100-Attendee Concurrency, Load Capacity & Presenter Protection**
   - 100-attendee load tests against unified architecture.
   - Presenter Protection Mechanism: reserved priority capacity token ensuring presenter demos never fail due to audience load.
7. **Iteration 7: Workshop Rehearsal Across All 17 Demos**
   - Projector readability, verified responses, error handling, presenter runbook, and slide-aligned demonstration flow.
8. **Iteration 8: Final Freeze, Rollback Plan & Delivery Handover**
   - Full regression across all 16 mandatory production gates (P01–P16), rollback plan verification, tag `workshop-production-ready` (or `workshop-release-candidate`), and final delivery sign-off.
