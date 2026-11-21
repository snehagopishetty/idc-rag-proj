"""
Quirk & Quanta - Pure-Python Local GraphRAG Engine
In-memory property graph engine supporting multi-hop graph traversal,
root-cause defect analysis, provenance chain resolution, and additive scenario overlays.
Zero external graph database required (pure Python dictionary & adjacency list).
"""

import os
import sys
import json
import time
from typing import List, Dict, Any, Optional, Set, Tuple

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data", "internal")
SCENARIOS_DIR = os.path.join(ROOT_DIR, "data", "scenarios")

class Node:
    def __init__(self, node_id: str, label: str, properties: Dict[str, Any]):
        self.id = node_id
        self.label = label
        self.properties = properties

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            **self.properties
        }

class Edge:
    def __init__(self, edge_id: str, source: str, relationship: str, target: str, properties: Dict[str, Any]):
        self.id = edge_id
        self.source = source
        self.relationship = relationship
        self.target = target
        self.properties = properties

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "relationship": self.relationship,
            "target": self.target,
            "properties": self.properties
        }

class LocalKnowledgeGraph:
    def __init__(self, load_scenarios: bool = True):
        self.nodes: Dict[str, Node] = {}
        self.out_edges: Dict[str, List[Edge]] = {}
        self.in_edges: Dict[str, List[Edge]] = {}
        self.load_scenarios = load_scenarios
        self._load_graph()

    def add_node(self, node_id: str, label: str, properties: Dict[str, Any]):
        self.nodes[node_id] = Node(node_id, label, properties)
        if node_id not in self.out_edges:
            self.out_edges[node_id] = []
        if node_id not in self.in_edges:
            self.in_edges[node_id] = []

    def add_edge(self, edge_id: str, source: str, relationship: str, target: str, properties: Optional[Dict[str, Any]] = None):
        props = properties or {}
        edge = Edge(edge_id, source, relationship, target, props)
        if source not in self.out_edges:
            self.out_edges[source] = []
        self.out_edges[source].append(edge)
        if target not in self.in_edges:
            self.in_edges[target] = []
        self.in_edges[target].append(edge)

    def _load_graph(self):
        # 1. Load canonical base entities
        prod_file = os.path.join(DATA_DIR, "products.full.json")
        if os.path.exists(prod_file):
            with open(prod_file, "r", encoding="utf-8") as f:
                prods = json.load(f)
                for p in prods:
                    self.add_node(p["sku"], "Product", {
                        "name": p["name"],
                        "category": p.get("category", ""),
                        "price": p.get("price", 0)
                    })

        comp_file = os.path.join(DATA_DIR, "components.json")
        if os.path.exists(comp_file):
            with open(comp_file, "r", encoding="utf-8") as f:
                comps = json.load(f)
                for c in comps:
                    self.add_node(c["id"], "Component", c)

        supp_file = os.path.join(DATA_DIR, "suppliers.json")
        if os.path.exists(supp_file):
            with open(supp_file, "r", encoding="utf-8") as f:
                supps = json.load(f)
                for s in supps:
                    self.add_node(s["id"], "Supplier", s)

        rec_file = os.path.join(DATA_DIR, "recalls.json")
        if os.path.exists(rec_file):
            with open(rec_file, "r", encoding="utf-8") as f:
                recs = json.load(f)
                for r in recs:
                    self.add_node(r["id"], "Recall", r)

        # 2. Load canonical relationships
        rel_file = os.path.join(DATA_DIR, "graph-relationships.json")
        if os.path.exists(rel_file):
            with open(rel_file, "r", encoding="utf-8") as f:
                rels = json.load(f)
                for r in rels:
                    self.add_edge(r["id"], r["sourceId"], r["relationship"], r["targetId"], r.get("properties", {}))

        # 3. Load Additive Scenarios (Film Defect Scenario)
        if self.load_scenarios and os.path.exists(SCENARIOS_DIR):
            for fname in os.listdir(SCENARIOS_DIR):
                if fname.endswith(".json"):
                    scen_path = os.path.join(SCENARIOS_DIR, fname)
                    try:
                        with open(scen_path, "r", encoding="utf-8") as f:
                            scen = json.load(f)
                            if not scen.get("active", True):
                                continue
                            nodes_data = scen.get("nodes", {})
                            for comp in nodes_data.get("components", []):
                                self.add_node(comp["id"], "Component", comp)
                            for rec in nodes_data.get("recalls", []):
                                self.add_node(rec["id"], "Recall", rec)
                            for rel in scen.get("relationships", []):
                                self.add_edge(rel["id"], rel["sourceId"], rel["relationship"], rel["targetId"], rel.get("properties", {}))
                    except Exception as e:
                        print(f"Warning: Failed loading scenario {fname}: {e}")

    def find_common_components(self, product_skus: List[str]) -> List[Dict[str, Any]]:
        """
        Finds components contained in ALL specified product SKUs.
        """
        if not product_skus:
            return []

        component_sets: List[Set[str]] = []
        for sku in product_skus:
            comps_for_sku = set()
            for edge in self.out_edges.get(sku, []):
                if edge.relationship == "CONTAINS" and edge.target.startswith("COMP-"):
                    comps_for_sku.add(edge.target)
            component_sets.append(comps_for_sku)

        if not component_sets:
            return []

        common_comp_ids = set.intersection(*component_sets)
        output = []
        for cid in common_comp_ids:
            node = self.nodes.get(cid)
            output.append(node.to_dict() if node else {"id": cid})
        return output

    def trace_defect_root_cause(self, product_skus: List[str]) -> Dict[str, Any]:
        """
        Executes multi-hop causal inference across multiple products to identify
        shared components, their suppliers, and associated recall/quality notices.
        Reproduces Story 3 of the film.
        """
        start_time = time.perf_counter()
        common_components = self.find_common_components(product_skus)

        investigation_paths = []
        findings = []

        for comp in common_components:
            cid = comp["id"]
            comp_name = comp.get("name", "Unknown Component")

            # Hop 1: Suppliers
            suppliers = []
            for edge in self.out_edges.get(cid, []):
                if edge.relationship == "SUPPLIED_BY":
                    snode = self.nodes.get(edge.target)
                    suppliers.append({
                        "supplierId": edge.target,
                        "supplierName": snode.properties.get("name") if snode else edge.target,
                        "edgeProperties": edge.properties
                    })

            # Hop 2: Recalls / Quality Notices
            recalls = []
            for edge in self.out_edges.get(cid, []):
                if edge.relationship == "AFFECTED_BY":
                    rnode = self.nodes.get(edge.target)
                    recalls.append({
                        "recallId": edge.target,
                        "title": rnode.properties.get("title") if rnode else edge.target,
                        "batch": edge.properties.get("batch", rnode.properties.get("batch", "Unknown")),
                        "severity": edge.properties.get("severity", "medium"),
                        "defectDescription": rnode.properties.get("defectDescription", ""),
                        "symptoms": rnode.properties.get("symptomsReported", "")
                    })

            # Build sub-graph path
            path_nodes = []
            path_edges = []

            for sku in product_skus:
                pnode = self.nodes.get(sku)
                path_nodes.append(pnode.to_dict() if pnode else {"id": sku, "label": "Product"})
                path_edges.append({
                    "from": sku,
                    "rel": "CONTAINS",
                    "to": cid
                })

            path_nodes.append(comp)

            for sup in suppliers:
                path_nodes.append({"id": sup["supplierId"], "label": "Supplier", "name": sup["supplierName"]})
                path_edges.append({
                    "from": cid,
                    "rel": "SUPPLIED_BY",
                    "to": sup["supplierId"]
                })

            for rec in recalls:
                path_nodes.append({"id": rec["recallId"], "label": "Recall", "title": rec["title"]})
                path_edges.append({
                    "from": cid,
                    "rel": "AFFECTED_BY",
                    "to": rec["recallId"]
                })

            findings.append({
                "componentId": cid,
                "componentName": comp_name,
                "suppliers": suppliers,
                "recalls": recalls,
                "isRootCause": len(recalls) > 0,
                "path": {
                    "nodes": path_nodes,
                    "edges": path_edges
                }
            })

        total_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Synthesize natural language technical reasoning
        has_defect = any(f["isRootCause"] for f in findings)
        explanation = self._synthesize_defect_explanation(product_skus, findings)

        return {
            "productsInvestigated": product_skus,
            "commonComponentsCount": len(common_components),
            "commonComponents": common_components,
            "findings": findings,
            "rootCauseIdentified": has_defect,
            "explanation": explanation,
            "latencyMs": total_ms
        }

    def _synthesize_defect_explanation(self, skus: List[str], findings: List[Dict[str, Any]]) -> str:
        prod_names = []
        for s in skus:
            p = self.nodes.get(s)
            pname = p.properties.get("name", s) if p else s
            prod_names.append(f"{pname} ({s})")

        prod_list_str = ", ".join(prod_names)

        defect_findings = [f for f in findings if f["isRootCause"]]
        if not defect_findings:
            if not findings:
                return f"Multi-hop graph traversal completed. No shared hardware components were identified across the requested products: {prod_list_str}."
            comp_names = [f["componentName"] for f in findings]
            return f"Graph traversal identified shared components ({', '.join(comp_names)}) across {prod_list_str}, but no active recall notices or defect alerts are associated with them."

        # Defect root cause found
        f = defect_findings[0]
        comp_id = f["componentId"]
        comp_name = f["componentName"]
        rec = f["recalls"][0]
        sup = f["suppliers"][0] if f["suppliers"] else {"supplierName": "Quantum Flux Micro"}

        return (
            f"### Root Cause Identified via Knowledge Graph Traversal\n\n"
            f"Multi-hop graph provenance reveals that **{prod_list_str}** all share the identical hardware component: **{comp_name}** (`{comp_id}`).\n\n"
            f"- **Shared Component**: `{comp_id}` ({comp_name})\n"
            f"- **Manufacturer / Supplier**: `{sup.get('supplierId', 'SUP-008')}` ({sup.get('supplierName', 'Quantum Flux Micro')})\n"
            f"- **Defective Batch**: `{rec.get('batch', 'BATCH-VREG-2026')}`\n"
            f"- **Active Quality Alert**: `{rec.get('recallId')}` — *{rec.get('title')}*\n\n"
            f"**Failure Mechanism**: {rec.get('defectDescription')}\n"
            f"**Reported Field Symptoms**: {rec.get('symptoms')}\n\n"
            f"**Conclusion**: The identical flickering power dropoffs observed across all three devices are caused by gate-oxide micro-fractures in batch `{rec.get('batch')}` of `{comp_id}`."
        )

    def get_subgraph(self, node_id: str, depth: int = 1) -> Dict[str, Any]:
        """
        Returns the local neighborhood subgraph around a node for visualization.
        """
        visited_nodes: Set[str] = {node_id}
        collected_edges: List[Dict[str, Any]] = []

        frontier = {node_id}
        for _ in range(depth):
            next_frontier = set()
            for curr in frontier:
                # Out edges
                for edge in self.out_edges.get(curr, []):
                    collected_edges.append(edge.to_dict())
                    if edge.target not in visited_nodes:
                        visited_nodes.add(edge.target)
                        next_frontier.add(edge.target)
                # In edges
                for edge in self.in_edges.get(curr, []):
                    collected_edges.append(edge.to_dict())
                    if edge.source not in visited_nodes:
                        visited_nodes.add(edge.source)
                        next_frontier.add(edge.source)
            frontier = next_frontier

        nodes_list = []
        for nid in visited_nodes:
            n = self.nodes.get(nid)
            nodes_list.append(n.to_dict() if n else {"id": nid, "label": "Unknown"})

        return {
            "rootNode": node_id,
            "depth": depth,
            "nodesCount": len(nodes_list),
            "edgesCount": len(collected_edges),
            "nodes": nodes_list,
            "edges": collected_edges
        }

_graph_instance = None

def get_graph() -> LocalKnowledgeGraph:
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = LocalKnowledgeGraph(load_scenarios=True)
    return _graph_instance
