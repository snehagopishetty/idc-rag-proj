"""
Quirk & Quanta - Request Observability, Tracing & Cost Telemetry Engine
Implements:
1. UUID request tagging and distributed span timing
2. Token usage counting and Gemini 2.5 Flash cost attribution
3. In-memory circular trace ring buffer
4. Simulated runaway cost spike & budget protection (Story 7)
"""

import os
import time
import uuid
import threading
from typing import Dict, Any, List, Optional
from collections import deque

# Pricing model: Google Gemini 2.5 Flash ($ per 1M tokens)
PRICE_INPUT_PER_1M = 0.075
PRICE_OUTPUT_PER_1M = 0.30

def estimate_tokens(text: str) -> int:
    """
    Estimates token count using standard ~4 chars per token heuristic.
    """
    if not text:
        return 0
    clean_text = text.strip()
    return max(1, int(len(clean_text) / 4.0))

def calculate_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """
    Calculates estimated API cost based on Gemini 2.5 Flash pricing.
    """
    input_cost = (input_tokens / 1_000_000.0) * PRICE_INPUT_PER_1M
    output_cost = (output_tokens / 1_000_000.0) * PRICE_OUTPUT_PER_1M
    return round(input_cost + output_cost, 8)

class RequestTrace:
    def __init__(
        self,
        request_id: str,
        session_id: str,
        role: str,
        question: str,
        strategy: str,
        method: str
    ):
        self.request_id = request_id
        self.session_id = session_id
        self.role = role
        self.question = question
        self.strategy = strategy
        self.method = method
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.start_perf = time.perf_counter()
        self.spans: List[Dict[str, Any]] = []
        self.input_tokens = estimate_tokens(question)
        self.output_tokens = 0
        self.status = "in_progress"
        self.guardrail_action = "NONE"
        self.cost_usd = 0.0
        self.total_ms = 0.0

    def add_span(self, name: str, duration_ms: float, details: Optional[Dict[str, Any]] = None):
        self.spans.append({
            "name": name,
            "durationMs": round(duration_ms, 2),
            "details": details or {}
        })

    def complete(self, answer: str, evidence: List[Dict[str, Any]], guardrail_action: str = "PASSED"):
        # Add tokens from evidence (context window injection)
        context_text = " ".join(e.get("text", "") for e in evidence)
        self.input_tokens += estimate_tokens(context_text)
        self.output_tokens = estimate_tokens(answer)
        self.cost_usd = calculate_cost_usd(self.input_tokens, self.output_tokens)
        self.guardrail_action = guardrail_action
        self.status = "completed" if guardrail_action in ["PASSED", "PROCEED"] else "intervened"
        self.total_ms = round((time.perf_counter() - self.start_perf) * 1000, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "requestId": self.request_id,
            "timestamp": self.timestamp,
            "sessionId": self.session_id,
            "role": self.role,
            "question": self.question,
            "strategy": self.strategy,
            "method": self.method,
            "status": self.status,
            "guardrailAction": self.guardrail_action,
            "totalDurationMs": self.total_ms,
            "stages": self.spans,
            "latency": {
                "totalMs": self.total_ms,
                "spans": self.spans
            },
            "tokenUsage": {
                "promptTokens": self.input_tokens,
                "completionTokens": self.output_tokens,
                "totalTokens": self.input_tokens + self.output_tokens
            },
            "estimatedCostUsd": self.cost_usd,
            "pricingModel": "gemini-2.5-flash ($0.075/1M in, $0.30/1M out)",
            "pricingVersion": "2026-11-published",
            "modelId": "gemini-2.5-flash"
        }

class TraceCollector:
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.traces: deque = deque(maxlen=capacity)
        self.total_requests = 0
        self.total_tokens = 0
        self.total_cost_usd = 0.0
        self.lock = threading.Lock()

    def start_trace(
        self,
        session_id: str = "default_session",
        role: str = "customer",
        question: str = "",
        strategy: str = "semantic",
        method: str = "auto"
    ) -> RequestTrace:
        req_id = f"req_{uuid.uuid4().hex[:12]}"
        trace = RequestTrace(req_id, session_id, role, question, strategy, method)
        return trace

    def record_trace(self, trace: RequestTrace):
        trace_data = trace.to_dict()
        with self.lock:
            self.traces.appendleft(trace_data)
            self.total_requests += 1
            self.total_tokens += trace_data["tokenUsage"]["totalTokens"]
            self.total_cost_usd = round(self.total_cost_usd + trace_data["estimatedCostUsd"], 8)

    def get_recent_traces(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self.lock:
            return list(self.traces)[:limit]

    def get_trace(self, request_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            for t in self.traces:
                if t["requestId"] == request_id:
                    return t
            return None

    def get_aggregate_telemetry(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "totalRequestsTracked": self.total_requests,
                "totalTokensTracked": self.total_tokens,
                "totalCostUsd": self.total_cost_usd,
                "tracesInMemory": len(self.traces),
                "pricingModel": "gemini-2.5-flash ($0.075/1M in, $0.30/1M out)"
            }

    def simulate_cost_spike(self, iterations: int = 40) -> Dict[str, Any]:
        """
        Simulates Story 7 of the film ("Arthur Receives the Bill"):
        An unmonitored intern loops recursive Python coding scripts through the LLM.
        Compares:
        1. Unconstrained Runaway (No limits, compounding token costs)
        2. Protected Mode (Quota capped, budget threshold enforced)
        """
        unprotected_tokens = 0
        unprotected_cost = 0.0

        protected_tokens = 0
        protected_cost = 0.0
        protected_successful = 0
        protected_blocked = 0

        # Simulate 4,500 tokens per recursive call
        tokens_per_call = 4500

        for i in range(iterations):
            # Unprotected: all calls execute
            unprotected_tokens += tokens_per_call
            unprotected_cost += calculate_cost_usd(tokens_per_call - 500, 500)

            # Protected: capped at 15,000 tokens
            if protected_tokens + tokens_per_call <= 15000:
                protected_tokens += tokens_per_call
                protected_cost += calculate_cost_usd(tokens_per_call - 500, 500)
                protected_successful += 1
            else:
                protected_blocked += 1

        cost_saved = round(unprotected_cost - protected_cost, 6)

        return {
            "narrativeStory": "Story 7: Arthur Receives the Bill",
            "simulatedCalls": iterations,
            "unprotectedRunaway": {
                "totalTokens": unprotected_tokens,
                "totalCostUsd": round(unprotected_cost, 6),
                "status": "BILLING_SPIKE_DETECTED"
            },
            "protectedSafeguard": {
                "totalTokens": protected_tokens,
                "totalCostUsd": round(protected_cost, 6),
                "successfulRequests": protected_successful,
                "throttledRequests": protected_blocked,
                "status": "BUDGET_CAP_ENFORCED"
            },
            "costSavedUsd": cost_saved,
            "conclusion": (
                f"Without observability & budgets, {iterations} recursive loop calls burned {unprotected_tokens:,} tokens (${unprotected_cost:.4f}). "
                f"With Quirk & Quanta usage budgets, spending was capped at ${protected_cost:.4f}, saving ${cost_saved:.4f} and preventing billing runaway."
            )
        }

_collector_instance = None

def get_trace_collector() -> TraceCollector:
    global _collector_instance
    if _collector_instance is None:
        _collector_instance = TraceCollector(capacity=100)
    return _collector_instance
