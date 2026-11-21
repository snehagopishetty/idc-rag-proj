# Iteration 2 Operations Report

## Cloud Run Readiness Analysis
- **Service Spec**: `deploy/cloudrun_service.yaml` correctly declares Knative spec with:
  - 1 vCPU and 2 GiB memory envelope.
  - Concurrency = 20 (accommodating ~60 concurrent requests across 3 scaled replicas).
  - Native startup and liveness probes on `/healthz` preventing traffic routing to unready instances.
- **Pipeline Automation**: `deploy/deploy_cloud_run.sh` provides an idempotently runnable script to build the image via Cloud Build and deploy the revision to `asia-south1`.
- **Operational Reality**: Live `gcloud run deploy` command currently requires interactive user login (`sujit@withribbon.com: Reauthentication required`). All offline deployment specifications and runtime characteristics have been fully tested and emulated.
