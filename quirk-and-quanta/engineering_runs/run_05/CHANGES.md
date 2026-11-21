# Engineering Run 05: Changes
## P0-G: Observability, Structured Tracing, Token Usage, Latency Breakdown & Simulated Cost Spikes

### Summary of Modifications:
1. **`rag/observability.py`**:
   - Implemented `RequestTrace` data model with UUID request IDs, timestamp, distributed latency spans (`auth_verification`, `retrieval`, `guardrails`, `generation`), input/output token counters, and Gemini 2.5 Flash cost model (\$0.075/1M in, \$0.30/1M out).
   - Implemented `TraceCollector` with thread-safe circular ring buffer (max 100 traces) and aggregate telemetry (`totalRequestsTracked`, `totalTokensTracked`, `totalCostUsd`).
   - Implemented `simulate_cost_spike()` reproducing Story 7 of the film ("Arthur Receives the Bill") comparing unconstrained recursive billing vs protected usage limits.
2. **`rag/pipeline.py`**:
   - Integrated `TraceCollector` into `ask()` and `ask_graph()`.
   - Recorded distributed latency spans and attached `trace` and `requestId` to output response.
3. **`rag/server.py`**:
   - Added `GET /api/rag/traces` and `GET /api/rag/traces/aggregate`.
   - Added `POST /api/rag/simulate-spike` (Demo 14).
   - Updated `/api/rag/status` with `ENABLE_OBSERVABILITY: true` and live aggregate stats.
4. **`site/workshop.html` & `site/js/workshop.js`**:
   - Added "📈 Simulate Runaway Cost Spike (Demo 14)" button.
   - Enhanced Telemetry Bar with Request ID, Token breakdown (in/out), and Estimated Cost ($ USD).
   - Added interactive Cost Spike simulation comparison card showing tokens burned, dollar savings, and throttling status.
5. **`tests/test-observability.py`**:
   - Added 5 unit tests covering token estimation, pricing arithmetic, trace span recording, ring buffer bound, cost spike simulation, and pipeline trace delivery.
