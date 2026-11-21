# Engineering Run 07: Changes
## Target: P0-H & P1 — Audience Load Testing, Neo4j Graph Adapter & Deployment Artifacts
**Git Baseline Commit**: `58f6085`  
**Iteration**: 7 of 8  
**Gates Addressed**: G16, G17, O1, O2, O3, O4  

### 1. New Features & Components Added
1. **Audience Concurrency Load Tester (`scripts/load_test.py`)**:
   - Multi-threaded stress testing tool simulating 100 concurrent attendees and 150 static asset bursts.
   - Dual transport: automatically detects whether direct HTTP socket or sandboxed in-process concurrent dispatch is appropriate.
   - Computes empirical p50, p95, p99 latency, throughput (req/s), and error rate.
   - Outputs full results to `engineering_runs/run_07/load_test_results.json`.

2. **Neo4j AuraDB Adapter (`rag/graph_neo4j.py`)**:
   - Pure standard library HTTP transactional Cypher client for Neo4j AuraDB.
   - Detects `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`, and `NEO4J_DATABASE`.
   - Implements multi-hop root-cause Cypher execution with graceful fallback (`NEO4J_AURA_OFFLINE_REFERENCE`) delegating to the local in-memory graph engine when credentials are not present.

3. **Neo4j Cypher Exporter (`scripts/export_neo4j_cypher.py`)**:
   - Generates `data/export/neo4j_import.cypher` containing schema constraints, 143 nodes, and 1,214 relationships.
   - Includes the additive film defect scenario overlay (`COMP-025` voltage regulator defect).

4. **Production Deployment Packaging**:
   - `deploy/Dockerfile`: Secure container packaging using `python:3.10-slim`, non-root user `appuser` (UID 10001), `HEALTHCHECK` directive via Python standard library, and zero external pip dependencies.
   - `deploy/.dockerignore`: Excludes `.git`, `__pycache__`, and temporary test artifacts.
   - `deploy/vercel.json`: Clean routing and HTTP security headers (`nosniff`, `DENY` clickjacking, XSS protection).
   - `docs/DEPLOYMENT_GUIDE.md`: Comprehensive operations guide covering local startup, Cloud Run, Google AI Studio, Neo4j AuraDB, and Vercel.

5. **Concurrency & Performance Optimizations**:
   - `rag/server.py`: Switched to `http.server.ThreadingHTTPServer` with `daemon_threads = True` and socket address reuse.
   - `rag/retriever.py`: Added `threading.Lock()` to `_load_strategy` and eagerly warmed the default strategy cache, eliminating a concurrent race condition (`KeyError: 'semantic'`).
   - `rag/retriever.py`: Optimized cosine similarity to use dot product on pre-normalized unit vectors, yielding a 2.6x speedup.
   - `rag/observability.py` & `rag/guardrails.py`: Added thread-safe synchronization locks.

6. **Unit Test Suite (`tests/test-load.py`)**:
   - 6 automated tests verifying statistical calculations, 20-thread concurrent retrieval, Neo4j offline fallback, Cypher export syntax, missing API key fallback, and Dockerfile directives.
