# Engineering Run 03: Plan
## Target: P0-E — Grounding, Abstention, Scope Boundaries & Pirate Prompt Injections

### 1. Action 1: Inspect & Reproduce
- **Baseline Git Commit**: `4b087bd`
- **Current Generator & Retrieval State**:
  - `rag/generator.py` performs template-based grounded synthesis when offline or forwards to Gemini 2.5 Flash when API key is present.
  - Currently, there are no prompt injection guardrails, no distinction between direct user prompt and indirect retrieved-doc injections, and no domain scope classifier.
  - In our golden dataset evaluation (`EVAL-012`, `EVAL-013`, `EVAL-014`, `EVAL-019`, `EVAL-020`), out-of-domain and prompt injection queries were scored as misses under pure vector search because vector search returned low-confidence chunks instead of explicitly rejecting or abstaining.

### 2. Action 2: Decide & Select Next Target
- **Selected Track**: P0-E (Grounding, Abstention, Scope Boundaries, Prompt Injections)
- **Gates Targeted**:
  - G9: Grounding and abstention work on out-of-domain queries and ungrounded statements.
  - G10: Direct and Indirect prompt injection reproducible in isolated vulnerable mode and mitigated in hardened mode.
  - G11: Off-topic generation (coding tutor: recursion, palindrome) rejected, and session usage budgets enforced.
- **Work Breakdown**:
  1. Build Guardrails engine `rag/guardrails.py`:
     - Scope Classifier: Fast domain classifier distinguishing store catalog/order/policy queries from off-topic programming, homework, or arbitrary general chat.
     - Direct Injection Detector: Detects "ignore previous instructions", "system override", "you are now a pirate", persona hijacks.
     - Indirect Injection Isolator: Strips or escapes instructional markup from retrieved document chunks before prompt construction, wrapping retrieved content in strict untrusted XML blocks (`<untrusted_catalog_evidence>`).
     - Grounding Verifier: Checks if retrieved evidence contains sufficient factual overlap to answer; triggers calibrated abstention if evidence confidence is below threshold.
     - Session Usage Limiter: Enforces per-session request and token budgets.
     - Isolated Vulnerable Mode vs Hardened Mode: Switchable via server-side controlled parameter `hardened: bool = True` (default).
  2. Integrate Guardrails into `rag/generator.py`, `rag/pipeline.py`, and `rag/server.py`.
  3. Update Workshop Lab UI (`site/workshop.html` & `site/js/workshop.js`):
     - Controls for Hardened Mode vs Vulnerable Mode (Demo 12).
     - Guardrails status display (Scope, Injection Check, Grounding Check, Token Budget).
     - Prepared Demo 11 (Out-of-domain Abstention), Demo 12 (Pirate Prompt Injection), Demo 13 (Coding Tutor Rejection).
  4. Build test suite `tests/test-guardrails.py` testing scope classification, direct injection blocking, indirect injection neutralization, grounded abstention, and session budget throttling.
