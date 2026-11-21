# Engineering Run 01: Decision

### Status: GREEN (Accepted)

### Findings:
1. Pure Python Okapi BM25 implementation (`rag/bm25.py`) successfully indexes 1,623 chunks with domain-aware tokenization preserving part numbers like `QQ-0018`.
2. Hybrid Reciprocal Rank Fusion (`rag/hybrid.py`) merges dense vectors and sparse BM25 scores with Cormack $k=60$ constant and full telemetry.
3. Benchmark evaluation demonstrates that BM25 boosts Hit Rate @ 5 from 54.5% to 68.2%, and MRR from 0.5455 to 0.6152. Hybrid RRF achieves 59.1% Hit Rate with high reciprocal ranking for exact matches.
4. All 23 unit tests across 3 test suites pass cleanly.
5. Workshop Lab updated with method dropdown, comparison button, and 3-column side-by-side view.

### Acceptance Gates Status:
- **G4 (BM25 Retrieval)**: GREEN
- **G5 (Hybrid RRF Retrieval)**: GREEN

### Next Target:
- **Iteration 2 (P0-C)**: Film-Aligned 3-Product Defect Scenario & Local GraphRAG Traversal (Story 3, Gates G6 & G7).
