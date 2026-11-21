# Quirk & Quanta: Observability & Evaluations Test Report

**Report Date:** November 21, 2026  
**Status:** ALL TESTS PASSING (100% Success Rate)  
**Test Suite:** `tests/test-observability-evals.py` + Full Regression Suite  
**Google Cloud Project:** `idc-rag-proj`  
**Execution Environment:** macOS Darwin, Python 3.11 Standard Library  

---

## 1. Executive Summary

A comprehensive automated test suite was constructed and executed to validate the **Observability & Evaluations Dashboard** (Tab 6 of the Workshop Lab). The test suite verifies the 15 specific requirements outlined in the engineering specification, including nanosecond timing accuracy, token usage calculations, Gemini 2.5 Flash economics, benchmark evaluations, the Dr. Boon challenge (`EVAL-003`), Story 7 intern loop runaway simulation, high-concurrency stability, and strict RBAC isolation.

Across all 13 test suites in the repository (123 tests total), **100% of test cases passed with zero failures and zero errors**.

---

## 2. Test Execution Summary

| Test Suite | Total Tests | Passed | Failed | Errors | Duration |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `tests/test-observability-evals.py` | 15 | 15 | 0 | 0 | 2.52s |
| `tests/test-observability.py` | 5 | 5 | 0 | 0 | 0.13s |
| `tests/test-under-the-hood.py` | 12 | 12 | 0 | 0 | 0.26s |
| `tests/test-workshop-bench.py` | 7 | 7 | 0 | 0 | 0.18s |
| `tests/test-security.py` | 8 | 8 | 0 | 0 | 0.15s |
| `tests/test-guardrails.py` | 7 | 7 | 0 | 0 | 0.17s |
| `tests/test-demos.py` | 17 | 17 | 0 | 0 | 0.54s |
| `tests/test-data.py` | 8 | 8 | 0 | 0 | 0.03s |
| `tests/test-graph.py` | 7 | 7 | 0 | 0 | 0.09s |
| `tests/test-hybrid.py` | 6 | 6 | 0 | 0 | 0.27s |
| `tests/test-rag.py` | 9 | 9 | 0 | 0 | 0.30s |
| `tests/test-evaluation.py` | 6 | 6 | 0 | 0 | 0.00s |
| `tests/test-load.py` | 6 | 6 | 0 | 0 | 0.60s |
| **TOTAL** | **123** | **123** | **0** | **0** | **5.24s** |

---

## 3. Detailed Verification of the 15 Core Requirements

### Requirement 1: Request Timing Accuracy
- **Test:** `test_01_timing_accuracy`
- **Result:** PASSED. Verified high-resolution monotonic performance counters (`time.perf_counter()`). Pipeline stages record sub-millisecond durations accurately; `totalDurationMs` matches the aggregate of individual spans.

### Requirement 2: Token Accounting & Gemini 2.5 Flash Cost Calculation
- **Test:** `test_02_token_accounting_and_flash_pricing`
- **Result:** PASSED. Verified Gemini 2.5 Flash published rates ($0.075 / 1M prompt tokens, $0.30 / 1M completion tokens). 1,000,000 prompt tokens calculates to exactly $0.075000; 1,000,000 completion tokens calculates to $0.300000. Standard query turn (800 in / 150 out) calculates to $0.000105.

### Requirement 3: Offline Mode Zero Spend
- **Test:** `test_03_offline_mode_zero_spend`
- **Result:** PASSED. When executing under offline reference synthesizer or Graceful Degradation mode, estimated API spend accurately reflects $0.00 live external billing. `modelId` and `pricingVersion` headers remain fully populated.

### Requirement 4: Story 7 Intern Runaway Loop Simulation
- **Test:** `test_04_story7_intern_spike_simulation`
- **Result:** PASSED. Simulated 40 recursive loops of an unmonitored intern agent script. Unprotected simulation generated 1,360,000 tokens ($10.20 API burn in 28 seconds; $15,300+ overnight projection). Safeguarded simulation enforced token budget caps at loop 11, downshifting to offline reference mode with an actual spend of only $0.0012 (99.98% cost avoidance).

### Requirement 5: Golden Benchmark Dataset Integrity
- **Test:** `test_05_golden_benchmark_dataset_metrics`
- **Result:** PASSED. Confirmed existence and schema of `eval_summary.json` in both `data/evaluation/` and `site/data/evaluation/`. Contains 42 curated test cases across 7 functional query families with 100% valid ground-truth target chunk IDs.

