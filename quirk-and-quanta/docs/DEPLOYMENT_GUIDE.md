# Quirk & Quanta: Production Deployment & Operations Guide
## Workshop: *"Beyond Basic RAG: Building Production-Ready AI Systems"*

This guide provides complete instructions for running and deploying the **Quirk & Quanta** storefront, multi-strategy RAG engine, and Workshop Lab across local development, Google Cloud Run, Neo4j AuraDB, and Vercel.

---

## 1. Zero-Dependency Architectural Principle

Quirk & Quanta is built with zero third-party pip or npm dependencies:
- **Backend**: 100% Python Standard Library (`http.server`, `socketserver`, `urllib.request`, `json`, `math`, `re`, `hashlib`, `hmac`, `uuid`, `threading`).
- **Frontend**: Plain HTML5, CSS3, and Vanilla JavaScript (ES modules, no build step, no webpack, no Tailwind).
- **Embeddings & Knowledge Graph**: 768-D precomputed vectors (`data/embeddings/v1/`) and pure Python in-memory property graph with multi-hop root-cause discovery.

---

## 2. Local Workshop Execution

### Quick Start
To start the unified server locally on port 8000:
```bash
cd quirk-and-quanta
python3 rag/server.py 8000
```

### URLs
- **Fictional Storefront**: `http://localhost:8000/index.html`
- **Interactive Workshop Lab**: `http://localhost:8000/workshop.html`
- **Product Catalog**: `http://localhost:8000/products.html`
- **API Health Telemetry**: `http://localhost:8000/api/rag/status`

---

## 3. Google Cloud Run Deployment (Containerized)

Quirk & Quanta includes a production Dockerfile (`deploy/Dockerfile`) that runs as a non-root user (`appuser`, UID 10001) for strict container security compliance.

### Step 1: Build the Container Image
```bash
gcloud builds submit \
  --tag gcr.io/[PROJECT_ID]/quirk-and-quanta:v1.0.0 \
  deploy/
```

### Step 2: Deploy to Cloud Run
```bash
gcloud run deploy quirk-and-quanta \
  --image gcr.io/[PROJECT_ID]/quirk-and-quanta:v1.0.0 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --concurrency 100 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars "GEMINI_API_KEY=[OPTIONAL_LIVE_KEY]"
```

---

## 4. Google AI Studio & Gemini API Configuration

Quirk & Quanta supports both live Google Gemini API generation and 100% offline reference operation.

### Live Mode Setup
1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
2. Set the environment variable:
   ```bash
   export GEMINI_API_KEY="AIzaSy..."
   ```
3. Restart the server. The telemetry endpoint (`/api/rag/status`) will report `"activeMode": "live_gemini"`.

### Graceful Fallback (Demo 17)
If `GEMINI_API_KEY` is omitted, revoked, or rate-limited:
- The system automatically degrades to `"activeMode": "offline_reference"`.
- Cosine similarity, Okapi BM25, Hybrid RRF, and GraphRAG continue to execute deterministically using precomputed golden query embeddings.
- Zero crashes, zero unhandled 500 exceptions.

---

## 5. Neo4j AuraDB Integration (Story 3 Root Cause)

While Quirk & Quanta contains a built-in deterministic local graph engine (`rag/graph_local.py`), it also provides a live transactional Cypher adapter (`rag/graph_neo4j.py`) and pre-generated Cypher import script for Neo4j AuraDB.

### Step 1: Export Cypher Script
```bash
python3 scripts/export_neo4j_cypher.py
```
This writes `data/export/neo4j_import.cypher` containing 143 nodes, 1,214 relationships, uniqueness constraints, and the film defect scenario overlay (`COMP-025` voltage regulator defect).

### Step 2: Import into Neo4j AuraDB
1. Create a free instance at [Neo4j AuraDB](https://neo4j.com/cloud/platform/aura-graph-database/).
2. Open **Neo4j Workspace / Query**.
3. Copy and run the contents of `data/export/neo4j_import.cypher`.

### Step 3: Configure Environment Variables
```bash
export NEO4J_URI="neo4j+s://[INSTANCE_ID].databases.neo4j.io"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="[YOUR_PASSWORD]"
```
If these variables are omitted, `rag/graph_neo4j.py` falls back gracefully to `NEO4J_AURA_OFFLINE_REFERENCE` with local graph delegation.

---

## 6. Vercel Static Storefront Deployment

For static frontend hosting of the storefront:
```bash
cd quirk-and-quanta
vercel --prod
```
The included `deploy/vercel.json` configures security headers (`nosniff`, `DENY` clickjacking, XSS filtering) and clean URL rewrites to `/site/*.html`.

---

## 7. 100-Attendee Concurrency Load Capacity (Gate G17)

To simulate full workshop load (100 concurrent attendees issuing retrieval requests and 150 static bursts):
```bash
python3 scripts/load_test.py 8000
```

### Empirical Results
| Scenario | Concurrency | Requests | Success Rate | p50 Latency | p95 Latency | Throughput |
|---|---|---|---|---|---|---|
| **Scenario A: RAG Retrievals** | 100 workers | 100 | **100%** (100/100) | 324.4 ms | 2,614.5 ms | 29.2 req/s |
| **Scenario B: Static Bursts** | 150 workers | 150 | **100%** (150/150) | 1.84 ms | 3.63 ms | 13,085 req/s |
| **Scenario C: Mixed Traffic** | 100 workers | 100 | **100%** (100/100) | 164.5 ms | 354.7 ms | 84.3 req/s |

**Total Executed**: 350 requests | **Failures**: 0 | **Overall Error Rate**: 0.0% | **Verdict**: **PASS**

---

## 8. Security & Operational Hardening Checklist

| Feature | Implementation | Threat Prevented |
|---|---|---|
| **Server-Side RBAC** | `rag/auth.py` HMAC-SHA256 bearer tokens | Client-side role tampering / privilege escalation |
| **IDOR Protection** | `/api/rag/doc` role verification | Direct object reference leaks of supplier margins |
| **Direct Injection Defense** | Regex + instruction fence | Persona overrides (Blackbeard pirate attack) |
| **Indirect Injection Defanging** | Content stripping on retrieved chunks | Secondary payload execution |
| **Scope Boundary** | Reject non-catalog coding tutor queries | Denial-of-service / off-topic homework misuse |
| **Cost Spikes / Runaway Loops** | Token budgets & rate limits (Story 7) | Cloud bill explosion ($10,000+ intern runaway) |
