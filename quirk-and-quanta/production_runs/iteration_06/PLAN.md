# Iteration 6 Plan: 100-Attendee Reliability, Load Testing & Presenter Protection (Gates P13, P14, P15, O02, O03)

## 1. Objectives
- Validate 100 simultaneous attendee concurrency across 3 operational load scenarios:
  - Scenario A: 100 concurrent RAG queries.
  - Scenario B: 150 concurrent static asset requests.
  - Scenario C: 100 mixed concurrent API and static requests.
- Implement and verify the Presenter Protection Token (`X-Presenter-Token`):
  - Constant-time secret verification (`hmac.compare_digest`).
  - Dedicated capacity reservation preventing presenter live demos from throttling during attendee query spikes.
- Validate request observability: UUID request tagging, distributed span latency tracking, and token usage accounting.
- Verify safe dependency degradation under simulated upstream API outages (zero 500 crashes).
- Validate attendee deployment paths (Google AI Studio and Vercel).

## 2. Acceptance Criteria
- 100% of 350 load test requests succeed with 0 failures (well surpassing >=99% requirement).
- Presenter token verified: noisy student session throttled at 30 requests, while presenter request succeeds immediately with `isPresenter=True`.
- Forged presenter tokens safely rejected and downgraded.
- All 6 suites in `scripts/verify_concurrency_resilience.py` pass.
