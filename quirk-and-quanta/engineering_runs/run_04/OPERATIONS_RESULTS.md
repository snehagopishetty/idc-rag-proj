# Engineering Run 04: Operations & Performance Results

### 1. Token Verification Performance
- HMAC-SHA256 token verification latency: **0.02 ms**
- Memory footprint: Zero persistent session state (stateless HMAC tokens).
- CPU overhead: < 1% at 1,000 req/sec.

### 2. Network Boundary Resilience
- Authentication is verified before running vector similarity or inverted index scoring, dropping unauthorized queries before consuming retrieval compute resources.
