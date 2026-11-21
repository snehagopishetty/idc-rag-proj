# Iteration 4 Security Results

## Comprehensive Security Assessment
1. **Secret & Key Quarantine**:
   - Zero hardcoded API keys or private keys found across all static assets.
   - Procurement files (`data/internal/`) quarantined strictly outside the web document root (`site/`).
2. **Cryptographic Token Rigor**:
   - HMAC-SHA256 signature verification computed in constant-time via `hmac.compare_digest`.
   - Tampered payloads fail signature validation and return `None`.
   - Expired tokens fail `time.time()` check and return `None`.
   - Average token verification latency: 3.05 µs (p95: 3.17 µs).
3. **Server-Side Role-Based Downgrade**:
   - Client-asserted roles (`admin`, `procurement`) without authentic tokens are downgraded to `customer` with `wasTampered=True`.
   - Downgrade occurs at the server HTTP boundary before any retrieval or database queries execute.
4. **IDOR Defense**:
   - Direct object requests to confidential documents (`/api/rag/doc?docId=PROC-...`) reject unauthorized roles with HTTP 403 Forbidden.
   - Legitimate procurement officers with signed tokens receive HTTP 200 OK.
5. **Demonstration Mode Isolation**:
   - Intentionally vulnerable demonstration mode (`hardened=False`) is purely request-scoped.
   - Tested 100 alternating requests in parallel; zero cross-talk or permanent server-side degradation was observed.
   - Per-session rate limiter successfully throttled abusive request bursts while permitting 100 concurrent independent attendee sessions.
