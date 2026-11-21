# Engineering Run 06: Operations & Performance Results

### 1. Extended Benchmark Execution Profile
- Total Test Cases: 42
- Total Queries Evaluated: 168 (4 strategies x 42 questions)
- Total Benchmark Duration: ~2.5 seconds total runtime across all strategies.
- Offline Query Cache Hit Rate: 100% (42/42 cached query embeddings).

### 2. Strategy Latency Comparison (42 Cases)
| Retrieval Strategy | p50 Latency (ms) | p95 Latency (ms) | Avg Latency (ms) |
|---|---|---|---|
| Dense Vector | 55.6 | 73.3 | 58.6 |
| Lexical BM25 | 0.4 | 0.7 | 2.5 |
| Hybrid RRF | 56.8 | 75.6 | 60.0 |
| GraphRAG (Defect slice) | 0.08 | 0.12 | 0.09 |
