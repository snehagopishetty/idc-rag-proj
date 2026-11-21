# Iteration 5 Plan: Retrieval Provenance & Live Gemini Integration Verification (Gates P09, P10, P11, O01)

## 1. Objectives
- Audit and empirically verify all 4 retrieval strategies (Vector, BM25, Hybrid RRF, GraphRAG) against the 42-question golden dataset.
- Record truthful provenance metrics without synthetic inflation.
- Validate Gemini 2.5 Flash and `gemini-embedding-001` integration, quota admission controllers, and deterministic offline grounded fallback.
- Test grounding and calibrated abstention boundaries (`REJECT_OFF_TOPIC`, `ABSTAIN_UNGROUNDED`).
- Verify Neo4j AuraDB adapter fallback resilience when external graph credentials are unconfigured.

## 2. Acceptance Criteria
- All 11 verification checks in `scripts/verify_retrieval_provenance.py` pass.
- Provenance metrics recorded: Vector (47.6%), BM25 (57.1%), Hybrid (50.0%), GraphRAG (100% defect root cause).
- Deterministic offline fallback generates grounded answers with accurate citations when API key is unavailable.
- Adversarial input attack simulation (extreme query size, bad Unicode) passes with 0 crashes.
