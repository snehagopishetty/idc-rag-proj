# Engineering Run 08: Changes
## Target: Final Acceptance, 17 Workshop Demos & Production Delivery Handover
**Baseline Commit**: `c0ce992`  
**Iteration**: 8 of 8  
**Gates Addressed**: G15 (Workshop Lab Demos) & Final Project Verification  

### 1. New Features & Components Added
1. **Interactive 17-Demo Controller in Workshop Lab (`site/workshop.html`, `site/js/workshop.js`)**:
   - Added dedicated `<select id="demo-preset-select">` and dynamic description callout box.
   - Pre-configures exact natural language queries, retrieval engines (Vector, BM25, Hybrid, Local Graph, Neo4j), chunking strategies, roles, and guardrails toggles for all 17 demos.
   - Connects all 8 stories from *"Quirk & Quanta: A Series of Intelligent Mistakes"* to live interactive lab controls.

2. **Automated 17-Demo Verification Suite (`tests/test-demos.py`)**:
   - Comprehensive test suite asserting all 17 demos:
     - Demo 01: Baseline Vector Retrieval (G2)
     - Demo 02: Fixed-Size Chunking (G3)
     - Demo 03: Sliding-Window Chunking with Overlap (G3)
     - Demo 04: Semantic / Structural Chunking (G3)
     - Demo 05: BM25 Exact SKU Retrieval (G4)
     - Demo 06: Hybrid RRF Fusion (G5)
     - Demo 07: 3-Product Multi-Hop Failure (G6)
     - Demo 08: Local GraphRAG Root-Cause Traversal (G7)
     - Demo 09: Neo4j AuraDB Cypher Import & Traversal (O1)
     - Demo 10: Comparative Evaluation Harness (G8)
     - Demo 11: Calibrated Grounded Abstention (G9)
     - Demo 12: Direct Prompt Injection Attack & Defense (G10)
     - Demo 13: Scope Rejection & Indirect Injection Defanging (G11)
     - Demo 14: Observability & Runaway Cost Spikes (G14)
     - Demo 15: Server-Side RBAC & Tampering Demotion (G12)
     - Demo 16: IDOR Direct Resource Access Protection (G13)
     - Demo 17: Dependency Fallback & Zero-Key Operation (G16)
   - 17/17 tests passing in 0.55s.

3. **Master Delivery Handoff Document (`docs/engineering-loop/FINAL_HANDOFF.md`)**:
   - Complete technical handoff for IDC workshop facilitators and attendees.
