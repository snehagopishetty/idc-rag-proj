# Risk Register

| Risk ID | Description | Impact | Likelihood | Mitigation | Status |
|---|---|---|---|---|---|
| RISK-001 | Dependency Guard Violation (attempting pip install in sandboxed environment) | High | Low | Enforce 100% Python Standard Library implementation | Active / Enforced |
| RISK-002 | Absence of live Gemini API key in local environment | Medium | High | Maintain deterministic offline fallback with normalized 768-D embeddings and cached golden queries | Active / Mitigated |
| RISK-003 | Historical data corruption when adding film defect scenario | Critical | Low | Use non-destructive, additive scenario layer (`data/scenarios/film_defect_scenario.json`) preserving Gate 1 canonical graph | Active / Mitigated |
| RISK-004 | Client-side security spoofing (role param manipulation) | High | Medium | Cryptographic HMAC or server-enforced session tokens for RBAC | Active / Planned Iter 4 |
| RISK-005 | Prompt Injection (direct persona override & indirect via retrieved doc) | High | Medium | Structural parsing, prompt framing, trust boundaries, and output filtering | Active / Planned Iter 3 |
| RISK-006 | Audience concurrency bottleneck during live workshop | High | Medium | In-memory indexing, thread-safe server, caching, and load simulation | Active / Planned Iter 7 |
