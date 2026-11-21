"""
Quirk & Quanta - Hybrid Retriever with Reciprocal Rank Fusion (RRF)
Combines dense semantic vector retrieval with sparse BM25 lexical retrieval.
Uses the industry-standard Cormack et al. RRF formula:
RRF_score(d) = sum_m [ weight_m / (k + rank_m(d)) ]
Provides complete provenance and rank contribution telemetry.
"""

from typing import List, Dict, Any, Optional

DEFAULT_RRF_K = 60
DEFAULT_VECTOR_WEIGHT = 1.0
DEFAULT_BM25_WEIGHT = 1.0

class HybridRetriever:
    def __init__(
        self,
        rrf_k: int = DEFAULT_RRF_K,
        vector_weight: float = DEFAULT_VECTOR_WEIGHT,
        bm25_weight: float = DEFAULT_BM25_WEIGHT
    ):
        self.rrf_k = rrf_k
        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight

    def fuse(
        self,
        vector_results: List[Dict[str, Any]],
        bm25_results: List[Dict[str, Any]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Merges dense vector and BM25 lexical results using Reciprocal Rank Fusion (RRF).
        """
        all_chunks: Dict[str, Dict[str, Any]] = {}
        rrf_scores: Dict[str, float] = {}
        provenance: Dict[str, Dict[str, Any]] = {}

        # 1. Process Vector Rankings
        for rank, item in enumerate(vector_results, 1):
            cid = item["chunkId"]
            all_chunks[cid] = item
            score_contribution = self.vector_weight / (self.rrf_k + rank)
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + score_contribution
            if cid not in provenance:
                provenance[cid] = {
                    "vectorRank": rank,
                    "vectorScore": item.get("score", 0.0),
                    "bm25Rank": None,
                    "bm25Score": None,
                    "matchedTerms": []
                }
            else:
                provenance[cid]["vectorRank"] = rank
                provenance[cid]["vectorScore"] = item.get("score", 0.0)

        # 2. Process BM25 Rankings
        for rank, item in enumerate(bm25_results, 1):
            cid = item["chunkId"]
            if cid not in all_chunks:
                all_chunks[cid] = item
            score_contribution = self.bm25_weight / (self.rrf_k + rank)
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + score_contribution

            if cid not in provenance:
                provenance[cid] = {
                    "vectorRank": None,
                    "vectorScore": None,
                    "bm25Rank": rank,
                    "bm25Score": item.get("score", 0.0),
                    "matchedTerms": item.get("matchedTerms", [])
                }
            else:
                provenance[cid]["bm25Rank"] = rank
                provenance[cid]["bm25Score"] = item.get("score", 0.0)
                provenance[cid]["matchedTerms"] = item.get("matchedTerms", [])

        # 3. Sort by combined RRF score descending
        sorted_cids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
        top_cids = sorted_cids[:top_k]

        fused_evidence = []
        for rank, cid in enumerate(top_cids, 1):
            base_item = all_chunks[cid].copy()
            prov = provenance[cid]

            base_item["rank"] = rank
            base_item["score"] = round(rrf_scores[cid], 6)
            base_item["rrfScore"] = round(rrf_scores[cid], 6)
            base_item["vectorRank"] = prov["vectorRank"]
            base_item["vectorScore"] = prov["vectorScore"]
            base_item["bm25Rank"] = prov["bm25Rank"]
            base_item["bm25Score"] = prov["bm25Score"]
            base_item["matchedTerms"] = prov["matchedTerms"]
            base_item["strategy"] = "hybrid"

            fused_evidence.append(base_item)

        return fused_evidence
