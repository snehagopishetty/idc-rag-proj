# Quirk & Quanta: Production Rollback & Disaster Recovery Plan
## IDC Masterclass Workshop: *"Beyond Basic RAG"*

This document defines the exact, pre-tested procedures to roll back deployments, recover from outages, or isolate failure modes during the live workshop on November 21, 2026.

---

## 1. Recovery Objectives

- **Recovery Time Objective (RTO)**: $< 60$ seconds.
- **Recovery Point Objective (RPO)**: 0 data loss (all catalog data, graph relationships, and precomputed vectors are immutable and stored in version-controlled Git history).

---

## 2. Google Cloud Run Instant Rollback

Google Cloud Run stores all deployed revisions immutably. If a newly deployed backend revision causes crashes or unexpected behavior:

### Step 1: List Past Healthy Revisions
```bash
gcloud run revisions list \
  --service quirk-quanta-rag \
  --region asia-south1 \
  --project idc-rag-proj
```

### Step 2: Shift 100% Traffic to Previous Known Good Revision
```bash
# Example rolling back to revision quirk-quanta-rag-00001-xyz
gcloud run services update-traffic quirk-quanta-rag \
  --to-revisions=quirk-quanta-rag-00001-xyz=100 \
  --region asia-south1 \
  --project idc-rag-proj
```
*Latency: Traffic redirection takes $< 5$ seconds.*

### Step 3: Validate Restored Health
```bash
curl -I https://quirk-quanta-rag-313632490992.asia-south1.run.app/health
# Expected: HTTP/1.1 200 OK
```

---

## 3. Firebase Hosting Instant Rollback

Firebase Hosting maintains a complete immutable history of deployed site releases.

### Step 1: Rollback via Firebase CLI
```bash
firebase hosting:rollback --project idc-rag-proj
```
*This command points the public edge CDN instantly back to the preceding release.*

### Step 2: Validate Edge Health
```bash
curl -I https://idc-rag-proj.web.app/index.html
# Expected: HTTP/2 200, cache-control: public, max-age=300
```

---

## 4. Upstream Dependency Degradation (Zero-Touch Local Fallback)

The application includes built-in circuit breakers and automatic offline fallbacks that require NO manual intervention:

1. **Gemini API Outage / 429 Quota Exhaustion**:
   - The generator catches HTTP/network timeouts and upstream error codes.
   - Transparently falls back to local grounded synthesis with verified citations (`mode: offline_reference`).
   - Response latency drops to $< 1$ ms with zero 500 errors.
2. **Neo4j AuraDB Network Drop**:
   - If AuraDB is unreachable or credentials expire, `Neo4jGraphAdapter` automatically routes queries to `LocalKnowledgeGraph`.
   - The 3-hop defect traversal completes in 0.2 ms with `fallbackUsed: True`.

---

## 5. Local Hot-Standby Emergency Failover

If cloud networking at the workshop venue fails completely, the presenter can spin up the full local hot-standby server in 3 seconds:

```bash
cd quirk-and-quanta
python3 rag/server.py 8080
```
Then present locally at `http://localhost:8080/workshop.html`. All 17 demos, 100 products, 202 SVGs, and precomputed embeddings function 100% offline.
