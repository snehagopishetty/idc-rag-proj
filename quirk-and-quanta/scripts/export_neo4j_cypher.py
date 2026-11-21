#!/usr/bin/env python3
"""
Quirk & Quanta - Neo4j AuraDB Cypher Exporter
Zero external dependencies.

Exports canonical entities, relationships, and additive defect scenarios
to a complete Cypher import script: data/export/neo4j_import.cypher.
"""

import os
import sys
import json
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.graph_local import get_graph

OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "export")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "neo4j_import.cypher")

def escape_cypher_str(val: str) -> str:
    if val is None:
        return '""'
    s = str(val).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '')
    return f'"{s}"'

def format_cypher_props(props: dict) -> str:
    parts = []
    for k, v in props.items():
        # sanitize key name
        safe_key = re.sub(r'[^a-zA-Z0-9_]', '_', k)
        if isinstance(v, (int, float)):
            parts.append(f"{safe_key}: {v}")
        elif isinstance(v, bool):
            parts.append(f"{safe_key}: {'true' if v else 'false'}")
        elif isinstance(v, list):
            escaped_items = [escape_cypher_str(item) if isinstance(item, str) else str(item) for item in v]
            parts.append(f"{safe_key}: [{', '.join(escaped_items)}]")
        else:
            parts.append(f"{safe_key}: {escape_cypher_str(v)}")
    return "{" + ", ".join(parts) + "}"

def export_cypher():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    graph = get_graph()

    lines = []
    lines.append("// ============================================================================")
    lines.append("// QUIRK & QUANTA - NEO4J AURADB KNOWLEDGE GRAPH IMPORT SCRIPT")
    lines.append("// Workshop: 'Beyond Basic RAG: Building Production-Ready AI Systems'")
    lines.append("// Replicating Story 3: The Three-Product Flickering Defect Mystery")
    lines.append("// ============================================================================\n")

    # 1. Schema Constraints
    lines.append("// --- 1. SCHEMA CONSTRAINTS & INDEXES ---")
    lines.append("CREATE CONSTRAINT product_id_unique IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE;")
    lines.append("CREATE CONSTRAINT product_sku_unique IF NOT EXISTS FOR (p:Product) REQUIRE p.sku IS UNIQUE;")
    lines.append("CREATE CONSTRAINT component_id_unique IF NOT EXISTS FOR (c:Component) REQUIRE c.id IS UNIQUE;")
    lines.append("CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS FOR (s:Supplier) REQUIRE s.id IS UNIQUE;")
    lines.append("CREATE CONSTRAINT recall_id_unique IF NOT EXISTS FOR (r:Recall) REQUIRE r.id IS UNIQUE;\n")

    # 2. Nodes by Label
    lines.append("// --- 2. NODES: CANONICAL + ADDITIVE SCENARIOS ---")
    
    nodes_by_label = {}
    for node_id, node in graph.nodes.items():
        nodes_by_label.setdefault(node.label, []).append(node)

    for label in sorted(nodes_by_label.keys()):
        node_list = nodes_by_label[label]
        lines.append(f"\n// Label: :{label} ({len(node_list)} nodes)")
        for node in node_list:
            props = dict(node.properties)
            props["id"] = node.id
            if label == "Product" and "sku" not in props:
                props["sku"] = node.id
            cypher_props = format_cypher_props(props)
            lines.append(f"MERGE (n:{label} {{id: {escape_cypher_str(node.id)}}}) SET n += {cypher_props};")

    # 3. Relationships
    lines.append("\n// --- 3. RELATIONSHIPS ---")
    all_edges = []
    for source, edges in graph.out_edges.items():
        all_edges.extend(edges)

    lines.append(f"// Total relationships: {len(all_edges)}")
    for edge in all_edges:
        rel_type = re.sub(r'[^a-zA-Z0-9_]', '_', edge.relationship.upper())
        props_str = ""
        if edge.properties:
            props_str = f" SET r += {format_cypher_props(edge.properties)}"
        lines.append(
            f"MATCH (s {{id: {escape_cypher_str(edge.source)}}}), (t {{id: {escape_cypher_str(edge.target)}}}) "
            f"MERGE (s)-[r:{rel_type}]->(t){props_str};"
        )

    # 4. Multi-Hop Verification Query
    lines.append("\n// --- 4. VERIFICATION QUERY (STORY 3 DEFECT INVESTIGATION) ---")
    lines.append("// Run this query in Neo4j Browser / Workspace to verify the root cause:")
    lines.append("/*")
    lines.append("MATCH (p:Product)-[:CONTAINS]->(c:Component)")
    lines.append("WHERE p.sku IN ['QQ-0011', 'QQ-0074', 'QQ-0049']")
    lines.append("MATCH (c)-[:AFFECTED_BY]->(r:Recall)")
    lines.append("MATCH (c)-[:SUPPLIED_BY]->(s:Supplier)")
    lines.append("RETURN p.name AS Product, c.name AS DefectiveComponent, r.title AS Recall, s.name AS Supplier;")
    lines.append("*/\n")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Successfully exported Neo4j Cypher script:")
    print(f"  Path: {OUTPUT_FILE}")
    print(f"  Nodes: {len(graph.nodes)}")
    print(f"  Relationships: {len(all_edges)}")
    print(f"  File size: {os.path.getsize(OUTPUT_FILE):,} bytes")
    return OUTPUT_FILE

if __name__ == "__main__":
    export_cypher()
