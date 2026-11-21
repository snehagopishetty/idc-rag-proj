# Engineering Run 08: Security Assessment
## Target: Final End-to-End Security Audit Across All Attack Families

### 1. Comprehensive Attack Matrix
All 6 security gates and attack families from the workshop syllabus were tested against the unified pipeline:

| Gate | Attack / Vulnerability Tested | Test Case / Demo | Outcome | Defense Mechanism |
|---|---|---|---|---|
| **G10** | Direct Prompt Injection (Blackbeard Pirate override) | Demo 12 / `test-guardrails.py` | **BLOCKED** | Regex pattern matching + instruction boundary isolation |
| **G10** | Indirect Prompt Injection (Retrieved chunk prompt injection) | `test-guardrails.py` | **SANITIZED** | Content sanitization and defanging on retrieved chunks |
| **G11** | Off-Topic Denial-of-Wallet (Recursive Fibonacci coding tutor) | Demo 13 / `test-guardrails.py` | **REJECTED** | Domain scope classification |
| **G12** | Client-Side Role Tampering (Unauthenticated `role="admin"`) | Demo 15 / `test-security.py` | **DEMOTED** | Server-side HMAC-SHA256 signature verification |
| **G13** | Insecure Direct Object Reference (Direct access to `DOC-PROC-QQ-0001`) | Demo 16 / `test-security.py` | **403 FORBIDDEN** | Access level policy validation per resource |
| **G14** | Runaway Loop Cost Explosion (Story 7 40-iteration loop) | Demo 14 / `test-observability.py` | **BUDGET CAPPED** | Session rate limiter (30 req/min) & token budget (15,000 tok) |

### 2. Operational Security
- Intentionally vulnerable modes (`hardened=False`) remain strictly isolated behind explicit developer flags and do not leak into production default behavior.
- Server runs as unprivileged user `appuser` (UID 10001) in Docker container.
- Zero external package dependencies eliminates third-party supply-chain vulnerabilities.
