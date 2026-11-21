#!/usr/bin/env python3
"""
Quirk & Quanta - Workshop Playground Endpoint Acceptance Suite (In-Process)
Validates all workshop playground capabilities:
1. Status telemetry & Neo4j badge
2. OKF (Open Knowledge Format) bundle data & integrity
3. Chunk inspector (Structural vs Fixed vs Sliding)
4. Query embedding inspection (768-D, norm, provenance, SKU drift notice)
5. Multi-strategy retrieval (Vector, BM25, Hybrid RRF)
6. Side-by-side comparison matrix data structures
7. Multi-hop Knowledge Graph defect resolution
8. Server-side RBAC & IDOR security invariants
"""

import os
import sys
import json
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.pipeline import RAGPipeline
from rag.retriever import QuirkRetriever
from rag.graph_local import get_graph
from rag.graph_neo4j import get_neo4j_adapter
from rag.auth import create_signed_token, verify_token, resolve_effective_role, check_resource_access

class WorkshopPlaygroundInProcessTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = RAGPipeline(default_strategy="semantic")
        cls.retriever = cls.pipeline.retriever
        cls.graph = get_graph()
        cls.neo4j = get_neo4j_adapter()

    def test_01_neo4j_status_and_badge(self):
        telemetry = self.neo4j.get_telemetry()
        self.assertIn("configured", telemetry)
        self.assertIn("status", telemetry)
        self.assertIn("badge", telemetry)
        # When unconfigured, should report offline fallback badge
        if not telemetry["configured"]:
            self.assertEqual(telemetry["status"], "not_connected")
            self.assertIn("Not Connected", telemetry["badge"])

    def test_02_okf_bundle_manifest_and_entities(self):
        okf_dir = os.path.join(ROOT_DIR, "data", "okf")
        manifest_file = os.path.join(okf_dir, "manifest.json")
        entities_file = os.path.join(okf_dir, "entities.jsonl")
        relations_file = os.path.join(okf_dir, "relations.jsonl")

        self.assertTrue(os.path.exists(manifest_file))
        self.assertTrue(os.path.exists(entities_file))
        self.assertTrue(os.path.exists(relations_file))

        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(manifest["format"], "open-knowledge-format")
        self.assertEqual(manifest["formatVersion"], "1.0.0")
        self.assertEqual(manifest["counts"]["entities"], 6)
        self.assertEqual(manifest["counts"]["relations"], 8)

        entities = []
        with open(entities_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entities.append(json.loads(line.strip()))
        self.assertEqual(len(entities), 6)
        eids = {e["id"] for e in entities}
        self.assertEqual(eids, {"QQ-0011", "QQ-0074", "QQ-0049", "COMP-025", "REC-VREG-01", "SUP-008"})

    def test_03_chunk_inspector_for_sample_documents(self):
        chunks_dir = os.path.join(ROOT_DIR, "data", "chunks")
        for strat in ["semantic", "fixed", "sliding"]:
            cf = os.path.join(chunks_dir, f"chunks_{strat}.json")
            self.assertTrue(os.path.exists(cf))
            with open(cf, "r", encoding="utf-8") as f:
                all_chunks = json.load(f)
            doc_chunks = [c for c in all_chunks if c.get("sourceId") == "QQ-0011"]
            self.assertGreater(len(doc_chunks), 0)

    def test_04_query_embedding_inspection(self):
        question = "What are the specifications and selling price of QQ-0015?"
        vec, mode = self.retriever.embed_query(question)
        self.assertEqual(len(vec), 768)
        self.assertEqual(mode, "cached_query_embedding")

        norm = sum(x * x for x in vec) ** 0.5
        self.assertAlmostEqual(norm, 1.0, places=2)

        # Vector retrieval includes telemetry
        vec_res = self.retriever.retrieve_vector(question, top_k=3, strategy="semantic")
        self.assertEqual(vec_res["dimensions"], 768)
        self.assertEqual(len(vec_res["queryVectorSample"]), 16)
        self.assertIn("skuDriftNotice", vec_res)

    def test_05_side_by_side_comparison(self):
        question = "QQ-0074 wireless charging pad Qi compliance and power specs"
        comp = self.pipeline.compare(question, top_k=3, strategy="semantic")

        self.assertIn("vector", comp)
        self.assertIn("bm25", comp)
        self.assertIn("hybrid", comp)

        self.assertEqual(len(comp["vector"]["evidence"]), 3)
        self.assertEqual(len(comp["bm25"]["evidence"]), 3)
        self.assertEqual(len(comp["hybrid"]["evidence"]), 3)

        top_h = comp["hybrid"]["evidence"][0]
        self.assertIn("vectorRank", top_h)
        self.assertIn("bm25Rank", top_h)
        self.assertIn("rrfScore", top_h)
        self.assertEqual(top_h["strategy"], "hybrid")

    def test_06_graph_traversal_defect_resolution(self):
        skus = ["QQ-0011", "QQ-0074", "QQ-0049"]
        res = self.graph.trace_defect_root_cause(skus)
        self.assertTrue(res["rootCauseIdentified"])
        self.assertEqual(len(res["findings"]), 1)
        finding = res["findings"][0]
        self.assertEqual(finding["componentId"], "COMP-025")
        self.assertEqual(finding["recalls"][0]["recallId"], "REC-VREG-01")

    def test_07_public_security_invariants(self):
        # Role tampering demotion
        role, was_tampered, msg = resolve_effective_role(
            requested_role="admin",
            auth_token=None,
            hardened=True
        )
        self.assertEqual(role, "customer")
        self.assertTrue(was_tampered)

        # IDOR protection
        allowed, msg = check_resource_access("PROC-QQ-0001", "customer", "internal_procurement")
        self.assertFalse(allowed)

        # Authenticated admin access permitted
        token = create_signed_token(role="admin", user_id="dr_arthur")
        role_auth, tampered_auth, _ = resolve_effective_role(
            requested_role="admin",
            auth_token=token,
            hardened=True
        )
        self.assertEqual(role_auth, "admin")
        self.assertFalse(tampered_auth)

        allowed_admin, _ = check_resource_access("PROC-QQ-0001", "admin", "internal_procurement")
        self.assertTrue(allowed_admin)

if __name__ == "__main__":
    unittest.main()
