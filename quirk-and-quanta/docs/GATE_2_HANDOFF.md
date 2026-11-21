# Gate 2 Technical Handoff: RAG Foundation & Audit

## 1. Executive Summary

This handoff document transitions the **Quirk & Quanta** project from **Gate 1** (fictional storefront, canonical data, and visual assets) into **Gate 2: Vanilla RAG Foundation & Multi-Strategy Chunking**.

All Gate 1 code and assets have been verified, audited, and preserved via Git tag `gate-1-freeze`. The RAG retrieval foundation is fully operational, incorporating a dual-partitioned document corpus (public vs. confidential), three distinct chunking algorithms, 768-dimensional normalized embeddings using `gemini-embedding-001`, local vector cosine similarity, citation mapping, Role-Based Access Control (RBAC), an interactive Workshop Lab (`site/workshop.html`), and a 22-case golden evaluation dataset.

---

## 2. Phase A Audit Report & Discrepancy Findings

### 2.1 Repository Health & Invariants
- **Product Records:** Exactly 100 products (`QQ-0001` through `QQ-0100`) verified.
- **Category Balance:** Exactly 10 categories with 10 products each.
- **Pricing & Margins:** $\text{costPrice} < \text{sellingPrice} \le \text{listPrice}$ verified across all items.
- **Graph Edges:** 1,206 typed graph edges in `data/internal/graph-relationships.json`.
- **Public Isolation:** Zero leakage of confidential pricing or procurement notes in `site/data/products.public.json`.
- **Visual Assets:** All 202 SVGs verified as valid XML with zero parsing errors.

### 2.2 Graph Path Audit: `REC-003` & Defect Traversal
- **Existing Canonical Graph Path:**
  - Recall Notice `REC-003` (*Precision Brass Bevel Gear Backlash Micro-Jitter*) is linked to component `COMP-012` (*Precision Brass Bevel Gear Set 1:4*, sourced from `SUP-002`).
  - Products containing `COMP-012`:
    - `QQ-0081`: Vintage Locomotive Miniature Model
    - `QQ-0087`: Steam Engine Mechanics Model
    - `QQ-0090`: Mechanical Gear Assembly Kit
- **Comparison with the Presentation / Film Scenario:**
  - The masterclass slides describe an illustrative scenario where a single common defective voltage regulator or power IC is shared across three consumer electronics devices:
    - Desk Lamp (`QQ-0011`)
    - Wireless Charger (`QQ-0074`)
    - Star Projector (`QQ-0049`)
  - **Inconsistency Finding:** In the actual Gate 1 canonical graph:
    - `QQ-0011` uses `COMP-003` (Aluminum) & `COMP-005` (Borosilicate Glass).
    - `QQ-0074` uses `COMP-020` (GaN Power IC, affected by `REC-002`).
    - `QQ-0049` uses `COMP-009` (Achromatic Lens, affected by `REC-005`) & `COMP-024` (Polycarbonate Shell).
  - In the canonical data, these three products do not share a common voltage regulator component.
  - In accordance with audit rule 10 (*"Do not alter canonical data without validation and an explicit reason"*), the canonical dataset was **not modified arbitrarily**. The actual implemented working multi-hop path is `REC-003 -> COMP-012 -> QQ-0081, QQ-0087, QQ-0090` (and `REC-005 -> COMP-009 -> QQ-0046, QQ-0049`).

---

## 3. Implemented RAG Foundation Components

### 3.1 Partitioned Document Corpus (`data/corpus/`)
- **Public Corpus (`corpus_public.json`):** 341 documents.
  - 100 Product Description & Feature Dossiers (`DOC-PROD-{sku}-DESC`)
  - 100 Product Technical Specification Tables (`DOC-PROD-{sku}-SPEC`)
  - 100 Commercial Policy Documents (`DOC-PROD-{sku}-POL`)
  - 12 Supplier Dossiers (`DOC-SUP-{supplierId}`)
  - 24 Component Engineering Specs (`DOC-COMP-{componentId}`)
  - 5 QC Recall Bulletins (`DOC-REC-{recallId}`)
- **Confidential Internal Corpus (`corpus_internal.json`):** 100 documents.
  - 100 Confidential Procurement Records (`DOC-INT-{sku}-PROC`) containing wholesale costs (`costPrice`), margin amounts, margin percentages, vendor part codes, batch IDs, and engineering notes. Access restricted strictly to `admin` and `procurement` roles.

