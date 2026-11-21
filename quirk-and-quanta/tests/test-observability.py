#!/usr/bin/env python3
"""
Quirk & Quanta - Observability, Tracing & Cost Telemetry Test Suite
Tests request UUID tagging, span timing, token estimation, cost calculation,
ring buffer capacity, and runaway usage spike simulation (Story 7).
"""

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.observability import (
    estimate_tokens,
    calculate_cost_usd,
    RequestTrace,
    TraceCollector,
    get_trace_collector
)
from rag.pipeline import RAGPipeline

class TestObservabilityAndTracing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collector = get_trace_collector()
        cls.pipeline = RAGPipeline(default_strategy="semantic")

    def test_token_estimation_and_cost_calculation(self):
        text = "What are the technical specifications of the Quantum Microscope?"
        tokens = estimate_tokens(text)
        self.assertGreater(tokens, 5)
        # Cost for 1,000 input tokens and 200 output tokens:
        # (1000/1e6)*0.075 + (200/1e6)*0.30 = 0.000075 + 0.000060 = 0.000135
        cost = calculate_cost_usd(1000, 200)
        self.assertEqual(cost, 0.000135)

    def test_request_trace_spans_and_completion(self):
        collector = TraceCollector(capacity=10)
        trace = collector.start_trace(
            session_id="session_test",
            role="customer",
            question="Tell me about the Quantum Microscope",
            strategy="semantic",
            method="vector"
        )
        self.assertTrue(trace.request_id.startswith("req_"))
        trace.add_span("auth_verification", 0.15)
        trace.add_span("vector_retrieval", 25.4)
        trace.complete(
            answer="The Quantum Microscope features 500x magnification.",
            evidence=[{"text": "Dossier for Quantum Microscope"}],
            guardrail_action="PASSED"
        )
        collector.record_trace(trace)

        retrieved_trace = collector.get_trace(trace.request_id)
        self.assertIsNotNone(retrieved_trace)
        self.assertEqual(retrieved_trace["status"], "completed")
        self.assertEqual(len(retrieved_trace["latency"]["spans"]), 2)
        self.assertGreater(retrieved_trace["tokenUsage"]["totalTokens"], 0)
        self.assertGreater(retrieved_trace["estimatedCostUsd"], 0.0)

    def test_trace_collector_ring_buffer_capacity(self):
        small_collector = TraceCollector(capacity=5)
        for i in range(10):
            t = small_collector.start_trace(question=f"Question {i}")
            t.complete(f"Answer {i}", [])
            small_collector.record_trace(t)

        self.assertEqual(len(small_collector.traces), 5)
        self.assertEqual(small_collector.total_requests, 10)

    def test_cost_spike_simulation_story7(self):
        sim = self.collector.simulate_cost_spike(iterations=40)
        self.assertIn("unprotectedRunaway", sim)
        self.assertIn("protectedSafeguard", sim)
        self.assertGreater(sim["unprotectedRunaway"]["totalTokens"], sim["protectedSafeguard"]["totalTokens"])
        self.assertGreater(sim["costSavedUsd"], 0.0)
        self.assertGreater(sim["protectedSafeguard"]["throttledRequests"], 0)

    def test_pipeline_ask_returns_trace_and_request_id(self):
        query = "What is the price of QQ-0015?"
        res = self.pipeline.ask(query, top_k=2, role="customer")
        self.assertIn("requestId", res)
        self.assertTrue(res["requestId"].startswith("req_"))
        self.assertIn("trace", res)
        self.assertIn("tokenUsage", res["trace"])
        self.assertIn("spans", res["trace"]["latency"])

if __name__ == "__main__":
    unittest.main()
