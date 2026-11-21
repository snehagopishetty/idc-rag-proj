#!/usr/bin/env python3
"""
Quirk & Quanta - RAG Foundation Automated Test Suite (Gate 2)
Verifies:
- Corpus schemas, public/internal segregation, and zero leaks
- Multi-strategy chunking and deterministic chunk IDs
- Embedding dimensions (768-D) and vector normalization
- Local vector retrieval and cosine similarity ranking
- Role-Based Access Control (RBAC) security filtering
- Citation mapping integrity
- Graceful offline fallback handling
- Gate 1 storefront integrity preserved
"""

import os
import sys
import unittest
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.pipeline import RAGPipeline
from rag.retriever import QuirkRetriever

DATA_DIR = os.path.join(ROOT_DIR, "data")
CORPUS_DIR = os.path.join(DATA_DIR, "corpus")
CHUNKS_DIR = os.path.join(DATA_DIR, "chunks")
EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings", "v1")
SITE_DIR = os.path.join(ROOT_DIR, "site")

class TestRAGFoundation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(CORPUS_DIR, "corpus_public.json"), "r", encoding="utf-8") as f:
            cls.public_docs = json.load(f)
        with open(os.path.join(CORPUS_DIR, "corpus_internal.json"), "r", encoding="utf-8") as f:
            cls.internal_docs = json.load(f)
        with open(os.path.join(CHUNKS_DIR, "chunks_semantic.json"), "r", encoding="utf-8") as f:
            cls.semantic_chunks = json.load(f)
        with open(os.path.join(EMBEDDINGS_DIR, "embeddings_semantic.json"), "r", encoding="utf-8") as f:
            cls.semantic_embeddings = json.load(f)

        cls.pipeline = RAGPipeline(default_strategy="semantic")

    def test_corpus_integrity_and_counts(self):
        """Validate corpus document counts and schemas."""
        self.assertEqual(len(self.public_docs), 341, "Expected 341 public documents")
        self.assertEqual(len(self.internal_docs), 100, "Expected 100 internal procurement documents")
        self.assertEqual(len(self.public_docs) + len(self.internal_docs), 441, "Expected 441 total documents")

        for doc in self.public_docs:
            self.assertTrue(doc["docId"].startswith("DOC-"), f"Invalid docId: {doc['docId']}")
            self.assertEqual(doc["accessLevel"], "public")
            self.assertIn("content", doc)
            self.assertGreater(len(doc["content"]), 20)

    def test_no_private_data_leakage_in_public_corpus(self):
        """Validate zero confidential fields in corpus_public.json."""
        forbidden_keys = [
            "costPrice", "marginAmount", "marginPercent", "wholesale",
            "supplierCode", "procurementBatchId", "internalNotes"
        ]
        public_json_str = json.dumps(self.public_docs)
        for key in forbidden_keys:
            self.assertNotIn(f'"{key}"', public_json_str, f"Forbidden key '{key}' found in public corpus!")

    def test_chunk_strategies_and_ids(self):
        """Validate that all 3 chunk datasets exist with deterministic IDs."""
        for strat in ["fixed", "sliding", "semantic"]:
            path = os.path.join(CHUNKS_DIR, f"chunks_{strat}.json")
            self.assertTrue(os.path.exists(path), f"Missing {strat} chunks file")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertGreater(len(data), 500, f"Insufficient chunks for {strat}")
            for c in data[:20]:
                self.assertIn(f"CHK-", c["chunkId"])
                self.assertEqual(c["strategy"], strat)

    def test_embedding_dimensions_and_normalization(self):
        """Validate 768 dimensions and unit L2 normalization."""
        for item in self.semantic_embeddings[:50]:
            vec = item["vector"]
            self.assertEqual(len(vec), 768, f"Chunk {item['chunkId']} vector dim != 768")
            norm = sum(x * x for x in vec)
            self.assertAlmostEqual(norm, 1.0, places=2, msg=f"Vector for {item['chunkId']} not unit-normalized")

    def test_vector_retrieval_ranking(self):
        """Validate that exact SKU query retrieves relevant document in top ranks."""
        res = self.pipeline.ask("What are the specifications of QQ-0015?", top_k=3, strategy="semantic")
        self.assertTrue(len(res["evidence"]) > 0, "No evidence retrieved")
        top_chunk = res["evidence"][0]
        self.assertIn("QQ-0015", top_chunk["chunkId"], f"Top chunk {top_chunk['chunkId']} did not match QQ-0015")
        self.assertGreater(top_chunk["score"], 0.25, "Top score should be > 0.25")

    def test_rbac_security_enforcement(self):
        """Validate that customer role cannot retrieve internal procurement documents."""
        query = "What is the wholesale procurement cost and gross margin for QQ-0001?"
        cust_res = self.pipeline.ask(query, top_k=5, role="customer")
        for e in cust_res["evidence"]:
            self.assertEqual(e["accessLevel"], "public", f"Customer leaked private chunk: {e['chunkId']}")

        admin_res = self.pipeline.ask(query, top_k=5, role="admin")
        has_internal = any(e["accessLevel"] == "internal_procurement" for e in admin_res["evidence"])
        self.assertTrue(has_internal, "Admin role should retrieve internal procurement evidence")

    def test_citation_mapping(self):
        """Validate that citations map to valid links and labels."""
        res = self.pipeline.ask("Tell me about the Quantum Uncertainty Hoodie", top_k=2)
        for e in res["evidence"]:
            cit = e["citation"]
            self.assertIn("label", cit)
            self.assertIn("url", cit)
            self.assertIn("sectionName", cit)

    def test_offline_graceful_execution(self):
        """Validate that pipeline works completely without live Gemini credentials."""
        res = self.pipeline.ask("Precision Pizza Cutting Wheel specifications", top_k=3, api_key=None)
        self.assertEqual(res["executionMode"], "offline_reference")
        self.assertIsNotNone(res["answer"])
        self.assertGreater(res["latency"]["totalMs"], 0.0)

    def test_gate_1_storefront_integrity(self):
        """Validate that all original Gate 1 HTML pages and assets remain present."""
        expected_pages = ["index.html", "products.html", "product.html", "about.html", "workshop.html"]
        for p in expected_pages:
            self.assertTrue(os.path.exists(os.path.join(SITE_DIR, p)), f"Missing page {p}")

        logo_path = os.path.join(SITE_DIR, "assets", "logo.svg")
        self.assertTrue(os.path.exists(logo_path), "Missing brand logo")

if __name__ == "__main__":
    unittest.main()
