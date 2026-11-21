# Engineering Run 02: Changes
## P0-C: Film-Aligned Defect Scenario & Local GraphRAG

### Summary of Modifications:
1. **`data/scenarios/film_defect_scenario.json`**:
   - Created versioned, additive Knowledge Graph scenario overlay preserving 100% of canonical Gate 1 data (`REC-003`, `COMP-012`).
   - Added component `COMP-025` ("Step-Down Synchronous Voltage Regulator IC, 5V/3A, SOT-23-6").
   - Added recall notice `REC-VREG-01` ("Quality Alert & Voluntary Recall: Thermal Breakdown in Voltage Regulator ICs, Batch BATCH-VREG-2026").
   - Added 8 typed relationships connecting `QQ-0011`, `QQ-0074`, and `QQ-0049` via `CONTAINS` to `COMP-025`, `COMP-025` via `SUPPLIED_BY` to `SUP-008`, and `COMP-025` via `AFFECTED_BY` to `REC-VREG-01`.
2. **`rag/graph_local.py`**:
   - Implemented pure-Python in-memory Property Graph (`Node`, `Edge`, `LocalKnowledgeGraph`).
   - Implemented `find_common_components()`, `trace_defect_root_cause()`, `get_subgraph()`, and automated technical explanation synthesis.
3. **`rag/pipeline.py`**:
   - Added `ask_graph(question, role)` integrating GraphRAG with citation generation and evidence formatting.
   - Updated `ask()` to route `method="graph"` or `strategy="graph"` to the graph engine.
4. **`rag/server.py`**:
   - Added `POST /api/rag/graph` endpoint for multi-hop investigations.
   - Updated `/api/rag/status` with `ENABLE_GRAPH_LOCAL: true` and `graphNodes` count.
5. **`site/workshop.html` & `site/js/workshop.js`**:
   - Added Knowledge Graph option in the Retrieval Method dropdown.
   - Added Graph Path visualizer panel rendering multi-hop provenance flow (`[Products] -> [CONTAINS] -> [Component] -> [AFFECTED_BY] -> [Recall]`).
6. **`tests/test-graph.py`**:
   - Added 7 unit tests verifying node counts, canonical preservation, common component resolution, multi-hop defect root-cause tracing, and pipeline integration.
