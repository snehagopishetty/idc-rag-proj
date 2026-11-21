# Iteration 4 Changes

## Files Created & Updated
1. `scripts/security_audit.py`:
   - Comprehensive automated security test suite covering:
     - Static file secret scanning.
     - Internal procurement data isolation.
     - Cryptographic HMAC-SHA256 token verification, tampering, expiration, and formatting.
     - Server HTTP boundary role resolution (customer default, escalation downgrade, admin elevation).
     - IDOR access control enforcement on `/api/rag/doc`.
     - Request-level demonstration isolation for prompt injection and role bypass.
2. `deploy/cloudrun_service.yaml`:
   - Added `QUIRK_AUTH_SECRET` environment configuration referencing Secret Manager secret `quirk-quanta-auth-secret`.
