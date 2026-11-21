# Iteration 2 Changes

## Files Created & Updated
1. `deploy/cloudrun_service.yaml`:
   - Knative `serving.knative.dev/v1` Service declaration.
   - Resource limits: 1 vCPU, 2 GiB memory (`memory: 2Gi`, `cpu: 1000m`).
   - Concurrency: 20 (`containerConcurrency: 20`).
   - Autoscaling: `autoscaling.knative.dev/minScale: "1"`, `maxScale: "3"`.
   - Probes: `startupProbe` and `livenessProbe` on `/healthz`, port 8080.
2. `deploy/cloudbuild.yaml`:
   - Two-step build: `docker build` using `deploy/Dockerfile` -> `docker push` to Google Artifact Registry (`asia-south1-docker.pkg.dev/$PROJECT_ID/quirk-quanta/rag-service:$SHORT_SHA`).
3. `deploy/deploy_cloud_run.sh`:
   - Production deployment helper automating project verification, Cloud Build image compilation, Cloud Run service revision deployment, and healthcheck smoke test.
4. `scripts/simulate_cloud_run_runtime.py`:
   - End-to-end local harness simulating Cloud Run container initialization, memory envelope tracking, `/healthz` probing, and 20-worker thread pool concurrency bursts.
