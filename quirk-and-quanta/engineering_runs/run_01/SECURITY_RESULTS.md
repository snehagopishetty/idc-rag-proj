# Engineering Run 01: Security Results

### 1. RBAC Enforcement under BM25 and Hybrid Retrieval
- **Test Case**: Customer queries attempting to retrieve internal procurement cost data (`QQ-0001` supplier margin).
- **Result**:
  - In pure BM25 search: Filtered candidates strictly enforce `accessLevel == "public"` when `role == "customer"`. 0 internal chunks returned.
  - In Hybrid search: Vector candidates and BM25 candidates are both pre-filtered before fusion. 0 internal chunks returned.
  - In Admin queries: Internal documents are accessible as permitted.

### 2. Lexical Identifier Attacks
- **Test Case**: Non-existent SKUs (`QQ-9999`) and malicious punctuation delimiters.
- **Result**: Handled gracefully with empty result set; no exceptions or token leakage.

### 3. Term Saturation Attacks
- **Test Case**: Keyword repetition (20x "quantum").
- **Result**: IDF and BM25 term frequency denominator saturation curve prevented infinite scoring growth.
