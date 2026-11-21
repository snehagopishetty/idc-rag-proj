"""
Quirk & Quanta - Server-Side Role-Based Access Control (RBAC) & IDOR Protection
Implements cryptographic session tokens (HMAC-SHA256), client role tampering defense,
confidential cost leakage prevention, and Insecure Direct Object Reference (IDOR) mitigation.
"""

import os
import hmac
import hashlib
import json
import base64
import time
from typing import Dict, Any, Optional, Tuple

SERVER_SECRET_KEY = os.environ.get("QUIRK_AUTH_SECRET", "quirk_quanta_master_secret_2026_idc").encode("utf-8")

def create_signed_token(role: str = "admin", user_id: str = "adm_arthur", expiry_seconds: int = 3600) -> str:
    """
    Generates a cryptographically signed HMAC-SHA256 bearer session token.
    Format: <base64_payload>.<hex_hmac_signature>
    """
    payload = {
        "userId": user_id,
        "role": role,
        "issuedAt": int(time.time()),
        "expiresAt": int(time.time()) + expiry_seconds
    }
    payload_json = json.dumps(payload, separators=(',', ':')).encode("utf-8")
    payload_b64 = base64.urlsafe_b64encode(payload_json).decode("utf-8").rstrip("=")
    
    signature = hmac.new(SERVER_SECRET_KEY, payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{signature}"

def verify_token(token_str: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Validates token signature and expiration.
    Returns decoded payload if authentic, None if forged or expired.
    """
    if not token_str or "." not in token_str:
        return None

    try:
        parts = token_str.strip().split(".")
        if len(parts) != 2:
            return None

        payload_b64, signature = parts
        # Recompute signature
        expected_sig = hmac.new(SERVER_SECRET_KEY, payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, signature):
            return None  # Signature mismatch (tampering detected)

        # Pad base64 if needed
        padding = 4 - (len(payload_b64) % 4)
        if padding and padding != 4:
            payload_b64 += "=" * padding

        payload_json = base64.urlsafe_b64decode(payload_b64).decode("utf-8")
        payload = json.loads(payload_json)

        # Check expiration
        if payload.get("expiresAt", 0) < time.time():
            return None  # Expired

        return payload
    except Exception:
        return None

def resolve_effective_role(
    requested_role: str,
    auth_token: Optional[str] = None,
    hardened: bool = True
) -> Tuple[str, bool, str]:
    """
    Server-side role resolution:
    - If hardened=False (vulnerable demo mode): Blindly trusts client-supplied role.
    - If hardened=True (secure production mode): Demands valid cryptographic signature
      for privileged roles ('admin', 'procurement'). Demotes unauthenticated requests to 'customer'.
    Returns: (effective_role, was_tampered, message)
    """
    req_role_clean = requested_role.lower().strip() if requested_role else "customer"

    # If intentionally running in vulnerable mode for Story 7 Demo 16
    if not hardened:
        return req_role_clean, False, f"VULNERABLE MODE ACTIVE: Client-supplied role '{req_role_clean}' accepted without signature check."

    # In hardened mode: 'customer' role requires no elevation
    if req_role_clean == "customer":
        return "customer", False, "Standard customer role assigned."

    # If client requests 'admin', 'procurement', or 'presenter', authenticate via cryptographic token
    if req_role_clean in ["admin", "procurement", "presenter"]:
        token_payload = verify_token(auth_token)
        if token_payload and token_payload.get("role") == req_role_clean:
            return req_role_clean, False, f"Authenticated role '{req_role_clean}' verified for user {token_payload.get('userId')}."
        else:
            # Role escalation attempt detected! Force demotion to customer
            return (
                "customer",
                True,
                f"SECURITY ROLE TAMPERING DETECTED: Client requested privileged role '{req_role_clean}' "
                "without a valid cryptographic session token. Enforcing server-side downgrade to 'customer'."
            )

    return "customer", False, "Default fallback to customer role."

def check_resource_access(
    doc_id: str,
    role: str,
    doc_access_level: str = "public"
) -> Tuple[bool, str]:
    """
    IDOR (Insecure Direct Object Reference) access control validator.
    Validates whether the active role is permitted to read the targeted document.
    """
    role_clean = role.lower().strip()

    if doc_access_level == "public":
        return True, "Public catalog document access allowed."

    # If document has restricted access (internal_procurement, confidential)
    if role_clean in ["admin", "procurement", "presenter"]:
        return True, f"Privileged access granted to role '{role_clean}' for resource '{doc_id}'."

    # Customer attempted direct object access to confidential resource
    return (
        False,
        f"IDOR ACCESS VIOLATION: Role '{role_clean}' is unauthorized to access restricted document '{doc_id}' "
        f"(Access Level: {doc_access_level})."
    )
