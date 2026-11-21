# Engineering Run 01: Operations & Performance Results

### 1. In-Memory Footprint
- **BM25 Inverted Index**:
  - Total Chunks Indexed: 1,623 (semantic corpus)
  - Total Unique Terms: ~6,500
  - Inverted Index Memory Footprint: ~2.4 MB
  - Build Time: ~110 ms on cold startup

### 2. Retrieval Latency Profile (22 Test Questions)
| Method | p50 (ms) | p95 (ms) | Avg (ms) |
|---|---|---|---|
| Dense Vector | 56.8 | 75.9 | 63.0 |
| Lexical BM25 | 0.3 | 1.3 | 5.4 |
| Hybrid (RRF) | 57.9 | 78.3 | 64.6 |

### 3. Concurrency Implications
- BM25 index read operations are purely in-memory dictionaries and thread-safe for standard concurrent lookups without lock contention.
