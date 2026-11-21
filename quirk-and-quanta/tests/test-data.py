#!/usr/bin/env python3
"""
Quirk & Quanta - Automated Test Suite
Unit tests for data validity, schema adherence, referential integrity,
and security separation between internal canonical records and public site assets.
"""

import os
import unittest
import json
import xml.etree.ElementTree as ET

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_INTERNAL = os.path.join(ROOT_DIR, 'data', 'internal')
SITE_DIR = os.path.join(ROOT_DIR, 'site')
PUBLIC_DATA = os.path.join(SITE_DIR, 'data', 'products.public.json')

class TestQuirkAndQuantaData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(DATA_INTERNAL, 'products.full.json'), 'r', encoding='utf-8') as f:
            cls.products = json.load(f)
        with open(os.path.join(DATA_INTERNAL, 'suppliers.json'), 'r', encoding='utf-8') as f:
            cls.suppliers = json.load(f)
        with open(os.path.join(DATA_INTERNAL, 'components.json'), 'r', encoding='utf-8') as f:
            cls.components = json.load(f)
        with open(os.path.join(DATA_INTERNAL, 'collections.json'), 'r', encoding='utf-8') as f:
            cls.collections = json.load(f)
        with open(os.path.join(DATA_INTERNAL, 'recalls.json'), 'r', encoding='utf-8') as f:
            cls.recalls = json.load(f)
        with open(os.path.join(DATA_INTERNAL, 'policies.json'), 'r', encoding='utf-8') as f:
            cls.policies = json.load(f)
        with open(os.path.join(DATA_INTERNAL, 'graph-relationships.json'), 'r', encoding='utf-8') as f:
            cls.graph = json.load(f)
        with open(PUBLIC_DATA, 'r', encoding='utf-8') as f:
            cls.public_products = json.load(f)

    def test_product_count_and_skus(self):
        """Validate exactly 100 products with sequential SKUs QQ-0001 through QQ-0100."""
        self.assertEqual(len(self.products), 100, "Must contain exactly 100 products")
        expected_skus = [f"QQ-{i:04d}" for i in range(1, 101)]
        actual_skus = [p['sku'] for p in self.products]
        self.assertEqual(actual_skus, expected_skus, "SKUs must match QQ-0001 through QQ-0100 sequentially")

    def test_categories_distribution(self):
        """Validate exactly 10 categories with exactly 10 products in each."""
        cat_counts = {}
        for p in self.products:
            c = p['category']
            cat_counts[c] = cat_counts.get(c, 0) + 1
        
        self.assertEqual(len(cat_counts), 10, "Must have exactly 10 categories")
        for cat, count in cat_counts.items():
            self.assertEqual(count, 10, f"Category '{cat}' must have exactly 10 products")

    def test_pricing_and_margins(self):
        """Validate cost < selling <= list and accurate margin calculations."""
        for p in self.products:
            sku = p['sku']
            cost = p['internal']['costPrice']
            selling = p['public']['sellingPrice']
            list_p = p['public']['listPrice']
            margin_amt = p['internal']['marginAmount']
            margin_pct = p['internal']['marginPercent']

            self.assertLess(cost, selling, f"[{sku}] costPrice must be strictly less than sellingPrice")
            self.assertLessEqual(selling, list_p, f"[{sku}] sellingPrice must be <= listPrice")

            expected_amt = round(selling - cost, 2)
            self.assertAlmostEqual(margin_amt, expected_amt, delta=0.01, msg=f"[{sku}] marginAmount mismatch")

            expected_pct = round(((selling - cost) / selling) * 100, 2)
            self.assertAlmostEqual(margin_pct, expected_pct, delta=0.01, msg=f"[{sku}] marginPercent mismatch")

    def test_word_counts(self):
        """Validate description word count boundaries for RAG and chunking compliance."""
        for p in self.products:
            sku = p['sku']
            short_wc = len(p['public']['shortDescription'].split())
            long_wc = len(p['public']['longDescription'].split())

            self.assertTrue(15 <= short_wc <= 35, f"[{sku}] shortDescription ({short_wc} words) must be between 15 and 35 words")
            self.assertTrue(80 <= long_wc <= 150, f"[{sku}] longDescription ({long_wc} words) must be between 80 and 150 words")

    def test_referential_integrity(self):
        """Validate all foreign keys resolve to valid entities."""
        supplier_ids = {s['id'] for s in self.suppliers}
        component_ids = {c['id'] for c in self.components}
        collection_ids = {c['id'] for c in self.collections}
        recall_ids = {r['id'] for r in self.recalls}
        policy_ids = {pol['id'] for pol in self.policies}
        sku_set = {p['sku'] for p in self.products}

        for p in self.products:
            sku = p['sku']
            self.assertIn(p['internal']['supplierId'], supplier_ids, f"[{sku}] Invalid supplierId")
            self.assertIn(p['collectionId'], collection_ids, f"[{sku}] Invalid collectionId")
            
            for cid in p['relationships'].get('componentIds', []):
                self.assertIn(cid, component_ids, f"[{sku}] Invalid componentId: {cid}")
            
            rec = p['internal'].get('recallNoticeId')
            if rec:
                self.assertIn(rec, recall_ids, f"[{sku}] Invalid recallNoticeId: {rec}")

            for pid in p['relationships'].get('policyIds', []):
                self.assertIn(pid, policy_ids, f"[{sku}] Invalid policyId: {pid}")

            for rel_sku in p['relationships']['relatedProducts']:
                self.assertIn(rel_sku, sku_set, f"[{sku}] Invalid related SKU: {rel_sku}")
            for comp_sku in p['relationships']['compatibleWith']:
                self.assertIn(comp_sku, sku_set, f"[{sku}] Invalid compatible SKU: {comp_sku}")
            for bnd_sku in p['relationships']['bundleWith']:
                self.assertIn(bnd_sku, sku_set, f"[{sku}] Invalid bundle SKU: {bnd_sku}")

    def test_graph_relationships(self):
        """Validate graph edge counts meet workshop minimums."""
        edges = self.graph if isinstance(self.graph, list) else self.graph.get('relationships', [])
        rel_counts = {}
        for edge in edges:
            t = edge.get('relationship') or edge.get('type')
            rel_counts[t] = rel_counts.get(t, 0) + 1

        self.assertGreaterEqual(rel_counts.get('COMPATIBLE_WITH', 0), 15, "Need at least 15 COMPATIBLE_WITH edges")
        self.assertGreaterEqual(rel_counts.get('RELATED_TO', 0), 20, "Need at least 20 RELATED_TO edges")
        bundle_count = rel_counts.get('BUNDLED_WITH', 0) or rel_counts.get('BUNDLE_WITH', 0)
        self.assertGreaterEqual(bundle_count, 15, "Need at least 15 BUNDLED_WITH edges")

    def test_public_data_sanitization(self):
        """Validate zero sensitive internal fields exist in products.public.json."""
        self.assertEqual(len(self.public_products), 100, "Public dataset must contain 100 products")

        forbidden_keys = {
            'costPrice', 'marginAmount', 'marginPercent', 'supplierId',
            'supplierPartNumber', 'procurementBatchId', 'qcInspectionGrade',
            'reorderThresholdUnits', 'internalNotes', 'recallNoticeId', 'internal'
        }

        def check_object(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    self.assertNotIn(k, forbidden_keys, f"Sensitive key '{k}' found at {path}.{k}")
                    check_object(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    check_object(item, f"{path}[{idx}]")

        check_object(self.public_products, "public_json")

    def test_asset_coverage(self):
        """Validate that all 100 primary SVGs and 100 thumbnail SVGs exist and are valid XML."""
        products_dir = os.path.join(SITE_DIR, 'assets', 'products')
        for i in range(1, 101):
            sku = f"QQ-{i:04d}"
            primary = os.path.join(products_dir, f"{sku}.svg")
            thumb = os.path.join(products_dir, f"{sku}-thumb.svg")

            self.assertTrue(os.path.exists(primary), f"Missing primary image for {sku}")
            self.assertTrue(os.path.exists(thumb), f"Missing thumbnail image for {sku}")
            self.assertGreater(os.path.getsize(primary), 100, f"Primary image {sku} too small")
            self.assertGreater(os.path.getsize(thumb), 100, f"Thumbnail image {sku} too small")

            # Validate XML / SVG syntax
            try:
                ET.parse(primary)
            except ET.ParseError as e:
                self.fail(f"Primary SVG {sku} has invalid XML: {e}")

            try:
                ET.parse(thumb)
            except ET.ParseError as e:
                self.fail(f"Thumbnail SVG {sku} has invalid XML: {e}")

if __name__ == '__main__':
    unittest.main()
