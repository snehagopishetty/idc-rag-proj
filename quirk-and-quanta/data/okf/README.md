# Open Knowledge Format (OKF) Bundle
## Quirk & Quanta Workshop Defect Scenario

This directory contains a valid Open Knowledge Format (OKF) portable knowledge graph bundle conformant with the specification:
https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

### Bundle Contents
- `manifest.json`: Specification metadata, entity types, relation types, and dataset integrity counts.
- `entities.jsonl`: Discrete JSON Lines entities representing Products (`QQ-0011`, `QQ-0074`, `QQ-0049`), Component (`COMP-025`), Recall Notice (`REC-VREG-01`), and Supplier (`SUP-008`).
- `relations.jsonl`: Directed graph relationships (`CONTAINS`, `AFFECTED_BY`, `SUPPLIED_BY`, `AFFECTS_PRODUCT`).

### Architectural Taxonomy
1. **OKF (Open Knowledge Format)**: Portable, serialized data interchange standard for entities, schemas, and typed relationships.
2. **Local GraphRAG**: Pure-Python in-memory property graph engine executing deterministic multi-hop BFS traversals.
3. **Neo4j AuraDB**: Enterprise cloud graph database engine executing Cypher pattern queries with HTTP REST transactional commits.
