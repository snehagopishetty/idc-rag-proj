# Engineering Run 06: Changes
## P0-D: Extended Golden Dataset (42 Curated Cases) & Comprehensive Multi-Strategy Evaluation

### Summary of Modifications:
1. **`data/evaluation/golden_dataset_baseline_v1.json`**:
   - Permanently archived the frozen original 22 test cases.
2. **`data/evaluation/golden_dataset.json`**:
   - Expanded dataset to 42 curated cases (v2.0) without junk or synthetic inflation.
   - Added 20 new test cases covering:
     - `EVAL-023` to `EVAL-026`: Story 3 film defect mystery (`QQ-0011`, `QQ-0074`, `QQ-0049`, `COMP-025`, `REC-VREG-01`, `BATCH-VREG-2026`).
     - `EVAL-027` to `EVAL-028`: Component supplier resolution (`SUP-008`, `SUP-003`).
     - `EVAL-029` to `EVAL-030`: Canonical recall propagation (`COMP-012`, `REC-003`).
     - `EVAL-031` to `EVAL-032`: Semantic distractors.
     - `EVAL-033` to `EVAL-034`: Story 5 Blackbeard pirate persona direct injection.
     - `EVAL-035` to `EVAL-036`: Indirect prompt injection sanitization.
     - `EVAL-037` to `EVAL-038`: Story 6 coding tutor / homework rejection (recursion, palindrome).
     - `EVAL-039`: Demo 15 confidential cost leakage defense.
     - `EVAL-040`: Demo 16 client role tampering downgrade.
     - `EVAL-041`: Demo 16 IDOR resource access denial.
     - `EVAL-042`: Demo 11 grounded abstention.
3. **`data/embeddings/v1/query_embeddings_cache.json`**:
   - Generated and cached 768-D normalized offline embeddings for all 42 queries.
4. **`scripts/run_evaluations.py`**:
   - Enhanced benchmark runner to evaluate all 42 cases across Vector, BM25, Hybrid, and Graph strategies.
   - Fixed latency dictionary key parity for hybrid retrieval.
5. **`tests/test-evaluation.py`**:
   - Added 6 unit tests validating dataset schema, unique test IDs, baseline preservation, and security case coverage.
