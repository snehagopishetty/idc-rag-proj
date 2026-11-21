# Engineering Run 06: Plan
## Target: P0-D — Extended Golden Dataset (42 Curated Cases) & Comprehensive Multi-Strategy Evaluation

### 1. Action 1: Inspect & Reproduce
- **Baseline Git Commit**: `fa8e05d`
- **Current Dataset State**:
  - `data/evaluation/golden_dataset.json` contains 22 baseline cases (`EVAL-001` through `EVAL-022`).
  - Evaluation runner `scripts/run_evaluations.py` tests Vector, BM25, and Hybrid.
  - Required by Section H & Gate G8: Expand dataset to 40+ cases without inflating with junk, retaining the frozen 22 cases as baseline, and covering all 8 stories of the film and security attack families.

### 2. Action 2: Decide & Select Next Target
- **Selected Track**: P0-D (Golden Dataset Expansion & Multi-Strategy Benchmark)
- **Gate Targeted**: G8 (Golden evaluations produce real comparative metrics across strategies)
- **Work Breakdown**:
  1. Archive frozen baseline `data/evaluation/golden_dataset_baseline_v1.json` (22 cases).
  2. Expand `data/evaluation/golden_dataset.json` to 42 curated cases (v2.0) with complete metadata:
     - `id`, `family`, `question`, `expectedBehavior`, `expectedAnswer`, `expectedEntities`, `expectedGraphPath`, `relevantSourceIds`, `relevantDocIds`, `authorizedRoles`, `notes`.
  3. Precompute and cache query embeddings for newly added questions in `data/embeddings/v1/query_embeddings_cache.json`.
  4. Enhance benchmark runner `scripts/run_evaluations.py` to evaluate:
     - Dense Vector
     - Lexical BM25
     - Hybrid RRF
     - Knowledge Graph (GraphRAG)
     - Guardrails & Hardened Mode (Injection, Scope, Abstention)
  5. Add test suite `tests/test-evaluation.py` verifying dataset schema, unique test IDs, non-empty questions, entity references, and evaluation execution.
  6. Measure empirical metrics across all 42 cases for each strategy and record comparative results.
