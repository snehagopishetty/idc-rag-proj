#!/usr/bin/env bash
# ==============================================================================
# Quirk & Quanta - Firebase Hosting Deployment Automation
# Authoritative Target Project: idc-rag-proj
# Workshop: "Beyond Basic RAG: Building Production-Ready AI Systems"
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

AUTHORITATIVE_PROJECT="idc-rag-proj"
SERVICE_NAME="quirk-quanta-rag"
REGION="asia-south1"

echo "======================================================================"
echo "QUIRK & QUANTA - FIREBASE HOSTING DEPLOYMENT"
echo "Target Project: ${AUTHORITATIVE_PROJECT}"
echo "Cloud Run:      ${SERVICE_NAME} (${REGION})"
echo "======================================================================"

cd "${PROJECT_ROOT}"

# 1. Preflight checks
if [ ! -f "firebase.json" ]; then
    echo "❌ FATAL: firebase.json not found in ${PROJECT_ROOT}" >&2
    exit 1
fi

if [ ! -d "site" ]; then
    echo "❌ FATAL: site/ directory not found in ${PROJECT_ROOT}" >&2
    exit 1
fi

if [ ! -f "site/index.html" ] || [ ! -f "site/workshop.html" ]; then
    echo "❌ FATAL: Essential storefront HTML files missing from site/" >&2
    exit 1
fi

# Verify .firebaserc default project matches idc-rag-proj
if ! grep -q "\"default\": \"${AUTHORITATIVE_PROJECT}\"" .firebaserc; then
    echo "❌ FATAL: .firebaserc does not match authoritative project ${AUTHORITATIVE_PROJECT}!" >&2
    exit 1
fi

echo "--> Preflight check passed. Site directory, configuration, and project isolation verified."

# 2. Check for Firebase CLI
FIREBASE_CMD=""
if command -v firebase >/dev/null 2>&1; then
    FIREBASE_CMD="firebase"
elif command -v npx >/dev/null 2>&1; then
    FIREBASE_CMD="npx --yes firebase-tools"
fi

if [ -z "${FIREBASE_CMD}" ]; then
    echo "❌ FATAL: Neither 'firebase' nor 'npx' CLI found in PATH." >&2
    exit 1
fi

echo "--> Using Firebase CLI: ${FIREBASE_CMD}"
echo "--> Deploying hosting configuration to ${AUTHORITATIVE_PROJECT}..."

${FIREBASE_CMD} deploy --only hosting --project "${AUTHORITATIVE_PROJECT}"

echo "======================================================================"
echo "FIREBASE HOSTING DEPLOYMENT COMPLETE"
echo "Public Domain: https://${AUTHORITATIVE_PROJECT}.web.app"
echo "               https://${AUTHORITATIVE_PROJECT}.firebaseapp.com"
echo "======================================================================"
