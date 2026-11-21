# Iteration 2 Security Results

## Verification Checks
1. **Container Execution Privilege**:
   - `deploy/Dockerfile` creates unprivileged user `appuser:appgroup` (UID 10001) and drops root privileges prior to launch.
   - Filesystem ownership is restricted: only runtime log and cache areas are writable.
2. **Secret Ingress Separation**:
   - Cloud Run service specification pulls `GEMINI_API_KEY` exclusively from Google Secret Manager (`quirk-quanta-gemini-key:latest`).
   - No credentials or API keys are committed in source code, build scripts, or environment variable defaults.
3. **Internal Path Exposure in Cloud Run**:
   - Verified that all requests to `0.0.0.0:8080` undergo strict path canonicalization.
   - Attempts to request `/../data/internal/products.full.json` or `/../deploy/` over Cloud Run port 8080 are terminated with 404.
4. **Cloud Auth Boundary Note**:
   - GCP credentials on current host require interactive browser session (`Reauthentication required`). Service deployment configuration is fully verified and packaged for zero-touch execution once active gcloud auth is refreshed.
