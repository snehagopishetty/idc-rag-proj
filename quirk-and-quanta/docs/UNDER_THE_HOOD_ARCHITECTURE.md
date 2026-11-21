# UNDER THE HOOD: ARCHITECTURE & TECHNICAL SPECIFICATION
**Project:** Quirk & Quanta  
**Subsystem:** Interactive Technical Learning Environment ("Under the Hood")  
**Workshop Target:** IDC Workshop — November 21, 2026  
**Audience:** 100 Simultaneous Engineers, Technical Leaders, and Practitioners  

---

## 1. Architectural Mission & Overview

The "Under the Hood" subsystem transforms the Workshop Lab from a passive demonstration into an interactive whitebox engineering environment. As attendees interact with the Quirk & Quanta storefront and workshop controls, the system visualizes the exact algorithmic sequence, displays concise educational pseudocode, and surfaces verifiable runtime execution evidence.

### Architectural Invariants:
1. **Zero External Frontend Dependencies:** No bundlers, npm dependencies, or JavaScript frameworks. Vanilla HTML5, CSS3, and standard ES2020 JavaScript.
2. **Standard Library Backend:** Python 3.10 standard library exclusively (`urllib`, `json`, `math`, `time`, `re`, `http.server`).
3. **Dual State Transparency:** Shows both pre-execution *planned pipeline state* and real-time *measured execution evidence* with millisecond durations and stage states.
4. **Deterministic Attribution:** Grounded generative answers and citations attribute 100% of facts to retrieved chunks.
5. **Projector-Optimized UI:** High-contrast design (#0F172A slate code block, #F8FAFC text, distinct stage badges) visible across 1080p and 4K conference displays.

---

## 2. System Architecture & Component Diagram

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT BROWSER                                    |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                 UNDER THE HOOD PANEL (#under-the-hood-panel)                |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | [1. Visual Pipeline] (COMPLETED | FALLBACK | SKIPPED | INTERVENED)     |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | [2. The Code] Syntax-Highlighted Educational Python Pseudocode (3-8 L)  |  |  |
|  |  |    + Mathematical Invariant Box (Cosine / BM25 / RRF / Cost Formula)  |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | [3. Execution Evidence] Sub-ms Latency, Roles, Tokens, Provenance     |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | [4. Deeper Details] Key Insights, Failure Modes, Source Module Links  |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                    |               |
                   GET /api/rag/teaching    POST /api/rag/ask, retrieve, compare
                                    |               |
+-----------------------------------+---------------+-------------------------------+
|                                CLOUD RUN BACKEND                                  |
|                                                                                   |
|  +------------------------+  +------------------------+  +---------------------+  |
|  |   Teaching Manifest    |  |      RAGPipeline       |  |  GuardrailsEngine   |  |
|  |   (pipelines.json)     |  |   _build_execution_    |  |  Injection check    |  |
|  |   14 Curated Modes     |  |   trace() collector    |  |  Grounding check    |  |
|  +------------------------+  +------------------------+  +---------------------+  |
|                                         |                                         |
|              +--------------------------+--------------------------+              |
|              |                          |                          |              |
|     +-----------------+        +-----------------+        +-----------------+     |
|     | QuirkRetriever  |        |    OkapiBM25    |        | QuirkKnowledge  |     |
|     | 768-D Vector    |        | Inverted Index  |        |      Graph      |     |
|     +-----------------+        +-----------------+        +-----------------+     |
+-----------------------------------------------------------------------------------+
```

---

## 3. Teaching Manifest Data Model (`pipelines.json`)

The teaching manifest is version-controlled at `data/teaching/pipelines.json` and mirrored to `site/data/teaching/pipelines.json`. It acts as the single source of truth for technical education:

```json
{
  "modeId": "hybrid",
  "displayTitle": "Hybrid RAG (Reciprocal Rank Fusion)",
  "badge": "Rank Fusion (k=60)",
  "subtitle": "Interleaved dense vector topicality & exact lexical inverted index precision",
  "description": "Executes parallel retrieval across dense vector space and Okapi BM25 inverted index...",
  "stages": [
    { "id": "auth_verification", "name": "1. Server RBAC Verification" },
    { "id": "parallel_dispatch", "name": "2. Parallel Query Dispatch" },
    { "id": "dense_retrieval", "name": "3a. Dense Vector Search" },
    { "id": "lexical_retrieval", "name": "3b. Lexical BM25 Search" },
    { "id": "rrf_fusion", "name": "4. Reciprocal Rank Fusion" },
    { "id": "guardrails", "name": "5. Grounding & Safety Verification" },
    { "id": "generation", "name": "6. Attributed Synthesis" }
  ],
  "conceptualSnippet": "vec_ranks = vector_search(query, k=50)\nbm25_ranks = bm25_search(query, k=50)\n\nfor chunk in union_chunks:\n    score = (1 / (60 + vec_rank)) + (1 / (60 + bm25_rank))\n\nevidence = top_k(ranked_by_score, k=5)",
  "formula": "RRF_Score(d) = Σ [1 / (k + rank_m(d))],  k = 60",
  "keyLearningPoint": "Hybrid search solves the Alphanumeric Drift Problem...",
  "commonFailureMode": "Naive linear score addition fails due to incompatible score scales...",
  "sourceReferences": [
    { "file": "rag/hybrid.py", "symbol": "QuirkHybridRetriever.fuse_rrf", "description": "Pure-Python RRF implementation" }
  ]
}
```

### Covered Modes (14 Total):
1. `vector`: Dense Vector RAG (768-D Gemini embeddings, Cosine Similarity)
2. `bm25`: Lexical Retrieval (Pure-Python Inverted Index, Okapi BM25)
3. `hybrid`: Hybrid RRF (Vector + BM25, k=60 Rank Fusion)
4. `graph_local`: In-Memory Knowledge Graph (Multi-Hop Root-Cause Traversal)
5. `graph_neo4j`: Enterprise GraphRAG with AuraDB (Graceful Offline Degradation)
6. `embedding_explorer`: 768-D Latent Space Geometry (L2 Norm, Numerical Float Inspection)
7. `chunking_structural`: Heading-Aware Markdown Hierarchy (Context Preservation)
8. `chunking_fixed`: Fixed-Size 256-Word Slices (Boundary Truncation Failure)
9. `chunking_sliding`: Sliding Window with 50-Word Overlap (Redundancy Tradeoff)
10. `grounding_abstention`: Calibrated Abstention (Cosine Threshold 0.22 Safeguard)
11. `prompt_injection`: Adversarial System Prompt Hijack Interception
12. `rbac_idor`: HMAC Token Verification & Server-Side Demotion
13. `cost_observability`: Nanosecond Span Tracing, Token Pricing & Runaway Loop Protection
14. `golden_evaluations`: Offline Benchmark Harness across 42 Curated Cases

---

## 4. Backend Execution Trace Protocol

Every API response (`/api/rag/ask`, `/api/rag/retrieve`, `/api/rag/compare`, `/api/rag/ask_graph`) includes an `executionTrace` object:

```json
{
  "executionTrace": {
    "mode": "hybrid",
    "strategy": "semantic",
    "totalDurationMs": 28.4,
    "stages": [
      {
        "id": "auth_verification",
        "name": "1. Server RBAC Verification",
        "status": "COMPLETED",
        "durationMs": 0.2,
        "details": "Role 'customer' -> Effective 'customer' (tampered: False)"
      },
      {
        "id": "parallel_dispatch",
        "name": "2. Parallel Query Dispatch",
        "status": "COMPLETED",
        "durationMs": 1.4,
        "details": "Dispatched to 768-D dense vector embedder and Okapi BM25 index"
      },
      {
        "id": "dense_retrieval",
        "name": "3a. Dense Vector Search",
        "status": "COMPLETED",
        "durationMs": 12.1,
        "details": "Evaluated candidate dot products (source: live_gemini_api)"
      },
      {
        "id": "lexical_retrieval",
        "name": "3b. Lexical BM25 Search",
        "status": "COMPLETED",
        "durationMs": 3.4,
        "details": "Evaluated inverted index BM25 postings lists"
      },
      {
        "id": "rrf_fusion",
        "name": "4. Reciprocal Rank Fusion",
        "status": "COMPLETED",
        "durationMs": 0.2,
        "details": "Merged dual rankings using RRF formula (k=60) -> 5 chunks"
      },
      {
        "id": "guardrails",
        "name": "Safety & Grounding Check",
        "status": "COMPLETED",
        "durationMs": 1.1,
        "details": "Action: PROCEED"
      },
      {
        "id": "generation",
        "name": "Grounded Generation",
        "status": "COMPLETED",
        "source": "live_gemini",
        "durationMs": 10.0,
        "details": "Model: gemini-2.5-flash (3 citations attached)"
      }
    ]
  }
}
```

### Stage Status State Machine:
- `COMPLETED`: Stage executed normally and met empirical thresholds.
- `FALLBACK`: Stage detected offline dependency (e.g. Gemini quota exhausted or Neo4j AuraDB unconfigured) and seamlessly degraded to reference synthesizers without throwing an unhandled exception.
- `SKIPPED`: Stage intentionally bypassed (e.g., generation skipped when `retrievalOnly=True` to conserve token quota).
- `INTERVENED`: Security boundary or guardrail policy halted downstream generation (e.g. prompt injection defanged, out-of-scope query rejected, or untrusted admin demoted).
- `RUNNING`: Transient client state while asynchronous HTTP query is in flight.

---

## 5. Frontend Zero-Dependency Syntax Highlighting

The client implements an in-memory single-pass tokenizer in standard JavaScript without external dependencies (highlight.js or Prism):

```javascript
function highlightPython(code) {
  if (!code) return '';
  const tokenRegex = /(#[^\n]*)|("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(\b(?:def|class|return|if|elif|else|for|in|with|as|import|from|try|except|pass|not|and|or|True|False|None)\b)|(\b(?:len|range|print|dict|list|round|int|float|str)\b)|(\b[a-zA-Z_]\w*\b)(?=\()|(\b\d+(?:\.\d+)?\b)/g;

  return code.replace(tokenRegex, (match, gComment, gString, gKeyword, gBuiltin, gCall, gNumber) => {
    if (gComment) return `<span class="py-comment">${escapeHtml(gComment)}</span>`;
    if (gString) return `<span class="py-string">${escapeHtml(gString)}</span>`;
    if (gKeyword) return `<span class="py-keyword">${escapeHtml(gKeyword)}</span>`;
    if (gBuiltin) return `<span class="py-builtin">${escapeHtml(gBuiltin)}</span>`;
    if (gCall) return `<span class="py-call">${escapeHtml(gCall)}</span>`;
    if (gNumber) return `<span class="py-number">${escapeHtml(gNumber)}</span>`;
    return escapeHtml(match);
  });
}
```

### CSS Contrast Guarantee:
- Code block background: `#0F172A` (deep slate navy, 12:1 contrast against `#F8FAFC`)
- Comments: `#64748B` (slate gray, italic)
- Strings: `#A3E635` (lime green)
- Keywords: `#F43F5E` (rose red)
- Function Calls: `#67E8F9` (cyan)
- Numbers: `#FBBF24` (amber gold)
- Built-ins: `#C084FC` (purple)

---

## 6. Security & Isolation Architecture

1. **Fail-Closed Boundary:** Unauthenticated public requests claiming privileged roles (`admin`, `qa_lead`, `procurement`) are cryptographically demoted to `customer` (`wasTampered=True`).
2. **Credential Concealment:** Traces and manifests never output raw API keys, Secret Manager tokens, or authorization hashes.
3. **IDOR Neutralization:** Public requests cannot retrieve confidential procurement chunks (`accessLevel="internal_procurement"`), even if explicitly requested by ID.
4. **Quota Circuit Breakers:** Per-instance rate limiting (30 req/min) and session token caps protect against recursive runaway query loops.
