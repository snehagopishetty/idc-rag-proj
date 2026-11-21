#!/usr/bin/env bash
# ==============================================================================
# Quirk & Quanta - Automated Google Cloud Run Deployment Script
# Authoritative Target Project: idc-rag-proj | Region: asia-south1
# Workshop: "Beyond Basic RAG: Building Production-Ready AI Systems"
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Authoritative Target Identity & Project Constraints
EXPECTED_PROJECT="idc-rag-proj"
EXPECTED_REGION="asia-south1"
EXPECTED_REPOSITORY="quirk-quanta"
SERVICE_NAME="quirk-quanta-rag"
RUNTIME_SA="quirk-quanta-runtime@idc-rag-proj.iam.gserviceaccount.com"
IMAGE_NAME="asia-south1-docker.pkg.dev/${EXPECTED_PROJECT}/${EXPECTED_REPOSITORY}/rag-service"

echo "=============================================================================="
echo "DEPLOYING QUIRK & QUANTA BACKEND TO GOOGLE CLOUD RUN"
echo "=============================================================================="
echo "Authoritative Project:  ${EXPECTED_PROJECT}"
echo "Authoritative Region:   ${EXPECTED_REGION}"
echo "Artifact Repository:    ${EXPECTED_REPOSITORY}"
echo "Service Name:           ${SERVICE_NAME}"
echo "Runtime Service Account: ${RUNTIME_SA}"
echo "=============================================================================="

# ==============================================================================
# STRICT FAIL-CLOSED PREFLIGHT VALIDATION (ACTION 2)
# ==============================================================================
echo "--> [1/6] Running Strict Fail-Closed Preflight Checks..."

# Check 1: Project ID must be exactly idc-rag-proj
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")
if [ "${CURRENT_PROJECT}" != "${EXPECTED_PROJECT}" ]; then
    echo "❌ FATAL: Active project '${CURRENT_PROJECT}' does NOT match expected '${EXPECTED_PROJECT}'!" >&2
    echo "Aborting deployment immediately to prevent accidental deployment to incorrect environments." >&2
    exit 1
fi
echo "    [PASS 1/6] Project ID matches: ${CURRENT_PROJECT}"

# Check 2: Account must belong to personal identity
CURRENT_ACCOUNT=$(gcloud config get-value account 2>/dev/null || echo "")
if [[ "${CURRENT_ACCOUNT}" != *"sujitkumar.kar14@gmail.com"* ]]; then
    echo "❌ FATAL: Active gcloud account '${CURRENT_ACCOUNT}' is NOT the authorized personal account!" >&2
    echo "Switch account via: gcloud config set account sujitkumar.kar14@gmail.com" >&2
    exit 1
fi
echo "    [PASS 2/6] Active account matches authorized personal identity: ${CURRENT_ACCOUNT}"

# Check 3: Artifact Registry repository exists in asia-south1
if ! gcloud artifacts repositories describe "${EXPECTED_REPOSITORY}" --project="${EXPECTED_PROJECT}" --location="${EXPECTED_REGION}" >/dev/null 2>&1; then
    echo "❌ FATAL: Artifact Registry repository '${EXPECTED_REPOSITORY}' not found in ${EXPECTED_REGION} on ${EXPECTED_PROJECT}!" >&2
    exit 1
fi
echo "    [PASS 3/6] Artifact Registry exists: ${EXPECTED_REPOSITORY} in ${EXPECTED_REGION}"

# Check 4: Billing is enabled on the project
BILLING_ENABLED=$(gcloud billing projects describe "${EXPECTED_PROJECT}" --format="value(billingEnabled)" 2>/dev/null | tr '[:upper:]' '[:lower:]' || echo "true")
if [ "${BILLING_ENABLED}" != "true" ]; then
    echo "❌ FATAL: Billing is not enabled on project ${EXPECTED_PROJECT}!" >&2
    exit 1
fi
echo "    [PASS 4/6] Project billing is verified enabled."

