# Engineering Run 02: Plan
## Target: P0-C — Film-Aligned Defect Scenario & Local GraphRAG

### 1. Action 1: Inspect & Reproduce
- **Baseline Git Commit**: `b01ddae`
- **Current Retrieval Capability**:
  - Dense Vector, BM25, and Hybrid (RRF) search are functional.
  - Multi-hop relationship queries (e.g. `EVAL-009`, `EVAL-010`, `EVAL-011`) pass only when direct text tokens overlap, but cross-document multi-hop causal inference across three disparate products fails to resolve the common root-cause component and supplier batch without graph traversal.
  - Canonical Gate 1 graph contains `REC-003 -> COMP-012 -> QQ-0081, QQ-0087, QQ-0090`.
  - The film narrative explicitly requires:
    - `QQ-0011` (Atomic Orbit Desk Lamp)
    - `QQ-0074` (Atomic Orbit Wireless Fast Charger)
    - `QQ-0049` (Digital Astronomy Star Projector)
    all sharing a defective voltage regulator component (`COMP-025` / `COMP-VREG`), supplied by `SUP-008` (Quantum Flux Micro), in batch `BATCH-VREG-2026`, under quality alert `REC-VREG-01`.

### 2. Action 2: Decide & Select Next Target
- **Selected Track**: P0-C (Film Defect Scenario & Local GraphRAG)
- **Gates Targeted**:
  - G6: The film's defect scenario is present in a validated additive graph.
  - G7: Local GraphRAG returns correct multi-hop paths and grounded answers.
- **Work Breakdown**:
  1. Build versioned additive scenario overlay `data/scenarios/film_defect_scenario.json` containing:
     - Component: `COMP-025` ("Step-Down Synchronous Voltage Regulator IC, 5V/3A, SOT-23-6")
     - Recall Notice: `REC-VREG-01` ("Thermal Degradation & Voltage Fluctuation Advisory")
     - Batch: `BATCH-VREG-2026`
     - Products: `QQ-0011`, `QQ-0074`, `QQ-0049`
     - Typed relationships linking products -> `COMP-025`, `COMP-025` -> `SUP-008`, and `REC-VREG-01` -> `COMP-025`.
     - Preserves canonical historical Gate 1 data (`REC-003`, `COMP-012`) completely intact.
  2. Implement `rag/graph_local.py`:
     - In-memory property graph engine loaded from canonical `data/canonical/relationships.json` + `data/scenarios/film_defect_scenario.json`.
     - Multi-hop traversal engine supporting:
       - `find_common_components(product_skus: List[str])`
       - `trace_defect_root_cause(product_skus: List[str])`
       - `get_neighborhood(node_id: str, depth: int = 2)`
       - Subgraph extraction and Cypher-like pattern matching.
       - Natural language reasoning generation synthesizing graph paths into factual explanations.
  3. Integrate GraphRAG into `rag/pipeline.py` and `rag/server.py` (`POST /api/rag/graph`).
  4. Expose Demo 07 (Hybrid fails multi-hop defect question) and Demo 08 (GraphRAG resolves defect path) in Workshop Lab (`site/workshop.html` & `site/js/workshop.js`).
  5. Add test suite `tests/test-graph.py` verifying graph loading, multi-hop traversal, root-cause resolution, and failure recovery.
  6. Measure latency, accuracy, and graph explanation fidelity.
