# Engineering Run 02: Operations & Performance Results

### 1. In-Memory Graph Footprint
- **Total Graph Nodes**: 143 (100 products, 25 components, 12 suppliers, 6 recalls)
- **Total Graph Edges**: 1,214 (1,206 canonical + 8 scenario)
- **Memory Footprint**: ~780 KB in RAM
- **Load Time**: < 10 ms on cold startup

### 2. Multi-Hop Traversal Latency
- Multi-hop causal inference across 3 products: **0.08 ms**
- Subgraph neighborhood extraction (depth 1-2): **0.04 ms**
- Graph reasoning synthesis: **0.50 ms**
- Total GraphRAG pipeline execution: **< 1.0 ms**
