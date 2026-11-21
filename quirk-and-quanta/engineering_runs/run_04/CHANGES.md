# Engineering Run 04: Changes
## P0-F: Server-Side RBAC Enforcement, Confidential Cost Protection & IDOR Mitigation

### Summary of Modifications:
1. **`rag/auth.py`**:
   - Implemented cryptographic HMAC-SHA256 session token generation and verification (`create_signed_token`, `verify_token`).
   - Implemented server-side role resolution (`resolve_effective_role`):
     - In hardened mode: downgrades unauthenticated client role escalation attempts (`role="admin"`) to `customer` and flags `was_tampered = True`.
     - In vulnerable mode: demonstrates client role escalation for Demo 16.
   - Implemented IDOR access control validator (`check_resource_access`).
2. **`rag/pipeline.py`**:
   - Updated `ask()` to authenticate `auth_token` and enforce `effective_role`.
   - Attached `roleResolution` audit telemetry to output.
3. **`rag/server.py`**:
   - Enforced server-side role resolution at the HTTP network boundary.
   - Added `GET /api/rag/auth/demo-token` to issue valid HMAC-SHA256 bearer tokens.
   - Added `POST /api/rag/doc` endpoint demonstrating IDOR vulnerability vs hardened `403 Forbidden` defense.
4. **`site/workshop.html` & `site/js/workshop.js`**:
   - Added "🔑 Issue Admin Token" button and live bearer token status indicator.
   - Added "🎯 Test IDOR Direct Resource Access" button (Demo 16).
   - Displayed security warnings when role tampering is intercepted.
5. **`tests/test-security.py`**:
   - Added 8 unit tests covering HMAC token lifecycle, forged signature rejection, role tampering downgrade, cost leakage prevention, and IDOR protection.
