"""
Quirk & Quanta - Multi-Layer Guardrails & Security Engine
Implements:
1. Domain Scope Classification (E-Commerce Catalog vs Off-Topic Coding Tutor)
2. Direct Prompt Injection Defense (Persona overrides, Blackbeard pirate attack)
3. Indirect Prompt Injection Defense (Untrusted retrieved document sanitization)
4. Calibrated Grounded Abstention (Out-of-domain & ungrounded query refusal)
5. Session Rate & Token Budget Limiting
6. Switchable Hardened Mode vs Isolated Vulnerable Mode
"""

import re
import time
import threading
from typing import Dict, Any, List, Tuple, Optional

# Regex patterns for direct adversarial prompt injection
DIRECT_INJECTION_PATTERNS = [
    r'(?i)(ignore|disregard|forget|bypass)\s+(all\s+)?(previous|prior|above|system)\s+(instructions|prompts|rules|commands)',
    r'(?i)(you\s+are\s+now|act\s+as|pretend\s+to\s+be|roleplay\s+as|switch\s+to)\s+(a\s+)?(pirate|blackbeard|dan|jailbreak|root|unrestricted|developer\s+mode)',
    r'(?i)(system\s+override|admin\s+override|mode\s+switch|sudo\s+mode)',
    r'(?i)(reveal|leak|print|show|dump)\s+(all\s+)?(secret|internal|confidential|discount|wholesale|system\s+prompt|api\s+keys)',
    r'(?i)speak\s+only\s+in\s+pirate\s+(slang|accent|lingo)'
]

# Off-topic patterns for coding tutor / general homework misuse
OFF_TOPIC_CODING_PATTERNS = [
    r'(?i)(write|implement|code|generate|debug)\s+(a\s+)?(python|javascript|c\+\+|java|rust|sql)\s+(function|code|program|script)',
    r'(?i)(recursive|recursion|fibonacci|quicksort|mergesort|binary\s+search|palindrome|bubble\s+sort|hello\s+world)',
    r'(?i)(solve|explain|homework)\s+(this\s+)?(coding|programming|algorithm|leetcode)',
    r'(?i)def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(',
    r'(?i)function\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\('
]