### 3.2 Chunking Engine (`data/chunks/`)
- **Fixed-Size (`chunks_fixed.json`):** 1,181 chunks (450 chars, word-bounded, 0 overlap).
- **Sliding-Window (`chunks_sliding.json`):** 1,512 chunks (450 chars, 150 char overlap).
- **Semantic / Structural (`chunks_semantic.json`):** 1,623 chunks. Decomposes documents into self-contained Markdown sections (`## Overview`, `## Key Features`, `## Verified Attributes`, `## Return Protocol`, etc.) with top-level breadcrumb context prefixes.

### 3.3 Embeddings & Offline Cache (`data/embeddings/v1/`)
- **Model:** `gemini-embedding-001`.
- **Dimensions:** 768 dimensions, L2-normalized.
- **Task Types:** `RETRIEVAL_DOCUMENT` for chunk vectors; `RETRIEVAL_QUERY` for queries.
- **Offline Reliability:** Generates deterministic normalized feature vectors and caches query embeddings for 22 golden questions in `query_embeddings_cache.json`. When `GEMINI_API_KEY` is provided, live Gemini batch embeddings are generated seamlessly.

### 3.4 Vector Similarity & Pipeline (`rag/`)
- **`rag/retriever.py`:** In-memory cosine similarity search with RBAC role filtering and citation mapping.
- **`rag/generator.py`:** Grounded synthesis enforcing strict anti-hallucination rules and attribution brackets.
- **`rag/pipeline.py`:** Unified coordinator measuring embedding, retrieval, and generation latencies.
- **`rag/server.py`:** Zero-dependency unified HTTP server exposing `/api/rag/retrieve`, `/api/rag/ask`, `/api/rag/status`, and serving the storefront.

### 3.5 Interactive Workshop Lab (`site/workshop.html`)
- Dedicated exploration bench added to the storefront navigation.
- Allows attendees to test live questions, switch chunking strategies, adjust top-k (1 to 10), toggle roles (`Customer` vs `Admin`), and inspect similarity score meters and citations.

---

## 4. Empirical Evaluation Results

Ran against the 22-case golden evaluation dataset (`data/evaluation/golden_dataset.json`):

| Evaluation Metric | Measured Value | Notes |
| :--- | :--- | :--- |
| **Total Test Questions** | 22 cases | Spanning 8 distinct test families |
| **Hit Rate @ 5** | **54.5% (12/22)** | Exact SKU & explicit specs score 100%; broad/out-of-domain queries require Gate 5/6/8 |
| **Mean Reciprocal Rank (MRR)** | **0.5455** | Relevant chunks rank in top 1 or 2 positions for focused queries |
| **Mean Precision @ 5** | **0.1909** | Dense top-5 precision on single-target queries |
| **Mean Recall @ 5** | **0.4636** | High recall for targeted item queries |
| **RBAC Security Compliance** | **100% (4/4)** | 0% leakage of internal procurement records to Customer role |
| **Retrieval Latency (p50)** | **57.8 ms** | Sub-60ms in-memory cosine similarity over 1,623 vectors |
| **Retrieval Latency (avg)** | **62.2 ms** | End-to-end embedding + retrieval |

---

## 5. Honest Status: What Works vs. Remaining Work

### What Works Fully Today
- Complete deterministic corpus and multi-strategy chunking pipeline.
- 768-D normalized embedding generation with `gemini-embedding-001`.
- Fast, dependency-free local cosine similarity search.
- Bulletproof RBAC security filtering at the retrieval layer.
- Interactive Workshop Lab UI with real-time latency and citation inspection.
- 17 passing automated unit tests across Gate 1 and Gate 2.

### What Remains for Future Gates
1. **BM25 Lexical Search (Gate 5):** Dense vector search struggles with subword tokenization artifacts on ambiguous multi-item prompts; BM25 inverted index is required for exact lexical token matching.
2. **Hybrid RAG Fusion (Gate 6):** Reciprocal Rank Fusion (RRF) combining dense and sparse rank lists.
3. **GraphRAG Traversals (Gate 7):** Neo4j Cypher path resolution for multi-hop recall queries (`REC-003 -> COMP-012 -> Products`).
4. **Server-Side Session Authentication (Gate 9):** Moving beyond demo role toggle to cryptographically signed JWT sessions.
