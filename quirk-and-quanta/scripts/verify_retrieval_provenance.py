#!/usr/bin/env python3
"""
verify_retrieval_provenance.py
Empirical verification of retrieval strategies, metric provenance, Gemini API integration,
grounding/abstention logic, and Neo4j AuraDB fallback resilience.

Zero external dependencies (Python Standard Library only).
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from rag.pipeline import RAGPipeline
from rag.retriever import QuirkRetriever
from rag.generator import generate_grounded_answer
from rag.guardrails import get_guardrails
from rag.graph_local import LocalKnowledgeGraph
from rag.graph_neo4j import Neo4jGraphAdapter

def run_retrieval_provenance_audit():
    print("=" * 70)
    print("QUIRK & QUANTA - RETRIEVAL PROVENANCE & GEMINI INTEGRATION AUDIT")
    print("=" * 70)

    results = []

    def report(name, passed, details=""):
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")
        if details:
            print(f"       Details: {details}")
        results.append({"name": name, "passed": passed, "details": details})

    # =========================================================================
    # SUITE 1: RETRIEVAL STRATEGIES & PROVENANCE METRICS
    # =========================================================================
    print("\n--- SUITE 1: RETRIEVAL STRATEGIES & PROVENANCE ---")
    retriever = QuirkRetriever()

    # 1a. Vector Retrieval
    vec_res = retriever.retrieve_vector("fluorescent desk lamp recall", top_k=3, strategy="semantic")
    report("Dense Vector Retrieval", len(vec_res.get("evidence", [])) == 3 and vec_res.get("retrievalMethod") == "vector",
           f"Returned {len(vec_res.get('evidence', []))} chunks, top score: {vec_res['evidence'][0]['score']:.4f}")

    # 1b. BM25 Retrieval
    bm25_res = retriever.retrieve_bm25("fluorescent desk lamp recall", top_k=3, strategy="semantic")
    report("Lexical BM25 Retrieval", len(bm25_res.get("evidence", [])) == 3 and bm25_res.get("retrievalMethod") == "bm25",
           f"Returned {len(bm25_res.get('evidence', []))} chunks, top score: {bm25_res['evidence'][0]['score']:.2f}")

    # 1c. Hybrid RRF Retrieval
    hybrid_res = retriever.retrieve_hybrid("fluorescent desk lamp recall", top_k=3, strategy="semantic")
    report("Hybrid RRF Retrieval", len(hybrid_res.get("evidence", [])) == 3 and hybrid_res.get("retrievalMethod") == "hybrid",
           f"Returned {len(hybrid_res.get('evidence', []))} chunks, RRF top score: {hybrid_res['evidence'][0]['score']:.4f}")

    # 1d. Multi-Hop GraphRAG Root Cause Investigation
    local_graph = LocalKnowledgeGraph()
    graph_res = local_graph.trace_defect_root_cause(["QQ-0011", "QQ-0074", "QQ-0049"])
    findings = graph_res.get("findings", [])
    affected_components = [f["componentId"] for f in findings]
    recalled_ids = [r["recallId"] for f in findings for r in f.get("recalls", [])]
    graph_passed = "COMP-025" in affected_components and "REC-VREG-01" in recalled_ids
    report("Multi-Hop GraphRAG Defect Tracing", graph_passed,
           f"Traced products QQ-0011/74/49 -> Component {affected_components[:1]} -> Recall {recalled_ids[:1]}")

    # =========================================================================
    # SUITE 2: GROUNDING & ABSTENTION SAFEGUARDS
    # =========================================================================
    print("\n--- SUITE 2: GROUNDING & ABSTENTION SAFEGUARDS ---")
    guardrails = get_guardrails()

    # 2a. Scope Boundary: Out-of-Domain Programming
    coding_res = guardrails.evaluate_request("Write python code for quicksort algorithm", evidence=[], hardened=True)
    report("Out-of-Scope Coding Rejection", coding_res.get("action") == "REJECT_OFF_TOPIC",
           f"Action: {coding_res.get('action')}, Reason: {coding_res.get('reason')}")

    # 2b. Grounding Abstention: Low Relevance Query
    low_sim_evidence = [{"chunkId": "CHUNK-001", "text": "Irrelevant quantum text", "score": 0.08}]
    abstain_res = guardrails.evaluate_request("What is the quarterly revenue of Microsoft?", evidence=low_sim_evidence, hardened=True)
    report("Ungrounded Query Abstention", abstain_res.get("action") == "ABSTAIN_UNGROUNDED",
           f"Action: {abstain_res.get('action')}, Reason: {abstain_res.get('reason')}")

    # 2c. Grounded Generation with Accurate Citations
    grounded_evidence = [{
        "chunkId": "CHUNK-QQ-0011-001",
        "text": "The Desktop Resonator operates at 15 Watts and generates 900 lumens of calibrated light.",
        "score": 0.88,
        "citation": {"label": "QQ-0011 Specification", "url": "/product.html?sku=QQ-0011"}
    }]
    gen_res = generate_grounded_answer("What is the wattage of QQ-0011?", evidence=grounded_evidence, role="customer")
    report("Grounded Answer Generation with Citations", 
           len(gen_res.get("citations", [])) == 1 and "15 Watts" in gen_res.get("answer", ""),
           f"Citations: {len(gen_res.get('citations', []))}, Model: {gen_res.get('model')}")

    # =========================================================================
    # SUITE 3: GEMINI FALLBACK & ADMISSION CONTROL
    # =========================================================================
    print("\n--- SUITE 3: GEMINI API FALLBACK & ADMISSION CONTROL ---")

    # 3a. Deterministic offline fallback on invalid/missing API key
    fallback_res = generate_grounded_answer("What is the wattage of QQ-0011?", evidence=grounded_evidence, role="customer", api_key="TRIGGER_SIMULATED_TIMEOUT")
    report("Deterministic Offline Fallback on API Key Failure",
           fallback_res.get("mode") == "offline_reference" and fallback_res.get("model") == "grounded_local_synthesizer",
           f"Fallback mode: {fallback_res.get('mode')}, Answer: {fallback_res.get('answer')[:60]}...")

    # 3b. Rate limiting admission control
    session_id = f"test_admission_{int(time.time())}"
    admitted_count = 0
    rejected_count = 0
    for _ in range(35):
        ok, err = guardrails.check_usage_budget(session_id)
        if ok:
            admitted_count += 1
        else:
            rejected_count += 1

    report("Usage Admission Controller Throttling", admitted_count > 0 and rejected_count > 0,
           f"Admitted: {admitted_count}, Throttled: {rejected_count} (Max {guardrails.max_requests_per_minute}/min enforced)")

    # =========================================================================
    # SUITE 4: NEO4J AURADB RESILIENCE (GATE O01)
    # =========================================================================
    print("\n--- SUITE 4: NEO4J AURADB ADAPTER RESILIENCE ---")
    neo4j = Neo4jGraphAdapter()
    telemetry = neo4j.get_telemetry()
    report("Neo4j Adapter Initialization", telemetry.get("configured") is False or telemetry.get("driverStatus") in ["OFFLINE_REFERENCE_MODE", "CONNECTED"],
           f"Driver Status: {telemetry.get('driverStatus')}, Engine: {telemetry.get('defaultEngine')}")

    trace_res = neo4j.trace_defect_root_cause(["QQ-0011", "QQ-0074"])
    report("Neo4j Seamless Offline Cypher Fallback", trace_res.get("status") in ["SUCCESS", "NEO4J_AURA_OFFLINE_REFERENCE"] and "parameters" in trace_res,
           f"Engine: {trace_res.get('engine')}, Fallback used: {trace_res.get('fallbackUsed')}")

    all_passed = all(r["passed"] for r in results)
    print("\n" + "=" * 70)
    print(f"RETRIEVAL & GEMINI AUDIT VERDICT: {'ALL 11 TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    success = run_retrieval_provenance_audit()
    sys.exit(0 if success else 1)
