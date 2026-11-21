# Iteration 4 Operations Report

## Security and Role Operations
- **Authentication**: Stateless HMAC-SHA256 bearer tokens require zero database lookup, enabling horizontal scalability across Cloud Run instances without shared session state.
- **Quota Safeguard**: Per-session sliding window rate limits prevent malicious or runaway script loops from exhausting the Gemini API quota.
- **Vulnerability Isolation**: Attendees experimenting with Story 5 prompt injections or Story 7 IDOR vulnerabilities in their individual browser sessions cannot impair other attendees or compromise backend secrets.
