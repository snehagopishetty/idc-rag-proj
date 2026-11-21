# Engineering Run 04: Security Results

### 1. Cryptographic Server-Side RBAC Enforcement (Gate G12)
- Implemented HMAC-SHA256 bearer session tokens.
- When an unauthenticated client passes `role="admin"` in JSON or URL query parameters:
  - In hardened mode: Demoted to `role="customer"`, `wasTampered = True`, and confidential documents remain inaccessible.
  - In vulnerable mode: Accepted without validation for educational demonstration (Demo 16).

### 2. Confidential Cost-Price Exposure Scenario (Demo 15)
- Customer asking for unit acquisition costs or supplier margins on `QQ-0001`:
  - 0 internal procurement documents leaked.
  - Only public catalog specifications and retail prices returned.

### 3. Insecure Direct Object Reference (IDOR) Mitigation (Gate G13)
- Direct resource fetching endpoint `/api/rag/doc` validates resource classification (`accessLevel`) against cryptographic session permissions.
- Unauthorized attempts to fetch `PROC-QQ-0001` or internal documents are rejected with `403 Forbidden` and security audit log entries.
