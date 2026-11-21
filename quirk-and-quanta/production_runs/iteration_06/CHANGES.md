# Iteration 6 Changes

## Files Created & Updated
1. `rag/guardrails.py`:
   - Added `is_presenter: bool = False` to `evaluate_request()`.
   - Presenter requests bypass per-session rate limits and token budgets while enforcing standard safety policies.
2. `rag/pipeline.py`:
   - Propagated `is_presenter` through `ask()` into guardrails evaluation.
3. `rag/server.py`:
   - Imported `hmac`.
   - Extracted `X-Presenter-Token` header and `presenterToken` body parameter.
   - Verified presenter token with `hmac.compare_digest` against `PRESENTER_TOKEN` environment variable (default: `[REDACTED_PRESENTER_TOKEN]`).
   - Attached `isPresenter: bool` to JSON API response telemetry.
4. `scripts/verify_concurrency_resilience.py`:
   - Comprehensive test harness covering 100 concurrent retrievals, 150 static bursts, presenter token priority, request span tracing, and upstream failure degradation.
