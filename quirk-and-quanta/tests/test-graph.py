#!/usr/bin/env python3
"""
Quirk & Quanta - Knowledge Graph & GraphRAG Test Suite
Tests in-memory property graph construction, additive scenario overlay,
multi-hop defect root-cause traversal, and film narrative parity (Story 3).
"""

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.graph_local import LocalKnowledgeGraph, get_graph
from rag.pipeline import RAGPipeline

class TestGraphRAG(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = get_graph()
        cls.pipeline = RAGPipeline(default_strategy="semantic")

    def test_graph_initialization_and_node_counts(self):
        # Must have loaded all base products (100), components, suppliers, recalls
        self.assertGreaterEqual(len(self.graph.nodes), 140)
        self.assertIn("QQ-0011", self.graph.nodes)
        self.assertIn("QQ-0074", self.graph.nodes)
        self.assertIn("QQ-0049", self.graph.nodes)
        self.assertIn("COMP-025", self.graph.nodes)
        self.assertIn("REC-VREG-01", self.graph.nodes)

    def test_canonical_graph_preservation(self):
        # Canonical recall REC-003 and COMP-012 from Gate 1 must remain intact
        self.assertIn("REC-003", self.graph.nodes)
        self.assertIn("COMP-012", self.graph.nodes)
        out_edges_comp12 = [e for e in self.graph.out_edges.get("COMP-012", []) if e.relationship == "AFFECTED_BY"]
        self.assertTrue(any(e.target == "REC-003" for e in out_edges_comp12))

    def test_film_defect_scenario_common_component(self):
        target_skus = ["QQ-0011", "QQ-0074", "QQ-0049"]
        common_comps = self.graph.find_common_components(target_skus)
        self.assertEqual(len(common_comps), 1)
        self.assertEqual(common_comps[0]["id"], "COMP-025")
        self.assertIn("Voltage Regulator", common_comps[0]["name"])

    def test_film_defect_multi_hop_root_cause_trace(self):
        target_skus = ["QQ-0011", "QQ-0074", "QQ-0049"]
        trace = self.graph.trace_defect_root_cause(target_skus)
        self.assertTrue(trace["rootCauseIdentified"])
        self.assertEqual(len(trace["findings"]), 1)

        f = trace["findings"][0]
        self.assertEqual(f["componentId"], "COMP-025")
        self.assertTrue(f["isRootCause"])
        self.assertEqual(len(f["recalls"]), 1)

        rec = f["recalls"][0]
        self.assertEqual(rec["recallId"], "REC-VREG-01")
        self.assertEqual(rec["batch"], "BATCH-VREG-2026")
        self.assertEqual(rec["severity"], "high")

        # Verify explanation text contains key facts
        explanation = trace["explanation"]
        self.assertIn("COMP-025", explanation)
        self.assertIn("BATCH-VREG-2026", explanation)
        self.assertIn("REC-VREG-01", explanation)
        self.assertIn("QQ-0011", explanation)
        self.assertIn("QQ-0074", explanation)
        self.assertIn("QQ-0049", explanation)

    def test_unrelated_products_yield_no_defect(self):
        unrelated_skus = ["QQ-0001", "QQ-0002"]
        trace = self.graph.trace_defect_root_cause(unrelated_skus)
        self.assertFalse(trace["rootCauseIdentified"])

    def test_subgraph_neighborhood_extraction(self):
        sub = self.graph.get_subgraph("COMP-025", depth=1)
        self.assertEqual(sub["rootNode"], "COMP-025")
        self.assertGreater(sub["nodesCount"], 3)
        self.assertGreater(sub["edgesCount"], 3)

    def test_pipeline_ask_graph(self):
        question = "Why are the Atomic Orbit Desk Lamp (QQ-0011), Wireless Charger (QQ-0074), and Star Projector (QQ-0049) flickering?"
        res = self.pipeline.ask_graph(question, role="customer")
        self.assertEqual(res["retrievalMethod"], "graph")
        self.assertTrue(res["graphAnalysis"]["rootCauseIdentified"])
        self.assertGreater(len(res["evidence"]), 0)
        self.assertIn("COMP-025", res["answer"])

if __name__ == "__main__":
    unittest.main()
