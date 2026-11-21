# Iteration 4 Plan: Secrets, Authentication & Demonstration Safety Isolation (Gates P06, P07, P08)

## 1. Objectives
- Audit repository and static assets for secrets, private keys, API credentials, or confidential wholesale margins.
- Implement automated security harness (`scripts/security_audit.py`) validating HMAC-SHA256 bearer tokens, role elevation resistance, and IDOR protection.
- Verify request-level isolation of intentionally vulnerable demonstration modes (`hardened=False` in Demo 12 and Demo 16), ensuring zero persistent state bleed across sessions.
- Stress-test concurrent authentication and session-level rate limiting under 100 concurrent simulated attendee sessions.

## 2. Acceptance Criteria
- Clean scan: zero API keys, PEM files, or confidential margin data in `site/`.
- All 15 security checks in `scripts/security_audit.py` pass.
- Role escalation attempts demoted to `customer` with `wasTampered=True`.
- IDOR access to `PROC-*` documents returns HTTP 403 for customers.
- 100 concurrent distinct session requests succeed without race conditions or state pollution.
