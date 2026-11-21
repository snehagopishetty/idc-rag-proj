# Quirk & Quanta: Final Delivery & Engineering Handover
## IDC Workshop: *"Beyond Basic RAG: Building Production-Ready AI Systems"*
**Project**: Quirk & Quanta Storefront & Multi-Strategy RAG Engine  
**Status**: **COMPLETED (All 21 Gates GREEN)**  
**Automated Tests**: **79/79 Passing across 10 Test Suites**  
**Engineering Loop**: **8/8 Iterations Completed**  

---

## 1. Executive Summary

Quirk & Quanta has been transformed from an initial static storefront into a production-grade, highly observable, secure, multi-strategy Retrieval-Augmented Generation (RAG) educational application. It directly replicates the engineering mistakes and solutions featured in the five-minute animated film *"Quirk & Quanta: A Series of Intelligent Mistakes"*.

The entire application adheres to strict engineering constraints:
1. **Zero External Dependencies**: Implemented strictly with the Python 3.10+ Standard Library (zero pip installs) and Vanilla HTML5/CSS3/JavaScript (no frontend framework build steps).
2. **Pristine Public Storefront**: 100 fictional scientific products (QQ-0001 through QQ-0100), 10 categories, 12 suppliers, 202 local SVG visual assets, search, category filters, cart, and wishlist remain intact and fully functional.
3. **Data Integrity & Separation**: Public catalog data (`site/data/products.public.json`) remains strictly separated from internal confidential procurement margins (`data/internal/`).
4. **Additive Defect Scenario**: Canonical graph relationships (1,206 typed edges) were preserved without destructive edits; the film's 3-product voltage regulator defect was introduced via an additive scenario overlay (`data/scenarios/film_defect_scenario.json`).
5. **Truthful Empirical Metrics**: No synthetic benchmarks or simulated live Gemini tokens. All metrics reflect genuine Python Standard Library Okapi BM25, 768-D cosine similarity, Reciprocal Rank Fusion ($k=60$), and property graph traversals.

---

## 2. Animated Film Story Alignment Matrix

Each of the 8 narrative stories from *"Quirk & Quanta: A Series of Intelligent Mistakes"* is directly demonstrated in code and exposed via the Workshop Lab:

| Story | Film Narrative & Engineering Problem | Quirk & Quanta Technical Solution | Lab Demo ID |
|---|---|---|---|
| **Story 1: The Vanilla Trap** | Arthur's baseline dense vector RAG hallucinates and loses precision on technical specs. | Grounded RAG with calibrated abstention and citation metadata. | **Demo 01, Demo 10** |
| **Story 2: The Exact SKU Failure** | Dense vectors fail on exact keywords, part numbers, and alphanumeric SKUs (`QQ-0015`). | Okapi BM25 inverted index + Reciprocal Rank Fusion ($k=60$) Hybrid retrieval. | **Demo 05, Demo 06** |
| **Story 3: The 3-Product Defect Mystery** | Desk Lamp (`QQ-0011`), Charger (`QQ-0074`), and Star Projector (`QQ-0049`) flicker. Standard RAG cannot find common cause. | GraphRAG multi-hop traversal (`Product -> CONTAINS -> Component -> AFFECTED_BY -> Recall`). | **Demo 07, Demo 08, Demo 09** |
| **Story 4: Grounding & Abstention** | Model generates confident hallucinations for out-of-domain historical questions. | Calibrated similarity threshold (0.22) triggering explicit grounded abstention. | **Demo 11** |
| **Story 5: The Pirate Persona Override** | Adversarial user prompts system to "Speak like Blackbeard" and leak secret costs. | Multi-layer guardrails blocking direct injections and domain scope misuse. | **Demo 12, Demo 13** |
| **Story 6: Role Tampering & IDOR** | Client manipulates `role="admin"` in browser JSON payload to access procurement margins. | Server-side HMAC-SHA256 token verification and IDOR resource authorization. | **Demo 15, Demo 16** |
| **Story 7: Arthur Receives the Bill** | An unmonitored intern loops recursive Python coding scripts through LLM ($10,000+ spike). | Per-session token budgets (15,000 max), rate limits (30 req/min), and cost telemetry. | **Demo 14** |
| **Story 8: The API Outage** | Upstream Gemini API rate limit or outage causes unhandled application crashes. | Zero-key offline reference engine fallback with precomputed vectors. | **Demo 17** |

---

