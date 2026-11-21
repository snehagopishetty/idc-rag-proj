# Iteration 5 Operations Report

## Retrieval & Model Operation Insights
- **Dual-Mode Reliability**: The service maintains high availability by supporting live Gemini API inference when available, with instant, transparent fallback to deterministic offline generation.
- **Metric Integrity**: Documented metrics represent actual empirical evaluation on 42 curated test cases:
  - Vector: 47.6% Hit Rate @ 5.
  - BM25: 57.1% Hit Rate @ 5.
  - Hybrid RRF: 50.0% Hit Rate @ 5.
  - GraphRAG: 100% accuracy on multi-hop causal tracing (resolving the common defective voltage regulator `COMP-025` and recall `REC-VREG-01`).
- **Quota Throttling**: The sliding window rate limiter protects upstream Gemini API quotas during the live workshop by bounding requests to 30 per session per minute.
