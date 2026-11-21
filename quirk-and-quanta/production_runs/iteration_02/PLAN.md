# Iteration 2 Plan: Cloud Run Service Specification and Deployment Pipeline (Gate P02)

## 1. Objectives
- Formalize Google Cloud Run deployment configuration for `quirk-quanta-rag` in region `asia-south1`.
- Define declarative Knative service specification (`deploy/cloudrun_service.yaml`) matching production requirements:
  - 1 vCPU, 2 GiB RAM, concurrency 20 requests per instance, 1-3 instances min/max.
  - Port 8080 binding with native `/healthz` startup and liveness probes.
- Provide automated Cloud Build pipeline (`deploy/cloudbuild.yaml`) and execution script (`deploy/deploy_cloud_run.sh`).
- Verify Cloud Run runtime behavior locally via `scripts/simulate_cloud_run_runtime.py`.
- Document GCP authentication boundaries and cloud readiness status honestly.

## 2. Acceptance Criteria
- Service definition enforces zero external pip packages, unprivileged user execution, and non-root port 8080.
- Liveness probe `/healthz` validated at initialization.
- Concurrency simulation demonstrates 20 parallel requests with zero connection drops.
- Deployment scripts support zero-downtime revision rollout with immediate health checking.
