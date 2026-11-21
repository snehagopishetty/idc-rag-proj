#!/usr/bin/env python3
"""
Quirk & Quanta - Canonical & Public Data Validator
Validates full internal data schema, pricing math, referential integrity,
graph relationships, and verifies zero sensitive data leakage in public data.
"""

import os
import sys
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_INTERNAL = os.path.join(ROOT_DIR, 'data', 'internal')
PUBLIC_DATA = os.path.join(ROOT_DIR, 'site', 'data', 'products.public.json')

def load_json(filepath):
    if not os.path.exists(filepath):
        print(f"[FAIL] Missing file: {filepath}")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_validation():
    print("=" * 60)
    print("QUIRK & QUANTA - DATA VALIDATION SUITE")
    print("=" * 60)

    # 1. Load entities
    products = load_json(os.path.join(DATA_INTERNAL, 'products.full.json'))
    suppliers = load_json(os.path.join(DATA_INTERNAL, 'suppliers.json'))
    components = load_json(os.path.join(DATA_INTERNAL, 'components.json'))
    collections = load_json(os.path.join(DATA_INTERNAL, 'collections.json'))
    recalls = load_json(os.path.join(DATA_INTERNAL, 'recalls.json'))
    policies = load_json(os.path.join(DATA_INTERNAL, 'policies.json'))
    graph = load_json(os.path.join(DATA_INTERNAL, 'graph-relationships.json'))
    public_products = load_json(PUBLIC_DATA)

    errors = []

    # 2. Product Count & SKUs
    print("Checking product count and SKU sequencing...")
    if len(products) != 100:
        errors.append(f"Expected 100 products in products.full.json, got {len(products)}")
    
    expected_skus = [f"QQ-{i:04d}" for i in range(1, 101)]
    actual_skus = [p['sku'] for p in products]
    if actual_skus != expected_skus:
        errors.append("SKU sequence mismatch or gaps detected.")

    # 3. Category Distribution (10 categories, 10 products each)
    print("Checking category distribution (10 categories x 10 products)...")
    cat_counts = {}
    for p in products:
        c = p['category']
        cat_counts[c] = cat_counts.get(c, 0) + 1
    
    if len(cat_counts) != 10:
        errors.append(f"Expected exactly 10 categories, found {len(cat_counts)}")
    for cat, count in cat_counts.items():
        if count != 10:
            errors.append(f"Category '{cat}' has {count} products; expected exactly 10")

    # 4. Pricing Math & Margin Verification
    print("Checking pricing math and margin calculations...")
    for p in products:
        sku = p['sku']
        cost = p['internal']['costPrice']
        selling = p['public']['sellingPrice']
        list_p = p['public']['listPrice']
        margin_amt = p['internal']['marginAmount']
        margin_pct = p['internal']['marginPercent']

        if not (cost < selling <= list_p):
            errors.append(f"[{sku}] Pricing invariant failed: costPrice ({cost}) < sellingPrice ({selling}) <= listPrice ({list_p})")

        calc_margin_amt = round(selling - cost, 2)
        if abs(margin_amt - calc_margin_amt) > 0.01:
            errors.append(f"[{sku}] marginAmount mismatch: recorded {margin_amt}, calculated {calc_margin_amt}")

        calc_margin_pct = round(((selling - cost) / selling) * 100, 2)
        if abs(margin_pct - calc_margin_pct) > 0.01:
            errors.append(f"[{sku}] marginPercent mismatch: recorded {margin_pct}, calculated {calc_margin_pct}")

    # 5. Word Count Boundaries
    print("Checking description word counts...")
    for p in products:
        sku = p['sku']
        short_words = len(p['public']['shortDescription'].split())
        long_words = len(p['public']['longDescription'].split())

        if not (15 <= short_words <= 35):
            errors.append(f"[{sku}] shortDescription word count {short_words} outside [15, 35]")
        if not (80 <= long_words <= 150):
            errors.append(f"[{sku}] longDescription word count {long_words} outside [80, 150]")

    # 6. Referential Integrity (Foreign Keys)
    print("Checking referential integrity across entities...")
    supplier_ids = {s['id'] for s in suppliers}
    component_ids = {c['id'] for c in components}
    collection_ids = {c['id'] for c in collections}
    recall_ids = {r['id'] for r in recalls}
    policy_ids = {pol['id'] for pol in policies}
    sku_set = set(actual_skus)

    for p in products:
        sku = p['sku']
        # Supplier
        sup = p['internal']['supplierId']
        if sup not in supplier_ids:
            errors.append(f"[{sku}] Invalid supplierId: {sup}")
        # Components / materials
        for cid in p['relationships'].get('componentIds', []):
            if cid not in component_ids:
                errors.append(f"[{sku}] Invalid componentId: {cid}")
        for mid in p['relationships'].get('materialIds', []):
            if mid not in component_ids:
                errors.append(f"[{sku}] Invalid materialId: {mid}")
        # Collection
        coll = p['collectionId']
        if coll not in collection_ids:
            errors.append(f"[{sku}] Invalid collectionId: {coll}")
        # Recall Notice
        rec = p['internal'].get('recallNoticeId')
        if rec and rec not in recall_ids:
            errors.append(f"[{sku}] Invalid recallNoticeId: {rec}")
        # Policies
        for pol_id in p['relationships'].get('policyIds', []):
            if pol_id not in policy_ids:
                errors.append(f"[{sku}] Invalid policyId: {pol_id}")
        # Graph links within product
        for rel_sku in p['relationships']['relatedProducts']:
            if rel_sku not in sku_set:
                errors.append(f"[{sku}] Invalid related product SKU: {rel_sku}")
        for comp_sku in p['relationships']['compatibleWith']:
            if comp_sku not in sku_set:
                errors.append(f"[{sku}] Invalid compatible product SKU: {comp_sku}")
        for bnd_sku in p['relationships']['bundleWith']:
            if bnd_sku not in sku_set:
                errors.append(f"[{sku}] Invalid bundle product SKU: {bnd_sku}")

    # 7. Graph Relationship Counts
    print("Checking graph relationship edges and constraints...")
    edges = graph if isinstance(graph, list) else graph.get('relationships', [])
    rel_counts = {}
    for edge in edges:
        t = edge.get('relationship') or edge.get('type')
        rel_counts[t] = rel_counts.get(t, 0) + 1

    compat_count = rel_counts.get('COMPATIBLE_WITH', 0)
    related_count = rel_counts.get('RELATED_TO', 0)
    bundle_count = rel_counts.get('BUNDLED_WITH', 0) or rel_counts.get('BUNDLE_WITH', 0)

    if compat_count < 15:
        errors.append(f"Expected at least 15 COMPATIBLE_WITH edges, got {compat_count}")
    if related_count < 20:
        errors.append(f"Expected at least 20 RELATED_TO edges, got {related_count}")
    if bundle_count < 15:
        errors.append(f"Expected at least 15 BUNDLE_WITH edges, got {bundle_count}")

    # 8. Public Data Leakage Verification
    print("Checking public data leakage (zero internal fields in site/data/products.public.json)...")
    if len(public_products) != 100:
        errors.append(f"Expected 100 products in products.public.json, got {len(public_products)}")

    forbidden_keys = {
        'costPrice', 'marginAmount', 'marginPercent', 'supplierId',
        'supplierPartNumber', 'procurementBatchId', 'qcInspectionGrade',
        'reorderThresholdUnits', 'internalNotes', 'recallNoticeId', 'internal'
    }

    def check_leak(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in forbidden_keys:
                    errors.append(f"LEAK DETECTED: key '{k}' found at {path}.{k}")
                check_leak(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                check_leak(item, f"{path}[{idx}]")

    check_leak(public_products, "public_json")

    # Final tally
    print("-" * 60)
    if errors:
        print(f"FAILED: Found {len(errors)} validation errors:")
        for e in errors[:20]:
            print(f"  - {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors.")
        sys.exit(1)
    else:
        print("SUCCESS: All 100 products, pricing equations, graph edges, and public data passed validation with 0 errors!")
        print(f"  - Total Products: {len(products)}")
        print(f"  - Categories: {len(cat_counts)} (10 items each)")
        print(f"  - Graph Edges: {len(edges)} total (Compat: {compat_count}, Related: {related_count}, Bundles: {bundle_count})")
        print(f"  - Zero sensitive fields leaked in public data.")
        sys.exit(0)

if __name__ == '__main__':
    run_validation()
