# Engineering Loop Changelog

## [Iteration 8 - Production Delivery Handover] - 2026-11-20
- Verified all 17 film-aligned workshop demos interactively in `site/workshop.html`.
- Added automated verification test suite `tests/test-demos.py` (17/17 passing).
- Published master delivery handover report `docs/engineering-loop/FINAL_HANDOFF.md`.
- Concluded autonomous loop with all 21 acceptance gates (G1–G17, O1–O4) marked GREEN.

## [Iteration 7 - Concurrency, Neo4j & Deployment] - 2026-11-20 (commit c0ce992)
- Built 100-attendee concurrency load test harness `scripts/load_test.py` (350 requests, 0% error rate).
- Switched server to `http.server.ThreadingHTTPServer` with socket address reuse.
- Implemented Neo4j AuraDB transactional adapter `rag/graph_neo4j.py` with offline fallback.
- Exported complete Cypher graph import script `data/export/neo4j_import.cypher` (143 nodes, 1,214 rels).
- Created secure non-root container packaging `deploy/Dockerfile` and `deploy/vercel.json`.
- Published comprehensive deployment and operations guide `docs/DEPLOYMENT_GUIDE.md`.

## [Iteration 6 - Extended Golden Dataset & Dr. Boon Benchmarks] - 2026-11-20 (commit 58f6085)
- Expanded golden dataset to 42 curated cases (`data/evaluation/golden_dataset.json`).
- Precomputed and cached 768-D query embeddings for all 42 questions.
- Benchmark results: Vector (47.6%), BM25 (57.1%), Hybrid (50.0%), GraphRAG (100% on multi-hop slice).

## [Iteration 5 - Observability, Distributed Tracing & Cost Spikes] - 2026-11-20 (commit fa8e05d)
- Implemented `rag/observability.py` with UUID tracking, latency breakdown spans, and Gemini 2.5 Flash USD pricing.
- Built circular trace ring buffer and cost spike simulator reproducing Story 7 ($10,000+ intern runaway).

## [Iteration 4 - Server-Side RBAC Enforcement & IDOR Mitigation] - 2026-11-20 (commit 5235de5)
- Implemented `rag/auth.py` with HMAC-SHA256 bearer token authentication.
- Enforced network trust boundary: demotes unauthenticated `role="admin"` to `customer` (`wasTampered=True`).
- Added IDOR defense on confidential procurement dossiers (`/api/rag/doc`).

## [Iteration 3 - Multi-Layer Guardrails & Injection Defense] - 2026-11-20 (commit fb0baff)
- Implemented `rag/guardrails.py` blocking direct Blackbeard pirate persona overrides and off-topic coding tutors.
- Defanged indirect prompt injection chunks and enforced calibrated grounded abstention (< 0.22 similarity).

## [Iteration 2 - Film Defect Scenario & Local GraphRAG] - 2026-11-20 (commit 4b087bd)
- Added additive scenario overlay `data/scenarios/film_defect_scenario.json` (`COMP-025`, `REC-VREG-01`).
- Implemented pure-Python in-memory property graph engine `rag/graph_local.py` traversing multi-hop defect in 0.08ms.

## [Iteration 1 - Lexical BM25 & Hybrid RRF] - 2026-11-20 (commit b01ddae)
- Implemented pure Python Okapi BM25 (`rag/bm25.py`) and Reciprocal Rank Fusion $k=60$ (`rag/hybrid.py`).
- Added side-by-side strategy comparison grid to Workshop Lab.

## [Gate 2 Baseline] - 2026-11-20 (commit c649390)
- Implemented deterministic corpus builder (441 docs).
- Implemented multi-strategy chunking (fixed, sliding, semantic).
- Generated gemini-embedding-001 768-D vectors and golden query cache.
- Built unified Python server and Workshop Lab.
- Created 22-case golden evaluation dataset.