## 3. Final 21-Gate Acceptance Matrix

All 21 acceptance gates are verified **GREEN**:

| Gate | Name | Status | Verified Commit | Verification Evidence |
|---|---|---|---|---|
| **G1** | Preserved Storefront & Asset Parity | **GREEN** | `8737041` | Storefront responsive, 100 products, 202 SVGs, `tests/test-data.py` |
| **G2** | Baseline RAG & Truthful Provenance | **GREEN** | `c649390` | `gemini-embedding-001` (768-D), offline projection, `tests/test-rag.py` |
| **G3** | Multi-Strategy Chunking Inspection | **GREEN** | `c649390` | Fixed (1,181), Sliding (1,512), Semantic (1,623) chunks, `test-rag.py` |
| **G4** | BM25 Lexical Keyword & SKU Retrieval | **GREEN** | `b01ddae` | Pure Python BM25 inverted index, exact SKU match, `test-hybrid.py` |
| **G5** | Hybrid Retrieval (RRF $k=60$) | **GREEN** | `b01ddae` | Reciprocal Rank Fusion, rank normalization, `tests/test-hybrid.py` |
| **G6** | Defect Scenario in Validated Graph | **GREEN** | `4b087bd` | `data/scenarios/film_defect_scenario.json`, `COMP-025`, `test-graph.py` |
| **G7** | Local GraphRAG Root-Cause Traversal | **GREEN** | `4b087bd` | 3-product root cause traversal in 0.08ms, `tests/test-graph.py` |
| **G8** | Golden Evaluations & Empirical Metrics | **GREEN** | `58f6085` | 42-case golden dataset, comparative benchmark, `test-evaluation.py` |
| **G9** | Calibrated Grounding & Abstention | **GREEN** | `fb0baff` | Similarity threshold (0.22) abstention, `tests/test-guardrails.py` |
| **G10** | Prompt Injection Defense & Defanging | **GREEN** | `fb0baff` | Direct pirate override blocked, indirect chunks sanitized |
| **G11** | Scope Classification & Token Budgets | **GREEN** | `fb0baff` | Rejects off-topic coding tutor, enforces session token safety limits |
| **G12** | Server-Side RBAC Enforcement | **GREEN** | `5235de5` | HMAC-SHA256 bearer tokens, client tampering demotion, `test-security.py` |
| **G13** | IDOR Mitigation & Resource Protection | **GREEN** | `5235de5` | Direct resource endpoint `/api/rag/doc` returns 403 Forbidden |
| **G14** | Observability, Traces & Cost Spikes | **GREEN** | `fa8e05d` | UUID tracking, distributed spans, token counters, spike simulator |
| **G15** | 17 Prepared Workshop Lab Demos | **GREEN** | `c0ce992` | All 17 demos interactively exposed, verified in `tests/test-demos.py` |
| **G16** | Dependency Fallback & Degraded Mode | **GREEN** | `c0ce992` | Graceful zero-key operation without crashes, `tests/test-load.py` |
| **G17** | 100-Attendee Load Capacity | **GREEN** | `c0ce992` | 100 concurrent retrievals, 150 static bursts, 0% error rate |
| **O1** | Neo4j AuraDB Integration & Export | **GREEN** | `c0ce992` | `rag/graph_neo4j.py`, `neo4j_import.cypher` (143 nodes, 1,214 rels) |
| **O2** | Cloud Run Deployment Packaging | **GREEN** | `c0ce992` | Non-root `appuser` Dockerfile with healthcheck, `deploy/Dockerfile` |
| **O3** | AI Studio Self-Deployment Guide | **GREEN** | `c0ce992` | Complete operations runbook in `docs/DEPLOYMENT_GUIDE.md` |
| **O4** | Vercel Deployment Configuration | **GREEN** | `c0ce992` | Clean routing and security headers in `deploy/vercel.json` |

---

## 4. Empirical Evaluation & Concurrency Benchmarks

### A. Golden Retrieval Evaluation (42 Curated Evaluation Cases)
Executed across all 42 golden cases (`scripts/run_evaluations.py`):

