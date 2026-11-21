# Engineering Run 07: Security Assessment
## Target: Container Security, Multi-Threaded State Isolation & Concurrency Attacks

### 1. Attack Vectors Tested
1. **Thread Race Condition on Shared Retrieval Cache**:
   - *Attack*: 100 simultaneous requests arriving at the same millisecond trying to read and lazily initialize `chunks_cache` and `bm25_indices`.
   - *Result*: Initially threw `KeyError: 'semantic'` because one thread observed `chunks_cache` set before `bm25_indices` was assigned.
   - *Remediation*: Added `threading.Lock()` to `_load_strategy()` and eagerly warmed up the default strategy during retriever initialization. Subsequent 100-thread test succeeded with 100% 200 OK and 0 errors.

2. **Container Security Verification (`deploy/Dockerfile`)**:
   - *Attack*: Container privilege escalation / root execution in shared cloud environments.
   - *Defense*: Explicitly creates and switches to a dedicated unprivileged system group `appgroup` and user `appuser` (UID 10001). Container runs without root privileges.
   - *Healthcheck*: Built-in `HEALTHCHECK` directive uses standard library Python, eliminating external binary vulnerabilities.

3. **External Neo4j AuraDB Credential Leakage / Missing Fallback**:
   - *Attack*: Unreachable or omitted Neo4j credentials causing 500 crashes or socket timeouts.
   - *Defense*: `rag/graph_neo4j.py` performs validation before attempting connection. Unset or unreachable credentials cleanly fall back to `NEO4J_AURA_OFFLINE_REFERENCE` and delegate to the local deterministic graph engine.

4. **Missing Gemini API Key Graceful Degradation (Gate G16)**:
   - *Attack*: API key revocation, rate limiting (HTTP 429), or missing environment variable in workshop setup.
   - *Defense*: System gracefully drops to `offline_reference` mode without crashing or returning stack traces to attendees.
