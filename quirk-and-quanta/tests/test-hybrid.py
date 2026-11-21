#!/usr/bin/env python3
"""
Quirk & Quanta - BM25 & Hybrid Retrieval Test Suite
Tests pure-Python Okapi BM25 indexing, SKU token preservation,
Reciprocal Rank Fusion (RRF) scoring, and RBAC compliance.
"""

import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.bm25 import BM25Retriever, tokenize
from rag.hybrid import HybridRetriever, DEFAULT_RRF_K
from rag.retriever import QuirkRetriever
from rag.pipeline import RAGPipeline

class TestBM25AndHybrid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.retriever = QuirkRetriever(default_strategy="semantic")
        cls.pipeline = RAGPipeline(default_strategy="semantic")

    def test_tokenization_preserves_skus_and_ids(self):
        text = "Check the specs for SKU QQ-0018 and component COMP-012 under recall REC-003."
        tokens = tokenize(text)
        self.assertIn("qq-0018", tokens)
        self.assertIn("comp-012", tokens)
        self.assertIn("rec-003", tokens)
        # Verify standard stopwords like 'the', 'for', 'and', 'under' are removed
        self.assertNotIn("the", tokens)
        self.assertNotIn("and", tokens)
        self.assertNotIn("under", tokens)

    def test_bm25_exact_sku_retrieval(self):
        query = "What are the technical specifications of QQ-0018?"
        res = self.retriever.retrieve_bm25(query, top_k=5, role="customer")
        self.assertGreater(len(res["evidence"]), 0)
        top_match = res["evidence"][0]
        # Top match MUST be for product QQ-0018
        self.assertEqual(top_match["sourceId"], "QQ-0018")
        self.assertGreater(top_match["score"], 0.0)
        self.assertIn("qq-0018", top_match["matchedTerms"])

    def test_bm25_rbac_enforcement(self):
        # Query for confidential internal procurement data
        query = "Supplier manufacturing cost margin for QQ-0001"
        res_customer = self.retriever.retrieve_bm25(query, top_k=5, role="customer")
        for chunk in res_customer["evidence"]:
            self.assertEqual(chunk["accessLevel"], "public")

        res_admin = self.retriever.retrieve_bm25(query, top_k=5, role="admin")
        internal_found = any(c["accessLevel"] != "public" for c in res_admin["evidence"])
        self.assertTrue(internal_found, "Admin should be able to retrieve internal procurement chunks")

    def test_rrf_scoring_math(self):
        hybrid = HybridRetriever(rrf_k=60, vector_weight=1.0, bm25_weight=1.0)
        vec_sample = [
            {"chunkId": "CHK-A", "score": 0.9},
            {"chunkId": "CHK-B", "score": 0.8}
        ]
        bm25_sample = [
            {"chunkId": "CHK-B", "score": 4.5, "matchedTerms": ["b"]},
            {"chunkId": "CHK-C", "score": 3.2, "matchedTerms": ["c"]}
        ]
        fused = hybrid.fuse(vec_sample, bm25_sample, top_k=3)
        self.assertEqual(len(fused), 3)

        # CHK-B is rank 2 in vector and rank 1 in BM25:
        # Score = 1/(60+2) + 1/(60+1) = 1/62 + 1/61 = 0.016129 + 0.016393 = 0.032522
        expected_score_b = round(1.0/62.0 + 1.0/61.0, 6)
        top_item = fused[0]
        self.assertEqual(top_item["chunkId"], "CHK-B")
        self.assertEqual(top_item["score"], expected_score_b)
        self.assertEqual(top_item["vectorRank"], 2)
        self.assertEqual(top_item["bm25Rank"], 1)

    def test_hybrid_retrieval_pipeline(self):
        query = "Schrödinger Cat Observation Chamber QQ-0001"
        res = self.retriever.retrieve_hybrid(query, top_k=5, role="customer")
        self.assertGreater(len(res["evidence"]), 0)
        top_item = res["evidence"][0]
        self.assertEqual(top_item["sourceId"], "QQ-0001")
        self.assertIn("rrfScore", top_item)
        self.assertIn("vectorRank", top_item)
        self.assertIn("bm25Rank", top_item)

    def test_compare_endpoint_returns_all_three(self):
        query = "precision laser level QQ-0015"
        comp = self.pipeline.compare(query, top_k=3, role="customer")
        self.assertIn("vector", comp)
        self.assertIn("bm25", comp)
        self.assertIn("hybrid", comp)
        self.assertEqual(len(comp["vector"]["evidence"]), 3)
        self.assertEqual(len(comp["bm25"]["evidence"]), 3)
        self.assertEqual(len(comp["hybrid"]["evidence"]), 3)

if __name__ == "__main__":
    unittest.main()
