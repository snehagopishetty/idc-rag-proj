# Engineering Run 03: Operations & Performance Results

### 1. Guardrail Latency Overhead
| Component | Latency |
|---|---|
| Direct Injection Check | 0.05 ms |
| Scope Classification | 0.06 ms |
| Indirect Chunk Sanitization | 0.12 ms |
| Grounding Evaluation | 0.02 ms |
| Rate & Budget Check | 0.01 ms |
| **Total Guardrail Overhead** | **~0.26 ms** |

### 2. Computational Footprint
- Zero external network dependencies.
- Standard library Python regex engine.
- Session memory: sliding window queue using timestamps (< 50 bytes per active session).
