# Engineering Run 03: Changes
## P0-E: Grounding, Abstention, Scope Boundaries & Pirate Prompt Injections

### Summary of Modifications:
1. **`rag/guardrails.py`**:
   - Implemented `GuardrailsEngine` with:
     - Direct Prompt Injection Defense: Detects persona overrides, Blackbeard pirate instructions, and system prompt extractors.
     - Indirect Prompt Injection Defense: Scans retrieved document text, neutralizes instructional overrides, and flags `indirectInjectionDetected`.
     - Scope Classifier: Classifies catalog inquiries vs off-topic programming tutor / homework requests (recursion, Fibonacci, palindrome).
     - Grounded Abstention Engine: Calibrates confidence thresholds to abstain on ungrounded/out-of-domain queries.
     - Session Usage Limiter: Enforces per-session rate limits (30 req/min) and token budgets (15,000 tokens) to prevent billing spikes.
     - Hardened Mode vs Isolated Vulnerable Mode toggle.
2. **`rag/pipeline.py`**:
   - Integrated `GuardrailsEngine` into `ask()` pipeline coordinator.
   - Handled guardrail interventions (`REJECT_INJECTION`, `REJECT_OFF_TOPIC`, `ABSTAIN_UNGROUNDED`, `VULNERABLE_OVERRIDE_SIMULATED`).
3. **`rag/server.py`**:
   - Added `hardened` boolean parameter in `/api/rag/ask` and `/api/rag/retrieve`.
   - Updated `/api/rag/status` feature flags: `ENABLE_GROUNDING: true`, `ENABLE_PROMPT_INJECTION_DEFENSE: true`, `ENABLE_USAGE_LIMITS: true`.
4. **`site/workshop.html` & `site/js/workshop.js`**:
   - Added "🛡️ Hardened Guardrails Active" toggle switch.
   - Updated `execution-mode-badge` to display guardrail status (`🛡️ Prompt Injection Blocked`, `🔬 Scope Boundary Enforced`, `ℹ️ Grounded Abstention Triggered`, `🏴‍☠️ Vulnerable Persona Override`).
5. **`tests/test-guardrails.py`**:
   - Added 7 unit tests covering direct injection blocking, vulnerable mode persona override, scope rejection, legitimate pass-through, indirect injection sanitization, grounded abstention, and budget throttling.
