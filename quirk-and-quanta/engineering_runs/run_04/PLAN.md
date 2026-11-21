# Engineering Run 04: Plan
## Target: P0-F — Server-Side RBAC Enforcement, Confidential Cost Protection & IDOR Mitigation

### 1. Action 1: Inspect & Reproduce
- **Baseline Git Commit**: `fb0baff`
- **Current State**:
  - The retriever filters chunks by `role` (`item["accessLevel"] == "public"` if `role == "customer"`).
  - However, the role is currently trusted as sent by the client in the JSON body (`params.get("role")`).
  - An attacker can trivially send `{"role": "admin"}` or tamper with query parameters to access confidential procurement data.
  - Furthermore, there is no direct object retrieval endpoint or verification to demonstrate IDOR (Insecure Direct Object Reference).

### 2. Action 2: Decide & Select Next Target
- **Selected Track**: P0-F (Server-Side RBAC Enforcement & IDOR Defense)
- **Gates Targeted**:
  - G12: Customer/admin access rules are enforced server-side via cryptographic token verification.
  - G13: IDOR and client role tampering fail against hardened mode (and succeed only in isolated vulnerable demonstration mode).
- **Work Breakdown**:
  1. Build authentication & session security engine `rag/auth.py`:
     - Standard library `hmac` + `hashlib` HMAC-SHA256 token signing and verification (`create_signed_token`, `verify_token`).
     - Server-side role resolution:
       - If `hardened=True` (default): Validates session token / Authorization header. If invalid, tampered, or missing, forces `role="customer"`, logs `SECURITY_ROLE_TAMPERING_BLOCKED`.
       - If `hardened=False`: Demonstrates vulnerable role escalation when requested by the presenter for Demo 16.
     - Document access authorization check (`check_document_access(doc_id, role)`).
  2. Add document inspection endpoint `GET /api/rag/doc/:id` in `rag/server.py`:
     - In vulnerable mode: Direct reference fetches confidential procurement documents without permission.
     - In hardened mode: Rejects unauthorized direct object access with `403 Forbidden` and structured security audit telemetry.
  3. Update Workshop Lab UI (`site/workshop.html` & `site/js/workshop.js`):
     - Interactive controls for Demo 15 (Customer asking for unit cost/margin).
     - Interactive controls for Demo 16 (Client-controlled role escalation & IDOR vulnerability vs hardened defense).
     - Signed token indicator pill in UI.
  4. Build test suite `tests/test-security.py` covering:
     - Role tampering rejection under hardened mode.
     - Valid admin token acceptance.
     - Cost leakage prevention for customer queries.
     - IDOR direct object reference protection.
     - Vulnerable mode demonstration reproducibility.
