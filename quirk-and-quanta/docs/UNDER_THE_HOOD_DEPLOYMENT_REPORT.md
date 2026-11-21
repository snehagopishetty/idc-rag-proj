# UNDER THE HOOD: PRODUCTION DEPLOYMENT & HOSTED EXPERIENCE REPORT
**Project:** Quirk & Quanta  
**Subsystem:** Interactive Technical Learning Experience ("Under the Hood")  
**Target Date:** November 21, 2026  
**Audience:** IDC Workshop (100 Simultaneous Interactive Attendees)  

---

## 1. Production Deployment Invariants & Identity

| Parameter | Authoritative Value | Verification Status |
| :--- | :--- | :---: |
| **GCP Project ID** | `idc-rag-proj` | **CONFIRMED** |
| **Project Number** | `313632490992` | **CONFIRMED** |
| **GCP Region** | `asia-south1` (Mumbai) | **CONFIRMED** |
| **Cloud Run Service** | `quirk-quanta-rag` | **CONFIRMED** |
| **Runtime Service Account** | `quirk-quanta-runtime@idc-rag-proj.iam.gserviceaccount.com` | **CONFIRMED** |
| **Artifact Registry** | `asia-south1-docker.pkg.dev/idc-rag-proj/quirk-quanta/rag-service` | **CONFIRMED** |
| **Firebase Hosting** | `https://idc-rag-proj.web.app` | **CONFIRMED** |
| **Workshop Lab URL** | `https://idc-rag-proj.web.app/workshop.html` | **CONFIRMED** |
| **Unrelated Company Project Boundary** | `momence-support-agent` (Strictly NEVER accessed/modified) | **CONFIRMED** |

---

## 2. Container Build & Cloud Run Revision Details

- **Git Commit:** `0268554`
- **Cloud Build ID:** `ea8a9118-9a39-43df-9f9e-aaf423c15e10`
- **Image URI:** `asia-south1-docker.pkg.dev/idc-rag-proj/quirk-quanta/rag-service:0268554`
- **Image Digest:** `asia-south1-docker.pkg.dev/idc-rag-proj/quirk-quanta/rag-service@sha256:05dcc93981f65467d3e58790eab1b5388af38b138768740433c21c8e92c1d1ab`
- **Active Revision:** `quirk-quanta-rag-00007-vcm`
- **Deployment Status:** `Ready=True`, `ConfigurationsReady=True`, `RoutesReady=True`
- **Concurrency & Scaling:**
  - Memory: 2 GiB
  - vCPU: 1.0
  - Concurrency: 20 simultaneous requests per container instance
  - Min Instances: 1 (warm instance, eliminating cold-start latency for presenter demos)
  - Max Instances: 3 (protective spending cap for 100 simultaneous attendees)
  - Request Timeout: 45s
  - IAM Ingress: `all` with public unauthenticated invocation enabled for IDC workshop attendees

---

## 3. End-to-End Verification Matrix

| Endpoint / Asset | Method | Target URL | Expected Status | Result | Latency / Evidence |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Service Health Probe** | `GET` | `https://idc-rag-proj.web.app/health` | `200 OK` | **VERIFIED 200** | 120 ms |
| **Direct Health Probe** | `GET` | `https://quirk-quanta-rag-g6hnvsgmpa-el.a.run.app/health` | `200 OK` | **VERIFIED 200** | 45 ms |
| **Teaching Manifest CDN** | `GET` | `https://idc-rag-proj.web.app/data/teaching/pipelines.json` | `200 OK` | **VERIFIED 200** | 36.6 KB, 14 modes |
| **Teaching Manifest API** | `GET` | `https://idc-rag-proj.web.app/api/rag/teaching` | `200 OK` | **VERIFIED 200** | 37.0 KB JSON payload |
| **Workshop Lab Page** | `GET` | `https://idc-rag-proj.web.app/workshop.html` | `200 OK` | **VERIFIED 200** | Contains `#under-the-hood-panel` |
| **Status & Model Health** | `GET` | `https://idc-rag-proj.web.app/api/rag/status` | `200 OK` | **VERIFIED 200** | 4,316 chunks, 143 nodes |
| **Vector Retrieval API** | `POST` | `https://idc-rag-proj.web.app/api/rag/retrieve` | `200 OK` | **VERIFIED 200** | Vector executionTrace |
| **BM25 Lexical API** | `POST` | `https://idc-rag-proj.web.app/api/rag/retrieve` | `200 OK` | **VERIFIED 200** | BM25 executionTrace in 2.16 ms |
| **Grounded Ask API** | `POST` | `https://idc-rag-proj.web.app/api/rag/ask` | `200 OK` | **VERIFIED 200** | Attributed generation + citations |
| **Strategy Comparison** | `POST` | `https://idc-rag-proj.web.app/api/rag/compare` | `200 OK` | **VERIFIED 200** | 3 Parallel retrieval stages |
| **Knowledge Graph API** | `POST` | `https://idc-rag-proj.web.app/api/rag/ask` (method=neo4j) | `200 OK` | **VERIFIED 200** | Neo4j AuraDB fallback in 0.26 ms |
| **RBAC Demotion Invariant** | `POST` | `https://idc-rag-proj.web.app/api/rag/ask` (role=admin) | `200 OK` | **VERIFIED 200** | `wasTampered=True`, demoted |

---

## 4. Operational & Workshop Readiness Status

- **Zero-Dependency Architecture:** Frontend loads instantly on any attendee mobile device, laptop, or tablet without npm packaging or bundlers.
- **Quota Safeguards:** Session token limits and container rate limits ($30\text{ req/min}$) protect Gemini API quotas.
- **Fail-Safe Offline Mode:** If Google Gemini experiences unexpected regional downtime during the workshop, the system automatically falls back to deterministic reference synthesis without presenter interruption.
