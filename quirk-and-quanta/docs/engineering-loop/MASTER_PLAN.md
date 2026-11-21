# Quirk & Quanta: Autonomous Engineering Master Plan
## Advanced RAG Masterclass Workshop ("Beyond Basic RAG: Building Production-Ready AI Systems")

### 1. Executive Summary
This master plan governs the autonomous engineering loop executing Gates 3 through 11 for the Quirk & Quanta workshop system.
The system delivers both:
1. A pristine, fictional scientific e-commerce storefront (`site/` HTML5/CSS3/Vanilla JS).
2. A comprehensive RAG Workshop Lab (`site/workshop.html`) replicating the 8 narrative stories of the animated film *"Quirk & Quanta: A Series of Intelligent Mistakes"*.

### 2. Architecture & Tech Stack Constraints
- **Runtime**: Standard Library Python 3.10+ (zero external pip packages) and Vanilla Browser JavaScript (ES6+).
- **Embeddings**: `gemini-embedding-001` (768-dimensional normalized vectors), precomputed offline storage in `data/embeddings/v1/`, query embedding cache, optional live Google AI Studio Gemini API key.
- **Retrieval Engine**:
  - Dense Vector: Local Cosine Similarity (`rag/retriever.py`)
  - Lexical: Pure Python BM25 Inverted Index (`rag/bm25.py`)
  - Hybrid: Reciprocal Rank Fusion (RRF, k=60) (`rag/hybrid.py`)
  - Knowledge Graph: Local Multi-hop Graph Traverser (`rag/graph_local.py`) & Neo4j Adapter (`rag/graph_neo4j.py`)
- **Security & Safety**:
  - Server-side RBAC enforcement with session token verification (`rag/auth.py`)
  - Grounding, prompt-injection defense (direct & indirect), scope classification (`rag/guardrails.py`)
  - Intentionally vulnerable modes strictly isolated from public traffic.
- **Observability**:
  - Per-request tracing with UUID, latency breakdown, token counting, cost estimator, budget alerting (`rag/observability.py`).

### 3. Acceptance Gates (G1 - G17 & O1 - O4)
- **G1**: Existing storefront still works without regressions.
- **G2**: Baseline RAG runs with truthful model provenance.
- **G3**: Chunking strategies (fixed, sliding, semantic) inspectable and comparable.
- **G4**: BM25 lexical retrieval tested and verified on exact SKU/keyword queries.
- **G5**: Hybrid retrieval performs genuine Reciprocal Rank Fusion.
- **G6**: Film-aligned 3-product defect scenario present in validated graph.
- **G7**: Local GraphRAG returns correct multi-hop paths and grounded answers.
- **G8**: Golden evaluations produce real comparative metrics.
- **G9**: Grounding and abstention work on out-of-domain and ungrounded queries.
- **G10**: Indirect prompt injection reproducible in vulnerable mode, mitigated in hardened mode.
- **G11**: Off-topic generation and usage budgets enforced.
- **G12**: Customer/admin access rules enforced server-side.
- **G13**: IDOR and role tampering blocked in hardened mode.
- **G14**: Request traces explain token usage, latency, and cost spikes.
- **G15**: Workshop Lab exposes all 17 prepared demonstrations.
- **G16**: Dependency fallbacks tested (API outage -> local offline fallback).
- **G17**: 100-attendee concurrency load exercised and documented.
- **O1**: Optional Neo4j AuraDB integration adapter.
- **O2**: Cloud Run Dockerfile and container verification.
- **O3**: AI Studio deployment guide and environment config.
- **O4**: Vercel deployment config.

### 4. Eight-Iteration Execution Schedule
- **Iteration 1 (P0-B)**: BM25 Lexical Retrieval & Hybrid Reciprocal Rank Fusion (Gates G4, G5, Demo 05, Demo 06).
- **Iteration 2 (P0-C)**: Film-Aligned Defect Scenario & Local GraphRAG (Gates G6, G7, Demo 07, Demo 08).
- **Iteration 3 (P0-E)**: Grounding, Abstention, Scope Boundaries & Pirate Prompt Injections (Gates G9, G10, G11, Demo 11, Demo 12, Demo 13).
- **Iteration 4 (P0-F)**: Server-Side RBAC Enforcement, Confidential Cost Exposure & IDOR Mitigation (Gates G12, G13, Demo 15, Demo 16).
- **Iteration 5 (P0-G)**: Observability, Structured Tracing, Token Usage, Latency & Cost Spikes (Gate G14, Demo 14).
- **Iteration 6 (P0-D)**: Extended Golden Dataset (40+ Cases) & Comprehensive Benchmarks (Gate G8, Demo 10).
- **Iteration 7 (P0-H & P1)**: 100-Attendee Load Simulation, Neo4j Graph Adapter & Deployment Artifacts (Gates G16, G17, O1-O4, Demo 09, Demo 17).
- **Iteration 8**: Final Acceptance Verification, Regression Testing, Complete Master Documents & Workshop Handover (Gates G1-G3, G15).