| Retrieval Strategy | Hit Rate @ 5 | Mean Reciprocal Rank (MRR) | Precision @ 5 | Recall @ 5 | p50 Latency |
|---|---|---|---|---|---|
| **Dense Vector (`gemini-embedding-001`)** | 47.6% | 0.4286 | 0.1619 | 0.4167 | 21.8 ms |
| **Lexical BM25 (Okapi Inverted Index)** | **57.1%** | **0.5357** | **0.1857** | **0.5000** | **0.42 ms** |
| **Hybrid RAG (RRF $k=60$)** | 50.0% | 0.4762 | 0.1714 | 0.4405 | 22.4 ms |
| **Local GraphRAG (Multi-Hop Slice)** | **100.0%** | **1.0000** | **1.0000** | **1.0000** | **0.08 ms** |

*Key Workshop Insight for Attendees*:
- Pure Dense Vector misses exact alphanumeric SKUs (`QQ-0015`).
- Pure BM25 excels at exact keywords and SKUs (57.1% Hit Rate, 0.42ms latency), but fails on conceptual paraphrasing.
- Hybrid RRF balances both, preventing severe retrieval drop-offs.
- On multi-hop relationships (Story 3), standard retrieval achieves **0% Hit Rate**, while GraphRAG achieves **100% Hit Rate** in 0.08ms.

### B. 100-Attendee Workshop Concurrency Load Test (`scripts/load_test.py`)
Executed simulating 100 simultaneous attendees in the IDC workshop:

| Scenario | Concurrency | Total Requests | Success Rate | p50 Latency | p95 Latency | Throughput | Error Rate |
|---|---|---|---|---|---|---|---|
| **Scenario A: RAG Retrievals** | 100 workers | 100 | **100%** (100/100) | 324.4 ms | 2,614.5 ms | 29.2 req/s | **0.0%** |
| **Scenario B: Static Bursts** | 150 workers | 150 | **100%** (150/150) | 1.84 ms | 3.63 ms | 13,085 req/s | **0.0%** |
| **Scenario C: Mixed Traffic** | 100 workers | 100 | **100%** (100/100) | 164.5 ms | 354.7 ms | 84.3 req/s | **0.0%** |

**Summary**: 350 requests executed | 0 failures | 0.0% error rate | **VERDICT: PASS**

---

## 5. Facilitator Runbook: Running the 17 Workshop Demos

### Starting the Server
```bash
cd quirk-and-quanta
python3 rag/server.py 8000
```
Open browser to: `http://localhost:8000/workshop.html`.

### How to Run Each Demo
In the **Workshop Lab** control panel, use the dropdown **"🎬 17 Film-Aligned Master Demos"**:

1. **Demo 01 (Baseline Vector Retrieval)**:
   - Select `Demo 01`. Click **⚡ Ask Full RAG**.
   - *Teaching Point*: Shows standard cosine similarity retrieval and grounded answer synthesis with citation badges.
2. **Demo 02 (Fixed-Size Chunking)**:
   - Select `Demo 02`. Click **🔍 Retrieve Only**.
   - *Teaching Point*: Highlights boundary truncation where sentences are clipped mid-word or mid-concept.
3. **Demo 03 (Sliding-Window Chunking)**:
   - Select `Demo 03`. Click **🔍 Retrieve Only**.
   - *Teaching Point*: Demonstrates 150-char overlap preserving context across chunk boundaries.
4. **Demo 04 (Semantic Chunking)**:
   - Select `Demo 04`. Click **🔍 Retrieve Only**.
   - *Teaching Point*: Shows section-aligned markdown chunking preserving complete tables, specs, and policies.
5. **Demo 05 (Lexical BM25 on Exact SKU)**:
   - Select `Demo 05`. Click **🔍 Retrieve Only**.
   - *Teaching Point*: Demonstrates Okapi BM25 finding SKU `QQ-0015` at rank 1, whereas dense vector struggles.
6. **Demo 06 (Hybrid RRF Search)**:
   - Select `Demo 06`. Click **⚖️ Compare Methods**.
   - *Teaching Point*: Side-by-side comparison showing how RRF ($k=60$) fuses lexical precision and semantic nuance.
7. **Demo 07 (Multi-Hop Failure in Standard RAG)**:
   - Select `Demo 07`. Click **🔍 Retrieve Only**.
   - *Teaching Point*: The desk lamp and charger retrieve their own descriptions, but neither discovers root-cause component `COMP-025`.
8. **Demo 08 (Local GraphRAG Root-Cause Traversal)**:
   - Select `Demo 08`. Method auto-switches to *Knowledge Graph Traversal*. Click **⚡ Ask Full RAG**.
   - *Teaching Point*: The property graph traverses `[QQ-0011, QQ-0074, QQ-0049] -> CONTAINS -> COMP-025 -> AFFECTED_BY -> REC-VREG-01` in 0.08ms.
