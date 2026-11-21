# UNDER THE HOOD: TEST SUITE EXECUTION & VERIFICATION REPORT
**Project:** Quirk & Quanta  
**Subsystem:** Interactive Technical Learning Experience & RAG Engine  
**Test Date:** November 21, 2026  
**Target Environment:** Local Python 3.10 Sandbox & Google Cloud Run (`idc-rag-proj`)  

---

## 1. Executive Summary

A comprehensive automated test execution was conducted across all 12 unit, regression, security, and benchmark test suites in the Quirk & Quanta repository. All 98 individual tests passed with a 100% success rate and zero regressions.

```
Total Test Suites:    12
Total Executed Tests: 98
Passed:               98 (100.0%)
Failed:               0  (0.0%)
Errors:               0  (0.0%)
Total Execution Time: 2.78 seconds
```

---

## 2. Test Suite Breakdown

| Suite # | Test Suite File | Focus Area | Tests | Duration | Result |
| :---: | :--- | :--- | :---: | :---: | :---: |
| 1 | `tests/test-data.py` | Catalog schema, 100 products, JSON valid | 8 | 0.033s | **PASSED** |
| 2 | `tests/test-demos.py` | 17 Prepared workshop demonstration flows | 17 | 0.561s | **PASSED** |
| 3 | `tests/test-evaluation.py` | Golden dataset, evaluation metric scorers | 6 | 0.001s | **PASSED** |
| 4 | `tests/test-graph.py` | In-memory graph, component recall multi-hop | 7 | 0.093s | **PASSED** |
| 5 | `tests/test-guardrails.py` | Injection filters, grounding confidence | 7 | 0.166s | **PASSED** |
| 6 | `tests/test-hybrid.py` | Dense vector + BM25 reciprocal rank fusion | 6 | 0.261s | **PASSED** |
| 7 | `tests/test-load.py` | Concurrent requests, throughput, circuit breaker | 6 | 0.583s | **PASSED** |
| 8 | `tests/test-observability.py` | Distributed trace spans, token/cost meter | 5 | 0.120s | **PASSED** |
| 9 | `tests/test-rag.py` | Core RAG pipeline, context formatting | 9 | 0.307s | **PASSED** |
| 10 | `tests/test-security.py` | HMAC auth, RBAC demotion, IDOR access | 8 | 0.152s | **PASSED** |
| 11 | `tests/test-under-the-hood.py` | Manifest schema, trace stages, teaching codes | 12 | 0.254s | **PASSED** |
| 12 | `tests/test-workshop-bench.py` | In-process workshop lab benchmark suite | 7 | 0.175s | **PASSED** |
| **TOTAL** | **12 Test Suites** | **Complete Engine & Workshop Experience** | **98** | **2.706s** | **100% PASS** |

---

## 3. Dedicated "Under the Hood" Suite Verification (`test-under-the-hood.py`)

The newly implemented test suite validates all functional, architectural, and security invariants required for the "Under the Hood" experience:

1. `test_01_manifest_files_exist_and_match`: Confirms `data/teaching/pipelines.json` and `site/data/teaching/pipelines.json` exist and contain synchronized mode counts.
2. `test_02_all_required_modes_present`: Confirms all 14 workshop modes exist (`vector`, `bm25`, `hybrid`, `graph_local`, `graph_neo4j`, `embedding_explorer`, `chunking_structural`, `chunking_fixed`, `chunking_sliding`, `grounding_abstention`, `prompt_injection`, `rbac_idor`, `cost_observability`, `golden_evaluations`), with display titles, at least 2 stages, teaching snippets, formulas, key learning points, and common failure modes.
3. `test_03_manifest_source_files_exist`: Verifies that all `sourceReferences` point to existing Python files in `rag/` or `scripts/`.
4. `test_04_vector_execution_trace`: Confirms `ask(method="vector")` returns `executionTrace` with `query_embedding`, `vector_retrieval`, and `generation` stages with valid millisecond durations.
5. `test_05_bm25_execution_trace`: Confirms `ask(method="bm25")` returns `term_analysis`, `inverted_index_lookup`, and `bm25_scoring` stages.
6. `test_06_hybrid_rrf_execution_trace`: Confirms `ask(method="hybrid")` returns `parallel_dispatch`, `dense_retrieval`, `lexical_retrieval`, and `rrf_fusion` stages.
7. `test_07_graph_local_execution_trace`: Confirms local graph traversal returns `entity_resolution`, `relationship_traversal`, and `defect_root_cause` stages.
8. `test_08_neo4j_fallback_execution_trace`: Confirms Neo4j mode outputs `status: "FALLBACK"` on Stage 1 (`aura_connect`) and attaches the note `"Neo4j not connected: showing local graph fallback"`.
9. `test_09_retrieval_only_skips_generation_stage`: Confirms `retrieval_only=True` sets generation status to `SKIPPED`.
10. `test_10_guardrail_intervention_stage`: Confirms prompt injection attacks mark guardrails and generation as `INTERVENED`.
11. `test_11_compare_strategies_trace`: Confirms `compare()` returns `executionTrace` with 3 strategy stages and valid chunk citations.
12. `test_12_no_credential_or_secret_leakage`: Scans execution traces and teaching manifests to confirm zero presenter tokens, secret keys, or sensitive credentials are disclosed.

---

## 4. Frontend Code Verification

- `site/js/workshop.js` syntax verification:
  Command: `node -c site/js/workshop.js`
  Result: Exit code 0 (Syntax clean).
- Zero-dependency syntax highlighting:
  Tokenizer verified against all 14 Python snippets without regex backtracking or HTML escaping vulnerabilities.
- DOM binding:
  All elements (`#under-the-hood-panel`, `#uth-pipeline-stages`, `#uth-code-snippet`, `#uth-formula-box`, `#uth-evidence-grid`, `#uth-details`, `#btn-copy-uth-code`, `#btn-toggle-uth`) exist and bind properly to workshop controller lifecycle events.

---

## 5. Security & Invariant Audit

- **Fail-Closed RBAC:** Unauthenticated client requests attempting to claim `admin` role are safely demoted to `customer` (`wasTampered=True`) across all endpoints.
- **IDOR Protection:** Direct access to internal procurement dossiers (`accessLevel="internal_procurement"`) is rejected for anonymous and customer roles.
- **Spending Protection:** Token counters track prompt/completion tokens and enforce container rate limits ($30\text{ req/min}$) to protect workshop budgets.
