# Quirk & Quanta: Observability & Evaluations Deployment Report

**Deployment Date:** November 21, 2026  
**Status:** PRODUCTION DEPLOYED & VERIFIED  
**Google Cloud Project:** `idc-rag-proj` (`313632490992`)  
**Region:** `asia-south1` (Mumbai)  
**Strict Isolation Check:** Verified zero interaction, access, or modification to `momence-support-agent`.

---

## 1. Deployment Identifiers & Pipeline Provenance

| Parameter | Value |
| :--- | :--- |
| **Git Commit Hash** | `daf875b` (`feat(workshop): implement interactive Observability & Evals dashboard (Tab 6)`) |
| **Cloud Build Build ID** | `7ca25180-9605-4139-a390-57573f5ab3dc` |
| **Build Status & Duration** | `SUCCESS` (2 minutes 24 seconds) |
| **Artifact Registry Image** | `asia-south1-docker.pkg.dev/idc-rag-proj/quirk-quanta/rag-service:daf875b` |
| **Cloud Run Service** | `quirk-quanta-rag` |
| **Active Cloud Run Revision** | `quirk-quanta-rag-00009-pt4` (100% traffic allocation) |
| **Cloud Run Direct URL** | [https://quirk-quanta-rag-g6hnvsgmpa-el.a.run.app](https://quirk-quanta-rag-g6hnvsgmpa-el.a.run.app) |
| **Firebase Hosting Version** | Release Version Finalized & Released |
| **Public Storefront URL** | [https://idc-rag-proj.web.app](https://idc-rag-proj.web.app) |
| **Workshop Lab URL** | [https://idc-rag-proj.web.app/workshop.html](https://idc-rag-proj.web.app/workshop.html) |

---

## 2. Production Verification Checklist

All endpoints were verified using direct HTTP requests against both Cloud Run directly and through Firebase Hosting CDN rewrites.

### 1. Cloud Run Direct Endpoints

| Endpoint | HTTP Method | Expected Code | Actual Code | Measured Latency | Verification Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `/health` | `GET` | `200 OK` | **200** | 0.278s | **VERIFIED** |
| `/api/rag/status` | `GET` | `200 OK` | **200** | 0.312s | **VERIFIED** |
| `/api/rag/evaluations` | `GET` | `200 OK` | **200** | 0.164s | **VERIFIED** |

### 2. Firebase Hosting Public Endpoints

| Endpoint | HTTP Method | Expected Code | Actual Code | Measured Latency | Verification Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `https://idc-rag-proj.web.app/health` | `GET` | `200 OK` | **200** | 0.326s | **VERIFIED** |
| `https://idc-rag-proj.web.app/api/rag/evaluations` | `GET` | `200 OK` | **200** | 1.279s | **VERIFIED** |
| `https://idc-rag-proj.web.app/data/evaluation/eval_summary.json` | `GET` | `200 OK` | **200** | 0.461s | **VERIFIED** |
| `https://idc-rag-proj.web.app/workshop.html` | `GET` | `200 OK` | **200** | 0.690s | **VERIFIED** |

---

## 3. Live Functional Trace Verification

A live POST request to `/api/rag/ask` was executed against the production service to confirm live trace capture and token accounting:

```bash
curl -s -X POST https://idc-rag-proj.web.app/api/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the return window for the Molecular Measuring Spoon Kit?", "topK": 3, "strategy": "semantic", "role": "customer", "method": "hybrid"}'
```

### Verified Response Payload Attributes:
- **Request ID:** `req_4d92737cd8b7`
- **Execution Mode:** `offline_reference` (Graceful Degradation active)
- **Guardrail Action:** `PASSED`
- **Role Resolution:** `customer` (Tampered: `false`)
- **Measured Latency:** `totalMs: 553.5` (`embeddingMs: 150.9`, `retrievalMs: 215.83`, `generationMs: 337.13`)
- **Token Accounting:**
  - `promptTokens`: 252
  - `completionTokens`: 47
  - `totalTokens`: 299
  - `estimatedCostUsd`: `$0.000033`
  - `pricingModel`: `gemini-2.5-flash ($0.075/1M in, $0.30/1M out)`
  - `pricingVersion`: `2026-11-published`
  - `modelId`: `gemini-2.5-flash`

---

## 4. UI Component & DOM Verification

The production HTML served at `https://idc-rag-proj.web.app/workshop.html` was verified to confirm the active presence of all Tab 6 elements:
- `data-tab="observability"`: **FOUND** (6th navigation tab button)
- `id="tab-observability"`: **FOUND** (Main tab panel container)
- Top 4 KPI Cards:
  - `id="kpi-session-queries"`: **FOUND**
  - `id="kpi-session-latency"`: **FOUND**
  - `id="kpi-session-cost"`: **FOUND**
  - `id="kpi-golden-hitrate"`: **FOUND**
- Sub-Mode Switchers:
  - `id="btn-subtab-live"`: **FOUND** (Live Request Observability)
  - `id="btn-subtab-evals"`: **FOUND** (Golden Benchmark Evaluations)
- Tables & Visualizations:
  - `id="obs-history-tbody"`: **FOUND** (Request history table)
  - `id="obs-waterfall-card"`: **FOUND** (6-stage execution waterfall)
  - `id="btn-run-sim-spike"`: **FOUND** (Story 7 intern runaway spike simulation)
  - `id="obs-scorecard-tbody"`: **FOUND** (42-case golden scorecard)
  - `id="chart-hitrate-svg"`: **FOUND** (Native SVG Hit Rate chart)
  - `id="select-failed-eval"`: **FOUND** (Failed evaluation root-cause inspector)
  - `id="btn-load-boon-challenge"`: **FOUND** (Dr. Boon challenge loader)

---

## 5. Security & Isolation Affirmation

1. **Service Account:** Running under dedicated least-privilege service account: `quirk-quanta-runtime@idc-rag-proj.iam.gserviceaccount.com`.
2. **Secret Manager Bindings:**
   - `QUIRK_AUTH_SECRET` -> `quirk-quanta-auth-secret:latest`
   - `PRESENTER_TOKEN` -> `quirk-quanta-presenter-token:latest`
   - `GEMINI_API_KEY` -> `gemini-api-key:latest`
3. **Zero Credential Exposure:** All client responses demote public privilege escalation; zero secrets are logged or returned in trace payloads.
4. **Boundary Isolation:** No operations or files touched `momence-support-agent`.
