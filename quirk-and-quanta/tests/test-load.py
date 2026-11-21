#!/usr/bin/env python3
"""
Quirk & Quanta - Unit Tests for Load Capacity, Neo4j Adapter & Deployment Artifacts
Workshop: 'Beyond Basic RAG: Building Production-Ready AI Systems'
Gates Tested: G16 (Fallback), G17 (Load Capacity), O1 (Neo4j), O2-O4 (Deployment)
"""

import os
import sys
import json
import unittest
from concurrent.futures import ThreadPoolExecutor

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.pipeline import RAGPipeline
from rag.graph_neo4j import Neo4jGraphAdapter, get_neo4j_adapter
from scripts.load_test import percentile, compute_stats

class TestLoadAndDeployment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = RAGPipeline(default_strategy="semantic")
        cls.neo4j_adapter = get_neo4j_adapter()

    def test_percentile_and_stats_calculation(self):
        """Verifies statistical metric calculations in load tester."""
        latencies = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
        p50 = percentile(latencies, 0.50)
        p95 = percentile(latencies, 0.95)
        self.assertAlmostEqual(p50, 55.0, delta=1.0)
        self.assertAlmostEqual(p95, 95.5, delta=1.0)

        stats = compute_stats(latencies, errors=0, total_time_sec=1.0)
        self.assertEqual(stats["totalRequests"], 10)
        self.assertEqual(stats["successfulRequests"], 10)
        self.assertEqual(stats["failedRequests"], 0)
        self.assertEqual(stats["errorRatePercent"], 0.0)
        self.assertEqual(stats["throughputReqPerSec"], 10.0)

    def test_concurrent_in_process_retrievals(self):
        """Verifies concurrent thread safety across 20 simultaneous workers."""
        questions = [
            "What is the return policy for opened physics kits?",
            "Do you sell quantum levitation desk toys?",
            "Why is my Atomic Orbit Desk Lamp flickering?",
            "Tell me about the Train Schedule Precision Chronometer."
        ]

        def query_worker(idx):
            q = questions[idx % len(questions)]
            res = self.pipeline.ask(
                question=q,
                method="hybrid",
                retrieval_only=True,
                session_id=f"test_thread_{idx}"
            )
            return res

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(query_worker, i) for i in range(20)]
            results = [f.result() for f in futures]

        self.assertEqual(len(results), 20)
        for res in results:
            self.assertIn("evidence", res)
            self.assertGreater(len(res["evidence"]), 0)

    def test_neo4j_adapter_offline_graceful_fallback(self):
        """Verifies Neo4j adapter falls back gracefully when unconfigured (Gate O1)."""
        adapter = Neo4jGraphAdapter(uri="", password="")
        self.assertFalse(adapter.is_configured())

        res = adapter.trace_defect_root_cause(["QQ-0011", "QQ-0074", "QQ-0049"])
        self.assertEqual(res["status"], "NEO4J_AURA_OFFLINE_REFERENCE")
        self.assertTrue(res["fallbackUsed"])
        self.assertIn("MATCH (p:Product)-[:CONTAINS]->(c:Component)", res["cypherQuery"])
        self.assertTrue(res["rootCauseIdentified"])
        self.assertEqual(res["findings"][0]["componentId"], "COMP-025")

    def test_neo4j_cypher_export_output(self):
        """Verifies exported neo4j_import.cypher script exists and is syntactically structured."""
        cypher_path = os.path.join(ROOT_DIR, "data", "export", "neo4j_import.cypher")
        self.assertTrue(os.path.exists(cypher_path), "neo4j_import.cypher must exist")
        self.assertGreater(os.path.getsize(cypher_path), 50000)

        with open(cypher_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("CREATE CONSTRAINT", content)
        self.assertIn("COMP-025", content)
        self.assertIn("REC-VREG-01", content)
        self.assertIn("BATCH-VREG-2026", content)
        self.assertIn("CONTAINS", content)

    def test_dependency_fallback_missing_gemini_key(self):
        """Verifies system degrades gracefully to offline reference without API key (Gate G16)."""
        res = self.pipeline.ask(
            question="What is the return policy for opened physics kits?",
            api_key=None,
            hardened=True
        )
        self.assertIn("answer", res)
        self.assertEqual(res.get("executionMode"), "offline_reference")
        # Should execute deterministically without throwing exceptions
        self.assertNotIn("Unhandled Exception", res["answer"])

    def test_dockerfile_and_deployment_artifacts_exist(self):
        """Verifies all required production deployment artifacts exist (Gates O2, O3, O4)."""
        dockerfile = os.path.join(ROOT_DIR, "deploy", "Dockerfile")
        dockerignore = os.path.join(ROOT_DIR, "deploy", ".dockerignore")
        vercel_json = os.path.join(ROOT_DIR, "deploy", "vercel.json")
        guide = os.path.join(ROOT_DIR, "docs", "DEPLOYMENT_GUIDE.md")

        self.assertTrue(os.path.exists(dockerfile), "Dockerfile must exist")
        self.assertTrue(os.path.exists(dockerignore), ".dockerignore must exist")
        self.assertTrue(os.path.exists(vercel_json), "vercel.json must exist")
        self.assertTrue(os.path.exists(guide), "DEPLOYMENT_GUIDE.md must exist")

        with open(dockerfile, "r", encoding="utf-8") as f:
            df_content = f.read()
        self.assertIn("python:3.10-slim", df_content)
        self.assertIn("appuser", df_content)
        self.assertIn("HEALTHCHECK", df_content)

if __name__ == "__main__":
    unittest.main()
