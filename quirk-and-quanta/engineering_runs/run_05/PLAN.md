# Engineering Run 05: Plan
## Target: P0-G — Observability, Structured Tracing, Token Usage, Latency Breakdown & Simulated Cost Spikes

### 1. Action 1: Inspect & Reproduce
- **Baseline Git Commit**: `5235de5`
- **Current Observability State**:
  - Currently, requests return basic latency numbers (`embeddingMs`, `retrievalMs`, `generationMs`, `totalMs`).
  - However, there are no persistent trace logs, no request UUIDs, no detailed span hierarchy, no token usage counts (input tokens vs output tokens), no monetary cost estimations, and no way to inspect past request execution traces or cost spikes (Gate G14).

### 2. Action 2: Decide & Select Next Target
- **Selected Track**: P0-G (Observability, Structured Tracing & Cost Telemetry)
- **Gate Targeted**: G14 (Request traces explain token usage, latency breakdown, and cost spikes)
- **Work Breakdown**:
  1. Build Observability module `rag/observability.py`:
     - `TraceEvent`: Structured trace data class with `requestId`, `timestamp`, `sessionId`, `userRole`, `method`, `strategy`, `spans` (start/end/durationMs for auth, embedding, retrieval, guardrails, generation), `tokenUsage` (promptTokens, completionTokens, totalTokens), `costUsd` (estimated based on Gemini Flash pricing), and `status`.
     - `TraceCollector`: In-memory thread-safe circular trace ring buffer (stores last 100 traces) and helper methods to query traces by `requestId` or get aggregate cost summaries.
     - `simulate_cost_spike()`: Reproduces the Story 7 intern's recursive spam loop and compares unconstrained billing vs protected budget capping.
  2. Integrate `TraceCollector` into `rag/pipeline.py` and `rag/server.py`:
     - Generate UUID `requestId` on every request.
     - Add endpoint `GET /api/rag/traces` and `GET /api/rag/traces/:id`.
     - Add endpoint `POST /api/rag/simulate-spike` (Demo 14).
     - Update `/api/rag/status` with `ENABLE_OBSERVABILITY: true`.
  3. Update Workshop Lab UI (`site/workshop.html` & `site/js/workshop.js`):
     - Interactive Trace Timeline Inspector showing request ID, step-by-step latency bars, token counts, and estimated cost in USD.
     - Demo 14 trigger: "Simulate Runaway Usage Spike & Budget Attribution".
  4. Build test suite `tests/test-observability.py`:
     - Test trace generation, span timing, token estimation, cost calculation, ring buffer retention, and cost spike simulation.
