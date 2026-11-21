#!/usr/bin/env python3
"""
Master Canonical Data Generator for Quirk & Quanta.
Generates:
  - data/internal/suppliers.json (12 suppliers)
  - data/internal/components.json (24 components)
  - data/internal/collections.json (8 collections)
  - data/internal/recalls.json (5 quality / recall records)
  - data/internal/policies.json (8 return / warranty / shipping policies)
  - data/internal/products.full.json (Exactly 100 products)
  - data/internal/graph-relationships.json (Graph nodes and edges)
"""

import json
import os
import sys

# Ensure catalog_data is in python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from catalog_data.suppliers_data import SUPPLIERS
from catalog_data.components_data import COMPONENTS
from catalog_data.collections_data import COLLECTIONS
from catalog_data.recalls_data import RECALLS
from catalog_data.policies_data import POLICIES

from catalog_data.cat_a_apparel import get_apparel_products
from catalog_data.cat_b_desk import get_desk_products
from catalog_data.cat_c_kitchen import get_kitchen_products
from catalog_data.cat_d_home import get_home_products
from catalog_data.cat_e_gadgets import get_gadget_products
from catalog_data.cat_f_puzzles import get_puzzle_products
from catalog_data.cat_g_stationery import get_stationery_products
from catalog_data.cat_h_tech import get_tech_products
from catalog_data.cat_i_railway import get_railway_products
from catalog_data.cat_j_gifts import get_gifts_products

from catalog_data.graph_builder import build_graph_relationships

PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_INTERNAL_DIR = os.path.join(PROJECT_ROOT, "data", "internal")
os.makedirs(DATA_INTERNAL_DIR, exist_ok=True)

def main():
    print("==================================================")
    print("QUIRK & QUANTA: Generating Canonical Datasets")
    print("==================================================")

    # 1. Compile products
    all_products = []
    category_getters = [
        ("Apparel", get_apparel_products),
        ("Desk & Office", get_desk_products),
        ("Drinkware & Kitchen", get_kitchen_products),
        ("Home & Decor", get_home_products),
        ("Science Gadgets", get_gadget_products),
        ("Puzzles & Games", get_puzzle_products),
        ("Stationery & Learning", get_stationery_products),
        ("Tech Accessories", get_tech_products),
        ("Railway & Engineering", get_railway_products),
        ("Gifts & Collectibles", get_gifts_products)
    ]

    for cat_name, getter_fn in category_getters:
        items = getter_fn()
        if len(items) != 10:
            raise ValueError(f"Category '{cat_name}' returned {len(items)} products (expected exactly 10)!")
        all_products.extend(items)
        print(f"Loaded category '{cat_name}': 10 products ({items[0]['sku']} to {items[-1]['sku']})")

    if len(all_products) != 100:
        raise ValueError(f"Total product count {len(all_products)} != 100!")

    # Verify unique SKUs and IDs
    skus = [p["sku"] for p in all_products]
    if len(skus) != len(set(skus)):
        raise ValueError("Duplicate SKUs detected!")
    
    ids = [p["id"] for p in all_products]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate product IDs detected!")

    # 2. Build graph relationships
    graph_rels = build_graph_relationships(
        products=all_products,
        suppliers=SUPPLIERS,
        components=COMPONENTS,
        collections=COLLECTIONS,
        recalls=RECALLS,
        policies=POLICIES
    )

    # 3. Write files
    def write_json(filename, data):
        filepath = os.path.join(DATA_INTERNAL_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Wrote {filepath} ({len(data)} records)")

    write_json("suppliers.json", SUPPLIERS)
    write_json("components.json", COMPONENTS)
    write_json("collections.json", COLLECTIONS)
    write_json("recalls.json", RECALLS)
    write_json("policies.json", POLICIES)
    write_json("products.full.json", all_products)
    write_json("graph-relationships.json", graph_rels)

    print("\nCanonical data generation successful!")
    print(f"Total Products: {len(all_products)}")
    print(f"Total Suppliers: {len(SUPPLIERS)}")
    print(f"Total Components: {len(COMPONENTS)}")
    print(f"Total Collections: {len(COLLECTIONS)}")
    print(f"Total Recalls: {len(RECALLS)}")
    print(f"Total Policies: {len(POLICIES)}")
    print(f"Total Graph Relationships: {len(graph_rels)}")

if __name__ == "__main__":
    main()