### Requirement 6: Strategy Scorecard Metrics Accuracy
- **Test:** `test_06_strategy_scorecard_metrics`
- **Result:** PASSED. Verified exact metrics across all strategies:
  - Vector: Hit Rate@5 = 47.62%, MRR = 0.4762, P50 Latency = 22.52ms
  - BM25: Hit Rate@5 = 57.14%, MRR = 0.5187, P50 Latency = 0.35ms (Fastest)
  - Hybrid RRF: Hit Rate@5 = 50.00%, MRR = 0.4841, P50 Latency = 22.32ms
  - Local GraphRAG: Hit Rate@5 = 4.76%, MRR = 0.0476, P50 Latency = 0.02ms

### Requirement 7: Dr. Boon's Challenge (`EVAL-003`)
- **Test:** `test_07_dr_boon_challenge_eval_003`
- **Result:** PASSED. Test case `EVAL-003` (*"Do you have comfortable apparel for cold weather featuring physics wave equations?"*) validated:
  - Vector: `hit = False`, reciprocal rank = 0.0, top score = 0.2366 (Missed target `QQ-0001` with diffuse false confidence).
  - BM25: `hit = True`, reciprocal rank = 0.333, top score = 16.76 (Direct lexical hit on Heisenberg wave equations screen-printed on the sleeves).

### Requirement 8: Failed Evaluation Inspector Diff Calculation
- **Test:** `test_08_failed_evaluation_inspector_diff`
- **Result:** PASSED. Verified that failed evaluations correctly compute diffs between `relevantDocIds` and retrieved evidence. Missing chunks are tagged for red-pill display and unexpected chunks are tagged for amber-pill display.

### Requirement 9: Server-Side Evaluations API Latency
- **Test:** `test_09_evaluations_api_response_time_and_schema`
- **Result:** PASSED. `GET /api/rag/evaluations` loads and serves the complete 42-question benchmark summary in < 2ms (0.16s over network), consuming 0 LLM tokens and 0 external API quota.

### Requirement 10: Ring Buffer Capacity Bounds
- **Test:** `test_10_trace_collector_ring_buffer`
- **Result:** PASSED. Verified that after 50 consecutive requests, `TraceCollector` enforces its strict capacity bound of 30 items without memory leaks, while tracking cumulative total requests (50) and lifetime tokens.

### Requirement 11: Zero Hardcoded Credentials or Secret Leakage
- **Test:** `test_11_no_credentials_leakage`
- **Result:** PASSED. Verified that trace serialization (`to_dict()`) contains zero Google API keys (`AIza*`), OpenAI keys (`sk-*`), HMAC secrets, or presenter credentials.

### Requirement 12: Workshop HTML Compliance
- **Test:** `test_12_workshop_html_compliance`
- **Result:** PASSED. Verified DOM element IDs in `site/workshop.html`: `#tab-observability`, `#btn-subtab-live`, `#btn-subtab-evals`, `#obs-history-tbody`, `#obs-waterfall-card`, `#chart-hitrate-svg`, `#select-failed-eval`, and `#btn-load-boon-challenge`.

### Requirement 13: Frontend JavaScript Controller Completeness
- **Test:** `test_13_workshop_js_completeness`
- **Result:** PASSED. Verified that `site/js/workshop.js` defines all required controllers and lifecycle hooks: `setupObservabilityTab()`, `recordSessionQuery()`, `renderRequestWaterfall()`, `renderHistoryTable()`, `executeInternSimulation()`, `loadEvaluationSummary()`, `renderFailedEvalInspector()`, and `executeBoonChallenge()`. JavaScript syntax validated with `node -c`.

### Requirement 14: High Concurrency Stability
- **Test:** `test_14_concurrency_stability`
- **Result:** PASSED. Executed 100 simultaneous concurrent queries using a 10-worker thread pool. 100/100 requests succeeded with full evidence retrieval and zero deadlocks, race conditions, or unhandled exceptions.

### Requirement 15: RBAC Customer Isolation During Tracing
- **Test:** `test_15_rbac_customer_isolation_during_tracing`
- **Result:** PASSED. Tested queries targeting internal wholesale procurement margins (`QQ-0001`). Confirmed that post-retrieval verification enforces customer-level isolation, returning 0 confidential procurement documents (`DOC-PROC-*`) in traced evidence.

---

## 4. Conclusion

The Observability & Evaluations Dashboard satisfies all 15 operational, security, and educational requirements. All 123 automated regression tests pass unconditionally.
