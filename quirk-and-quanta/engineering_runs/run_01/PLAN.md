# Engineering Run 01: Plan
## Target: P0-B — BM25 Lexical Retrieval & Reciprocal Rank Fusion (Hybrid RAG)

### 1. Action 1: Inspect & Reproduce
- **Baseline Git Commit**: `c649390`
- **Reproduced Tests**:
  - `tests/test-data.py`: 8/8 PASS
  - `tests/test-rag.py`: 9/9 PASS
  - `scripts/run_evaluations.py`: 22 test cases evaluated. Baseline Hit Rate @ 5: 54.5%, MRR: 0.5455, Precision @ 5: 0.1909, Recall @ 5: 0.4636.
- **Identified Deficiency**:
  - Pure dense vector retrieval struggles with exact part numbers, rare keywords, and SKU queries (e.g. `QQ-0018`, exact supplier code lookups) because semantic embeddings map based on conceptual proximity rather than exact token overlap.
  - Workshop requirements demand BM25 lexical retrieval and Hybrid RAG via Reciprocal Rank Fusion (RRF), corresponding to Story 2 of the film and Gates G4 & G5.

### 2. Action 2: Decide & Select Next Target
- **Selected Track**: P0-B (BM25 & Hybrid Fusion)
- **Gates Targeted**: G4 (BM25 works & exact SKU matching tested), G5 (Hybrid RRF ranked fusion)
- **Work Breakdown**:
  1. Build pure-Python BM25 inverted index engine (`rag/bm25.py`) with customizable $k_1$ ($1.5$), $b$ ($0.75$), tokenization preserving SKUs (`QQ-XXXX`), punctuation handling, and IDF calculation.
  2. Build Hybrid search engine (`rag/hybrid.py`) implementing Reciprocal Rank Fusion (RRF, $k=60$) combining normalized dense vector scores and BM25 ranks.
  3. Integrate BM25 and Hybrid retrieval into `rag/retriever.py`, `rag/pipeline.py`, and `rag/server.py` (`/api/rag/retrieve`, `/api/rag/query` supporting `strategy="vector"`, `strategy="bm25"`, `strategy="hybrid"`).
  4. Update Workshop Lab UI (`site/workshop.html`, `site/js/workshop.js`) to support Demo 05 (BM25 exact SKU) and Demo 06 (Hybrid RAG) with side-by-side strategy comparison.
  5. Add test suite `tests/test-hybrid.py` testing BM25 tokenization, inverted indexing, SKU recall, and RRF rank blending.
  6. Attack with typos, rare tokens, and adversarial lexical queries.
  7. Run evaluation on golden test cases to measure Hit Rate and MRR improvement.
