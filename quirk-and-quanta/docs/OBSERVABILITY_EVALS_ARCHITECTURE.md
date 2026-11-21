# Quirk & Quanta: Observability & Evaluations Dashboard Architecture

**Document Version:** 1.0.0  
**Workshop Date:** November 21, 2026  
**Audience:** Technical Attendees, RAG Practitioners, SREs, Workshop Facilitators  
**Google Cloud Project:** `idc-rag-proj` (`313632490992`)  
**Cloud Run Service:** `quirk-quanta-rag` (`asia-south1`)  
**Production Web URL:** [https://idc-rag-proj.web.app/workshop.html](https://idc-rag-proj.web.app/workshop.html)  

---

## 1. Executive Summary & Design Philosophy

The **Observability & Evals** dashboard (Tab 6 in the Quirk & Quanta Workshop Lab) provides an interactive, production-grade telemetry and benchmark evaluation interface for workshop attendees. 

Designed without complex third-party SaaS dependencies (no Prometheus, Grafana, Datadog, BigQuery, or Firestore), the system utilizes:
- **Backend:** Python Standard Library high-resolution monotonic performance counters (`time.perf_counter()`), in-memory ring buffers, and lightweight REST endpoints.
- **Frontend:** Vanilla HTML5, CSS3, native SVG charting, and a bounded `sessionStorage` ring buffer (capped at 30 requests).
- **Evaluation Engine:** Precomputed golden benchmark evaluation artifacts (`eval_summary.json`) over 42 curated test cases across 7 functional query families, delivering sub-millisecond dashboard renders with zero token consumption.

---

## 2. The Five Core Observability Questions

The dashboard directly answers the five critical production RAG questions:

| Question | Architectural Solution | UI Visual Presentation |
| :--- | :--- | :--- |
| **1. What question was asked?** | Full query provenance captured in `RequestTrace` including timestamp, user role, requested strategy, and input text. | Request History Table with question preview, full tooltip, and query family tags. |
| **2. What did the pipeline execute?** | Traces exact execution path: RBAC demotion checks, guardrail heuristics, retrieval strategy (Vector, BM25, Hybrid, or Graph), and synthesis mode (`live_gemini` vs `offline_reference`). | Status Badges (`COMPLETED`, `FALLBACK`, `SKIPPED`, `INTERVENED`) and stage labels. |
| **3. How long did each operation take?** | High-precision timing across 6 pipeline stages: Auth, Guardrails, Embedding/Tokenization, Retrieval, RBAC Filtering, and Synthesis. | Interactive horizontal waterfall bars scaled to total request latency, millisecond readouts. |
| **4. How many tokens & cost incurred?** | Token estimation (~4 chars/token) + exact API token counts mapped to Google Gemini 2.5 Flash pricing ($0.075/1M in, $0.30/1M out). | Dedicated Token & Cost Explorer Card, per-request and cumulative session spend, Story 7 intern loop simulation. |
| **5. Was the retrieved evidence correct?** | Golden evaluation dataset (42 curated cases) measuring Hit Rate@5, MRR, Precision@5, and Recall@5 against ground-truth document IDs. | Golden Scorecard Table, Hit Rate bar chart, Latency P50/P95 chart, and Failed Evaluation Root-Cause Inspector. |

---

## 3. Dashboard Modes & Component Architecture

### Mode A: Live Request Observability (Attendee Browser Session)

1. **Top 4 KPI Metrics:**
   - **Queries Executed:** Bounded client-side session counter (ring buffer of last 30 requests).
   - **Latency (Avg / P95):** Real-time client-side statistical calculation over recent requests.
   - **Gemini Token Cost:** Cumulative estimated API cost based on Gemini 2.5 Flash pricing.
   - **Golden Baseline Accuracy:** Baseline reference indicator (BM25: 57.1% | Hyb: 50.0%).

2. **Client Session Request History Table:**
   - Supports strategy filtering (`All`, `Vector`, `BM25`, `Hybrid`, `Graph`).
   - Interactive row selection: clicking any historical request dynamically binds its execution trace to the waterfall and token explorer.
   - **Clear Session:** Resets client session storage and KPI cards.
   - **Export JSON:** Formats session history as a structured JSON file for local analysis.

3. **Execution Stage Waterfall:**
   - Visualizes the 6 core pipeline phases with nanosecond instrumentation:
     - `1. Authentication & Demotion Check` (Client bearer verification, privilege demotion)
     - `2. Input Guardrails & Injection Screening` (Prompt injection, scope boundaries)
     - `3. Query Vectorization / Tokenization` (Dense embedding vs BM25 tokenizer)
     - `4. Knowledge Index Retrieval` (4,316 corpus chunks across Vector/BM25/Graph)
     - `5. Post-Retrieval Verification & RBAC` (Document authorization, zero procurement leakage)
     - `6. Response Synthesis & Attribution` (Live Gemini 2.5 Flash vs offline reference synthesizer)
   - Status badges: `COMPLETED` (Teal), `FALLBACK` (Amber), `SKIPPED` (Navy), `INTERVENED` (Red).
   - "Deep Inspect Algorithm in Under the Hood" button connects observability telemetry to algorithm mechanics.

4. **Story 7: Arthur Receives the Bill (Intern Spike Simulation):**
   - Simulates 40 recursive loops of an unmonitored intern agent script (`while True: call_rag()`).
   - Compares:
     - **Unprotected LLM Runaway:** 40 queries × 34,000 tokens = 1,360,000 tokens; $10.20 burn in 28 seconds; projected overnight invoice: **$15,300+**.
     - **Quirk & Quanta Guardrails:** Enforced at iteration 11 (Token ceiling & 60 RPM limiter); engages Graceful Degradation to offline synthesizer; actual total cost: **$0.0012** (99.98% cost avoidance).
   - Distinctly labeled: `⚠️ SIMULATION — NO ACTUAL GEMINI SPEND INCURRED`.

---

### Mode B: Golden Benchmark Evaluations (42 Curated Cases)

1. **Consolidated Benchmark Scorecard:**
   Evaluates all 4 retrieval strategies across 42 test cases covering 7 functional query families:

   | Retrieval Strategy | Hit Rate@5 | MRR | Precision@5 | Recall@5 | Latency P50 | Latency P95 | RBAC Compliance |
   | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
   | **Dense Semantic Vector** | 47.6% (20/42) | 0.4762 | 19.5% | 38.0% | 22.52 ms | 24.54 ms | 100% (Pass) |
   | **Okapi BM25** | **57.1% (24/42)** | **0.5187** | **22.4%** | **45.1%** | **0.35 ms** | **0.78 ms** | 100% (Pass) |
   | **Hybrid RRF (k=60)** | 50.0% (21/42) | 0.4841 | 20.5% | 39.2% | 22.32 ms | 24.49 ms | 100% (Pass) |
   | **Local GraphRAG** | 4.8% (2/42)* | 0.0476 | 4.8% | 4.8% | **0.02 ms** | **0.03 ms** | 100% (Pass) |

   *\*Note: Local GraphRAG is specialized for multi-hop relational root-cause defect analysis (Story 3), achieving 100% precision on relational defect queries, but is not designed for broad lexical catalog discovery.*

2. **Native SVG Visualizations:**
   - **Hit Rate@5 by Strategy Bar Chart:** High-contrast SVG comparing Vector (47.6%), BM25 (57.1%), and Hybrid (50.0%).
   - **Retrieval Latency (P50 / P95):** Millisecond comparison highlighting BM25's sub-millisecond execution (0.4ms) vs Vector (24.5ms).

3. **Failed Evaluation Root-Cause Inspector:**
   - Dropdown of failed golden test cases.
   - Side-by-side comparison of Vector, BM25, and Hybrid results with `HIT` and `MISSED` badges.
   - Target evidence pill tags (`DOC-PROD-QQ-0001-DESC`) with diff tags:
     - `MISSING: DOC-...` (Red pill)
     - `UNEXPECTED: DOC-...` (Amber pill)
   - Technical Failure Analysis: Grounded explanation of underlying mechanics (e.g. subword token drift, lexical vocabulary mismatch, out-of-domain abstention).
   - "Rerun this Question in Side-by-Side Comparison" button for live experimentation.

4. **Dr. Boon's Evaluation Challenge (`EVAL-003`):**
   - Query: *"Do you have comfortable apparel for cold weather featuring physics wave equations?"*
   - Target: `QQ-0001` (Quantum Uncertainty Hoodie).
   - Divergence: Vector search returns irrelevant products with false cosine confidence (>0.35), while BM25 directly indexes "wave equations" in the description, achieving rank #1. Demonstrates the core workshop lesson: *"Working retrieval is not necessarily correct retrieval."*

---

## 4. API & Data Flow Contracts

### `GET /api/rag/evaluations`
- **Purpose:** Delivers consolidated golden benchmark summary across all 42 cases.
- **Latency:** < 2 ms (zero LLM calls).
- **Payload Schema:**
```json
{
  "version": "1.0.0",
  "benchmarkDate": "2026-11-20T20:42:00Z",
  "datasetVersion": "v1.0-42q",
  "totalQuestions": 42,
  "strategies": {
    "vector": { "metrics": { ... }, "testCases": [ ... ] },
    "bm25": { "metrics": { ... }, "testCases": [ ... ] },
    "hybrid": { "metrics": { ... }, "testCases": [ ... ] },
    "graph": { "metrics": { ... }, "testCases": [ ... ] }
  },
  "goldenDataset": [ ... ]
}
```

### Request Tracing Schema (`RequestTrace.to_dict()`)
```json
{
  "requestId": "req_4d92737cd8b7",
  "timestamp": "2026-11-21T04:41:08Z",
  "sessionId": "default_session",
  "role": "customer",
  "question": "What is the return window for the Molecular Measuring Spoon Kit?",
  "strategy": "semantic",
  "method": "hybrid",
  "status": "completed",
  "guardrailAction": "PASSED",
  "totalDurationMs": 553.5,
  "stages": [
    { "name": "auth_verification", "durationMs": 0.01, "status": "COMPLETED" },
    { "name": "guardrail_evaluation", "durationMs": 0.34, "status": "COMPLETED" },
    { "name": "query_embedding", "durationMs": 150.9, "status": "COMPLETED" },
    { "name": "hybrid_retrieval", "durationMs": 215.83, "status": "COMPLETED" },
    { "name": "response_synthesis", "durationMs": 337.13, "status": "FALLBACK" }
  ],
  "tokenUsage": {
    "promptTokens": 252,
    "completionTokens": 47,
    "totalTokens": 299
  },
  "estimatedCostUsd": 0.000033,
  "pricingModel": "gemini-2.5-flash ($0.075/1M in, $0.30/1M out)",
  "pricingVersion": "2026-11-published",
  "modelId": "gemini-2.5-flash"
}
```

---

## 5. Security & Boundary Enforcement
1. **Client Ring Buffer Isolation:** Traces reside exclusively within attendee browser session memory (`sessionStorage`), preventing cross-attendee data leakage.
2. **Zero Credential Exposure:** Neither API keys, HMAC secrets, nor presenter tokens are ever serialized into trace outputs or client logs.
3. **RBAC Verification:** Traced queries enforce customer-level access. Direct requests for internal procurement dossiers (`DOC-PROC-*`) are cleanly stripped by post-retrieval verification.
4. **Project Isolation:** All operations run strictly within Google Cloud project `idc-rag-proj`. Zero connection or deployment to external workspaces.
