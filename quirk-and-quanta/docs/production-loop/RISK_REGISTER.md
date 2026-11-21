# Quirk & Quanta: Production Risk Register
## Operational & Deployment Risk Matrix

| Risk ID | Category | Risk Description | Severity | Likelihood | Mitigation Strategy | Status |
|---|---|---|---|---|---|---|
| **RSK-01** | Cloud Auth | `gcloud` interactive re-authentication needed for live Google Cloud operations. | High | High | Detect status, generate exact gcloud commands, implement robust local container/mock testing, mark cloud gates BLOCKED gracefully if credentials unavailable. | Active |
| **RSK-02** | Concurrency | 100 concurrent attendees causing thread contention or memory exhaustion on single Cloud Run instance. | High | Medium | Optimize cosine dot-product; implement ThreadingHTTPServer with connection pooling; tune Cloud Run concurrency to 20-30 per instance with max 5 instances. | Mitigated locally |
| **RSK-03** | Quota Shock | Attendees querying live Gemini API exhausts RPM/TPM quota or triggers denial-of-wallet. | High | High | Pre-compute and cache 42 golden queries; enforce session rate limits (30 req/min) & token caps (15k tokens); default to deterministic offline reference when key absent. | Mitigated |
| **RSK-04** | Presenter Failure | Audience traffic saturates Cloud Run workers during presenter's live demonstration. | High | Medium | Implement Presenter Protection Token (`X-Presenter-Priority` or priority bearer token) that bypasses audience queue and guarantees capacity. | Planned (Iter 6) |
| **RSK-05** | IDOR / Data Leak | Anonymous users accessing confidential procurement records (`data/internal/`). | Critical | Low | Static server explicitly restricts `site/` directory; `/api/rag/doc` checks HMAC bearer token; internal dossiers never copied to deployable static assets. | Mitigated |
| **RSK-06** | Vulnerable Mode Abuse | Toggle for vulnerable demo mode (Story 5 pirate attack) being abused on public URL. | High | Medium | Ensure vulnerable mode is sandboxed per-session or runs on recorded reference traces, never disabling global production authorization. | Planned (Iter 4) |
| **RSK-07** | Proxy Timeout | Firebase Hosting proxy has a 60-second timeout; slow generation could return 504. | Medium | Low | Cloud Run API timeout set to 25s; streaming/instant local responses; offline projection latency < 50ms. | Mitigated |
