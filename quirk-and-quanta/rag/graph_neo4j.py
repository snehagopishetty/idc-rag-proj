"""
Quirk & Quanta - Neo4j AuraDB Graph Adapter
Zero external dependencies (uses standard library urllib.request and json).

Provides:
1. HTTP REST transactional Cypher execution against Neo4j AuraDB / Neo4j 5.x
2. Multi-hop defect root-cause Cypher query generation
3. Graceful offline fallback mode (NEO4J_AURA_OFFLINE_REFERENCE) with local graph delegation
4. Telemetry and connection health check
"""

import os
import json
import base64
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from rag.graph_local import get_graph

class Neo4jGraphAdapter:
    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: str = "neo4j"
    ):
        self.uri = uri or os.environ.get("NEO4J_URI", "")
        self.user = user or os.environ.get("NEO4J_USER", "neo4j")
        self.password = password or os.environ.get("NEO4J_PASSWORD", "")
        self.database = database or os.environ.get("NEO4J_DATABASE", "neo4j")
        self._local_graph = get_graph()

    def is_configured(self) -> bool:
        """Returns True if URI and password environment variables or parameters are present."""
        return bool(self.uri and self.password)

    def _get_http_endpoint(self) -> Optional[str]:
        """
        Converts bolt/neo4j URI into transactional HTTP REST endpoint:
        e.g., neo4j+s://xxx.databases.neo4j.io -> https://xxx.databases.neo4j.io:7473/db/{database}/tx/commit
        or http://localhost:7474 -> http://localhost:7474/db/{database}/tx/commit
        """
        if not self.uri:
            return None
        uri = self.uri.strip()
        if uri.startswith("neo4j+s://") or uri.startswith("neo4j://"):
            host = uri.split("://")[1].split("/")[0]
            # Neo4j AuraDB HTTPS discovery port is 7473 or default 443
            base = f"https://{host}"
        elif uri.startswith("bolt+s://") or uri.startswith("bolt://"):
            host = uri.split("://")[1].split("/")[0]
            base = f"https://{host}"
        elif uri.startswith("http://") or uri.startswith("https://"):
            base = uri.rstrip("/")
        else:
            base = f"https://{uri}"

        return f"{base}/db/{self.database}/tx/commit"

    def execute_cypher(self, statement: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes a Cypher statement against Neo4j AuraDB HTTP transactional endpoint.
        Falls back to local offline mode if unconfigured or unreachable.
        """
        if not self.is_configured():
            return {
                "success": False,
                "status": "NEO4J_AURA_OFFLINE_REFERENCE",
                "message": "Neo4j AuraDB credentials not configured. Operating in offline reference mode.",
                "statement": statement,
                "parameters": params or {}
            }

        endpoint = self._get_http_endpoint()
        if not endpoint:
            return {
                "success": False,
                "status": "NEO4J_INVALID_URI",
                "message": f"Unable to construct HTTP endpoint from URI: {self.uri}"
            }

        payload = {
            "statements": [
                {
                    "statement": statement,
                    "parameters": params or {}
                }
            ]
        }
        body = json.dumps(payload).encode("utf-8")
        auth_str = f"{self.user}:{self.password}"
        b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

        req = urllib.request.Request(
            endpoint,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json;charset=UTF-8",
                "Authorization": f"Basic {b64_auth}"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                errors = resp_data.get("errors", [])
                if errors:
                    return {
                        "success": False,
                        "status": "CYPHER_ERROR",
                        "errors": errors,
                        "statement": statement
                    }
                return {
                    "success": True,
                    "status": "CONNECTED",
                    "results": resp_data.get("results", [])
                }
        except urllib.error.URLError as e:
            return {
                "success": False,
                "status": "NEO4J_AURA_OFFLINE_REFERENCE",
                "error": str(e),
                "message": "Failed to connect to Neo4j AuraDB. Falling back to local offline mode."
            }

    def trace_defect_root_cause(self, product_skus: List[str]) -> Dict[str, Any]:
        """
        Multi-hop defect root cause inquiry (reproducing Story 3 & Demo 09).
        If live Neo4j is configured, runs Cypher; otherwise seamlessly uses local in-memory graph.
        """
        cypher_query = (
            "MATCH (p:Product)-[:CONTAINS]->(c:Component)\n"
            "WHERE p.sku IN $skus\n"
            "MATCH (c)-[:AFFECTED_BY]->(r:Recall)\n"
            "MATCH (c)-[:SUPPLIED_BY]->(s:Supplier)\n"
            "RETURN p.sku AS productSku, p.title AS productTitle, c.componentId AS componentId, "
            "c.name AS componentName, r.recallId AS recallId, r.severity AS severity, "
            "s.supplierId AS supplierId, s.name AS supplierName"
        )

        if self.is_configured():
            cypher_res = self.execute_cypher(cypher_query, {"skus": product_skus})
            if cypher_res.get("success"):
                return {
                    "engine": "Neo4j AuraDB (Live Cypher)",
                    "status": "SUCCESS",
                    "cypherQuery": cypher_query,
                    "parameters": {"skus": product_skus},
                    "neo4jResults": cypher_res.get("results", []),
                    "fallbackUsed": False
                }

        # Offline Reference / Fallback mode
        local_res = self._local_graph.trace_defect_root_cause(product_skus)
        return {
            **local_res,
            "engine": "Neo4j AuraDB (Offline Reference Mode)",
            "status": "NEO4J_AURA_OFFLINE_REFERENCE",
            "fallbackUsed": True,
            "cypherQuery": cypher_query,
            "parameters": {"skus": product_skus},
            "note": "AuraDB cloud credentials not set or unreachable; executed via deterministic local graph engine."
        }

    def get_telemetry(self) -> Dict[str, Any]:
        is_conf = self.is_configured()
        return {
            "configured": is_conf,
            "status": "connected" if is_conf else "not_connected",
            "badge": "🟢 Neo4j AuraDB: Connected" if is_conf else "⚠️ Neo4j AuraDB: Not Connected (In-Memory Cypher Fallback)",
            "uri": self.uri if self.uri else None,
            "database": self.database,
            "engine": "Neo4j AuraDB" if is_conf else "Neo4j AuraDB (Offline Reference Mode)",
            "localNodesAvailable": len(self._local_graph.nodes)
        }

_neo4j_adapter_instance = None

def get_neo4j_adapter() -> Neo4jGraphAdapter:
    global _neo4j_adapter_instance
    if _neo4j_adapter_instance is None:
        _neo4j_adapter_instance = Neo4jGraphAdapter()
    return _neo4j_adapter_instance