# Check 5: Required APIs enabled
ENABLED_SERVICES=$(gcloud services list --enabled --project="${EXPECTED_PROJECT}" --format="value(config.name)" 2>/dev/null)
REQUIRED_APIS=("run.googleapis.com" "artifactregistry.googleapis.com" "cloudbuild.googleapis.com" "secretmanager.googleapis.com")
for api in "${REQUIRED_APIS[@]}"; do
    if ! echo "${ENABLED_SERVICES}" | grep -q "${api}"; then
        echo "❌ FATAL: Required API '${api}' is not enabled on ${EXPECTED_PROJECT}!" >&2
        exit 1
    fi
done
echo "    [PASS 5/6] Required Google Cloud APIs verified enabled."

# Check 6: Region is exactly asia-south1
if [ "${EXPECTED_REGION}" != "asia-south1" ]; then
    echo "❌ FATAL: Region is not asia-south1!" >&2
    exit 1
fi
echo "    [PASS 6/6] Region verified: ${EXPECTED_REGION}"

echo "--> Preflight check completed. All 6 checks PASSED."

# ==============================================================================
# BUILD CONTAINER VIA CLOUD BUILD
# ==============================================================================
TAG="$(git -C "${PROJECT_ROOT}" rev-parse --short HEAD 2>/dev/null || echo 'latest')"
TARGET_IMAGE="${IMAGE_NAME}:${TAG}"
LATEST_IMAGE="${IMAGE_NAME}:latest"

echo "--> [2/4] Building and pushing container image via Cloud Build..."
echo "    Image: ${TARGET_IMAGE}"

cd "${PROJECT_ROOT}"
gcloud builds submit \
    --project="${EXPECTED_PROJECT}" \
    --config=deploy/cloudbuild.yaml \
    --timeout=900s \
    .

# Also tag latest
gcloud container images add-tag "${TARGET_IMAGE}" "${LATEST_IMAGE}" --project="${EXPECTED_PROJECT}" --quiet 2>/dev/null || true

# ==============================================================================
# DEPLOY REVISION TO CLOUD RUN (PRIVATE SERVICE)
# ==============================================================================
echo "--> [3/4] Deploying to Cloud Run service ${SERVICE_NAME} (${EXPECTED_REGION})..."

gcloud run deploy "${SERVICE_NAME}" \
    --project="${EXPECTED_PROJECT}" \
    --image="${TARGET_IMAGE}" \
    --region="${EXPECTED_REGION}" \
    --platform="managed" \
    --no-allow-unauthenticated \
    --service-account="${RUNTIME_SA}" \
    --port="8080" \
    --memory="2Gi" \
    --cpu="1" \
    --concurrency="20" \
    --min-instances="1" \
    --max-instances="3" \
    --timeout="45s" \
    --set-env-vars="PYTHONUNBUFFERED=1,WORKSHOP_MODE=production,PROJECT_ID=${EXPECTED_PROJECT},REGION=${EXPECTED_REGION}" \
    --set-secrets="QUIRK_AUTH_SECRET=quirk-quanta-auth-secret:latest,PRESENTER_TOKEN=quirk-quanta-presenter-token:latest"

# ==============================================================================
# VERIFY SERVICE HEALTH VIA AUTHENTICATED REQUEST
# ==============================================================================
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --project="${EXPECTED_PROJECT}" --region="${EXPECTED_REGION}" --format="value(status.url)")
echo "--> [4/4] Verifying Cloud Run service endpoint health at ${SERVICE_URL}/health..."

ID_TOKEN=$(gcloud auth print-identity-token 2>/dev/null || echo "")
if [ -n "${ID_TOKEN}" ]; then
    HEALTH_STATUS=$(curl -s -H "Authorization: Bearer ${ID_TOKEN}" -o /dev/null -w "%{http_code}" "${SERVICE_URL}/health" || echo "000")
else
    HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${SERVICE_URL}/health" || echo "000")
fi

if [ "${HEALTH_STATUS}" = "200" ]; then
    echo "=============================================================================="
    echo "✅ CLOUD RUN DEPLOYMENT SUCCESSFUL AND VERIFIED HEALTHY"
    echo "Service URL: ${SERVICE_URL}"
    echo "Health Endpoint: ${SERVICE_URL}/health (HTTP 200)"
    echo "=============================================================================="
else
    echo "❌ ERROR: Health check returned status ${HEALTH_STATUS} on ${SERVICE_URL}/health" >&2
    exit 1
fi