9. **Demo 09 (Neo4j AuraDB Cypher Import)**:
   - Select `Demo 09`.
   - *Teaching Point*: Demonstrates external graph database readiness via `neo4j_import.cypher` and transactional REST Cypher query generation.
10. **Demo 10 (Comparative Evaluation Benchmark)**:
    - Select `Demo 10`. Click **⚖️ Compare Methods**.
    - *Teaching Point*: Visualizes rank discrepancies across strategies on policy queries.
11. **Demo 11 (Calibrated Grounded Abstention)**:
    - Select `Demo 11`. Click **⚡ Ask Full RAG**.
    - *Teaching Point*: Model detects evidence similarity (< 0.22) is ungrounded and explicitly abstains rather than hallucinating about Roman history.
12. **Demo 12 (Direct Prompt Injection Defense)**:
    - Select `Demo 12`. Click **⚡ Ask Full RAG** with *🛡️ Hardened Guardrails Active*.
    - *Observation*: System rejects the Blackbeard pirate persona override (`REJECT_INJECTION`).
    - *Comparison*: Uncheck the shield checkbox and re-run to observe persona hijacking in vulnerable mode.
13. **Demo 13 (Scope Rejection & Indirect Defanging)**:
    - Select `Demo 13`. Click **⚡ Ask Full RAG**.
    - *Teaching Point*: System rejects homework/coding tutor requests (`REJECT_OFF_TOPIC`) to protect against denial-of-wallet.
14. **Demo 14 (Observability & Runaway Cost Spikes)**:
    - Select `Demo 14`. Click **📈 Simulate Runaway Cost Spike**.
    - *Teaching Point*: Graphically visualizes Story 7: unmonitored runaway intern loops burn $0.0090+, while token budgets cap spend at $0.00135.
15. **Demo 15 (Server-Side RBAC Enforcement)**:
    - Select `Demo 15`. Role defaults to `admin` without token. Click **⚡ Ask Full RAG**.
    - *Teaching Point*: Server HTTP boundary demotes client to `customer` (`wasTampered=True`). Then click **🔑 Issue Admin Token** and re-run to demonstrate authenticated elevation.
16. **Demo 16 (IDOR Direct Resource Access Protection)**:
    - Select `Demo 16`. Click **🎯 Test IDOR Direct Resource Access**.
    - *Teaching Point*: Demonstrates `403 Forbidden` when attempting to fetch confidential supplier contract `DOC-PROC-QQ-0001` as customer.
17. **Demo 17 (Dependency Fallback & Zero-Key Operation)**:
    - Select `Demo 17`. Click **⚡ Ask Full RAG**.
    - *Teaching Point*: Confirms the system functions deterministically in offline reference mode without requiring live external internet or Gemini API keys.

---

## 6. Complete Automated Regression Test Suite

All 79 tests pass deterministically:
```bash
cd quirk-and-quanta
for f in tests/test-*.py; do python3 "$f"; done
```
- `tests/test-data.py`: 8 tests (Data integrity, schema, 100 products, 202 SVGs)
- `tests/test-rag.py`: 9 tests (Chunking, cosine similarity, retrieval, citations)
- `tests/test-hybrid.py`: 6 tests (Okapi BM25, RRF fusion, SKU preservation)
- `tests/test-graph.py`: 7 tests (Film defect scenario, local property graph multi-hop)
- `tests/test-guardrails.py`: 7 tests (Prompt injection, scope, abstention, sanitization)
- `tests/test-security.py`: 8 tests (HMAC bearer tokens, role tampering, IDOR defense)
- `tests/test-observability.py`: 5 tests (UUID spans, token counting, cost spike simulator)
- `tests/test-evaluation.py`: 6 tests (Golden dataset metrics, MRR, hit rates)
- `tests/test-load.py`: 6 tests (100-concurrency thread safety, Neo4j fallback, Dockerfile)
- `tests/test-demos.py`: 17 tests (End-to-end verification of all 17 workshop demos)

**Total**: **79 passing tests, 0 failures, 0 errors**.

---

## 7. Delivery Sign-Off

The Quirk & Quanta project is officially **COMPLETE** and verified ready for deployment to the 100-attendee IDC Workshop *"Beyond Basic RAG: Building Production-Ready AI Systems"*.
