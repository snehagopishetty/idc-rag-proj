# Engineering Run 01: Changes
## P0-B: BM25 Lexical Retrieval & Reciprocal Rank Fusion (Hybrid RAG)

### Summary of Modifications:
1. **`rag/bm25.py`**:
   - Implemented Okapi BM25 inverted index ($k_1=1.5, b=0.75$).
   - Designed domain-aware tokenizer preserving scientific part numbers (`QQ-XXXX`, `COMP-XXX`, `REC-XXX`, `SUP-XXX`).
   - Implemented term frequency calculation, Robertson-Spärck Jones IDF with smoothing, and RBAC role filtering.
2. **`rag/hybrid.py`**:
   - Implemented Reciprocal Rank Fusion (RRF) algorithm using standard constant $k=60$.
   - Fuses dense vector scores and sparse BM25 scores with full provenance attribution (`vectorRank`, `vectorScore`, `bm25Rank`, `bm25Score`, `matchedTerms`).
3. **`rag/retriever.py`**:
   - Integrated `BM25Retriever` and `HybridRetriever`.
   - Exposed `retrieve_vector`, `retrieve_bm25`, `retrieve_hybrid`, and unified `retrieve(method=...)`.
4. **`rag/pipeline.py`**:
   - Updated pipeline coordinator to support multi-strategy methods (`vector`, `bm25`, `hybrid`).
   - Added `compare()` method for side-by-side strategy evaluation.
5. **`rag/server.py`**:
   - Added `POST /api/rag/compare` endpoint.
   - Updated `/api/rag/retrieve` and `/api/rag/ask` to accept `method` parameter.
   - Updated status endpoint with feature flags `ENABLE_BM25: true` and `ENABLE_HYBRID: true`.
6. **`site/workshop.html` & `site/js/workshop.js`**:
   - Added Retrieval Method dropdown (Dense Vector, Lexical BM25, Hybrid RRF).
   - Added "⚖️ Compare Methods" button and dynamic side-by-side comparison card.
   - Enhanced evidence card rendering to display RRF scores, vector/BM25 ranks, and matched terms.
7. **`tests/test-hybrid.py`**:
   - Added 6 unit tests covering tokenization, exact SKU matching, RBAC access enforcement, RRF arithmetic, hybrid pipeline integration, and compare endpoint.
8. **`scripts/run_evaluations.py`**:
   - Enhanced benchmark runner to accept `--method vector|bm25|hybrid`.
