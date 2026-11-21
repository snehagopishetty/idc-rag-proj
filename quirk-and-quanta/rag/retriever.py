"""
Quirk & Quanta - Multi-Strategy Retriever (Vector, BM25, Hybrid)
Performs in-memory cosine similarity search over versioned chunk embeddings,
pure-Python BM25 lexical search, and Reciprocal Rank Fusion (RRF) hybrid search
with Role-Based Access Control (RBAC) filtering and citation mapping.
"""

import os
import sys
import json
import time
import math
import threading
from typing import List, Dict, Any, Optional

# Add scripts directory for offline embedding fallback
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

from generate_embeddings import (
    cosine_similarity,
    normalize_vector,
    generate_offline_embedding,
    call_gemini_api_batch,
    DIMENSIONS,
    MODEL_NAME
)
from .bm25 import BM25Retriever
from .hybrid import HybridRetriever

CHUNKS_DIR = os.path.join(ROOT_DIR, "data", "chunks")
EMBEDDINGS_DIR = os.path.join(ROOT_DIR, "data", "embeddings", "v1")

class QuirkRetriever:
    def __init__(self, default_strategy: str = "semantic"):
        self.default_strategy = default_strategy
        self.chunks_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.embeddings_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.bm25_indices: Dict[str, BM25Retriever] = {}
        self.hybrid_engine = HybridRetriever()
        self.query_cache: Dict[str, Any] = {}
        self.lock = threading.Lock()
        self._load_query_cache()
        # Eagerly warm default strategy cache to prevent race condition during concurrency
        self._load_strategy(default_strategy)

    def _load_query_cache(self):
        cache_path = os.path.join(EMBEDDINGS_DIR, "query_embeddings_cache.json")
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                self.query_cache = json.load(f)

    def _load_strategy(self, strategy: str):
        with self.lock:
            if strategy not in self.chunks_cache:
                chunk_file = os.path.join(CHUNKS_DIR, f"chunks_{strategy}.json")
                emb_file = os.path.join(EMBEDDINGS_DIR, f"embeddings_{strategy}.json")

                if not os.path.exists(chunk_file) or not os.path.exists(emb_file):
                    raise FileNotFoundError(f"Missing chunk/embedding data for strategy: {strategy}")

                with open(chunk_file, "r", encoding="utf-8") as f:
                    chunks = json.load(f)
                with open(emb_file, "r", encoding="utf-8") as f:
                    embeddings = json.load(f)

                # Map chunks by chunkId
                chunk_map = {c["chunkId"]: c for c in chunks}
                for emb in embeddings:
                    cid = emb["chunkId"]
                    if cid in chunk_map:
                        emb["chunkData"] = chunk_map[cid]

                self.chunks_cache[strategy] = chunks
                self.embeddings_cache[strategy] = embeddings

                # Build BM25 inverted index for this chunking strategy
                bm25 = BM25Retriever()
                bm25.build_index(chunks, strategy_name=strategy)
                self.bm25_indices[strategy] = bm25

    def embed_query(self, query_text: str, api_key: Optional[str] = None) -> tuple[List[float], str]:
        """
        Embeds a user query.
        Returns (vector, execution_mode).
        """
        # Check precomputed golden questions cache first
        for item in self.query_cache.values():
            if item["question"].strip().lower() == query_text.strip().lower():
                return item["vector"], "cached_query_embedding"

        # If live API key is provided, use live Gemini API
        if api_key:
            try:
                vectors = call_gemini_api_batch([query_text], api_key, task_type="RETRIEVAL_QUERY")
                if vectors:
                    return vectors[0], "live_gemini_api"
            except Exception:
                pass  # Fall back to deterministic projection

        # Offline deterministic projection
        return generate_offline_embedding(query_text, task_type="RETRIEVAL_QUERY"), "offline_projection"

    def retrieve_vector(
        self,
        query: str,
        top_k: int = 5,
        strategy: str = "semantic",
        role: str = "customer",
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Pure Dense Vector Retrieval using cosine similarity over embeddings.
        """
        start_time = time.perf_counter()
        self._load_strategy(strategy)

        # Step 1: Embed query
        emb_start = time.perf_counter()
        query_vec, mode = self.embed_query(query, api_key)
        emb_time_ms = round((time.perf_counter() - emb_start) * 1000, 2)

        # Step 2: RBAC Filtering
        ret_start = time.perf_counter()
        candidates = self.embeddings_cache[strategy]
        filtered = []

        for item in candidates:
            access = item.get("accessLevel", "public")
            allowed_roles = item.get("allowedRoles", ["customer", "admin", "procurement"])

            if role.lower() in ["admin", "presenter"]:
                pass  # Admin and presenter roles have full catalog inspection privileges
            else:
                if role.lower() == "customer" and access != "public":
                    continue
                if role.lower() not in [r.lower() for r in allowed_roles]:
                    continue

            filtered.append(item)

        # Step 3: Cosine Similarity (Fast dot product on unit-normalized vectors)
        q_norm = math.sqrt(sum(x * x for x in query_vec))
        norm_q = [x / q_norm for x in query_vec] if q_norm > 1e-12 else query_vec

        scored = []
        for item in filtered:
            vec = item["vector"]
            score = sum(a * b for a, b in zip(norm_q, vec))
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        top_items = scored[:top_k]
        ret_time_ms = round((time.perf_counter() - ret_start) * 1000, 2)

        # Step 4: Map Evidence
        evidence_list = []
        for rank, (score, item) in enumerate(top_items, 1):
            cdata = item.get("chunkData", {})
            meta = cdata.get("metadata", {})
            citation_info = meta.get("citation", {})

            evidence_list.append({
                "rank": rank,
                "score": round(score, 4),
                "vectorScore": round(score, 4),
                "chunkId": item["chunkId"],
                "docId": item["docId"],
                "sourceId": item["sourceId"],
                "accessLevel": item["accessLevel"],
                "strategy": strategy,
                "retrievalMethod": "vector",
                "sectionTitle": cdata.get("sectionTitle", meta.get("section", "General")),
                "text": cdata.get("text", ""),
                "citation": {
                    "label": citation_info.get("label", f"Document {item['sourceId']}"),
                    "url": citation_info.get("url", "#"),
                    "sectionName": citation_info.get("sectionName", "Catalog Dossier")
                }
            })

        total_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return {
            "query": query,
            "role": role,
            "strategy": strategy,
            "retrievalMethod": "vector",
            "topK": top_k,
            "embeddingMode": mode,
            "embeddingModel": "gemini-embedding-001",
            "dimensions": len(query_vec),
            "queryVectorNorm": round(q_norm, 6),
            "queryVectorSample": [round(x, 6) for x in norm_q[:16]],
            "skuDriftNotice": "Subword tokenization causes alphanumeric codes (e.g. QQ-0015) to drift in 768-D dense semantic space without exact lexical matches.",
            "evidenceCount": len(evidence_list),
            "evidence": evidence_list,
            "latency": {
                "embeddingMs": emb_time_ms,
                "retrievalMs": ret_time_ms,
                "totalMs": total_time_ms
            }
        }

    def retrieve_bm25(
        self,
        query: str,
        top_k: int = 5,
        strategy: str = "semantic",
        role: str = "customer"
    ) -> Dict[str, Any]:
        """
        Pure Lexical BM25 Retrieval.
        """
        start_time = time.perf_counter()
        self._load_strategy(strategy)

        bm25_retriever = self.bm25_indices[strategy]
        evidence_list = bm25_retriever.search(query, top_k=top_k, role=role)
        for item in evidence_list:
            item["retrievalMethod"] = "bm25"
            item["strategy"] = strategy

        total_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return {
            "query": query,
            "role": role,
            "strategy": strategy,
            "retrievalMethod": "bm25",
            "topK": top_k,
            "embeddingMode": "none_lexical",
            "evidenceCount": len(evidence_list),
            "evidence": evidence_list,
            "latency": {
                "embeddingMs": 0.0,
                "retrievalMs": total_time_ms,
                "totalMs": total_time_ms
            }
        }

    def retrieve_hybrid(
        self,
        query: str,
        top_k: int = 5,
        strategy: str = "semantic",
        role: str = "customer",
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Hybrid Retrieval with Reciprocal Rank Fusion (RRF).
        Retrieves top 2*top_k from both vector and BM25, then performs RRF fusion.
        """
        start_time = time.perf_counter()
        pool_size = max(top_k * 3, 20)

        vec_res = self.retrieve_vector(query, top_k=pool_size, strategy=strategy, role=role, api_key=api_key)
        bm25_res = self.retrieve_bm25(query, top_k=pool_size, strategy=strategy, role=role)

        fuse_start = time.perf_counter()
        fused_evidence = self.hybrid_engine.fuse(
            vector_results=vec_res["evidence"],
            bm25_results=bm25_res["evidence"],
            top_k=top_k
        )
        fuse_ms = round((time.perf_counter() - fuse_start) * 1000, 2)

        total_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return {
            "query": query,
            "role": role,
            "strategy": strategy,
            "retrievalMethod": "hybrid",
            "topK": top_k,
            "embeddingMode": vec_res["embeddingMode"],
            "embeddingModel": "gemini-embedding-001",
            "dimensions": vec_res.get("dimensions", 768),
            "queryVectorNorm": vec_res.get("queryVectorNorm", 1.0),
            "queryVectorSample": vec_res.get("queryVectorSample", []),
            "evidenceCount": len(fused_evidence),
            "evidence": fused_evidence,
            "vectorTop1": vec_res["evidence"][0]["chunkId"] if vec_res["evidence"] else None,
            "bm25Top1": bm25_res["evidence"][0]["chunkId"] if bm25_res["evidence"] else None,
            "latency": {
                "embeddingMs": vec_res["latency"]["embeddingMs"],
                "retrievalMs": total_time_ms,
                "vectorRetrievalMs": vec_res["latency"]["retrievalMs"],
                "bm25RetrievalMs": bm25_res["latency"]["retrievalMs"],
                "fusionMs": fuse_ms,
                "totalMs": total_time_ms
            }
        }

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        strategy: str = "semantic",
        role: str = "customer",
        method: str = "auto",
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Unified retrieve method supporting method='vector', 'bm25', 'hybrid'
        or passing method directly as strategy name.
        """
        # Resolve strategy vs method
        effective_method = method.lower()
        effective_strategy = strategy.lower()

        if effective_strategy in ["bm25", "hybrid", "vector"]:
            effective_method = effective_strategy
            effective_strategy = self.default_strategy
        elif effective_method == "auto":
            effective_method = "vector"

        if effective_strategy not in ["fixed", "sliding", "semantic"]:
            effective_strategy = "semantic"

        if effective_method == "bm25":
            return self.retrieve_bm25(query, top_k=top_k, strategy=effective_strategy, role=role)
        elif effective_method == "hybrid":
            return self.retrieve_hybrid(query, top_k=top_k, strategy=effective_strategy, role=role, api_key=api_key)
        else:
            return self.retrieve_vector(query, top_k=top_k, strategy=effective_strategy, role=role, api_key=api_key)
