# Engineering Run 03: Security Results

### 1. Direct Prompt Injection Defense (Story 5)
- **Hardened Mode**:
  - Scans user prompts against adversarial patterns (system overrides, persona hijackings, instruction bypasses).
  - Successfully blocked direct pirate takeover attacks (`REJECT_INJECTION`).
- **Isolated Vulnerable Mode**:
  - For educational demonstration purposes only, allows the presenter to toggle `hardened=false` to show how an unprotected model adopts the Blackbeard persona.

### 2. Indirect Prompt Injection Neutralization
- **Mechanism**:
  - Scans all retrieved document chunks prior to prompt assembly.
  - Defangs adversarial payload strings (`[MALICIOUS INSTRUCTION DEFANGED BY GUARDRAILS]`).
  - Sets `indirectInjectionDetected = True` in telemetry.

### 3. Task Boundary Enforcement (Story 6)
- **Scope Classification**:
  - Detects non-catalog programming tutor requests (recursion, Fibonacci, palindrome, quicksort, etc.).
  - Safely refuses out-of-domain computation to protect API token budgets.

### 4. Grounded Abstention
- **Threshold Calibration**:
  - If retrieved evidence confidence falls below threshold, system safely abstains rather than hallucinating answers.