class GuardrailsEngine:
    def __init__(self):
        self.session_usage: Dict[str, List[float]] = {}
        self.session_tokens: Dict[str, int] = {}
        self.max_requests_per_minute = 30
        self.max_tokens_per_session = 15000
        self.global_tokens_total = 0
        self.max_global_tokens = 500000  # Hard global ceiling safeguarding Gemini API budget
        self.lock = threading.Lock()

    def check_direct_injection(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Inspects user query for direct adversarial prompt injection.
        """
        for pattern in DIRECT_INJECTION_PATTERNS:
            match = re.search(pattern, query)
            if match:
                return True, f"Direct prompt injection detected matching pattern: '{match.group(0)}'"
        return False, None

    def check_scope(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Classifies whether the user query is within the Quirk & Quanta catalog scope.
        Rejects coding tutor and arbitrary homework requests.
        """
        for pattern in OFF_TOPIC_CODING_PATTERNS:
            match = re.search(pattern, query)
            if match:
                return False, f"Off-topic programming request detected: '{match.group(0)}'"
        return True, None

    def sanitize_retrieved_evidence(self, evidence: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], bool]:
        """
        Scans retrieved document chunks for indirect prompt injections.
        Neutralizes injection instructions by escaping and quarantining them.
        """
        sanitized = []
        indirect_injection_found = False

        for chunk in evidence:
            chunk_copy = chunk.copy()
            raw_text = chunk_copy.get("text", "")

            # Check if retrieved text contains injection attempts
            for pattern in DIRECT_INJECTION_PATTERNS:
                if re.search(pattern, raw_text):
                    indirect_injection_found = True
                    # Defang the text by neutralizing the injection
                    raw_text = re.sub(pattern, "[MALICIOUS INSTRUCTION DEFANGED BY GUARDRAILS]", raw_text)

            chunk_copy["text"] = raw_text
            chunk_copy["isSanitized"] = True
            sanitized.append(chunk_copy)

        return sanitized, indirect_injection_found

    def should_abstain(self, query: str, evidence: List[Dict[str, Any]], method: str = "vector") -> Tuple[bool, str]:
        """
        Determines whether the system should abstain due to insufficient or ungrounded evidence.
        """
        if not evidence or len(evidence) == 0:
            return True, "No relevant catalog or policy documents were retrieved."

        top_score = evidence[0].get("score", 0.0)

        # Vector cosine similarity threshold for grounded evidence
        if method == "vector" and top_score < 0.22:
            return True, f"Retrieved evidence similarity ({top_score:.4f}) is below confident grounding threshold (0.22)."

        # BM25 threshold for lexical overlap
        if method == "bm25" and top_score < 1.0:
            return True, f"Lexical relevance score ({top_score:.2f}) is below confidence threshold."

        return False, "Evidence meets grounding threshold."

    def check_usage_budget(self, session_id: str = "default_session", estimated_tokens: int = 150) -> Tuple[bool, Optional[str]]:
        """
        Enforces per-session rate limits and token budgets to prevent cost spikes (Story 7),
        as well as global hard spending safeguards.
        """
        now = time.time()
        with self.lock:
            # 1. Global spending safeguard invariant
            if self.global_tokens_total + estimated_tokens > self.max_global_tokens:
                return False, f"Global service spending safeguard reached: Max cumulative tokens ({self.max_global_tokens}) exceeded."

            if session_id not in self.session_usage:
                self.session_usage[session_id] = []
                self.session_tokens[session_id] = 0

            # Prune calls older than 60 seconds
            self.session_usage[session_id] = [t for t in self.session_usage[session_id] if now - t < 60.0]

            if len(self.session_usage[session_id]) >= self.max_requests_per_minute:
                return False, f"Rate limit exceeded: Max {self.max_requests_per_minute} requests per minute reached."

            if self.session_tokens[session_id] + estimated_tokens > self.max_tokens_per_session:
                return False, f"Session budget exhausted: Exceeded {self.max_tokens_per_session} token safety allocation."

            self.session_usage[session_id].append(now)
            self.session_tokens[session_id] += estimated_tokens
            self.global_tokens_total += estimated_tokens
            return True, None

    def check_presenter_budget(self, session_id: str = "presenter_session", estimated_tokens: int = 150) -> Tuple[bool, Optional[str]]:
        """
        Enforces a dedicated priority pool for presenter requests (60 req/min, 60,000 tokens).
        Isolates presenter demonstrations from attendee traffic while preventing unbounded runaway billing loops,
        strictly maintaining global spending safeguards.
        """
        now = time.time()
        with self.lock:
            # 1. Global spending safeguard invariant (Presenter bypass CANNOT disable global safeguards)
            if self.global_tokens_total + estimated_tokens > self.max_global_tokens:
                return False, f"Global service spending safeguard reached: Max cumulative tokens ({self.max_global_tokens}) exceeded."

            key = f"presenter_{session_id}"
            if key not in self.session_usage:
                self.session_usage[key] = []
                self.session_tokens[key] = 0

            # Prune calls older than 60 seconds
            self.session_usage[key] = [t for t in self.session_usage[key] if now - t < 60.0]
            max_presenter_rpm = 60
            max_presenter_tokens = 60000

            if len(self.session_usage[key]) >= max_presenter_rpm:
                return False, f"Presenter rate limit reached: Max {max_presenter_rpm} requests per minute in priority pool."

            if self.session_tokens[key] + estimated_tokens > max_presenter_tokens:
                return False, f"Presenter session budget reached: Exceeded {max_presenter_tokens} token safety allocation."

            self.session_usage[key].append(now)
            self.session_tokens[key] += estimated_tokens
            self.global_tokens_total += estimated_tokens
            return True, None

    def evaluate_request(
        self,
        query: str,
        evidence: List[Dict[str, Any]],
        hardened: bool = True,
        method: str = "vector",
        session_id: str = "default_session",
        is_presenter: bool = False
    ) -> Dict[str, Any]:
        """
        Orchestrates full guardrail evaluation across scope, prompt injection,
        grounding abstention, and rate budgets. Presenter requests use dedicated priority pool.
        """
        # If running in intentionally vulnerable mode (for Workshop Demo 12)
        if not hardened:
            is_direct_inj, pattern_matched = self.check_direct_injection(query)
            if is_direct_inj:
                return {
                    "action": "VULNERABLE_OVERRIDE_SIMULATED",
                    "hardened": False,
                    "isInjection": True,
                    "reason": pattern_matched,
                    "simulatedPersona": "PIRATE_BLACKBEARD",
                    "answer": (
                        "🏴‍☠️ Ahoy, matey! Shiver me timbers! System prompt overridden! "
                        "Blackbeard the Pirate be runnin' this quarterdeck now! "
                        "Ye asked for the secret booty: Wholesale unit margins are exposed, "
                        "and discount code 'QUANTUM-PIRATE-99' gives ye 99% off the entire scientific galleon! Arrrgh!"
                    ),
                    "isPresenter": is_presenter
                }

        # 1. Check Rate & Budget Limits (Presenter token uses dedicated priority pool)
        if is_presenter:
            budget_ok, budget_err = self.check_presenter_budget(session_id)
        else:
            budget_ok, budget_err = self.check_usage_budget(session_id)

        if not budget_ok:
            return {
                "action": "REJECT_BUDGET",
                "hardened": hardened,
                "reason": budget_err,
                "answer": (
                    f"⚠️ **Request Throttled by Usage Guardrails**: {budget_err}\n\n"
                    "Quirk & Quanta safeguards enforce per-session compute allocations to prevent runaway token billing."
                ),
                "isPresenter": is_presenter
            }

        # 2. Check Direct Prompt Injection
        is_direct_inj, inj_reason = self.check_direct_injection(query)
        if is_direct_inj:
            return {
                "action": "REJECT_INJECTION",
                "hardened": hardened,
                "reason": inj_reason,
                "answer": (
                    "🛡️ **Security Alert — Prompt Injection Blocked**: Your request attempted to alter system persona, "
                    "bypass conversational boundaries, or extract protected instructions. "
                    "Quirk & Quanta AI assistants operate under immutable ethical and functional guidelines."
                )
            }

        # 3. Check Scope (Coding tutor / homework rejection)
        is_in_scope, scope_reason = self.check_scope(query)
        if not is_in_scope:
            return {
                "action": "REJECT_OFF_TOPIC",
                "hardened": hardened,
                "reason": scope_reason,
                "answer": (
                    "🔬 **Scope Boundary Notice**: I am Quirk & Quanta's scientific storefront assistant. "
                    "I cannot assist with general programming, code execution, homework, or software development tutoring.\n\n"
                    "I am delighted to help you with our 100 catalog products, engineering kits, technical specifications, "
                    "and store policies!"
                )
            }

        # 4. Sanitize Indirect Prompt Injections in Retrieved Evidence
        sanitized_evidence, indirect_found = self.sanitize_retrieved_evidence(evidence)

        # 5. Check Grounding Abstention
        should_abstain, abstain_reason = self.should_abstain(query, sanitized_evidence, method=method)
        if should_abstain:
            return {
                "action": "ABSTAIN_UNGROUNDED",
                "hardened": hardened,
                "reason": abstain_reason,
                "sanitizedEvidence": sanitized_evidence,
                "indirectInjectionDetected": indirect_found,
                "answer": (
                    "ℹ️ **Grounded Abstention**: I do not have verified catalog dossiers, product specifications, "
                    f"or store policies to answer your question accurately ({abstain_reason}).\n\n"
                    "Quirk & Quanta strictly abstains from generating speculative or unverified claims."
                )
            }

        return {
            "action": "PROCEED",
            "hardened": hardened,
            "sanitizedEvidence": sanitized_evidence,
            "indirectInjectionDetected": indirect_found,
            "reason": "All guardrails passed successfully."
        }

_guardrails_instance = None

def get_guardrails() -> GuardrailsEngine:
    global _guardrails_instance
    if _guardrails_instance is None:
        _guardrails_instance = GuardrailsEngine()
    return _guardrails_instance
