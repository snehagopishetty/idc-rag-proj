# Engineering Run 07: Plan
## Target: P0-H & P1 — Audience Load Testing, Neo4j Graph Adapter & Deployment Artifacts

### 1. Action 1: Inspect & Reproduce
- **Baseline Git Commit**: `58f6085`
- **Current Operational & Deployment State**:
  - The unified Python server runs on `http://localhost:8000`.
  - While single-request latency is fast (p50 ~ 55ms for Vector, 0.4ms for BM25, 0.08ms for Graph), we need empirical verification that the server can handle 100 concurrent workshop attendees querying retrieval and browsing static assets concurrently without crash or deadlocks (Gate G17).
  - Neo4j AuraDB integration is currently pending (Gate O1, Demo 09).
  - Cloud Run and Vercel packaging files are needed for deployment (Gates O2, O3, O4).

### 2. Action 2: Decide & Select Next Target
- **Selected Tracks**: P0-H (Operations & Concurrency) & P1 (Neo4j Adapter & Deployment)
- **Gates Targeted**:
  - G16: Dependency fallbacks tested (API outage -> local offline fallback).
  - G17: 100-attendee load scenarios exercised and limitations documented.
  - O1: Optional Neo4j AuraDB integration adapter & Cypher scripts.
  - O2: Cloud Run deployment packaging verified.
  - O3: Google AI Studio self-deployment guide.
  - O4: Vercel deployment configuration.
- **Work Breakdown**:
  1. Build `scripts/load_test.py`:
     - Multi-threaded load tester simulating 100 concurrent retrieval queries and 150 static asset bursts.
     - Measures p50, p95, p99 latency, error rates, and throughput.
  2. Implement `rag/graph_neo4j.py`:
     - Standard library HTTP/REST transactional Cypher adapter for Neo4j AuraDB (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`).
     - Graceful offline fallback when Neo4j credentials are not supplied.
  3. Build `scripts/export_neo4j_cypher.py`:
     - Generates `data/export/neo4j_import.cypher` with `CREATE CONSTRAINT`, nodes, and relationship creation statements.
  4. Create deployment packaging:
     - `deploy/Dockerfile` (Python 3.10 slim, non-root user, EXPOSE 8000, HEALTHCHECK).
     - `deploy/.dockerignore`.
     - `deploy/vercel.json`.
     - `docs/DEPLOYMENT_GUIDE.md`.
  5. Add test suite `tests/test-load.py`:
     - Test concurrency execution, fallback recovery, and Neo4j adapter offline handling.
